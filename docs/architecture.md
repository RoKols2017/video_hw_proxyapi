[← Getting Started](getting-started.md) · [Back to README](../README.md) · [Configuration →](configuration.md)

# Architecture

## Выбранный паттерн

Проект остаётся на `Layered Architecture`. Это даёт простые и понятные границы между конфигурацией, service-layer, CLI и интерфейсами второй части.

Подробные правила также зафиксированы в `.ai-factory/ARCHITECTURE.md`.

## Слои проекта

```text
main.py / test.py                  # Тонкие CLI entrypoint'ы
bot.py / app.py                    # Тонкие interface entrypoint'ы
src/video_app/config/              # Загрузка и валидация env
src/video_app/core/                # Общий backend/service layer
src/video_app/cli/                 # Терминальный UX
src/video_app/interfaces/          # Telegram и Flask адаптеры
templates/ + static/               # Flask frontend
outputs/                           # Скачанные видео и служебные файлы
```

## Service layer

Общий backend API находится в `src/video_app/core/service.py`.

Основные функции:

- `create_video_task(...)`
- `get_video_status(...)`
- `wait_for_video_completion(..., on_update=None)`
- `download_video_file(...)`
- `generate_video(..., on_update=None)`

Эти функции:

- не зависят от terminal UI;
- возвращают структурированные модели;
- используют callback `on_update` для прогресса;
- подходят для CLI, Telegram и Flask без дублирования сетевой логики.

## Что где находится

| Слой | Ответственность |
|------|------------------|
| `config` | env, dataclass `Settings`, валидация |
| `core` | ProxyAPI, poll loop, скачивание, dataclass-модели |
| `cli` | печать в терминал, argv, пользовательский вывод |
| `interfaces` | Telegram handlers, Flask routes, threading |

## Зависимости между слоями

| Откуда | Куда можно зависеть |
|--------|----------------------|
| `main.py`, `test.py`, `bot.py`, `app.py` | Только в специализированные entrypoint модули |
| `src.video_app.cli` | В `config` и `core` |
| `src.video_app.interfaces` | В `config` и `core` |
| `src.video_app.core` | Во внутренние модули `core`, но не в `cli` и не в `interfaces` |

## Как работает progress update

- CLI передаёт callback, который печатает статусы в терминал.
- Telegram использует callback для обновления одного сообщения в чате.
- Flask использует callback для обновления состояния задачи в in-memory словаре по `task_id`.

Такой подход позволяет переиспользовать backend без print-ориентированной привязки.

## See Also

- [Configuration](configuration.md) — как настройки попадают в backend и интерфейсы.
- [CLI](cli.md) — как устроен терминальный слой.
- [Interfaces](interfaces.md) — Telegram и Flask поверх общего service-layer.
