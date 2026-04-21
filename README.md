# Video HW Proxy API

Проект для ДЗ по генерации видео через ProxyAPI.

Сейчас поддержаны три интерфейса поверх общего backend слоя:
- консольный (`python main.py`, `python test.py`)
- Telegram-бот (`python bot.py`)
- Flask-сайт (`python app.py`)

## Что делает проект

- создаёт задачу генерации видео по prompt;
- отслеживает статус (`queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`);
- скачивает MP4 в `outputs/`;
- позволяет проверять статус отдельно;
- переиспользует одну backend-логику во всех интерфейсах.

## Архитектура

### Backend (`src/video_app/core`)

Общий service-layer с API:
- `create_video_task(...)`
- `get_video_status(...)`
- `wait_for_video_completion(..., on_update=None)`
- `download_video_file(...)`
- `generate_video(..., on_update=None)`

Backend возвращает структурированные dataclass-модели и использует callback `on_update`.
UI-слои (CLI/Telegram/Flask) не дублируют ProxyAPI логику.

### Telegram frontend

- файл запуска: `bot.py`
- реализация: `src/video_app/interfaces/telegram_bot.py`
- команды: `/start`, `/help`
- любой текст обрабатывается как prompt
- прогресс обновляется в одном сообщении
- после завершения отправляется видео через `send_video`

### Flask frontend

- файл запуска: `app.py`
- реализация: `src/video_app/interfaces/flask_app.py`
- роуты:
  - `GET /`
  - `POST /generate`
  - `GET /status/<task_id>`
  - `GET /download/<task_id>`
- задачи выполняются в `threading.Thread`
- состояние хранится in-memory (`tasks`)

## Конфигурация (.env)

Создай `.env` из примера:

```bash
cp .env.example .env
```

Основные переменные:

| Переменная | Описание |
|---|---|
| `PROXYAPI_API_KEY` | Ключ ProxyAPI |
| `VIDEO_MODEL` | `veo-3-fast` или `sora-2` (по умолчанию рекомендуется `veo-3-fast`) |
| `VIDEO_SECONDS` | Для ДЗ должно быть `4` |
| `VIDEO_OUTPUT_DIR` | Каталог артефактов (обычно `outputs`) |
| `POLL_INTERVAL_SECONDS` | Интервал опроса статуса |
| `LOG_LEVEL` | Уровень логирования |
| `BOT_TOKEN` | Токен Telegram-бота |
| `FLASK_HOST` | Хост Flask (`0.0.0.0`) |
| `FLASK_PORT` | Порт Flask (`5000`) |

## Установка зависимостей

Вариант через pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Или через editable install:

```bash
pip install -e .
```

## Запуск

### 1) Консольная версия

```bash
python main.py
python test.py
```

`main.py` запускает генерацию и скачивание.
`test.py` проверяет статус по `video_id` из аргумента или `outputs/last_video_id.txt`.

### 2) Telegram-бот

```bash
python bot.py
```

После запуска отправь боту обычный текстовый prompt.

### 3) Flask-сайт

```bash
python app.py
```

Открой в браузере `http://localhost:5000`.

### 4) Production nginx в Docker с доменом и готовыми сертификатами

Домен и путь к сертификатам задаются во время деплоя, без хардкода в проекте.

Пример для VPS, где сертификаты уже лежат в `/root/cert/<domain>/`:

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f compose.yml -f compose.production.yml up -d --build web nginx
```

Что ожидается в каталоге сертификатов:

- `fullchain.pem`
- `privkey.pem`

После запуска сайт будет доступен по `https://example.com`.

Для локальной разработки Flask можно запускать напрямую:

```bash
python app.py
```

Остановить стек:

```bash
docker compose down
```

## Проверка статуса и скачивание

- Telegram: бот сам обновляет статус и отправляет готовый файл.
- Flask: фронт опрашивает `/status/<task_id>`, скачивание через `/download/<task_id>`.
- CLI: `python test.py`.

Сгенерированные файлы сохраняются в `outputs/`.

## Какие скриншоты приложить к ДЗ

1. Код с кастомным prompt (например `src/video_app/cli/main.py`).
2. Терминал или Telegram/Flask с прогрессом и статусами (`queued -> in_progress -> completed`).
3. Готовое видео (первые/последние кадры или ссылка/QR на скачивание).

## Ограничения текущей версии

- хранение задач in-memory (без БД);
- без Docker/deploy-автоматизации для этой итерации;
- без очередей задач, используется `threading`.
