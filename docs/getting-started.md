[Back to README](../README.md) · [Architecture →](architecture.md)

# Getting Started

## Что это за проект

`video_hw_proxyapi` — учебный продукт для генерации видео через ProxyAPI. Он уже включает три интерфейса: консольный запуск, Telegram-бот и Flask-сайт. Все они работают через общий backend в `src/video_app/core`.

## Требования

| Компонент | Требование |
|-----------|------------|
| Python | 3.11+ |
| Пакетный менеджер | `pip` |
| Основные зависимости | `openai`, `python-dotenv`, `flask`, `pyTelegramBotAPI` |
| Секреты | Только через `.env` |

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Альтернатива:

```bash
pip install -e .
```

## Настройка `.env`

```bash
cp .env.example .env
```

Минимально нужно заполнить:

```env
PROXYAPI_API_KEY=
VIDEO_MODEL=veo-3-fast
VIDEO_SECONDS=4
VIDEO_OUTPUT_DIR=outputs
POLL_INTERVAL_SECONDS=5
LOG_LEVEL=DEBUG
BOT_TOKEN=
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Первый запуск

### CLI

```bash
python main.py
python test.py
```

### Telegram-бот

```bash
python bot.py
```

### Flask

```bash
python app.py
```

После запуска сайт будет доступен на `http://localhost:5000`.

## Что проверить

- `.env` читается без хардкода секретов.
- `outputs/` создаётся автоматически.
- `python main.py` сохраняет `last_video_id.txt`.
- `python test.py` может прочитать `video_id` из `outputs/`.
- `bot.py` и `app.py` стартуют без автогенерации при import.

## See Also

- [Architecture](architecture.md) — как общий backend используется во всех интерфейсах.
- [Configuration](configuration.md) — все переменные окружения и значения.
- [Interfaces](interfaces.md) — как работают Telegram и Flask.
