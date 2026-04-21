from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass
from typing import Any

from src.video_app.config.settings import get_settings
from src.video_app.core.models import VideoTaskStatus
from src.video_app.core.service import VideoServiceError, generate_video


logger = logging.getLogger(__name__)


@dataclass
class UserTaskState:
    status: str
    progress: float | None
    video_id: str | None
    output_path: str | None
    error_message: str | None


def run_bot_polling() -> None:
    try:
        import telebot
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Dependency pyTelegramBotAPI is not installed. Install project dependencies before running bot.py."
        ) from exc

    settings = get_settings()
    _configure_logging(settings.log_level)

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is required in .env to run Telegram bot.")

    bot = telebot.TeleBot(bot_token)
    user_tasks: dict[int, UserTaskState] = {}
    task_lock = threading.Lock()

    @bot.message_handler(commands=["start"])
    def on_start(message: Any) -> None:
        bot.reply_to(
            message,
            "Привет! Отправь текстовый prompt, и я сгенерирую видео через ProxyAPI.\n"
            "Команда /help покажет инструкции.",
        )

    @bot.message_handler(commands=["help"])
    def on_help(message: Any) -> None:
        bot.reply_to(
            message,
            "Как пользоваться:\n"
            "1) Отправь обычный текстовый prompt.\n"
            "2) Я покажу статусы queued/in_progress/downloading/completed.\n"
            "3) После завершения отправлю видео в этот чат.",
        )

    @bot.message_handler(func=lambda msg: bool(msg.text and not msg.text.startswith("/")))
    def on_prompt(message: Any) -> None:
        prompt = message.text.strip()
        if not prompt:
            bot.reply_to(message, "Пустой prompt. Отправь текст для генерации видео.")
            return

        progress_message = bot.send_message(message.chat.id, "Статус: queued\nПрогресс: 0%")
        worker = threading.Thread(
            target=_run_generation_worker,
            args=(bot, message.chat.id, message.from_user.id, progress_message.message_id, prompt, user_tasks, task_lock),
            daemon=True,
        )
        worker.start()

    logger.info("[telegram_bot.run_bot_polling] bot polling started")
    bot.infinity_polling(skip_pending=True)


def _run_generation_worker(
    bot: Any,
    chat_id: int,
    user_id: int,
    progress_message_id: int,
    prompt: str,
    user_tasks: dict[int, UserTaskState],
    task_lock: threading.Lock,
) -> None:
    settings = get_settings()

    def on_update(status: VideoTaskStatus) -> None:
        with task_lock:
            user_tasks[user_id] = UserTaskState(
                status=status.status,
                progress=status.progress,
                video_id=status.video_id,
                output_path=None,
                error_message=status.error_message,
            )

        text = _format_status_text(status)
        _safe_edit_message(bot, chat_id, progress_message_id, text)

    try:
        result = generate_video(prompt, settings, on_update=on_update)
        with task_lock:
            user_tasks[user_id] = UserTaskState(
                status="completed",
                progress=100.0,
                video_id=result.video_id,
                output_path=result.output_path,
                error_message=None,
            )

        _safe_edit_message(
            bot,
            chat_id,
            progress_message_id,
            f"Статус: completed\nПрогресс: 100%\nVideo ID: {result.video_id}",
        )

        with open(result.output_path, "rb") as video_file:
            bot.send_video(chat_id, video_file, caption=f"Готово. Модель: {result.model}")
    except VideoServiceError as exc:
        _safe_edit_message(bot, chat_id, progress_message_id, f"Статус: failed\nОшибка: {exc}")
        bot.send_message(chat_id, f"Ошибка генерации видео: {exc}")
    except Exception as exc:  # noqa: BLE001
        logger.error("[telegram_bot._run_generation_worker] unexpected error", exc_info=exc)
        _safe_edit_message(bot, chat_id, progress_message_id, f"Статус: error\nОшибка: {exc}")
        bot.send_message(chat_id, f"Непредвиденная ошибка: {exc}")


def _format_status_text(status: VideoTaskStatus) -> str:
    progress = f"{(status.progress or 0.0):.0f}%"
    lines = [f"Статус: {status.status}", f"Прогресс: {progress}", f"Video ID: {status.video_id}"]
    if status.error_message:
        lines.append(f"Ошибка: {status.error_message}")
    return "\n".join(lines)


def _safe_edit_message(bot: Any, chat_id: int, message_id: int, text: str) -> None:
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)
    except Exception:  # noqa: BLE001
        pass


def _configure_logging(log_level: str) -> None:
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(log_level)
        return
    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
