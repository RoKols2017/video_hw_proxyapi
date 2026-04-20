# AGENTS.md

> Project map for AI agents. Keep this file up-to-date as the project evolves.

## Project Overview
Python CLI project for homework-driven video generation through a Proxy API. The current codebase is structured so future Telegram and Flask interfaces can reuse the same backend logic.

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
|-- prompts/                     # Prompt assets used during project work
|   `-- implementation_prompt.md
|-- outputs/                     # Generated runtime artifacts such as downloaded videos
|-- src/
|   `-- video_app/
|       |-- cli/                 # CLI wrappers around core services
|       |-- config/              # Application configuration layer
|       |-- core/                # Shared domain and integration logic
|       `-- interfaces/          # Reserved future interfaces (bot/web)
|-- static/                      # Reserved static assets for future web UI
|-- templates/                   # Reserved templates for future web UI
|-- pyproject.toml               # Python package metadata and dependencies
|-- .env.example                 # Environment variable example file
`-- README.md                    # Project landing page and homework guide
```

## Key Entry Points
| File | Purpose |
|------|---------|
| `main.py` | Starts the main CLI flow by delegating to `src.video_app.cli.main.run`. |
| `test.py` | Starts the status-check CLI flow by delegating to `src.video_app.cli.status_check.run`. |
| `pyproject.toml` | Defines package metadata, Python requirement, and runtime dependencies. |
| `.ai-factory/specs/hw-video-proxyapi-evolvable.md` | Captures the current implementation and architecture requirements for the homework project. |

## Documentation
| Document | Path | Description |
|----------|------|-------------|
| README | `README.md` | Project landing page. |
| Getting Started | `docs/getting-started.md` | Installation, setup, first run. |
| Architecture | `docs/architecture.md` | Layers and dependency rules. |
| Configuration | `docs/configuration.md` | Environment variables and constraints. |
| CLI | `docs/cli.md` | Entrypoints and run scenarios. |
| Homework spec | `.ai-factory/specs/hw-video-proxyapi-evolvable.md` | Implementation requirements. |
| Interface note | `src/video_app/interfaces/README.md` | Future bot and web note. |

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
