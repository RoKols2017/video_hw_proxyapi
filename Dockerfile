FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS deps

COPY pyproject.toml README.md ./
COPY src ./src
COPY main.py test.py ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir .

FROM base AS development

COPY --from=deps /usr/local /usr/local
COPY . .

CMD ["python", "main.py"]

FROM base AS production

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY --from=deps /usr/local /usr/local
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "main.py"]
