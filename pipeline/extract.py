# pipeline/extract.py
import json
import pathlib
import re
from llm import ask


def _fix_json_escapes(s: str) -> str:
    """
    Walk the string character-by-character and double any backslash that is
    not part of a valid JSON escape sequence:
      \" \\ \/ \b \f \n \r \t \uXXXX  (XXXX = exactly 4 hex digits)
    Everything else (\alpha, \url, \u + non-hex, etc.) gets its backslash
    doubled so json.loads won't choke on it.
    """
    out: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch != "\\" or i + 1 >= len(s):
            out.append(ch)
            i += 1
            continue
        nxt = s[i + 1]
        if nxt in '"\\\/bfnrt':
            out.append(ch)
            out.append(nxt)
            i += 2
        elif nxt == "u" and i + 5 < len(s) and re.match(r"[0-9a-fA-F]{4}", s[i + 2 : i + 6]):
            out.append(s[i : i + 6])
            i += 6
        else:
            out.append("\\\\")  # escape the stray backslash
            i += 1
    return "".join(out)


def extract_key_ideas(paper: dict, tokenizer, model) -> dict:
    """Use Gemma 4 to extract a structured outline from the full paper text."""
    cache_file = pathlib.Path(f"cache/{paper['id']}_extraction.json")
    if cache_file.exists():
        print("  (cached) Skipping LLM extraction")
        return json.loads(cache_file.read_text())

    # ~24K chars ≈ 6K tokens — covers abstract + intro + methods + results
    # which is all the model needs; full 100K chars exhausts KV cache VRAM.
    text = paper["full_text"][:24_000]

    prompt = f"""You are a senior ML researcher. Read the research paper below and \
extract a structured outline for a technical blog post. Be precise — use exact \
component names, numbers, and terms from the paper. Do not invent or paraphrase \
any quantitative results.

Return ONLY valid JSON (no preamble, no markdown fences) with these fields:
{{
  "one_sentence_summary": "...",
  "problem_statement": "...",
  "prior_art_gaps": ["...", "...", "..."],
  "key_contributions": ["...", "...", "..."],
  "method_overview": "150-word paragraph — precise, no vague terms",
  "architecture_components": [
    {{"name": "...", "description": "..."}}
  ],
  "key_results": [
    {{"metric": "...", "value": "...", "baseline": "...", "source": "Table X"}}
  ],
  "practitioner_takeaways": ["...", "...", "..."],
  "limitations": ["...", "..."],
  "needs_fallback_diagram": true or false
}}

Set needs_fallback_diagram=true ONLY if:
  1. The method has a novel architecture that is hard to understand from text alone, AND
  2. You judge no architecture figure exists in the paper.

Paper:
<paper>
{text}
</paper>"""

    raw = ask(prompt, tokenizer, model, temperature=0.1)

    # Strip any accidental markdown fences before parsing
    cleaned = (
        raw.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )
    cleaned = _fix_json_escapes(cleaned)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        print(f"  ⚠️  JSON parse failed: {exc}")
        print(f"  LLM output around error (chars {max(0,exc.pos-80)}-{exc.pos+80}):")
        print(f"    {cleaned[max(0,exc.pos-80):exc.pos+80]!r}")
        raise
    cache_file.write_text(json.dumps(result, indent=2))
    return result
