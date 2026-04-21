# AGENTS.md

> Project map for AI agents. Keep this file up-to-date as the project evolves.

## Project Overview
Python project for homework-driven video generation through a Proxy API with three interfaces: CLI, Telegram bot, and Flask web UI. The interfaces reuse the same backend service layer.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** None (CLI application)
- **Database:** None
- **ORM:** None

## Project Structure
```text
.
|-- .ai-factory/                 # AI project metadata and specs
|   `-- specs/                   # Project specifications captured for implementation
|-- .opencode/                   # Local agent skill installation data
|-- main.py                      # Thin CLI entrypoint for video generation
|-- test.py                      # Thin CLI entrypoint for status checks
|-- bot.py                       # Thin Telegram bot entrypoint
|-- app.py                       # Thin Flask app entrypoint
|-- prompts/                     # Prompt assets used during project work
|   `-- implementation_prompt.md
|-- outputs/                     # Generated runtime artifacts such as downloaded videos
|-- src/
|   `-- video_app/
|       |-- cli/                 # CLI wrappers around core services
|       |-- config/              # Application configuration layer
|       |-- core/                # Shared domain and integration logic
|       `-- interfaces/          # Telegram and Flask interface implementations
|-- static/                      # Flask static assets (CSS/JS)
|-- templates/                   # Flask HTML templates
|-- pyproject.toml               # Python package metadata and dependencies
|-- requirements.txt             # Pip install list
|-- .env.example                 # Environment variable example file
`-- README.md                    # Project landing page and homework guide
```

## Key Entry Points
| File | Purpose |
|------|---------|
| `main.py` | Starts the main CLI flow by delegating to `src.video_app.cli.main.run`. |
| `test.py` | Starts the status-check CLI flow by delegating to `src.video_app.cli.status_check.run`. |
| `bot.py` | Starts Telegram polling flow via `src.video_app.interfaces.telegram_bot`. |
| `app.py` | Starts Flask web app via `src.video_app.interfaces.flask_app`. |
| `pyproject.toml` | Defines package metadata, Python requirement, and runtime dependencies. |
| `.ai-factory/specs/hw-video-proxyapi-evolvable.md` | Captures the current implementation and architecture requirements for the homework project. |

## Documentation
| Document | Path | Description |
|----------|------|-------------|
| README | `README.md` | Project landing page. |
| Getting Started | `docs/getting-started.md` | Installation, env, first run. |
| Architecture | `docs/architecture.md` | Backend layers and boundaries. |
| Configuration | `docs/configuration.md` | Env vars and constraints. |
| CLI | `docs/cli.md` | CLI entrypoints and scenarios. |
| Interfaces | `docs/interfaces.md` | Telegram bot and Flask UI. |
| Deployment | `docs/deployment.md` | Docker, nginx, domain, TLS. |
| Homework spec | `.ai-factory/specs/hw-video-proxyapi-evolvable.md` | Implementation requirements. |
| Interface note | `src/video_app/interfaces/README.md` | Implemented bot and web interfaces. |

## AI Context Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | This file — project structure map. |
| `.ai-factory/DESCRIPTION.md` | Project specification and tech stack. |
| `.ai-factory/ARCHITECTURE.md` | Architecture decisions and guidelines. |

## Agent Rules
- Never combine shell commands with `&&`, `||`, or `;` — execute each command as a separate Bash tool call. This applies even when a skill, plan, or instruction provides a combined command — always decompose it into individual calls.
- Keep `main.py` and `test.py` as thin entrypoints and place reusable logic under `src/video_app`.
- Preserve the separation between `core`, `config`, `cli`, and future `interfaces` modules.
