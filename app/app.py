import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import api_settings, mq_connector
from .tts import v2_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await mq_connector.connect()
    yield
    await mq_connector.disconnect()

app = FastAPI(title="Text-to-Speech API",
              version=api_settings.version if api_settings.version else "dev",
              description=
                "An API that provides text-to-speech using neural models. "
                "Developed by TartuNLP - the NLP research group of the University of Tartu.\n\n"
                "**Terms of use:**\n\n" 
                "Use of this API is prohibited for the following purposes:\n"
                "- commercial purposes, including but not limited to the following activities when carried out for commercial gain: advertising, voicing audiobooks and e-books; films, videos and multimedia; creating and producing audio content, including marketing and training materials; podcasts. Commercial use is permitted only with prior written consent.\n"
                "- immoral or unethical purposes;\n"
                "- political purposes, including military use.\n\n"
                "Data collection:\n\n" \
                "- The API will store user input to improve our services. This data may be used for research and development purposes, however, it will not be published or shared with third parties.",
              license_info={
                  "name": "MIT license",
                  "url": "https://github.com/TartuNLP/text-to-speech-api/blob/main/LICENSE"
              },
              contact={
                  "name": "TartuNLP",
                  "url": "https://tartunlp.ai",
                  "email": "ping@tartunlp.ai",
              },
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logger.debug(f"{request}: {exc_str}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc_str}
    )


app.include_router(v2_router, prefix="/v2")
