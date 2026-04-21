# Architecture: Layered Architecture

## Overview
This project uses a layered architecture adapted for a small Python CLI application with future interface expansion. The goal is to keep the current homework scope simple while preserving clear boundaries between configuration, reusable business logic, command-line interaction, and upcoming bot or web adapters.

For this project, layered architecture is a better fit than heavier patterns because the domain is still compact, deployment is single-unit, and the main engineering need is separation of concerns rather than advanced domain modeling. The existing folder structure already reflects these boundaries and should be extended, not replaced.

## Decision Rationale
- **Project type:** CLI application for Proxy API video generation with future Telegram and Flask reuse.
- **Tech stack:** Python 3.11+, no framework, no database.
- **Key factor:** keep implementation simple now while preventing CLI concerns from leaking into reusable backend logic.

## Folder Structure
```text
.
|-- main.py                          # Thin entrypoint for generation CLI
|-- test.py                          # Thin entrypoint for status-check CLI
|-- bot.py                           # Thin entrypoint for Telegram bot
|-- app.py                           # Thin entrypoint for Flask web app
`-- src/video_app/
    |-- cli/                         # Presentation layer for terminal interaction
    |   |-- main.py                  # CLI flow for generate command
    |   `-- status_check.py          # CLI flow for status checks
    |-- config/                      # Configuration layer
    |   `-- settings.py              # Env loading and validated settings
    |-- core/                        # Business and integration layer
    |   |-- client.py                # Proxy API client construction
    |   |-- models.py                # Domain data structures
    |   |-- progress.py              # Pure text progress formatting helpers
    |   |-- service.py               # Reusable application service API
    |   `-- storage.py               # Output file and local persistence helpers
    `-- interfaces/                  # Non-CLI adapters
        |-- telegram_bot.py          # Telegram interface implementation
        `-- flask_app.py             # Flask interface implementation
```

## Dependency Rules
The dependency direction must remain simple and explicit.

- ✅ `main.py` and `test.py` may import from `src.video_app.cli` only.
- ✅ `src.video_app.cli` may import from `src.video_app.config` and `src.video_app.core`.
- ✅ `src.video_app.core.service` may coordinate `client`, `models`, `progress`, and `storage`.
- ✅ `src.video_app.interfaces` may import from `config` and `core` when implemented.
- ❌ `src.video_app.core` must not import from `cli` or future `interfaces`.
- ❌ `config` must not depend on `cli` or `interfaces`.
- ❌ terminal printing, argument parsing, and formatting side effects must not be embedded in reusable core models or services.

## Layer Communication
- Entry points delegate immediately to CLI wrapper functions.
- CLI wrappers translate terminal input and output into calls to `core.service`.
- Core services expose interface-agnostic functions and optional callbacks for progress updates.
- Configuration is loaded once and passed inward as structured settings.
- Storage helpers handle local filesystem details so service functions do not duplicate path logic.

## Key Principles
1. Keep reusable logic in `core` and keep interface-specific behavior at the edges.
2. Pass data through structured models and validated settings instead of loose dictionaries.
3. Design progress reporting as callbacks so CLI, Telegram, and Flask can reuse the same service API.

## Code Examples

### Thin Entrypoint
```python
from src.video_app.cli.main import run


if __name__ == "__main__":
    run()
```

### CLI Depending On Core Only
```python
from src.video_app.config.settings import get_settings
from src.video_app.core.service import generate_video


def run() -> None:
    settings = get_settings()

    def on_update(status) -> None:
        print(status)

    result = generate_video("Custom homework prompt", settings, on_update=on_update)
    print(result.output_path)
```

## Anti-Patterns
- ❌ Importing CLI modules from `core` to print progress or parse arguments.
- ❌ Mixing API calls, filesystem writes, and terminal output in one large function.
- ❌ Letting future Telegram or Flask code bypass `core.service` and reimplement workflow logic.
