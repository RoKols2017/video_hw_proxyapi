# Homework Submission Guide

## What To Submit

- GitHub repository link: `https://github.com/rokols2017/video_hw_proxyapi`
- VPS URL or IP/port where the Flask app is available.
- Telegram bot username from BotFather.
- Screenshots listed below.
- Short explanation text from this file.

## Screenshot Checklist

- Telegram bot created in BotFather.
- Telegram `/start` command response.
- Telegram `/help` command response.
- Prompt sent to the Telegram bot.
- Telegram progress message showing `queued`, `in_progress`, or `downloading`.
- Telegram completed message and sent video.
- Flask page with prompt input.
- Flask page showing status and progress bar.
- Flask download button for generated MP4.
- `docker compose ps` showing `web` and `bot` containers running.
- Flask app opened by VPS IP or domain.
- GitHub repository main page with README visible.

## Safe Verification Without Paid API Calls

- `python -m unittest discover -s tests`
- `docker compose config`
- `docker compose build`
- `docker compose ps`
- Import checks for `app.py`, `bot.py`, `main.py`, and `test.py`

Do not run real generation until `.env` contains a valid ProxyAPI key and you are ready for a paid API call.

## Ready-To-Use Submission Text

This project is a Python video-generation application built around a shared backend service layer. The CLI, Telegram bot, and Flask website all reuse the same `core.service` workflow, so ProxyAPI logic is not duplicated between interfaces. The Telegram bot accepts normal text prompts, updates one progress message, and sends the generated MP4 back to the chat. The Flask app provides a prompt form, UUID task tracking, status polling, a progress bar, and a download endpoint. Docker Compose runs the web app and bot as separate services from the same image, with generated videos stored in the mounted `outputs/` directory. The project is prepared for VPS deployment by using `.env` configuration, restart policies, and domain-aware documentation. The main challenge was keeping the original CLI homework flow working while adding bot, web, and Docker deployment layers. A future improvement would be adding Redis or SQLite for task state persistence after container restarts and automating HTTPS through a reverse proxy.

## Manual Steps Before Final Delivery

- Fill `.env` with your own `PROXYAPI_API_KEY` and `BOT_TOKEN`.
- Run one real Telegram generation and one real Flask generation.
- Save screenshots from the checklist.
- If using a domain, point DNS to the VPS IP.
- If using HTTPS, configure an external reverse proxy or provide existing certificates for the included nginx overlay.
