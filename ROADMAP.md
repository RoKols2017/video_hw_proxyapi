# Roadmap

## Done

- Shared backend service layer for ProxyAPI video generation.
- CLI entrypoints for homework part 1: `main.py` and `test.py`.
- Telegram bot entrypoint with `/start`, `/help`, prompt handling, progress updates, and MP4 delivery.
- Flask UI with prompt form, UUID task IDs, status polling, progress bar, and MP4 download.
- Dockerfile and Docker Compose services for local and VPS-oriented runtime.
- Environment-based configuration with `.env.example` and no committed secrets.
- Portfolio packaging through README, docs, submission guide, and review report.

## Homework Part 2 Focus

- Keep CLI part working while presenting Telegram and Flask as the main user-facing interfaces.
- Run `web` and `bot` as separate Docker Compose services from one image.
- Persist generated MP4 files through `./outputs:/app/outputs`.
- Document local, Docker, and VPS launch flows.
- Prepare screenshots and final submission text.

## Next Improvements

- Add Redis or SQLite for task state persistence across Flask container restarts.
- Add CI for tests and Docker build checks.
- Add automated reverse proxy and HTTPS flow after VPS/domain requirements are final.
- Add real screenshots and optional demo video after deployment.
- Add stricter linting and formatting once homework scope is accepted.
