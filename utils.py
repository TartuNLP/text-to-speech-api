from webargs import fields
from webargs.flaskparser import FlaskParser
from nauron import Response

BODY_V2 = {
    "text": fields.Str(required=True),
    "speaker": fields.Str(required=True),
    "speed": fields.Float(missing=1, validate=lambda x: 0.5 <= x <= 2)
}

parser = FlaskParser()


@parser.error_handler
def _handle_error(error, *_, **__):
    Response(content=error.messages, http_status_code=400).flask_response()
