FROM python:3.8-alpine

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
        gcc \
        libffi-dev \
        musl-dev \
        git

ENV PYTHONIOENCODING=utf-8
WORKDIR /app

RUN adduser -D app && \
    chown -R app:app /app
USER app
ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app requirements/requirements.txt .
RUN pip install --user -r requirements.txt && \
    rm requirements.txt

COPY --chown=app:app . .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "config/gunicorn.ini.py", "--log-config", "config/logging.ini", "app:app"]
