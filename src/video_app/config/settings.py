from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from functools import lru_cache


logger = logging.getLogger(__name__)

ALLOWED_VIDEO_MODELS = {"veo-3-fast", "sora-2"}
DEFAULT_POLL_INTERVAL_SECONDS = 5
DEFAULT_VIDEO_OUTPUT_DIR = "outputs"
DEFAULT_LOG_LEVEL = "DEBUG"


@dataclass(frozen=True)
class Settings:
    proxyapi_api_key: str
    video_model: str
    video_seconds: int
    video_output_dir: str
    poll_interval_seconds: int
    log_level: str


def _normalize_log_level(raw_value: str | None) -> str:
    value = (raw_value or DEFAULT_LOG_LEVEL).strip().upper()
    if value not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        logger.warning("[settings._normalize_log_level] unsupported log level, using default", extra={"requested": value})
        return DEFAULT_LOG_LEVEL
    return value


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    logger.debug("[settings._require_env] loaded env presence", extra={"name": name, "is_set": bool(value)})
    if not value:
        raise ValueError(f"Environment variable {name} is required.")
    return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    logger.debug("[settings.get_settings] loading environment")
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Dependency python-dotenv is not installed. Install project dependencies before running the CLI."
        ) from exc

    load_dotenv()

    proxyapi_api_key = _require_env("PROXYAPI_API_KEY")
    video_model = _require_env("VIDEO_MODEL")
    video_seconds_raw = _require_env("VIDEO_SECONDS")
    video_output_dir = os.getenv("VIDEO_OUTPUT_DIR", DEFAULT_VIDEO_OUTPUT_DIR).strip() or DEFAULT_VIDEO_OUTPUT_DIR
    poll_interval_raw = os.getenv("POLL_INTERVAL_SECONDS", str(DEFAULT_POLL_INTERVAL_SECONDS)).strip()
    log_level = _normalize_log_level(os.getenv("LOG_LEVEL"))

    if video_model not in ALLOWED_VIDEO_MODELS:
        logger.error("[settings.get_settings] unsupported video model", extra={"video_model": video_model})
        raise ValueError("VIDEO_MODEL must be one of: veo-3-fast, sora-2.")

    try:
        video_seconds = int(video_seconds_raw)
    except ValueError as exc:
        logger.error("[settings.get_settings] invalid VIDEO_SECONDS", extra={"value": video_seconds_raw})
        raise ValueError("VIDEO_SECONDS must be an integer.") from exc

    if video_seconds != 4:
        logger.error("[settings.get_settings] unsupported VIDEO_SECONDS", extra={"video_seconds": video_seconds})
        raise ValueError("VIDEO_SECONDS must be exactly 4 for this homework.")

    try:
        poll_interval_seconds = int(poll_interval_raw)
    except ValueError as exc:
        logger.error("[settings.get_settings] invalid POLL_INTERVAL_SECONDS", extra={"value": poll_interval_raw})
        raise ValueError("POLL_INTERVAL_SECONDS must be an integer.") from exc

    if poll_interval_seconds <= 0:
        logger.error(
            "[settings.get_settings] non-positive POLL_INTERVAL_SECONDS",
            extra={"poll_interval_seconds": poll_interval_seconds},
        )
        raise ValueError("POLL_INTERVAL_SECONDS must be greater than 0.")

    settings = Settings(
        proxyapi_api_key=proxyapi_api_key,
        video_model=video_model,
        video_seconds=video_seconds,
        video_output_dir=video_output_dir,
        poll_interval_seconds=poll_interval_seconds,
        log_level=log_level,
    )
    logger.info(
        "[settings.get_settings] settings loaded",
        extra={
            "video_model": settings.video_model,
            "video_seconds": settings.video_seconds,
            "video_output_dir": settings.video_output_dir,
            "poll_interval_seconds": settings.poll_interval_seconds,
            "log_level": settings.log_level,
        },
    )
    return settings
