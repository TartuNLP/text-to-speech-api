# Text-to-Speech API

An API based on FastAPI for using neural text-to-speech synthesis. The API is designed to be used together with our
[text-to-speech workers](https://github.com/TartuNLP/text-to-speech-worker).

The project is developed by the [NLP research group](https://tartunlp.ai) at the [Universty of Tartu](https://ut.ee).
Speech synthesis can also be tested in our [web demo](https://www.neurokone.ee/).

## API usage

The API documentation will be available at the `/docs` endpoint when deployed.

To use the API, use the following POST request format:

POST `/v2`

BODY (JSON):

```
{
    "text": "Tere.",
    "speaker": "mari",
    "speed": 1
}
```

The `speaker` parameter is required and should contain the speaker's name. The `speed` parameter is optional,
and it is a multiplier between `0.5` and `2` compared to normal speed `1`. As a result the API will return audio
in `.wav` format.

## RabbitMQ communication

The API forwards requests to various TTS engines using the RabbitMQ message broker. The communication uses a direct
exchange named `text-to-speech` and a routing key of the request parameters using the format `text-to-speech.$speaker`.
TTS workers estabilish queues within the exchange that are bound routing keys that illustrate which requests that the
particular model can handle.

## Setup

The API can be deployed using the docker image published alongside the repository. Each image version correlates to
a specific release. The API is designed to work together with our
[text-to-speech worker](https://github.com/TartuNLP/text-to-speech-worker) worker containers and RabbitMQ.

The service is available on port `8000`. By default, logging configuration is loaded from `config/logging.prod.ini` and
service configuration from `config/config.yaml` files. The default versions of these files are included. To modify any
config files, they should be mounted at /app/config (the absolute path in the container).

The following environment variables should be specified when running the container:

- `MQ_USERNAME` - RabbitMQ username
- `MQ_PASSWORD` - RabbitMQ user password
- `MQ_HOST` - RabbitMQ host
- `MQ_PORT` (optional) - RabbitMQ port (`5672` by default)
- `MQ_TIMEOUT` (optional) - Message timeout in seconds (`30` by default)
- `MQ_EXCHANGE` (optional) - RabbitMQ exchange name (`text-to-speech` by default)
- `MQ_CONNECTION_NAME` (optional) - friendly connection name (`Text-to-Speech API` by default)
- `API_MAX_INPUT_LENGTH` (optional) - maximum input text length in characters (`10000` by default)
- `API_CONFIG_PATH` (optional) - path of the config file used (`config/config.yaml`)

The entrypoint of the container
is `["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers", "--log-config", "config/logging.ini"]`.

The `CMD` option can be used to override flags in the entrypoint or to overridde
different [Uvicorn parameters](https://www.uvicorn.org/deployment/). For example,
`["--log-config", "config/logging.debug.ini", "--root-path", "/text-to-speech"]` enables debug logging and allows the API
to be mounted under to the non-root path `/text-to-speech` when using a proxy server such as Nginx.

The setup can be tested with the following sample `docker-compose.yml` configuration:

```yaml
version: '3'
services:
  rabbitmq:
    image: 'rabbitmq'
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
    ports:
      - '8000:8000'
    depends_on:
      - rabbitmq
  tts_worker:
    image: ghcr.io/tartunlp/text-to-speech-worker:latest
    environment:
      - MQ_HOST=rabbitmq
      - MQ_PORT=5672
      - MQ_USERNAME=${RABBITMQ_USER}
      - MQ_PASSWORD=${RABBITMQ_PASS}
    command: [ "--model-name", "multispeaker" ]
    volumes:
      - ./models:/app/models
    depends_on:
      - rabbitmq
```