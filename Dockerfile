FROM python:3.8-alpine

# Install needed dependencies
RUN apk update \
  && apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    git

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "config/gunicorn.ini.py", "--log-config", "config/logging.ini", "app:app"]
