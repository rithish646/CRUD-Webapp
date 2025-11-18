# fastapi/Dockerfile
FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY fastapi/requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=build /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY fastapi/ ./

RUN chown -R appuser:appgroup /app

USER appuser
EXPOSE 8000

# Use uvicorn with Gunicorn (recommended for production)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2", "main:app"]
