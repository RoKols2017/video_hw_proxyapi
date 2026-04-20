from __future__ import annotations


def normalize_progress(progress: float | int | None) -> float:
    if progress is None:
        return 0.0
    return max(0.0, min(100.0, float(progress)))


def format_progress_bar(progress: float | int | None, width: int = 30) -> str:
    normalized = normalize_progress(progress)
    filled = int((normalized / 100.0) * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {normalized:5.1f}%"


def format_status_line(status: str, progress: float | int | None) -> str:
    return f"{status}: {format_progress_bar(progress)}"
