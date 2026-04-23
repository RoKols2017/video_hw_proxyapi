from __future__ import annotations

import logging
from pathlib import Path

from src.video_app.core.storage import ensure_output_dir


logger = logging.getLogger(__name__)

LAST_VIDEO_ID_FILENAME = "last_video_id.txt"


def save_last_video_id(output_dir: str | Path, video_id: str) -> Path:
    directory = ensure_output_dir(output_dir)
    target = directory / LAST_VIDEO_ID_FILENAME
    logger.debug("[cli.state.save_last_video_id] saving last video id", extra={"path": str(target), "video_id": video_id})
    target.write_text(f"{video_id}\n", encoding="utf-8")
    logger.info("[cli.state.save_last_video_id] last video id saved", extra={"path": str(target)})
    return target


def load_last_video_id(output_dir: str | Path) -> str | None:
    target = Path(output_dir) / LAST_VIDEO_ID_FILENAME
    logger.debug("[cli.state.load_last_video_id] loading last video id", extra={"path": str(target)})
    if not target.exists():
        logger.info("[cli.state.load_last_video_id] last video id file not found", extra={"path": str(target)})
        return None
    value = target.read_text(encoding="utf-8").strip()
    logger.info("[cli.state.load_last_video_id] last video id loaded", extra={"path": str(target), "is_set": bool(value)})
    return value or None
