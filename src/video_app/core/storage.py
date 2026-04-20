from __future__ import annotations

import logging
from pathlib import Path


logger = logging.getLogger(__name__)

LAST_VIDEO_ID_FILENAME = "last_video_id.txt"


def ensure_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    logger.debug("[storage.ensure_output_dir] ensuring output directory", extra={"path": str(path)})
    path.mkdir(parents=True, exist_ok=True)
    logger.info("[storage.ensure_output_dir] output directory ready", extra={"path": str(path)})
    return path


def save_last_video_id(output_dir: str | Path, video_id: str) -> Path:
    directory = ensure_output_dir(output_dir)
    target = directory / LAST_VIDEO_ID_FILENAME
    logger.debug("[storage.save_last_video_id] saving last video id", extra={"path": str(target), "video_id": video_id})
    target.write_text(f"{video_id}\n", encoding="utf-8")
    logger.info("[storage.save_last_video_id] last video id saved", extra={"path": str(target)})
    return target


def load_last_video_id(output_dir: str | Path) -> str | None:
    target = Path(output_dir) / LAST_VIDEO_ID_FILENAME
    logger.debug("[storage.load_last_video_id] loading last video id", extra={"path": str(target)})
    if not target.exists():
        logger.info("[storage.load_last_video_id] last video id file not found", extra={"path": str(target)})
        return None
    value = target.read_text(encoding="utf-8").strip()
    logger.info("[storage.load_last_video_id] last video id loaded", extra={"path": str(target), "is_set": bool(value)})
    return value or None


def build_output_video_path(output_dir: str | Path, video_id: str) -> Path:
    directory = ensure_output_dir(output_dir)
    path = directory / f"{video_id}.mp4"
    logger.debug("[storage.build_output_video_path] built output path", extra={"path": str(path), "video_id": video_id})
    return path
