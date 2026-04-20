# Project: Video HW Proxy API

## Overview
CLI application for generating videos through a Proxy API using an OpenAI-compatible client. The current scope covers homework part 1, while the internal structure is intentionally prepared for future Telegram bot and Flask web interface reuse.

## Core Features
- Start a video generation task from the command line with a custom prompt.
- Poll generation status through a separate status-check entrypoint.
- Download the resulting MP4 into the `outputs/` directory.
- Keep core logic reusable for future non-CLI interfaces.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** None (CLI application)
- **Database:** None
- **ORM:** None
- **Integrations:** OpenAI-compatible Proxy API, environment variables via `python-dotenv`

## Architecture Notes
- Entry points stay thin: `main.py` and `test.py` delegate into CLI wrappers.
- Shared business logic belongs under `src/video_app/core`.
- Configuration is isolated under `src/video_app/config`.
- Interface-specific code is separated into `src/video_app/cli` and `src/video_app/interfaces`.
- The architecture is intended to support future `bot.py` and `app.py` without changing the public core API.

## Non-Functional Requirements
- Logging: configurable through environment variables when added.
- Error handling: clear user-facing errors from core services and CLI wrappers.
- Security: secrets must stay in environment variables and never be hardcoded.
- Extensibility: core modules must remain independent from terminal rendering and future web or bot frameworks.

## Architecture
See `.ai-factory/ARCHITECTURE.md` for detailed architecture guidelines.
Pattern: Layered Architecture
