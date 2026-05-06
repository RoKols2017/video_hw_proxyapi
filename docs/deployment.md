[← Interfaces](interfaces.md) · [Back to README](../README.md)

# Deployment

## Local Docker Run

```bash
cp .env.example .env
mkdir -p outputs
docker compose build
docker compose up -d web bot
docker compose logs -f
docker compose ps
```

The Flask app is available at `http://localhost:5000`.

## VPS Run

Install Docker Engine with the Compose plugin on the VPS, then run:

```bash
git clone https://github.com/rokols2017/video_hw_proxyapi.git
cd video_hw_proxyapi
cp .env.example .env
mkdir -p outputs
docker compose up -d --build web bot
docker compose logs -f
docker compose ps
```

Fill `.env` before starting real generation:

- `PROXYAPI_API_KEY`
- `BOT_TOKEN`
- `VIDEO_MODEL=veo-3-fast`
- `VIDEO_SECONDS=4`
- `VIDEO_OUTPUT_DIR=outputs`

If the production image runs as a non-root user and the host directory is not writable, adjust ownership of `outputs/` for UID `1000` before using `compose.production.yml`.

## Domain

Point the domain DNS A record to the VPS IP.

If no reverse proxy is configured, the Flask app is available through the exposed port:

```text
http://<domain>:5000
http://<server-ip>:5000
```

This is enough for a basic homework demonstration if the VPS firewall allows port `5000`.

## Optional nginx Overlay

The repository includes `compose.production.yml` and `docker/nginx/default.conf.template` for an nginx reverse proxy, but certificate issuance is not automated.

Use this only if the VPS already has TLS certificates:

```bash
NGINX_DOMAIN=example.com SSL_CERTS_DIR=/root/cert/example.com docker compose -f docker-compose.yml -f compose.production.yml up -d --build web bot nginx
```

`SSL_CERTS_DIR` must contain:

- `fullchain.pem`
- `privkey.pem`

After that, nginx proxies `https://<domain>` to `web:5000` inside Docker.

## Service Strategy

- `web` runs Flask through `python app.py`.
- `bot` runs Telegram polling through `python bot.py`.
- Both services use the same Docker image and `.env` file.
- Both services mount `./outputs:/app/outputs`.
- Long-running VPS services use `restart: unless-stopped`.

## Common Commands

```bash
docker compose build
docker compose up -d web bot
docker compose logs -f
docker compose ps
docker compose restart web bot
docker compose down
```

CLI profile checks:

```bash
docker compose --profile cli run --rm app
docker compose --profile status run --rm status
```

## What To Check After Deploy

- `docker compose ps` shows `web` and `bot` as running.
- `docker compose logs -f web` has no startup errors.
- `docker compose logs -f bot` shows Telegram polling started.
- Flask opens by IP/port or domain.
- Telegram bot responds to `/start` and `/help`.
- Generated MP4 files appear in `outputs/`.

## Future Improvements

- Add automated HTTPS with Caddy, Traefik, nginx + Certbot, or a VPS panel.
- Add persistent task storage such as Redis or SQLite.
- Add CI checks for tests and Docker build.

## See Also

- [Interfaces](interfaces.md)
- [Configuration](configuration.md)
- [Getting Started](getting-started.md)
