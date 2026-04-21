[← Architecture](architecture.md) · [Back to README](../README.md) · [CLI →](cli.md)

# Configuration

## Источник настроек

Проект использует `.env` и `.env.example`. Конфигурация загружается в `src/video_app/config/settings.py` через `load_dotenv()` и возвращается как dataclass `Settings`.

## Переменные окружения

| Переменная | Значение по умолчанию | Назначение |
|------------|------------------------|------------|
| `PROXYAPI_API_KEY` | пусто | ключ ProxyAPI |
| `VIDEO_MODEL` | `veo-3-fast` | модель видео |
| `VIDEO_SECONDS` | `4` | длина ролика |
| `VIDEO_OUTPUT_DIR` | `outputs` | каталог MP4 и служебных файлов |
| `POLL_INTERVAL_SECONDS` | `5` | интервал poll loop |
| `LOG_LEVEL` | `DEBUG` | уровень логирования |
| `BOT_TOKEN` | пусто | токен Telegram-бота |
| `FLASK_HOST` | `0.0.0.0` | host Flask |
| `FLASK_PORT` | `5000` | порт Flask |

## Ограничения модели

| Настройка | Ограничение |
|-----------|-------------|
| `VIDEO_MODEL` | только `veo-3-fast` или `sora-2` |
| `VIDEO_SECONDS` | только `4` |
| `POLL_INTERVAL_SECONDS` | значение должно быть больше `0` |

## Production-переменные для nginx в Docker

Эти значения не хранятся в проекте жёстко и передаются во время деплоя:

| Переменная | Назначение |
|------------|------------|
| `NGINX_DOMAIN` | доменное имя для `server_name` |
| `SSL_CERTS_DIR` | путь на VPS к каталогу с `fullchain.pem` и `privkey.pem` |

Пример запуска:

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f compose.yml -f compose.production.yml up -d --build web nginx
```

## Практические рекомендации

- Не коммить рабочий `.env`.
- Не хранить секреты в коде и README.
- Для production-деплоя задавать домен и путь к сертификатам только командой запуска.

## Где используются настройки

- `core.service` использует модель, длительность и poll interval.
- `telegram_bot.py` требует `BOT_TOKEN`.
- `app.py` использует `FLASK_HOST` и `FLASK_PORT`.
- `compose.production.yml` использует `NGINX_DOMAIN` и `SSL_CERTS_DIR`.

## See Also

- [CLI](cli.md) — какие команды используют эти переменные.
- [Interfaces](interfaces.md) — какие интерфейсы требуют дополнительные env.
- [Deployment](deployment.md) — как использовать домен и сертификаты на VPS.
