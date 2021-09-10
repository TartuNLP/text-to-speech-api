# Text-to-Speech API

A simple Flask API for multi-speaker neural text-to-speech synthesis to be used together with
[text-to-speech workers](https://github.com/TartuNLP/text-to-speech).

The project is developed by the [NLP research group](https://tartunlp.ai) at the [Universty of Tartu](https://ut.ee).
Speech synthesis can also be tested in our [web demo](https://www.neurokone.ee/).

## API usage

To use the API, use the following POST request format:

POST `/text-to-speech/v2`

BODY (JSON):

```
{
    "text": "Tere.",
    "speaker": mari,
    "speed": 1
}
```

The `speaker` parameter is required and should contain the speaker's name. The `speed` parameter is optional, 
and it is a multiplier between `0.5` and `2` compared to normal speed `1`.

## Setup

The API can be deployed using the docker image published alongside the repository. Each image version correlates to 
a specific release. The API is designed to work together with our 
[text-to-speech worker](https://github.com/TartuNLP/text-to-speech) worker containers and RabbitMQ.

The service is available on port `5000`. Logs are stored in `/app/logs/`. Logging configuration is loaded from 
`/app/config/logging.ini` and service configuration from `/app/config/config.yaml` files.

The container uses Gunicorn to run the API. Gunicorn parameters can be modified with environment variables where
the variable name is capitalized and the prefix `GUNICORN_` is added. For example, the number of workers can be modified
as follows:

The RabbitMQ connection parameters are set with environment variables, exchange and queue names are dependent on the 
`service` value in `config.yaml` and the speaker name. The setup can be tested with the following sample
`docker-compose.yml` configuration:

```
version: '3'
services:
  rabbitmq:
    image: 'rabbitmq:3.6-alpine'
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASS}
  tts_api:
    image: ghcr.io/tartunlp/text-to-speech-api:latest
    environment:
      - MQ_HOST=rabbitmq
      - MQ_PORT=5672
      - MQ_USERNAME=${RABBITMQ_USER}
      - MQ_PASSWORD=${RABBITMQ_PASS}
      - GUNICORN_WORKERS=8
    ports:
      - '5000:5000'
    depends_on:
      - rabbitmq
  tts_worker_mari:
    image: ghcr.io/tartunlp/text-to-speech-worker:latest
      - MODEL_NAME=mari
      - MQ_HOST=rabbitmq
      - MQ_PORT=5672
      - MQ_USERNAME=${RABBITMQ_USER}
      - MQ_PASSWORD=${RABBITMQ_PASS}
    volumes:
      - ./models:/app/models
    depends_on:
      - rabbitmq
```