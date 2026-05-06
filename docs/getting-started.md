[Back to README](../README.md) · [Architecture →](architecture.md)

# Getting Started

## Что это за проект

`video_hw_proxyapi` — учебный продукт для генерации видео через ProxyAPI. Он уже включает три интерфейса: консольный запуск, Telegram-бот и Flask-сайт. Все они работают через общий backend в `src/video_app/core`.

## Требования

| Компонент | Требование |
|-----------|------------|
| Python | 3.11+ для локального запуска |
| Docker | Docker Engine с Compose plugin |
| Секреты | Только через `.env` |

## Подготовка

```bash
mkdir -p outputs
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

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
python test.py
python bot.py
python app.py
```

## Запуск через Docker

### CLI

```bash
docker compose --profile cli run --rm app
docker compose --profile status run --rm status
```

### Telegram-бот

```bash
docker compose up -d --build bot
```

### Flask

```bash
docker compose up -d --build web
```

После запуска сайт будет доступен на `http://localhost:5000`.

## Что проверить

- `.env` читается без хардкода секретов.
- `outputs/` монтируется в контейнеры, которые читают или сохраняют MP4.
- `docker compose --profile cli run --rm app` сохраняет `last_video_id.txt`.
- `docker compose --profile status run --rm status` может прочитать `video_id` из `outputs/`.
- `app.py` не запускает сервер при import, а запускает его только в блоке `if __name__ == "__main__"`.

## See Also

- [Architecture](architecture.md) — как общий backend используется во всех интерфейсах.
- [Configuration](configuration.md) — все переменные окружения и значения.
- [Interfaces](interfaces.md) — как работают Telegram и Flask.
