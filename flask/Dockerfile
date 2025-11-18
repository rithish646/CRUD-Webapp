# flask/Dockerfile
FROM python:3.11-slim AS build

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY flask/requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# system user (non-root)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# copy wheels and install
COPY --from=build /wheels /wheels
RUN pip install --no-cache /wheels/*

# copy app
COPY flask/ ./

# create runtime files
RUN mkdir -p /var/log/flask
RUN chown -R appuser:appgroup /app /var/log/flask

USER appuser
EXPOSE 5000

# Use Gunicorn to run flask app in production.
# Assumes your flask entrypoint is app.py and exposes `app` variable: app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app", "--worker-class", "gthread", "--threads", "2", "--timeout", "120"]
