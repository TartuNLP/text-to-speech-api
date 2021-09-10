from webargs import fields
from webargs.flaskparser import FlaskParser
from nauron import Response

BODY = {
    "text": fields.Str(required=True),
    "speaker_id": fields.Int()
}

parser = FlaskParser()


@parser.error_handler
def _handle_error(error, *_, **__):
    Response(content=error.messages, http_status_code=400).flask_response()
