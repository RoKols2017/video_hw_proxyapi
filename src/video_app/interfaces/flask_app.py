from __future__ import annotations

import logging
import threading
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file

from src.video_app.config.settings import get_settings
from src.video_app.core.models import VideoTaskStatus
from src.video_app.core.service import VideoServiceError, generate_video


logger = logging.getLogger(__name__)


@dataclass
class WebTaskState:
    task_id: str
    prompt: str
    status: str
    progress: float
    video_id: str | None = None
    output_path: str | None = None
    error_message: str | None = None


def create_flask_app() -> Flask:
    settings = get_settings()
    _configure_logging(settings.log_level)

    app = Flask(__name__, template_folder="../../../templates", static_folder="../../../static")
    tasks: dict[str, WebTaskState] = {}
    tasks_lock = threading.Lock()

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.post("/generate")
    def generate() -> tuple[dict[str, str], int]:
        payload = request.get_json(silent=True) or {}
        prompt = (payload.get("prompt") or request.form.get("prompt") or "").strip()
        if not prompt:
            return {"error": "Prompt is required"}, 400

        task_id = str(uuid.uuid4())
        with tasks_lock:
            tasks[task_id] = WebTaskState(
                task_id=task_id,
                prompt=prompt,
                status="queued",
                progress=0.0,
            )

        worker = threading.Thread(
            target=_run_web_generation_worker,
            args=(task_id, prompt, tasks, tasks_lock),
            daemon=True,
        )
        worker.start()

        return {
            "task_id": task_id,
            "status_url": f"/status/{task_id}",
            "download_url": f"/download/{task_id}",
        }, 202

    @app.get("/status/<task_id>")
    def status(task_id: str):
        with tasks_lock:
            task = tasks.get(task_id)
        if task is None:
            return {"error": "Task not found"}, 404
        return jsonify(asdict(task))

    @app.get("/download/<task_id>")
    def download(task_id: str):
        with tasks_lock:
            task = tasks.get(task_id)
        if task is None:
            abort(404, description="Task not found")
        if task.status != "completed" or not task.output_path:
            abort(409, description="Video is not ready yet")

        path = Path(task.output_path)
        if not path.exists():
            abort(404, description="Generated file not found")

        return send_file(path, as_attachment=True, download_name=f"{task.task_id}.mp4", mimetype="video/mp4")

    return app


def _run_web_generation_worker(
    task_id: str,
    prompt: str,
    tasks: dict[str, WebTaskState],
    tasks_lock: threading.Lock,
) -> None:
    settings = get_settings()

    def on_update(status: VideoTaskStatus) -> None:
        with tasks_lock:
            task = tasks.get(task_id)
            if task is None:
                return
            task.status = status.status
            task.progress = float(status.progress or 0.0)
            task.video_id = status.video_id
            task.error_message = status.error_message

    try:
        result = generate_video(prompt, settings, on_update=on_update)
        with tasks_lock:
            task = tasks.get(task_id)
            if task is None:
                return
            task.status = "completed"
            task.progress = 100.0
            task.video_id = result.video_id
            task.output_path = result.output_path
            task.error_message = None
    except VideoServiceError as exc:
        with tasks_lock:
            task = tasks.get(task_id)
            if task is None:
                return
            task.status = "failed"
            task.error_message = str(exc)
    except Exception as exc:  # noqa: BLE001
        logger.error("[flask_app._run_web_generation_worker] unexpected error", exc_info=exc)
        with tasks_lock:
            task = tasks.get(task_id)
            if task is None:
                return
            task.status = "error"
            task.error_message = str(exc)


def _configure_logging(log_level: str) -> None:
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(log_level)
        return
    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
