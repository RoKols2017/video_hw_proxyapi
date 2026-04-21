# Video HW Proxy API

> Генерация видео через ProxyAPI с единым backend, CLI, Telegram-ботом и Flask-сайтом.

Проект покрывает обе части ДЗ: сначала консольный workflow генерации и проверки статуса, затем два интерфейса поверх того же service-layer. Основная бизнес-логика живёт в `src/video_app/core`, а CLI, Telegram и Flask только используют её.

## Quick Start

```bash
cp .env.example .env
docker compose up --build web
```

Для VPS этот проект разворачивается только через Docker Compose. `venv`, `pip install` и ручной запуск Python-процессов на сервере не требуются.

## Key Features

- **Единый backend API** для CLI, Telegram и Flask без дублирования ProxyAPI-логики.
- **Прогресс-статусы** `queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`.
- **Скачивание MP4** в `outputs/` и отдельная проверка статуса через `test.py`.
- **Telegram-бот** с обновлением одного сообщения и отправкой готового видео.
- **Flask-интерфейс** с `task_id`, progress bar и download endpoint.
- **Production nginx в Docker** с доменом и существующими TLS-сертификатами.

## Example

```bash
docker compose up --build web
docker compose --profile cli up app
docker compose --profile status run --rm status
python bot.py
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Установка, `.env`, первый запуск |
| [Architecture](docs/architecture.md) | Backend/service-layer и границы модулей |
| [Configuration](docs/configuration.md) | Все env-переменные и ограничения |
| [CLI](docs/cli.md) | Консольные entrypoint'ы и сценарии |
| [Interfaces](docs/interfaces.md) | Telegram-бот и Flask-сайт |
| [Deployment](docs/deployment.md) | Docker, nginx, домен и сертификаты |

## VPS Deploy

Для production/VPS используется только Docker Compose:

```bash
NGINX_DOMAIN=your-domain.com SSL_CERTS_DIR=/root/cert/your-domain.com docker compose -f compose.yml -f compose.production.yml up -d --build web bot nginx
```

Что поднимется:
- `web` — Flask-приложение
- `bot` — Telegram-бот
- `nginx` — reverse proxy с TLS

## License

Лицензия в репозитории пока не указана.
