from __future__ import annotations

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def ensure_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    logger.debug("[storage.ensure_output_dir] ensuring output directory", extra={"path": str(path)})
    path.mkdir(parents=True, exist_ok=True)
    logger.info("[storage.ensure_output_dir] output directory ready", extra={"path": str(path)})
    return path


def build_output_video_path(output_dir: str | Path, video_id: str) -> Path:
    directory = ensure_output_dir(output_dir)
    path = directory / f"{video_id}.mp4"
    logger.debug("[storage.build_output_video_path] built output path", extra={"path": str(path), "video_id": video_id})
    return path
