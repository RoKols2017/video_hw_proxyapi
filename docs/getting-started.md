[Back to README](../README.md) · [Architecture →](architecture.md)

# Getting Started

## Что это за проект

`video_hw_proxyapi` готовит CLI-решение для домашнего задания по генерации видео через Proxy API. Первая часть фокусируется на локальном запуске и разделении кода, вторая будет использовать то же ядро из Telegram-бота и Flask-приложения.

## Текущее состояние

- В репозитории уже есть Python-пакет, entrypoint'ы и архитектурные документы.
- Реализация должна следовать спецификации в `.ai-factory/specs/hw-video-proxyapi-evolvable.md`.
- Команды `python main.py` и `python test.py` зарезервированы как основные способы запуска.

## Требования

| Компонент | Требование |
|-----------|------------|
| Python | 3.11+ |
| Пакетный менеджер | `pip` |
| Зависимости | `openai`, `python-dotenv` |
| Секреты | Через `.env` |

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Настройка окружения

Создайте локальный `.env` на основе примера:

```bash
cp .env.example .env
```

Минимальный набор настроек уже описан в `.env.example`:

```env
PROXYAPI_API_KEY=
VIDEO_MODEL=veo-3-fast
VIDEO_SECONDS=4
VIDEO_OUTPUT_DIR=outputs
POLL_INTERVAL_SECONDS=5
```

## Первый запуск

Основные команды проекта:

```bash
python main.py
python test.py
```

`main.py` предназначен для запуска генерации, а `test.py` для отдельной проверки статуса по `video_id`. Если прикладная часть ещё не реализована, ориентируйтесь на эти команды как на целевой интерфейс проекта.

## Что проверить после запуска

- Интерпретатор видит пакет из `src/`.
- Значения в `.env` читаются без хардкода секретов.
- Папка `outputs/` используется как целевой каталог для артефактов.

## See Also

- [Architecture](architecture.md) — как разделены слои и зависимости.
- [Configuration](configuration.md) — что означает каждая переменная окружения.
- [CLI](cli.md) — какие entrypoint'ы предусмотрены в проекте.
