# Video HW Proxy API

> Генерация видео через ProxyAPI с единым backend, CLI, Telegram-ботом и Flask-сайтом.

Проект покрывает обе части ДЗ: сначала консольный workflow генерации и проверки статуса, затем два интерфейса поверх того же service-layer. Основная бизнес-логика живёт в `src/video_app/core`, а CLI, Telegram и Flask только используют её.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

```bash
python main.py
python bot.py
python app.py
```

## Key Features

- **Единый backend API** для CLI, Telegram и Flask без дублирования ProxyAPI-логики.
- **Прогресс-статусы** `queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`.
- **Скачивание MP4** в `outputs/` и отдельная проверка статуса через `test.py`.
- **Telegram-бот** с обновлением одного сообщения и отправкой готового видео.
- **Flask-интерфейс** с `task_id`, progress bar и download endpoint.
- **Production nginx в Docker** с доменом и существующими TLS-сертификатами.

## Example

```bash
python main.py
python test.py
python bot.py
python app.py
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

## License

Лицензия в репозитории пока не указана.
