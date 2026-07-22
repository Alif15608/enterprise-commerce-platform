# ---------- Builder stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# System deps needed only to build Python packages (e.g. psycopg2 needs libpq headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Only the runtime lib for Postgres client, not the full -dev headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create the non-root user BEFORE copying anything, so ownership can be
# assigned correctly in one pass.
RUN addgroup --system django && adduser --system --ingroup django django

# --chown here ensures the django user actually owns (and can execute)
# everything pip installed — this is the fix for the Daphne/Gunicorn
# permission error: previously these files were copied while still
# root-owned, before USER django ever took effect.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=django:django . .
USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]