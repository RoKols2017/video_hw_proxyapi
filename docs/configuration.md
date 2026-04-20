[← Architecture](architecture.md) · [Back to README](../README.md) · [CLI →](cli.md)

# Configuration

## Источник настроек

Проект использует `.env` и пример `.env.example`. По спецификации загрузка конфигурации должна жить в `src/video_app/config/settings.py` через `load_dotenv()` и возвращать структурированный `Settings` dataclass.

## Переменные окружения

| Переменная | Значение по умолчанию | Назначение |
|------------|------------------------|------------|
| `PROXYAPI_API_KEY` | пусто | API-ключ для Proxy API |
| `VIDEO_MODEL` | `veo-3-fast` | Модель генерации видео |
| `VIDEO_SECONDS` | `4` | Длительность видео |
| `VIDEO_OUTPUT_DIR` | `outputs` | Каталог для MP4 и вспомогательных файлов |
| `POLL_INTERVAL_SECONDS` | `5` | Интервал опроса статуса |

## Ограничения из спецификации

| Настройка | Ограничение |
|-----------|-------------|
| `VIDEO_MODEL` | только `veo-3-fast` или `sora-2` |
| `VIDEO_SECONDS` | только `4` |
| `POLL_INTERVAL_SECONDS` | значение должно быть больше `0` |

## Практические рекомендации

- Не храните ключи в коде и не коммитьте рабочий `.env`.
- Используйте `.env.example` как единственный шаблон для команды или деплоя.
- Держите путь вывода в `VIDEO_OUTPUT_DIR`, а не захардкоженным в сервисах.

## Где эти настройки используются

- `cli` получает настройки один раз на запуск.
- `core.client` создаёт OpenAI-compatible клиент для Proxy API.
- `core.service` использует модель, длительность и poll interval.
- `core.storage` использует каталог вывода для файлов и `last_video_id.txt`.

## See Also

- [Getting Started](getting-started.md) — как создать `.env` и подготовить окружение.
- [Architecture](architecture.md) — как конфиг отделён от core и CLI.
- [CLI](cli.md) — какие команды читают эти настройки при запуске.
