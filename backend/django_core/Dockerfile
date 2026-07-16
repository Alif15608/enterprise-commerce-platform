# ---------- Builder stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# System deps needed only to build Python packages (e.g. psycopg2 needs libpq headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Only the runtime lib for Postgres client, not the full -dev headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder (not the build toolchain)
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Run as non-root user — security best practice
RUN addgroup --system django && adduser --system --ingroup django django
COPY --chown=django:django . .
USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]