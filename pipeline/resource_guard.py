"""
Aborts the pipeline early when the host is under resource pressure.

Checks (in order):
  1. Free system RAM  — model loading needs headroom
  2. CPU 5-min load   — skip when the machine is already busy
  3. GPU VRAM         — needs enough free VRAM for at least quantised inference
  4. Single-instance  — prevents two concurrent pipeline runs via a lock file
"""
import fcntl
import os
import pathlib

import psutil
import torch

from config import cfg

_LOCK_FILE = pathlib.Path("/tmp/jarvis-pipeline.lock")


class ResourceError(RuntimeError):
    """Raised when the host lacks resources to run the pipeline safely."""


def _check_ram() -> None:
    free_gib = psutil.virtual_memory().available / 1024**3
    needed = cfg.resources.min_free_ram_gib
    if free_gib < needed:
        raise ResourceError(
            f"RAM: {free_gib:.1f} GiB free, need >= {needed:.1f} GiB"
        )
    print(f"  RAM: {free_gib:.1f} GiB free (threshold {needed:.1f} GiB) ✓")


def _check_cpu() -> None:
    cores = psutil.cpu_count(logical=True) or 1
    load_per_core = os.getloadavg()[1] / cores  # 5-min average
    ceiling = cfg.resources.max_cpu_load_per_core
    if load_per_core > ceiling:
        raise ResourceError(
            f"CPU: 5-min load/core = {load_per_core:.2f}, threshold = {ceiling:.2f}"
        )
    print(f"  CPU: 5-min load/core = {load_per_core:.2f} (threshold {ceiling:.2f}) ✓")


def _check_vram() -> None:
    if not torch.cuda.is_available():
        print("  VRAM: no GPU detected, will run on CPU ✓")
        return
    free_gib = torch.cuda.mem_get_info()[0] / 1024**3
    needed = cfg.resources.min_free_vram_gib_hard
    if free_gib < needed:
        raise ResourceError(
            f"VRAM: {free_gib:.1f} GiB free, need >= {needed:.1f} GiB"
        )
    print(f"  VRAM: {free_gib:.1f} GiB free (threshold {needed:.1f} GiB) ✓")


class PipelineGuard:
    """
    Context manager: runs resource pre-checks then holds a single-instance lock
    for the duration of the pipeline run.

    Usage::

        try:
            with PipelineGuard():
                run_pipeline()
        except ResourceError as exc:
            print(f"Skipping run: {exc}")
            sys.exit(0)

    Raises ResourceError if any check fails or a lock cannot be acquired.
    The lock is released automatically when the context exits (even on error).
    """

    def __enter__(self) -> "PipelineGuard":
        print("\n🔒 Resource pre-flight check...")
        _check_ram()
        _check_cpu()
        _check_vram()

        self._fh = _LOCK_FILE.open("w")
        try:
            fcntl.flock(self._fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._fh.close()
            raise ResourceError("Another pipeline instance is already running")
        self._fh.write(str(os.getpid()))
        self._fh.flush()
        print("  All checks passed.\n")
        return self

    def __exit__(self, *_) -> None:
        fcntl.flock(self._fh, fcntl.LOCK_UN)
        self._fh.close()
        _LOCK_FILE.unlink(missing_ok=True)
