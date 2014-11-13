import logging
import os
import sys

from rainbow_logging_handler import RainbowLoggingHandler

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'celos')

DEBUG = True
PORT = 8000

MONGO = {
    'USERNAME': None,
    'PASSWORD': None,
    'HOST': 'localhost',
    'PORT': 27017,
    'NAME': 'celos',
}

SECRET_KEY = 'secret'

LOGIN_URL = '/login'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')

# logging
_log_lvl = logging.DEBUG if DEBUG else logging.WARNING
_format = '%(asctime)s %(levelname)s [%(module)s %(funcName)s @ %(lineno)d] %(message)s'

LOG = logging.getLogger('')

_formatter = logging.Formatter(_format)
_handler = RainbowLoggingHandler(sys.stderr)
_handler.setFormatter(_formatter)
LOG.addHandler(_handler)
LOG.setLevel(_log_lvl)
