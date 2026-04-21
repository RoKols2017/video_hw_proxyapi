[← Interfaces](interfaces.md) · [Back to README](../README.md)

# Deployment

## Важно

Для VPS-деплоя этот проект запускается только через Docker Compose.

На сервере не нужны:

- `python -m venv`
- `pip install -r requirements.txt`
- ручной запуск `python bot.py` или `python app.py`

Все production-процессы должны подниматься контейнерами.

## Локальный запуск Flask напрямую

```bash
python app.py
```

По умолчанию сайт доступен на `http://localhost:5000`.

## Production в Docker

Для production используется `compose.production.yml`, где:

- Flask-приложение запускается как сервис `web`;
- Telegram-бот запускается как сервис `bot`;
- `nginx` работает как reverse proxy;
- `nginx` принимает `80/443`;
- TLS-сертификаты монтируются с VPS в контейнер.

## Что нужно на VPS

Каталог сертификатов должен содержать:

- `fullchain.pem`
- `privkey.pem`

Пример расположения:

```text
/root/cert/example.com/fullchain.pem
/root/cert/example.com/privkey.pem
```

## Домен задаётся во время деплоя

Домен не хардкодится в проект. Он подставляется через `NGINX_DOMAIN` в шаблон nginx-конфига.

Команда запуска всех production-сервисов:

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f compose.yml -f compose.production.yml up -d --build web bot nginx
```

После запуска сайт будет доступен по:

```text
https://example.com
```

## Что делает nginx

- редиректит `http -> https`;
- использует `server_name` из `NGINX_DOMAIN`;
- подключает существующие сертификаты;
- проксирует запросы на `web:5000` внутри Docker-сети.

## Остановка

```bash
docker compose -f compose.yml -f compose.production.yml down
```

## Что проверить после деплоя

- домен указывает на IP VPS;
- сертификаты доступны в `SSL_CERTS_DIR`;
- `https://<domain>` открывает Flask UI;
- Telegram-бот отвечает через контейнер `bot`;
- загрузка `/status/<task_id>` и `/download/<task_id>` работает;
- `docker compose ps` показывает `web`, `bot`, `nginx` в статусе `Up`.

## Команды без Docker не нужны для VPS-деплоя

Для production-деплоя на VPS не требуется:

- `python -m venv`
- `pip install -r requirements.txt`
- запуск `bot.py` и `app.py` вручную через shell

Всё поднимается через Docker Compose.

## See Also

- [Interfaces](interfaces.md) — какие сервисы публикуются наружу.
- [Configuration](configuration.md) — deploy-переменные для домена и сертификатов.
- [Getting Started](getting-started.md) — базовый локальный запуск до production-деплоя.
