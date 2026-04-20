from __future__ import annotations

import logging
from dataclasses import dataclass

from src.video_app.config.settings import Settings


logger = logging.getLogger(__name__)

OPENAI_PROXY_BASE_URL = "https://api.proxyapi.ru/openai/v1"
GEMINI_PROXY_BASE_URL = "https://api.proxyapi.ru/google"
GEMINI_LONG_RUNNING_API_VERSION = "v1beta"


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    model: str
    base_url: str
    api_key_header: str


def resolve_provider_config(settings: Settings) -> ProviderConfig:
    logger.debug("[client.resolve_provider_config] resolving provider", extra={"video_model": settings.video_model})
    if settings.video_model == "sora-2":
        config = ProviderConfig(
            provider="openai",
            model=settings.video_model,
            base_url=OPENAI_PROXY_BASE_URL,
            api_key_header="Authorization",
        )
    elif settings.video_model == "veo-3-fast":
        config = ProviderConfig(
            provider="google",
            model=settings.video_model,
            base_url=GEMINI_PROXY_BASE_URL,
            api_key_header="x-goog-api-key",
        )
    else:
        logger.error("[client.resolve_provider_config] unsupported model", extra={"video_model": settings.video_model})
        raise ValueError(f"Unsupported video model: {settings.video_model}")

    logger.info(
        "[client.resolve_provider_config] provider resolved",
        extra={"provider": config.provider, "base_url": config.base_url, "model": config.model},
    )
    return config


def get_openai_client(settings: Settings):
    config = resolve_provider_config(settings)
    logger.debug(
        "[client.get_openai_client] creating openai-compatible client",
        extra={"provider": config.provider, "base_url": config.base_url},
    )
    if config.provider != "openai":
        logger.error(
            "[client.get_openai_client] invalid provider for openai client",
            extra={"provider": config.provider, "video_model": settings.video_model},
        )
        raise ValueError("OpenAI client can only be used with the sora-2 provider flow.")

    try:
        from openai import OpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError("Dependency openai is not installed. Install project dependencies before generating video.") from exc

    client = OpenAI(api_key=settings.proxyapi_api_key, base_url=config.base_url)
    logger.info("[client.get_openai_client] client created", extra={"base_url": config.base_url})
    return client
