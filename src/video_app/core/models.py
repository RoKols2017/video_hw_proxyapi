from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VideoTaskCreateResult:
    video_id: str
    status: str
    progress: float | None
    model: str
    seconds: int
    provider: str


@dataclass(frozen=True)
class VideoTaskStatus:
    video_id: str
    status: str
    progress: float | None
    model: str
    seconds: int
    provider: str
    download_url: str | None = None
    error_message: str | None = None

    @property
    def is_terminal(self) -> bool:
        return self.status in {"completed", "failed", "cancelled", "expired"}

    @property
    def is_success(self) -> bool:
        return self.status == "completed"


@dataclass(frozen=True)
class VideoGenerationResult:
    video_id: str
    status: str
    progress: float | None
    output_path: str
    model: str
    seconds: int
    provider: str


def pick_attr(payload: Any, name: str, default: Any = None) -> Any:
    if isinstance(payload, dict):
        return payload.get(name, default)
    return getattr(payload, name, default)
