# Gunicorn configuration file.
# This file can be used from the Gunicorn cli with the ``-c`` paramater.
# Eg. ``gunicorn -c <config_file>``
import os

bind = "0.0.0.0:5000"

for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split('_', 1)[1].lower()
        locals()[key] = v
