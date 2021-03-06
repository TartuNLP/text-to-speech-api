from os import environ
import yaml
from yaml.loader import SafeLoader
from pika import ConnectionParameters, credentials
from dotenv import load_dotenv

load_dotenv("config/.env")
load_dotenv("config/sample.env")

SECRET_KEY = environ.get("FLASK_SECRET_KEY", None)

CONFIG_FILE = 'config/config.yaml'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    _config = yaml.load(f, Loader=SafeLoader)

SERVICE_NAME = _config['service']

MQ_PARAMETERS = ConnectionParameters(
    host=environ.get('MQ_HOST', 'localhost'),
    port=int(environ.get('MQ_PORT', '5672')),
    credentials=credentials.PlainCredentials(
        username=environ.get('MQ_USERNAME', 'guest'),
        password=environ.get('MQ_PASSWORD', 'guest')
    )
)

MESSAGE_TIMEOUT = int(environ.get('GUNICORN_TIMEOUT', '30')) * 1000
