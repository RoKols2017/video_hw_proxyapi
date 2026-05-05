# Video HW Proxy API

> Генерация видео через ProxyAPI с единым backend, CLI, Telegram-ботом и Flask-сайтом.

Проект собирает генерацию видео в один переиспользуемый backend: CLI, Telegram-бот и Flask-интерфейс работают через общий service-layer и не дублируют ProxyAPI-логику.

## Какую задачу решает

Если генерация видео запускается отдельно через скрипты, бот и web-интерфейс, логика статусов, скачивания и обработки ошибок быстро начинает расходиться между интерфейсами.

Этот проект решает проблему за счет одного backend-слоя, который обслуживает сразу несколько способов запуска.

## Что делает решение

- принимает текстовый запрос на генерацию видео;
- отправляет задачу в ProxyAPI;
- отслеживает статусы `queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`;
- сохраняет MP4 в `outputs/`;
- отдает один и тот же workflow через CLI, Telegram и Flask.

## Что получает пользователь

- единый сценарий генерации без расхождений между интерфейсами;
- Telegram-бот для прикладного использования;
- web-интерфейс с progress bar и download endpoint;
- Docker-based запуск для локальной среды и VPS.

## Proof: user flow

```text
text prompt
  -> shared core.service
  -> ProxyAPI task creation
  -> status polling (queued -> in_progress -> downloading -> completed)
  -> MP4 in outputs/
  -> delivery through CLI, Telegram, or Flask
```

## Proof: what is actually implemented

- CLI запускается через `main.py`, а проверка статуса - через `test.py`.
- Telegram-бот принимает обычный текст как prompt, обновляет одно сообщение по мере прогресса и после завершения отправляет MP4.
- Flask поднимает HTML-страницу, создает задачу через `POST /generate`, показывает статус через `GET /status/<task_id>` и отдает файл через `GET /download/<task_id>`.
- Все интерфейсы работают через один `core.service`, а не через дублирующиеся ProxyAPI-вызовы в каждом слое.

## Quick Start

```bash
cp .env.example .env
docker compose -f docker-compose.yml up --build web
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
docker compose -f docker-compose.yml up --build web
docker compose -f docker-compose.yml --profile cli up app
docker compose -f docker-compose.yml --profile status run --rm status
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
NGINX_DOMAIN=your-domain.com SSL_CERTS_DIR=/root/cert/your-domain.com docker compose -f docker-compose.yml -f compose.production.yml up -d --build web bot nginx
```

Что поднимется:
- `web` — Flask-приложение
- `bot` — Telegram-бот
- `nginx` — reverse proxy с TLS

## License

Лицензия в репозитории пока не указана.
