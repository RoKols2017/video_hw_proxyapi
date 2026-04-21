[← Configuration](configuration.md) · [Back to README](../README.md) · [Interfaces →](interfaces.md)

# CLI

## Entry point'ы

| Файл | Назначение |
|------|------------|
| `main.py` | Генерация видео |
| `test.py` | Проверка статуса |

Оба файла остаются тонкими entrypoint'ами и только делегируют в `src.video_app.cli.*`.

## `python main.py`

```bash
python main.py
```

Что делает:

- загружает настройки;
- использует кастомный кинематографичный prompt;
- вызывает `core.service.generate_video(...)`;
- печатает модель, `video_id`, прогресс и итоговый путь;
- сохраняет `outputs/last_video_id.txt`.

## `python test.py`

```bash
python test.py
python test.py <video_id>
```

Что делает:

- вызывает `core.service.get_video_status(...)`;
- читает `video_id` из argv или `outputs/last_video_id.txt`;
- печатает статус и прогресс;
- не скачивает видео.

## Почему CLI не содержит backend-логику

CLI нужен только для терминального UX. Всё, что относится к ProxyAPI, poll loop, скачиванию MP4 и provider-specific логике, находится в `core.service` и переиспользуется в Telegram/Flask.

## Что относится к CLI-слою

- чтение аргументов;
- печать статусов;
- вывод ошибок пользователю;
- выбор, как отобразить progress bar.

## Что не относится к CLI-слою

- сетевые вызовы к ProxyAPI;
- poll loop и state machine задачи;
- скачивание MP4;
- dataclass-модели результатов.

## See Also

- [Interfaces](interfaces.md) — как тот же backend используется в Telegram и Flask.
- [Architecture](architecture.md) — границы между слоями.
- [Getting Started](getting-started.md) — быстрый запуск CLI.
