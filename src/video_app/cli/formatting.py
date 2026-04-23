from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


def normalize_progress(progress: float | int | None) -> float:
    logger.debug("[cli.formatting.normalize_progress] normalizing progress", extra={"progress": progress})
    if progress is None:
        return 0.0
    normalized = max(0.0, min(100.0, float(progress)))
    logger.info(
        "[cli.formatting.normalize_progress] progress normalized",
        extra={"progress": progress, "normalized_progress": normalized},
    )
    return normalized


def format_progress_bar(progress: float | int | None, width: int = 30) -> str:
    logger.debug(
        "[cli.formatting.format_progress_bar] formatting progress bar",
        extra={"progress": progress, "width": width},
    )
    normalized = normalize_progress(progress)
    filled = int((normalized / 100.0) * width)
    bar = "#" * filled + "-" * (width - filled)
    formatted = f"[{bar}] {normalized:5.1f}%"
    logger.info(
        "[cli.formatting.format_progress_bar] progress bar formatted",
        extra={"progress": progress, "width": width, "filled": filled},
    )
    return formatted


def format_status_line(status: str, progress: float | int | None) -> str:
    logger.debug(
        "[cli.formatting.format_status_line] formatting status line",
        extra={"status": status, "progress": progress},
    )
    formatted = f"{status}: {format_progress_bar(progress)}"
    logger.info(
        "[cli.formatting.format_status_line] status line formatted",
        extra={"status": status, "progress": progress},
    )
    return formatted
