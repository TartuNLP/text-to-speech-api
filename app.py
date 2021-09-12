import logging
from flask_cors import CORS
from nauron import Nauron

import settings
from utils import parser, BODY_V2

logger = logging.getLogger("gunicorn.error")

app = Nauron(__name__, timeout=settings.MESSAGE_TIMEOUT, mq_parameters=settings.MQ_PARAMETERS)
CORS(app)

app.add_service(name=settings.SERVICE_NAME, remote=True)


@app.post('/text-to-speech/v2')
@parser.use_args(BODY_V2, location="json")
def synthesize_v2(body):
    response = app.process_request(service_name=settings.SERVICE_NAME,
                                   content=body,
                                   routing_key=body["speaker"].lower())
    return response


if __name__ == '__main__':
    app.run()
