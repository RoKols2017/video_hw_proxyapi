# Homework spec: Proxy API video generator with extensible architecture

## Primary goal
Сейчас нужно реализовать решение, пригодное для сдачи ДЗ по первой части урока:
- генерация видео через Proxy API;
- модель через env: "veo-3-fast" или "sora-2";
- длительность 4 секунды;
- проверка статуса через отдельный test.py;
- скачивание MP4;
- прогресс и статусы в терминале.

## Secondary goal
Архитектура должна быть заранее пригодна для продолжения разработки во второй части урока:
- будущий Telegram-бот;
- будущий Flask-сайт;
- reuse общей backend-логики без рефакторинга ядра.

## Architectural rules
Критически важно:
1. Разделить проект на:
   - core/business logic
   - config
   - cli wrappers
   - future interfaces
2. Не смешивать:
   - вывод в терминал,
   - сетевые вызовы,
   - бизнес-логику,
   - файловую систему,
   - чтение аргументов CLI.
3. main.py и test.py должны быть тонкими entrypoint-обёртками.
4. Вся полезная логика должна жить в src/video_app/core.
5. Код должен быть расширяем для второго этапа без изменения public API core-модуля.

## Deliverables required now
Нужно создать и наполнить:
- main.py
- test.py
- pyproject.toml
- .env.example
- README.md
- src/video_app/config/settings.py
- src/video_app/core/models.py
- src/video_app/core/client.py
- src/video_app/core/service.py
- src/video_app/core/storage.py
- src/video_app/core/progress.py
- src/video_app/cli/main.py
- src/video_app/cli/status_check.py

## Required design

### src/video_app/config/settings.py
- load_dotenv()
- dataclass Settings
- функция get_settings()
- валидация:
  - VIDEO_MODEL только "veo-3-fast" или "sora-2"
  - VIDEO_SECONDS только 4
  - POLL_INTERVAL_SECONDS > 0

### src/video_app/core/models.py
- dataclasses для структурированных данных:
  - VideoTaskCreateResult
  - VideoTaskStatus
  - VideoGenerationResult
- никаких print внутри

### src/video_app/core/client.py
- создание OpenAI-compatible клиента для Proxy API
- функция get_openai_client(settings)

### src/video_app/core/storage.py
- вспомогательные функции:
  - ensure_output_dir(...)
  - save_last_video_id(...)
  - load_last_video_id(...)
  - build_output_video_path(...)
- никаких API-вызовов

### src/video_app/core/progress.py
- утилиты для рендера текстового progress bar
- только formatting helpers
- никаких сетевых вызовов

### src/video_app/core/service.py
Центральный backend API.
Должен содержать функции:
- create_video_task(prompt: str, settings) -> VideoTaskCreateResult
- get_video_status(video_id: str, settings) -> VideoTaskStatus
- wait_for_video_completion(video_id: str, settings, on_update=None) -> VideoTaskStatus
- download_video_file(video_id: str, settings, output_path=None) -> str
- generate_video(prompt: str, settings, on_update=None) -> VideoGenerationResult

Требования:
- on_update вызывается при изменении статуса/прогресса;
- это нужно для будущего Telegram-бота и Flask;
- никаких жёстких привязок к terminal UI;
- никакой зависимости от Flask/telebot;
- ошибки обрабатываются аккуратно и поднимаются с понятным текстом.

### src/video_app/cli/main.py
- использует core.service.generate_video(...)
- содержит свой кастомный prompt, не про чашку кофе;
- печатает:
  - модель
  - video_id
  - прогресс
  - путь к файлу
- сохраняет last_video_id в outputs/last_video_id.txt

### src/video_app/cli/status_check.py
- читает video_id из argv или outputs/last_video_id.txt
- вызывает core.service.get_video_status(...)
- печатает статус в консоль
- не скачивает видео

## Homework requirements for part 1
- решение должно быть полностью рабочим локально;
- подходить для скриншотов:
  - код с кастомным промптом;
  - терминал с прогрессом;
  - отдельный запуск test.py;
  - mp4 в outputs/.

## Forward compatibility requirements for part 2
В README нужно явно описать, что:
- Telegram-бот и Flask-сайт будут использовать core.service;
- для Telegram progress callback будет обновлять одно сообщение;
- для Flask progress callback будет обновлять состояние задачи по task_id;
- текущая архитектура подготовлена под bot.py и app.py.

## Constraints
- Не реализовывать Telegram и Flask сейчас.
- Не писать Docker сейчас.
- Не писать server deploy сейчас.
- Не использовать requests без необходимости.
- Не смешивать всё в одном request.py-файле.
- Но в README отметить, как эта структура будет продолжена во 2-й части.
