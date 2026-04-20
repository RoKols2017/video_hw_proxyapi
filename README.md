# Video HW Proxy API

> CLI-приложение для домашнего задания по генерации видео через ProxyAPI с переиспользуемым backend API для будущих Telegram и Flask интерфейсов.

Проект решает первую часть ДЗ через два сценария запуска:
- `python main.py` создаёт задачу генерации, ждёт завершения, скачивает MP4 и сохраняет `last_video_id`.
- `python test.py` отдельно проверяет статус уже созданной задачи по `video_id`.

Вся полезная логика находится в `src/video_app/core`, а CLI-слой только настраивает запуск и отображает прогресс в терминале.

## Запуск для части 1

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Заполните `PROXYAPI_API_KEY` в `.env`, затем используйте один из двух режимов:

```bash
python main.py
python test.py
```

## Переменные окружения

| Переменная | Значение | Описание |
|------------|----------|----------|
| `PROXYAPI_API_KEY` | обязательно | ключ ProxyAPI |
| `VIDEO_MODEL` | `veo-3-fast` или `sora-2` | модель генерации |
| `VIDEO_SECONDS` | только `4` | длительность ролика для ДЗ |
| `VIDEO_OUTPUT_DIR` | `outputs` | каталог для MP4 и `last_video_id.txt` |
| `POLL_INTERVAL_SECONDS` | `5` | интервал опроса статуса |
| `LOG_LEVEL` | `DEBUG` | уровень логирования |

## Что делает `python main.py`

- загружает и валидирует настройки из `.env`;
- использует кастомный кинематографичный prompt;
- создаёт задачу генерации через ProxyAPI;
- печатает модель, `video_id` и ASCII-прогресс;
- дожидается финального статуса;
- скачивает MP4 в `outputs/<video_id>.mp4`;
- сохраняет `outputs/last_video_id.txt`.

## Что делает `python test.py`

- читает `video_id` из первого аргумента CLI или из `outputs/last_video_id.txt`;
- запрашивает текущий статус задачи;
- печатает только статус и прогресс;
- ничего не скачивает.

Пример:

```bash
python test.py
python test.py operations/abc123
```

## Структура проекта

```text
main.py                              # Тонкий entrypoint генерации
test.py                              # Тонкий entrypoint проверки статуса
src/video_app/config/settings.py     # Загрузка и валидация env
src/video_app/core/models.py         # Dataclass-модели результата
src/video_app/core/client.py         # Фабрика клиентов и provider config
src/video_app/core/service.py        # Единый backend API для workflow
src/video_app/core/storage.py        # Работа с outputs/ и last_video_id.txt
src/video_app/core/progress.py       # ASCII progress helpers
src/video_app/cli/main.py            # Терминальный flow генерации
src/video_app/cli/status_check.py    # Терминальный flow проверки статуса
src/video_app/interfaces/            # Зарезервировано под bot/web
outputs/                             # MP4 и runtime-артефакты
```

## Архитектура для части 2

Подготовка ко второй части сделана через единый `core.service` API:

- Telegram-бот сможет вызывать те же функции `create_video_task`, `get_video_status`, `wait_for_video_completion`, `download_video_file`, `generate_video`.
- Для Telegram `on_update` callback можно использовать для обновления одного сообщения с прогрессом.
- Для Flask тот же callback можно связать с состоянием задачи по `task_id` и отдавать прогресс в UI.
- CLI, Telegram и Flask не должны дублировать сетевую или файловую логику, они работают поверх одного backend слоя.

Это позволяет продолжать разработку без рефакторинга public API core-модуля.

## Логирование и диагностика

- Логирование управляется через `LOG_LEVEL`.
- Ошибки конфигурации и сетевые ошибки поднимаются с понятным текстом.
- Секреты не выводятся в логах.

## Документация

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Установка, настройка и первый запуск |
| [Architecture](docs/architecture.md) | Слои проекта и правила зависимостей |
| [Configuration](docs/configuration.md) | Переменные окружения и ограничения |
| [CLI](docs/cli.md) | Entry point'ы и сценарии запуска |

## Docker

Локальный запуск через Docker Compose:

```bash
docker compose up --build app
docker compose run --rm status
docker compose down
```

Особенности текущего Docker-набора:

- контейнер получает настройки из `.env`;
- `outputs/` проброшен как bind mount, поэтому MP4 и `last_video_id.txt` остаются в проекте на хосте;
- сервис `app` запускает `python main.py`;
- сервис `status` запускает `python test.py`.

Полезные команды:

```bash
docker compose up --build app
docker compose run --rm status
docker compose ps
docker compose logs app
docker compose down
```

## Ограничения

- В проекте не реализованы Telegram-бот и Flask-приложение.
- Docker добавлен только как локальная оболочка запуска CLI, без отдельной web/db-инфраструктуры.
- Поддержка видео сделана под модели из homework spec: `veo-3-fast` и `sora-2`.

## License

Лицензия в репозитории пока не указана.
