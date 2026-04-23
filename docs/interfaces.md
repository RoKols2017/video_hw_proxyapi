[← CLI](cli.md) · [Back to README](../README.md) · [Deployment →](deployment.md)

# Interfaces

## Telegram-бот

### Точка входа

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f docker-compose.yml -f compose.production.yml up -d --build bot
```

### Реализация

- `bot.py`
- `src/video_app/interfaces/telegram_bot.py`

### Поведение

- `/start` — краткое приветствие;
- `/help` — инструкция;
- любой обычный текст — prompt для генерации видео.

После старта генерации бот:

- отправляет одно сообщение со статусом;
- обновляет это сообщение по мере прогресса;
- использует статусы `queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`;
- после завершения отправляет MP4 через `send_video`.

### Хранение состояния

Используется in-memory словарь `user_tasks`, где ключ — `user_id`.

## Flask-сайт

### Точка входа

```bash
docker compose -f docker-compose.yml up --build web
```

### Реализация

- `app.py`
- `src/video_app/interfaces/flask_app.py`
- `templates/index.html`
- `static/style.css`
- `static/app.js`

### Роуты

| Роут | Назначение |
|------|------------|
| `GET /` | HTML-страница с формой |
| `POST /generate` | создание новой задачи |
| `GET /status/<task_id>` | текущее состояние задачи |
| `GET /download/<task_id>` | скачивание MP4 |

### Хранение состояния

Используется in-memory словарь `tasks`, ключ — `task_id` (`uuid.uuid4()`).
Для refresh-flow браузер дополнительно сохраняет текущий `task_id` в `localStorage`, чтобы после перезагрузки страницы возобновить polling и сохранить доступ к `/download/<task_id>`.

### Фоновое выполнение

Генерация запускается в `threading.Thread`, чтобы Flask-роуты не блокировались тяжёлой backend-логикой.

## Что общего у интерфейсов

- оба используют один и тот же `core.service`;
- оба получают обновления через `on_update` callback;
- оба не дублируют ProxyAPI-вызовы;
- оба работают поверх общего конфигурационного слоя.
- оба используют общий каталог `outputs/`, который должен быть доступен runtime-сервисам через Docker volume mount.

## See Also

- [Deployment](deployment.md) — как публиковать Flask через nginx в Docker.
- [Configuration](configuration.md) — `BOT_TOKEN`, `FLASK_HOST`, `FLASK_PORT` и deploy-переменные.
- [Architecture](architecture.md) — роль service-layer в интерфейсах.
