from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Callable
from urllib import error, parse, request

from src.video_app.config.settings import Settings
from src.video_app.core.client import (
    GEMINI_LONG_RUNNING_API_VERSION,
    resolve_provider_config,
)
from src.video_app.core.models import (
    VideoGenerationResult,
    VideoTaskCreateResult,
    VideoTaskStatus,
    pick_attr,
)
from src.video_app.core.storage import build_output_video_path


logger = logging.getLogger(__name__)

StatusCallback = Callable[[VideoTaskStatus], None]


class VideoServiceError(RuntimeError):
    pass


def create_video_task(prompt: str, settings: Settings) -> VideoTaskCreateResult:
    logger.info("[service.create_video_task] creating video task", extra={"video_model": settings.video_model})
    provider_config = resolve_provider_config(settings)

    if provider_config.provider == "openai":
        result = _create_sora_video(prompt, settings)
    elif provider_config.provider == "google":
        result = _create_veo_video(prompt, settings)
    else:
        raise VideoServiceError(f"Unsupported provider: {provider_config.provider}")

    logger.info(
        "[service.create_video_task] video task created",
        extra={"video_id": result.video_id, "status": result.status, "provider": result.provider},
    )
    return result


def get_video_status(video_id: str, settings: Settings) -> VideoTaskStatus:
    logger.info(
        "[service.get_video_status] fetching video status",
        extra={"video_id": video_id, "video_model": settings.video_model},
    )
    provider_config = resolve_provider_config(settings)
    if provider_config.provider == "openai":
        status = _get_sora_status(video_id, settings)
    elif provider_config.provider == "google":
        status = _get_veo_status(video_id, settings)
    else:
        raise VideoServiceError(f"Unsupported provider: {provider_config.provider}")

    logger.info(
        "[service.get_video_status] video status fetched",
        extra={"video_id": status.video_id, "status": status.status, "progress": status.progress},
    )
    return status


def wait_for_video_completion(
    video_id: str,
    settings: Settings,
    on_update: StatusCallback | None = None,
) -> VideoTaskStatus:
    logger.info("[service.wait_for_video_completion] waiting for completion", extra={"video_id": video_id})
    last_signature: tuple[str, float | None] | None = None

    while True:
        status = get_video_status(video_id, settings)
        signature = (status.status, status.progress)

        if signature != last_signature:
            logger.debug(
                "[service.wait_for_video_completion] status changed",
                extra={"video_id": video_id, "status": status.status, "progress": status.progress},
            )
            _emit_update(on_update, status)
            last_signature = signature

        if status.is_terminal:
            if not status.is_success:
                raise VideoServiceError(status.error_message or f"Video task {video_id} finished with status {status.status}.")
            logger.info("[service.wait_for_video_completion] video completed", extra={"video_id": video_id})
            return status

        logger.debug(
            "[service.wait_for_video_completion] sleeping before next poll",
            extra={"video_id": video_id, "poll_interval_seconds": settings.poll_interval_seconds},
        )
        time.sleep(settings.poll_interval_seconds)


def download_video_file(video_id: str, settings: Settings, output_path: str | None = None) -> str:
    logger.info("[service.download_video_file] downloading video", extra={"video_id": video_id})
    status = get_video_status(video_id, settings)
    if not status.is_success:
        status = wait_for_video_completion(video_id, settings)

    target_path = Path(output_path) if output_path else build_output_video_path(settings.video_output_dir, video_id)
    provider_config = resolve_provider_config(settings)

    if provider_config.provider == "openai":
        _download_sora_video(video_id, settings, target_path)
    elif provider_config.provider == "google":
        _download_veo_video(status, settings, target_path)
    else:
        raise VideoServiceError(f"Unsupported provider: {provider_config.provider}")

    logger.info("[service.download_video_file] video downloaded", extra={"video_id": video_id, "output_path": str(target_path)})
    return str(target_path)


def generate_video(
    prompt: str,
    settings: Settings,
    on_update: StatusCallback | None = None,
) -> VideoGenerationResult:
    logger.info("[service.generate_video] generating video", extra={"video_model": settings.video_model})
    created = create_video_task(prompt, settings)

    initial_status = VideoTaskStatus(
        video_id=created.video_id,
        status=created.status,
        progress=created.progress,
        model=created.model,
        seconds=created.seconds,
        provider=created.provider,
    )
    _emit_update(on_update, initial_status)

    completed = wait_for_video_completion(created.video_id, settings, on_update=on_update)
    output_path = download_video_file(created.video_id, settings)
    result = VideoGenerationResult(
        video_id=created.video_id,
        status=completed.status,
        progress=completed.progress,
        output_path=output_path,
        model=completed.model,
        seconds=completed.seconds,
        provider=completed.provider,
    )
    logger.info("[service.generate_video] generation completed", extra={"video_id": result.video_id, "output_path": result.output_path})
    return result


def _emit_update(callback: StatusCallback | None, status: VideoTaskStatus) -> None:
    if callback is None:
        return
    logger.debug(
        "[service._emit_update] invoking callback",
        extra={"video_id": status.video_id, "status": status.status, "progress": status.progress},
    )
    callback(status)


def _create_sora_video(prompt: str, settings: Settings) -> VideoTaskCreateResult:
    logger.debug("[service._create_sora_video] creating sora task")
    try:
        payload = _sora_request(
            method="POST",
            path="/videos",
            settings=settings,
            body={
                "model": settings.video_model,
                "prompt": prompt,
                "seconds": str(settings.video_seconds),
            },
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("[service._create_sora_video] create failed", exc_info=exc)
        raise VideoServiceError(f"Failed to create Sora video task: {exc}") from exc
    return VideoTaskCreateResult(
        video_id=str(pick_attr(payload, "id")),
        status=str(pick_attr(payload, "status", "queued")),
        progress=_coerce_progress(pick_attr(payload, "progress")),
        model=str(pick_attr(payload, "model", settings.video_model)),
        seconds=int(pick_attr(payload, "seconds", settings.video_seconds)),
        provider="openai",
    )


def _get_sora_status(video_id: str, settings: Settings) -> VideoTaskStatus:
    logger.debug("[service._get_sora_status] retrieving sora status", extra={"video_id": video_id})
    try:
        payload = _sora_request(method="GET", path=f"/videos/{video_id}", settings=settings)
    except Exception as exc:  # noqa: BLE001
        logger.error("[service._get_sora_status] retrieve failed", exc_info=exc)
        raise VideoServiceError(f"Failed to retrieve Sora video status: {exc}") from exc

    error_payload = pick_attr(payload, "error")
    error_message = None
    if error_payload is not None:
        error_message = str(pick_attr(error_payload, "message", error_payload))

    return VideoTaskStatus(
        video_id=str(pick_attr(payload, "id", video_id)),
        status=str(pick_attr(payload, "status", "unknown")),
        progress=_coerce_progress(pick_attr(payload, "progress")),
        model=str(pick_attr(payload, "model", settings.video_model)),
        seconds=int(pick_attr(payload, "seconds", settings.video_seconds)),
        provider="openai",
        error_message=error_message,
    )


def _download_sora_video(video_id: str, settings: Settings, target_path: Path) -> None:
    logger.debug("[service._download_sora_video] downloading sora content", extra={"video_id": video_id, "path": str(target_path)})
    provider_config = resolve_provider_config(settings)
    url = f"{provider_config.base_url}/videos/{video_id}/content?{parse.urlencode({'variant': 'video'})}"
    req = request.Request(url, headers={"Authorization": f"Bearer {settings.proxyapi_api_key}"}, method="GET")
    try:
        with request.urlopen(req, timeout=300) as response:  # noqa: S310
            target_path.write_bytes(response.read())
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        logger.error("[service._download_sora_video] http error", extra={"status": exc.code, "details": details})
        raise VideoServiceError(f"Failed to download Sora video: {details}") from exc
    except error.URLError as exc:
        logger.error("[service._download_sora_video] download request failed", exc_info=exc)
        raise VideoServiceError(f"Failed to request Sora video download: {exc}") from exc


def _sora_request(method: str, path: str, settings: Settings, body: dict | None = None) -> dict:
    provider_config = resolve_provider_config(settings)
    url = f"{provider_config.base_url}{path}"
    headers = {"Authorization": f"Bearer {settings.proxyapi_api_key}"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    logger.debug("[service._sora_request] sending request", extra={"method": method, "url": url})
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=300) as response:  # noqa: S310
            response_bytes = response.read()
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        logger.error("[service._sora_request] http error", extra={"status": exc.code, "details": details})
        raise VideoServiceError(f"Sora request failed with status {exc.code}: {details}") from exc
    except error.URLError as exc:
        logger.error("[service._sora_request] network error", exc_info=exc)
        raise VideoServiceError(f"Failed to reach Sora endpoint: {exc}") from exc

    payload = json.loads(response_bytes.decode("utf-8")) if response_bytes else {}
    logger.debug("[service._sora_request] request completed", extra={"url": url, "keys": sorted(payload.keys())})
    return payload


def _create_veo_video(prompt: str, settings: Settings) -> VideoTaskCreateResult:
    logger.debug("[service._create_veo_video] creating veo task")
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "durationSeconds": settings.video_seconds,
            "aspectRatio": "16:9",
            "resolution": "720p",
            "personGeneration": "allow_all",
        },
    }
    response_payload = _veo_request(
        method="POST",
        path=f"/{GEMINI_LONG_RUNNING_API_VERSION}/models/{settings.video_model}:predictLongRunning",
        settings=settings,
        body=payload,
    )
    operation_name = str(response_payload.get("name", ""))
    if not operation_name:
        raise VideoServiceError("Veo response did not include operation name.")
    return VideoTaskCreateResult(
        video_id=operation_name,
        status="queued",
        progress=0.0,
        model=settings.video_model,
        seconds=settings.video_seconds,
        provider="google",
    )


def _get_veo_status(video_id: str, settings: Settings) -> VideoTaskStatus:
    logger.debug("[service._get_veo_status] retrieving veo status", extra={"video_id": video_id})
    payload = _veo_request(method="GET", path=f"/{GEMINI_LONG_RUNNING_API_VERSION}/{video_id}", settings=settings)

    if not payload.get("done", False):
        metadata = payload.get("metadata", {})
        progress = _coerce_progress(metadata.get("progressPercentage") or metadata.get("progress_percent"))
        return VideoTaskStatus(
            video_id=video_id,
            status="in_progress",
            progress=progress,
            model=settings.video_model,
            seconds=settings.video_seconds,
            provider="google",
        )

    if "error" in payload:
        error_info = payload["error"]
        error_message = str(error_info.get("message", "Veo video generation failed."))
        return VideoTaskStatus(
            video_id=video_id,
            status="failed",
            progress=_coerce_progress(None),
            model=settings.video_model,
            seconds=settings.video_seconds,
            provider="google",
            error_message=error_message,
        )

    generated_video = _extract_veo_generated_video(payload.get("response", {}))
    download_url = generated_video.get("uri")
    return VideoTaskStatus(
        video_id=video_id,
        status="completed",
        progress=100.0,
        model=settings.video_model,
        seconds=settings.video_seconds,
        provider="google",
        download_url=download_url,
    )


def _download_veo_video(status: VideoTaskStatus, settings: Settings, target_path: Path) -> None:
    logger.debug(
        "[service._download_veo_video] downloading veo content",
        extra={"video_id": status.video_id, "download_url": status.download_url, "path": str(target_path)},
    )
    if not status.download_url:
        raise VideoServiceError("Completed Veo task does not contain a download URL.")

    req = request.Request(status.download_url, headers={"x-goog-api-key": settings.proxyapi_api_key}, method="GET")
    try:
        with request.urlopen(req, timeout=300) as response:  # noqa: S310
            target_path.write_bytes(response.read())
    except error.URLError as exc:
        logger.error("[service._download_veo_video] download failed", exc_info=exc)
        raise VideoServiceError(f"Failed to download Veo video: {exc}") from exc


def _veo_request(method: str, path: str, settings: Settings, body: dict | None = None) -> dict:
    provider_config = resolve_provider_config(settings)
    url = f"{provider_config.base_url}{path}"
    headers = {"x-goog-api-key": settings.proxyapi_api_key, "Content-Type": "application/json"}
    data = json.dumps(body).encode("utf-8") if body is not None else None
    logger.debug("[service._veo_request] sending request", extra={"method": method, "url": url})
    req = request.Request(url, data=data, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=300) as response:  # noqa: S310
            response_bytes = response.read()
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        logger.error("[service._veo_request] http error", extra={"status": exc.code, "details": details})
        raise VideoServiceError(f"Veo request failed with status {exc.code}: {details}") from exc
    except error.URLError as exc:
        logger.error("[service._veo_request] network error", exc_info=exc)
        raise VideoServiceError(f"Failed to reach Veo endpoint: {exc}") from exc

    payload = json.loads(response_bytes.decode("utf-8")) if response_bytes else {}
    logger.debug("[service._veo_request] request completed", extra={"url": url, "keys": sorted(payload.keys())})
    return payload


def _extract_veo_generated_video(response_payload: dict) -> dict:
    candidates = []
    generate_video_response = response_payload.get("generateVideoResponse", {})
    candidates.extend(generate_video_response.get("generatedSamples", []))
    candidates.extend(response_payload.get("generatedVideos", []))

    if not candidates:
        raise VideoServiceError("Veo response does not contain generated video metadata.")

    first = candidates[0]
    video_payload = first.get("video") if isinstance(first, dict) and "video" in first else first
    if not isinstance(video_payload, dict):
        raise VideoServiceError("Unexpected Veo generated video payload format.")
    return video_payload


def _coerce_progress(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
