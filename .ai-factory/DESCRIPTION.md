# Project: AI Video Generator Platform

## Overview
Production-oriented AI video generation project built for homework parts 1 and 2.  
The project uses a shared Python backend for video generation through a Proxy API with an OpenAI-compatible client, and exposes this functionality through three interfaces:

- CLI interface for homework part 1 validation
- Telegram bot for user-facing chat-based generation
- Flask web application for browser-based generation and download

The project is designed to be generated and iterated through **OpenCode** and **ai-factory**, then packaged and deployed in **Docker** on a **VPS**.

## Goal
Turn the existing console video-generation script into a reusable backend service and a user-facing product that can be:
- demonstrated locally,
- submitted as homework,
- continued as a portfolio project,
- deployed on a VPS with Docker.

## Core Features
- Generate videos from a custom text prompt through Proxy API.
- Support configurable video model selection through environment variables.
- Track generation lifecycle with statuses such as:
  - `queued`
  - `in_progress`
  - `downloading`
  - `completed`
  - `failed`
- Save generated MP4 files to persistent storage.
- Check task status from a dedicated status entrypoint.
- Reuse one backend service layer across CLI, Telegram bot, and Flask site.

## Interfaces
### 1. CLI
Used for homework part 1 and backend debugging:
- start generation with a custom prompt;
- poll status from terminal;
- save the resulting MP4;
- verify task status separately.

### 2. Telegram Bot
Used for homework part 2:
- accepts user text prompts;
- launches video generation through the shared backend;
- updates one progress message instead of sending many messages;
- sends the generated video back to the user;
- handles generation and API errors gracefully.

### 3. Flask Web App
Used for homework part 2:
- provides a prompt input form;
- starts generation tasks;
- shows task progress through polling;
- allows downloading the generated video after completion;
- keeps generated files available after page refresh.

## Supported Models
Video model is configured through environment variables.

Allowed values:
- `veo-3-fast`
- `sora-2`

Preferred default:
- `veo-3-fast`

## Tech Stack
- **Language:** Python 3.11+
- **Backend:** Python service layer
- **Bot:** pyTelegramBotAPI
- **Web:** Flask
- **Containerization:** Docker, Docker Compose
- **Deployment target:** VPS
- **Database:** None for homework scope (in-memory task storage is acceptable)
- **Integrations:** Proxy API via OpenAI-compatible client, Telegram Bot API, environment variables via `python-dotenv`

## Architecture Notes
- The project must keep a **shared backend/service layer** that contains all video-generation business logic.
- CLI, Telegram bot, and Flask must call the same backend functions instead of duplicating API calls.
- Entry points should stay thin.
- Configuration must stay isolated and environment-driven.
- Interface-specific code must remain separated from core logic.
- The architecture should allow future replacement of in-memory task storage with Redis or a database without rewriting the generation service.

## Suggested Structure
- `main.py` — CLI entrypoint
- `test.py` — standalone task status check
- `bot.py` — Telegram bot entrypoint
- `app.py` — Flask application entrypoint
- `src/video_app/core/` — shared backend logic
- `src/video_app/config/` — settings and env loading
- `templates/` — Flask HTML templates
- `static/` — Flask CSS/JS assets
- `outputs/` — generated files
- `Dockerfile` — image build
- `docker-compose.yml` — local/VPS orchestration
- `.env.example` — required environment variables

## Deployment Requirements
The project must be runnable on a VPS through Docker.

Required deployment characteristics:
- containerized application build;
- environment-based configuration;
- no hardcoded secrets;
- persistent storage for generated MP4 files;
- separate process strategy for web app and Telegram bot, or equivalent container split;
- restart-safe startup on VPS;
- easy rebuild and relaunch with Docker Compose.

## Non-Functional Requirements
- **Security:** API keys and bot tokens must be stored only in environment variables.
- **Maintainability:** backend logic must remain independent from CLI/Telegram/Flask rendering details.
- **Extensibility:** the current project should remain easy to evolve after homework submission.
- **Observability:** logs should be readable in Docker and useful for debugging on VPS.
- **Reliability:** failures from Proxy API and invalid configuration should produce explicit, user-friendly errors.

## Homework Scope
### Part 1
- CLI generation
- status polling
- MP4 download
- separate status checker

### Part 2
- Telegram bot
- Flask site
- UUID-based task tracking for web tasks
- in-memory task state for homework scope
- Dockerized VPS deployment

## Development Workflow
The project is intended to be developed iteratively with:
- **OpenCode** for code generation and refactoring
- **ai-factory** for project specification, architecture guidance, and structured implementation workflow

## Architecture
See `.ai-factory/ARCHITECTURE.md` for detailed architecture guidelines.  
Pattern: Layered Architecture with shared service layer and interface adapters.
