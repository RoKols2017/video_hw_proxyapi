from __future__ import annotations

import logging
import sys

from src.video_app.config.settings import get_settings
from src.video_app.core.progress import format_status_line
from src.video_app.core.service import get_video_status
from src.video_app.core.storage import load_last_video_id


logger = logging.getLogger(__name__)


def run() -> None:
    try:
        bootstrap_settings = get_settings()
        _configure_logging(bootstrap_settings.log_level)
        settings = get_settings()
        logger.info("[cli.status_check.run] status cli started")
        video_id = _resolve_video_id(settings.video_output_dir)
        status = get_video_status(video_id, settings)
        print(f"Video ID: {status.video_id}")
        print(f"Model: {status.model}")
        print(format_status_line(status.status, status.progress))
        if status.error_message:
            print(f"Error message: {status.error_message}")
        logger.info(
            "[cli.status_check.run] status cli finished",
            extra={"video_id": status.video_id, "status": status.status},
        )
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).error("[cli.status_check.run] status check failed", exc_info=exc)
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def _resolve_video_id(output_dir: str) -> str:
    cli_video_id = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    if cli_video_id:
        logger.debug("[cli.status_check._resolve_video_id] using argv video id", extra={"video_id": cli_video_id})
        return cli_video_id

    saved_video_id = load_last_video_id(output_dir)
    if saved_video_id:
        logger.debug(
            "[cli.status_check._resolve_video_id] using stored video id",
            extra={"video_id": saved_video_id, "output_dir": output_dir},
        )
        return saved_video_id

    logger.error("[cli.status_check._resolve_video_id] missing video id", extra={"output_dir": output_dir})
    raise ValueError("Provide video_id as an argument or run python main.py first to save outputs/last_video_id.txt.")


def _configure_logging(log_level: str) -> None:
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(log_level)
        return
    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
