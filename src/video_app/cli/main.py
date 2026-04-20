from __future__ import annotations

import logging
import sys

from src.video_app.config.settings import get_settings
from src.video_app.core.models import VideoTaskStatus
from src.video_app.core.progress import format_status_line
from src.video_app.core.service import generate_video
from src.video_app.core.storage import save_last_video_id


logger = logging.getLogger(__name__)

HOMEWORK_PROMPT = (
    "Cinematic nighttime tracking shot over a rain-soaked embankment in Saint Petersburg, "
    "a lone courier in a dark reflective coat walks toward camera through blue neon fog, "
    "wet cobblestones mirror the city lights, realistic motion, dramatic atmosphere, filmic lighting."
)


def run() -> None:
    try:
        bootstrap_settings = get_settings()
        _configure_logging(bootstrap_settings.log_level)
        settings = get_settings()
        logger.info("[cli.main.run] generation cli started", extra={"video_model": settings.video_model})
        print(f"Model: {settings.video_model}")
        print("Prompt: cinematic rainy-night city scene")

        def on_update(status: VideoTaskStatus) -> None:
            logger.debug(
                "[cli.main.run] rendering status update",
                extra={"video_id": status.video_id, "status": status.status, "progress": status.progress},
            )
            print(f"Video ID: {status.video_id}")
            print(format_status_line(status.status, status.progress))

        result = generate_video(HOMEWORK_PROMPT, settings, on_update=on_update)
        save_last_video_id(settings.video_output_dir, result.video_id)
        print(f"Saved video ID: {result.video_id}")
        print(f"Output file: {result.output_path}")
        logger.info(
            "[cli.main.run] generation cli finished",
            extra={"video_id": result.video_id, "output_path": result.output_path},
        )
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).error("[cli.main.run] generation failed", exc_info=exc)
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def _configure_logging(log_level: str) -> None:
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(log_level)
        return
    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
