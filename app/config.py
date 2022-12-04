from typing import List, Dict, Optional

import yaml
from yaml.loader import SafeLoader
from pydantic import BaseSettings, BaseModel


class Speaker(BaseModel):
    languages: List[str]


class APIConfig(BaseModel):
    speakers: Dict[str, Speaker]
    alt_names: Dict[str, str]


class APISettings(BaseSettings):
    max_input_length: int = 10000
    config_path = "config/config.yaml"

    class Config:
        env_file = 'config/.env'
        env_prefix = 'api_'


class MQSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5672
    username: str = 'guest'
    password: str = 'guest'
    exchange: str = 'text-to-speech'
    connection_name: str = 'Text-to-Speech API'
    timeout: int = 30

    class Config:
        env_file = 'config/.env'
        env_prefix = 'mq_'


api_settings = APISettings()
mq_settings = MQSettings()

with open(api_settings.config_path, 'r', encoding='utf-8') as f:
    api_config = APIConfig(**yaml.load(f, Loader=SafeLoader))
