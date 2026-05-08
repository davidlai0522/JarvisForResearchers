# pipeline/figures.py
import json
import fitz
import pathlib
import re

# Save as JPEG to keep the git repo small.
_JPEG_QUALITY = 85
# DPI used when rendering page regions — 150 gives crisp output at reasonable size
_RENDER_DPI = 150

# --- Quality filter thresholds ---
_MIN_WIDTH = 200
_MIN_HEIGHT = 150
_MAX_ASPECT_RATIO = 8.0
_MIN_STDDEV = 15.0
_MIN_CONTENT_RATIO = 0.05
# Pixels with all channels > this are "near-white" (catches subtle gradients too)
_NEAR_WHITE_THRESH = 200
# Pixels with mean brightness < this are "dark"
_DARK_THRESH = 30
_MAX_DARK_RATIO = 0.85   # reject if >85% of pixels are very dark (icon on black bg)

# How far above a figure caption to look for the figure body (in PDF points, 1pt ≈ 0.35mm)
_CAPTION_LOOKBACK_PT = 480
# Typical running-header height to skip in the blind fallback
_PAGE_HEADER_PT = 50
# Maximum uncaptioned raster clusters to extract per page (avoids fragment floods)
_MAX_UNCAPTIONED_PER_PAGE = 3


def _render_region(page: fitz.Page, rect: fitz.Rect) -> fitz.Pixmap:
    """
    Render a rectangular region of *page* to an RGB pixmap via MuPDF's full
    rendering pipeline.  This correctly handles all colorspaces, soft masks,
    transparency, and vector/raster composites — avoiding the mal-transformation
    artefacts that occur when extracting raw image bytes.
    """
    zoom = _RENDER_DPI / 72
    mat = fitz.Matrix(zoom, zoom)
    return page.get_pixmap(matrix=mat, clip=rect, colorspace=fitz.csRGB)


def _is_quality_figure(pix: fitz.Pixmap) -> tuple[bool, str]:
    """Return (True, "") if the pixmap looks like a real figure."""
    w, h = pix.width, pix.height
    if w < _MIN_WIDTH or h < _MIN_HEIGHT:
        return False, f"too small ({w}×{h})"
    if w / h > _MAX_ASPECT_RATIO:
        return False, f"banner aspect ratio ({w/h:.1f})"

    n = pix.n  # 3 for RGB
    samples = pix.samples
    total_pixels = w * h
    step = max(1, total_pixels // 4000)
    pixel_sum = pixel_sq_sum = near_white = dark_pixels = sampled = 0

    for i in range(0, total_pixels, step):
        offset = i * n
        r, g, b = samples[offset], samples[offset + 1], samples[offset + 2]
        brightness = (r + g + b) / 3
        pixel_sum += brightness
        pixel_sq_sum += brightness * brightness
        # Near-white: all channels above _NEAR_WHITE_THRESH (catches pastel gradients)
        if r > _NEAR_WHITE_THRESH and g > _NEAR_WHITE_THRESH and b > _NEAR_WHITE_THRESH:
            near_white += 1
        # Very dark: mean brightness below _DARK_THRESH (icon on black background)
        if brightness < _DARK_THRESH:
            dark_pixels += 1
        sampled += 1

    mean = pixel_sum / sampled
    stddev = (pixel_sq_sum / sampled - mean * mean) ** 0.5
    near_white_ratio = near_white / sampled
    dark_ratio = dark_pixels / sampled

    if stddev < _MIN_STDDEV:
        return False, f"near-uniform colour (stddev={stddev:.1f})"
    if near_white_ratio > (1.0 - _MIN_CONTENT_RATIO):
        return False, f"near-white/blank ({near_white_ratio*100:.0f}%)"
    if dark_ratio > _MAX_DARK_RATIO:
        return False, f"mostly dark — icon fragment ({dark_ratio*100:.0f}%)"
    return True, ""


def _captions_on_page(page: fitz.Page) -> list[tuple[fitz.Rect, str]]:
    """Return (rect, text) for every figure-caption block on the page."""
    results = []
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text = block[0], block[1], block[2], block[3], block[4]
        text = text.strip()
        if re.match(r"^(Figure|Fig\.?)\s*\d+", text, re.IGNORECASE):
            results.append((fitz.Rect(x0, y0, x1, y1), text[:300]))
    return results


def _rects_overlap(a: fitz.Rect, b: fitz.Rect) -> bool:
    return not a.intersect(b).is_empty


def _merge_rects(rects: list[fitz.Rect], gap: float = 8.0) -> list[fitz.Rect]:
    """Merge rectangles that overlap or are within *gap* points of each other."""
    if not rects:
        return []
    sorted_rects = sorted(rects, key=lambda r: (r.y0, r.x0))
    merged = [fitz.Rect(sorted_rects[0])]
    for r in sorted_rects[1:]:
        last = merged[-1]
        expanded = fitz.Rect(last.x0 - gap, last.y0 - gap, last.x1 + gap, last.y1 + gap)
        if not expanded.intersect(r).is_empty:
            merged[-1] = last | r  # union
        else:
            merged.append(fitz.Rect(r))
    return merged


def _drawing_clusters(page: fitz.Page, min_area: float = 800.0) -> list[fitz.Rect]:
    """Return merged bounding boxes of vector-path groups on the page.
    Ignores tiny decorative paths (rules, borders, tick marks) by area.
    Gap of 15pt merges scattered paths within the same figure without
    crossing typical column gutters (~12pt).
    """
    rects = []
    for d in page.get_drawings():
        r = d.get("rect")
        if r:
            rect = fitz.Rect(r)
            if not rect.is_empty and rect.width * rect.height >= min_area:
                rects.append(rect)
    return _merge_rects(rects, gap=15.0)


def _figure_region_above(
    cap_rect: fitz.Rect,
    clusters: list[fitz.Rect],
    raster_rects: list[fitz.Rect],
    page_top: float,
    max_lookback: float = _CAPTION_LOOKBACK_PT,
) -> fitz.Rect | None:
    """
    Return the merged bounding box of ALL drawing clusters and raster rects
    that lie within *max_lookback* points above *cap_rect* and overlap it
    horizontally.

    Collecting every source (rather than only the nearest) gives the true
    extent of complex figures that mix vector paths, raster insets, and labels.
    Returns None if nothing is found in the search window.
    """
    search_top = cap_rect.y0 - max_lookback

    def h_overlap(a: fitz.Rect, b: fitz.Rect) -> bool:
        return a.x0 < b.x1 and a.x1 > b.x0

    matching: list[fitz.Rect] = []
    for r in clusters + raster_rects:
        if r.y1 > cap_rect.y0:   # must end above caption top
            continue
        if r.y0 < search_top:    # too far up the page
            continue
        if not h_overlap(r, cap_rect):
            continue
        matching.append(r)

    if not matching:
        return None

    x0 = min(r.x0 for r in matching)
    y0 = min(r.y0 for r in matching)
    x1 = max(r.x1 for r in matching)
    y1 = max(r.y1 for r in matching)
    return fitz.Rect(x0, y0, x1, y1)


def extract_figures(paper_id: str, pdf_path: str) -> list[dict]:
    """
    Extract figures from the PDF using a three-source merge strategy.

    Strategy 1 (caption-driven):
      For each "Figure N" caption, all drawing clusters and raster rects within
      _CAPTION_LOOKBACK_PT above it are merged into one bounding box.  This
      captures the full extent of complex figures that mix vector paths and
      embedded images.  If no source is found the region directly above the
      caption is used as a fallback (skipping the top _PAGE_HEADER_PT to avoid
      running headers).

    Strategy 2 (uncaptioned rasters):
      Raster images not claimed by any caption are grouped spatially (gap 15pt)
      and rendered as a unit — preventing the icon-fragment flood caused by
      papers that embed many small images inside one composite figure.
      At most _MAX_UNCAPTIONED_PER_PAGE clusters are kept per page.
    """
    cache_file = pathlib.Path(f"cache/{paper_id}_figures.json")
    if cache_file.exists():
        print("  (cached) Skipping figure extraction")
        return json.loads(cache_file.read_text())

    doc = fitz.open(pdf_path)
    out_dir = pathlib.Path(f"docs/assets/figures/{paper_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict] = []
    skipped = 0
    captured_rects: list[fitz.Rect] = []

    for page_num, page in enumerate(doc):
        pr = page.rect
        captions = _captions_on_page(page)
        clusters = _drawing_clusters(page)

        # Build raster image rects for this page (reused in both passes)
        raster_rects: list[fitz.Rect] = []
        xref_to_rects: dict[int, list[fitz.Rect]] = {}
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                rs = [r for r in page.get_image_rects(xref)
                      if not r.is_empty
                      and r.width >= _MIN_WIDTH
                      and r.height >= _MIN_HEIGHT]
            except Exception:
                rs = []
            if rs:
                xref_to_rects[xref] = rs
                raster_rects.extend(rs)

        # ── Strategy 1: caption-driven (all sources merged) ──────────────────
        for cap_rect, cap_text in captions:
            source = _figure_region_above(
                cap_rect, clusters, raster_rects, page_top=pr.y0
            )

            if source is not None:
                fig_rect = fitz.Rect(
                    max(pr.x0 + 5, source.x0 - 5),
                    max(pr.y0,     source.y0 - 5),
                    min(pr.x1 - 5, source.x1 + 5),
                    cap_rect.y0 - 2,
                )
            else:
                # Blind fallback: skip the running-header area at the top of the page
                top = max(pr.y0 + _PAGE_HEADER_PT, cap_rect.y0 - _CAPTION_LOOKBACK_PT)
                fig_rect = fitz.Rect(pr.x0 + 20, top, pr.x1 - 20, cap_rect.y0 - 2)

            if fig_rect.is_empty or fig_rect.height < 80:
                continue
            if any(_rects_overlap(fig_rect, seen) for seen in captured_rects):
                continue

            pix = _render_region(page, fig_rect)
            ok, reason = _is_quality_figure(pix)
            if not ok:
                skipped += 1
                continue

            fig_num = _parse_fig_num(cap_text)
            fname = f"fig_p{page_num + 1}_c{fig_num or 'x'}.jpg"
            _save_figure(pix, str(out_dir / fname))
            captured_rects.append(fig_rect)
            figures.append({
                "path": f"../assets/figures/{paper_id}/{fname}",
                "caption": cap_text,
                "page": page_num + 1,
                "figure_number": fig_num,
            })

        # ── Strategy 2: uncaptioned rasters, clustered to avoid fragments ────
        all_uncaptured: list[fitz.Rect] = []
        for xref, img_rects in xref_to_rects.items():
            for img_rect in img_rects:
                if not any(_rects_overlap(img_rect, seen) for seen in captured_rects):
                    all_uncaptured.append(img_rect)

        # Cluster spatially so sub-images of the same composite figure merge
        clustered = _merge_rects(all_uncaptured, gap=15.0)
        page_uncaptioned = 0

        for cluster_rect in clustered:
            if page_uncaptioned >= _MAX_UNCAPTIONED_PER_PAGE:
                break
            if any(_rects_overlap(cluster_rect, seen) for seen in captured_rects):
                continue

            pix = _render_region(page, cluster_rect)
            ok, reason = _is_quality_figure(pix)
            if not ok:
                skipped += 1
                continue

            caption = next(
                (t for r, t in captions if 0 <= r.y0 - cluster_rect.y1 < 90),
                "",
            )
            fig_num = _parse_fig_num(caption)
            fname = f"fig_p{page_num + 1}_u{page_uncaptioned}.jpg"
            _save_figure(pix, str(out_dir / fname))
            captured_rects.append(cluster_rect)
            figures.append({
                "path": f"../assets/figures/{paper_id}/{fname}",
                "caption": caption,
                "page": page_num + 1,
                "figure_number": fig_num,
            })
            page_uncaptioned += 1

    figures.sort(key=lambda f: (f["page"], f["figure_number"] or 99))
    print(
        f"  Extracted {len(figures)} figures from PDF "
        f"({skipped} low-quality regions skipped)"
    )
    cache_file.write_text(json.dumps(figures))
    return figures


def select_blog_figures(figures: list[dict], max_figures: int = 4) -> list[dict]:
    """Pick the best figures to embed in the blog post."""
    captioned = [f for f in figures if f["caption"]]
    uncaptioned = [f for f in figures if not f["caption"]]
    pool = captioned if captioned else uncaptioned
    return pool[:max_figures]


def _save_figure(pix: fitz.Pixmap, path: str, white_thresh: int = 245) -> None:
    """Autocrop near-white margins on all four sides, then save as JPEG."""
    from PIL import Image
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    mask = img.convert("L").point(lambda p: 0 if p > white_thresh else 255)
    bbox = mask.getbbox()  # tight bounding box of non-white content
    if bbox:
        pad = 6
        x0 = max(0, bbox[0] - pad)
        y0 = max(0, bbox[1] - pad)
        x1 = min(img.width, bbox[2] + pad)
        y1 = min(img.height, bbox[3] + pad)
        img = img.crop((x0, y0, x1, y1))
    img.save(path, format="JPEG", quality=_JPEG_QUALITY)


def _parse_fig_num(caption: str) -> int | None:
    m = re.search(r"(?:Figure|Fig\.?)\s*(\d+)", caption, re.IGNORECASE)
    return int(m.group(1)) if m else None
