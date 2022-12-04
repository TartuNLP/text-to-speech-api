from typing import Union

import base64

import logging

from fastapi import APIRouter
from fastapi.responses import Response

from app import mq_connector, api_config
from . import Config, Speaker, Request, ErrorMessage, ResponseContent

LOGGER = logging.getLogger(__name__)

v2_router = APIRouter(tags=["v2"])


@v2_router.get('/', include_in_schema=False)
@v2_router.get('', response_model=Config, description="Get the configuration of available models and speakers.")
async def get_config():
    config = Config(speakers=[Speaker(
        name=name,
        languages=speaker.languages
    )
        for name, speaker in api_config.speakers.items()])
    return config


@v2_router.post('/', include_in_schema=False)
@v2_router.post('', response_class=Response,
                description="Submit a text-to-speech request.",
                responses={
                    422: {"model": ErrorMessage},
                    200: {"content": {"audio/wav": {}}, "description": "Returns the synthesized audio."}
                })
async def synthesis(body: Request):
    content, correlation_id = await mq_connector.publish_request(body, body.speaker)
    audio = base64.b64decode(content['audio'])
    response = Response(
        content=audio,
        media_type="audio/wav",
        headers={'Content-Disposition': f'attachment; filename="{correlation_id}.wav"'}
    )
    return response


@v2_router.post('/verbose', response_model=ResponseContent,
                description="Submit a text-to-speech request and return only some information about the output.",
                responses={422: {"model": ErrorMessage}, 200: {"model": ResponseContent}})
async def synthesis_info(body: Request):
    content, correlation_id = await mq_connector.publish_request(body, body.speaker)
    return content
