#FROM python:3.12-slim AS builder
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FROM python:3.12-slim AS runtime

# WORKDIR /app
# COPY --from=builder /root/.local /root/.local
# ENV PATH=/root/.local/bin:$PATH

RUN addgroup --system fastapi && adduser --system --ingroup fastapi fastapi && chown -R fastapi:fastapi /app
#COPY --chown=fastapi:fastapi . .
USER fastapi

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]