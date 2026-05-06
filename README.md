# Video HW Proxy API

> Portfolio-ready homework project: AI video generation through ProxyAPI with one shared Python backend, CLI, Telegram bot, Flask UI, and Docker/VPS deployment path.

This repository is built for Prompt Engineering 2.0 homework part 2 and for publication on the GitHub profile `github.com/rokols2017`. It demonstrates AI automation, LLM/API integration, prompt-driven product thinking, Telegram bot development, Flask development, Docker packaging, and VPS deployment practice.

## Demo Description

The user submits a text prompt through CLI, Telegram, or the web page. The shared backend creates a video-generation task in ProxyAPI, polls status updates, downloads the generated MP4 into `outputs/`, and returns the result through the selected interface.

## Problem

Video-generation prototypes often start as one CLI script. When a bot and a web UI are added later, API calls, status handling, downloads, and error handling are easy to duplicate across interfaces.

## Solution

The project keeps ProxyAPI logic in `src/video_app/core/` and exposes it through thin adapters:

- `main.py` and `test.py` for the original CLI homework flow.
- `bot.py` for Telegram polling.
- `app.py` for the Flask website.
- Docker Compose services for local checks and VPS runtime.

## Features

- Shared backend service layer for CLI, Telegram, and Flask.
- Supported statuses: `queued`, `in_progress`, `downloading`, `completed`, `failed`, `error`.
- Telegram commands `/start` and `/help`.
- Telegram prompt handling from normal text messages.
- Telegram progress updates by editing one message instead of spamming the chat.
- Flask routes: `GET /`, `POST /generate`, `GET /status/<task_id>`, `GET /download/<task_id>`.
- Flask background generation with `threading.Thread` and UUID task IDs.
- MP4 persistence in `outputs/` through Docker bind mounts.
- Docker services for `web`, `bot`, CLI generation, and status checks.
- Optional production overlay with nginx when a domain and existing TLS certificates are available.

## Tech Stack

- Python 3.11+
- Flask
- pyTelegramBotAPI
- ProxyAPI video models: `veo-3-fast`, `sora-2`
- python-dotenv
- Docker and Docker Compose
- OpenCode, GPT-5.5, ai-factory workflow

## Architecture

```text
main.py / test.py          -> src/video_app/cli/
bot.py                     -> src/video_app/interfaces/telegram_bot.py
app.py                     -> src/video_app/interfaces/flask_app.py
CLI / Telegram / Flask     -> src/video_app/core/service.py
core.service               -> ProxyAPI + local outputs/
config.settings            -> validated environment variables
```

The important boundary is that `bot.py` and `app.py` do not implement ProxyAPI workflow themselves. They call `generate_video()` from the shared service layer and receive progress through callbacks.

See also: [`docs/architecture.md`](docs/architecture.md).

## How It Works

```text
prompt
  -> interface adapter
  -> shared core.service
  -> ProxyAPI task creation
  -> polling: queued -> in_progress -> downloading -> completed
  -> MP4 saved in outputs/
  -> CLI output, Telegram video, or Flask download link
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` with your own `PROXYAPI_API_KEY` and, for Telegram, `BOT_TOKEN`.

Run the original CLI flow:

```bash
python main.py
python test.py
```

Run Telegram bot:

```bash
python bot.py
```

Run Flask web UI:

```bash
python app.py
```

Local Flask URL: `http://localhost:5000`.

## Docker Setup

```bash
cp .env.example .env
mkdir -p outputs
docker compose build
docker compose up -d web bot
docker compose logs -f
docker compose ps
docker compose restart web bot
docker compose down
```

CLI checks are available through profiles:

```bash
docker compose --profile cli run --rm app
docker compose --profile status run --rm status
```

The default compose file runs Flask on `0.0.0.0:5000` inside the container and publishes it as `localhost:5000` on the host. Generated files are stored through `./outputs:/app/outputs`.

## VPS Deployment

Basic VPS flow without adding a reverse proxy to this repository:

```bash
git clone https://github.com/rokols2017/video_hw_proxyapi.git
cd video_hw_proxyapi
cp .env.example .env
mkdir -p outputs
docker compose up -d --build web bot
docker compose logs -f
docker compose ps
```

Point the domain DNS A record to the VPS IP. If no reverse proxy is configured on the VPS, Flask is available through the exposed port: `http://<domain>:5000` or `http://<server-ip>:5000`.

Optional production overlay if you already have a domain and TLS certificates on the VPS:

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f docker-compose.yml -f compose.production.yml up -d --build web bot nginx
```

This repository includes an nginx overlay, but it does not issue certificates. HTTPS requires existing `fullchain.pem` and `privkey.pem` in `SSL_CERTS_DIR` or an external reverse proxy such as Caddy, Traefik, nginx, or a hosting panel.

## Environment Variables

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `PROXYAPI_API_KEY` | yes | empty in example | ProxyAPI key |
| `VIDEO_MODEL` | yes | `veo-3-fast` | Allowed: `veo-3-fast`, `sora-2` |
| `VIDEO_SECONDS` | yes | `4` | Homework-safe default duration |
| `VIDEO_OUTPUT_DIR` | yes | `outputs` | MP4 output directory |
| `POLL_INTERVAL_SECONDS` | no | `5` | Status polling interval |
| `LOG_LEVEL` | no | `DEBUG` | Docker/local logging level |
| `BOT_TOKEN` | for bot | empty in example | Telegram bot token |
| `FLASK_HOST` | for web | `0.0.0.0` | Flask bind host |
| `FLASK_PORT` | for web | `5000` | Flask port |
| `NGINX_DOMAIN` | optional | deploy-time only | Domain for nginx overlay |
| `SSL_CERTS_DIR` | optional | deploy-time only | Existing TLS certificate directory |

No real secrets, IP addresses, domains, or tokens are committed.

## Project Structure

```text
.
|-- main.py                         # CLI generation entrypoint
|-- test.py                         # CLI status-check entrypoint
|-- bot.py                          # Telegram bot entrypoint
|-- app.py                          # Flask app entrypoint
|-- src/video_app/config/           # env loading and validation
|-- src/video_app/core/             # shared ProxyAPI workflow and storage
|-- src/video_app/cli/              # CLI adapters
|-- src/video_app/interfaces/       # Telegram and Flask adapters
|-- templates/                      # Flask HTML
|-- static/                         # Flask CSS/JS
|-- outputs/                        # generated runtime files, ignored by Git
|-- docs/                           # detailed documentation
|-- Dockerfile
|-- docker-compose.yml
|-- compose.production.yml
|-- .env.example
`-- REVIEW_REPORT.md
```

## Screenshots

Recommended screenshots for homework and portfolio publication:

- Telegram bot created in BotFather.
- `/start` and `/help` conversation.
- Telegram prompt message and edited progress message.
- Telegram completed video delivery.
- Flask page with prompt input.
- Flask progress bar during generation.
- Flask download button for MP4.
- `docker compose ps` on local machine or VPS.
- Website opened by VPS IP or domain.
- GitHub repository main page.

See [`docs/SUBMISSION.md`](docs/SUBMISSION.md) for the full submission checklist and a ready-to-use homework text.

## Homework Submission Checklist

- CLI part remains available through `main.py` and `test.py`.
- Telegram bot uses `BOT_TOKEN` from `.env`.
- Telegram bot supports `/start`, `/help`, text prompts, progress updates, and video sending.
- Flask app supports prompt input, status polling, progress bar, and download endpoint.
- Backend service layer is shared across CLI, Telegram, and Flask.
- Docker Compose can run `web` and `bot` as separate services.
- `outputs/` is mounted for generated MP4 persistence.
- `.env.example`, `.gitignore`, `.dockerignore`, and Docker files are present.
- No real secrets are committed.

## Limitations

- Web task state is in memory. Page refresh works while the same Flask process is running, but process restart clears task metadata.
- No Redis, database, Celery, or job queue is included because the homework scope does not require it.
- The nginx overlay expects existing TLS certificates and does not automate certificate issuance.
- Real generation requires a valid ProxyAPI key and may incur API cost.

## Future Improvements

- Add Redis or SQLite for restart-safe task state.
- Add a queue worker for long-running jobs.
- Add automated HTTPS setup with Caddy, Traefik, nginx + Certbot, or VPS panel integration.
- Add CI checks for tests, Docker build, and linting.
- Add screenshots or a short demo video after deployment.

## Skills Demonstrated

- AI automation workflow design.
- LLM and ProxyAPI integration.
- Prompt engineering product flow from text prompt to generated video.
- Python backend/service-layer design.
- Telegram bot development.
- Flask web interface development.
- Docker image and Compose orchestration.
- VPS deployment readiness and domain-aware documentation.
- Security hygiene with env-based secrets and ignored runtime artifacts.

## License

MIT. See [`LICENSE`](LICENSE).
