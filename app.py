import logging
from flask_cors import CORS
from nauron import Nauron

import settings
from utils import parser, BODY

logger = logging.getLogger("gunicorn.error")

app = Nauron(__name__, timeout=settings.MESSAGE_TIMEOUT, mq_parameters=settings.MQ_PARAMETERS)
CORS(app)

app.add_service(name=settings.SERVICE_NAME, remote=True)


@app.post('/text-to-speech/v1')
@parser.use_args(BODY, location="json")
def synthesize(body):
    response = app.process_request(service_name=settings.SERVICE_NAME,
                                   content=body,
                                   routing_key=settings.ROUTE)
    return response


if __name__ == '__main__':
    app.run()
