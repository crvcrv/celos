import logging
FORMAT = '%(asctime)s %(levelname)s [%(module)s %(funcName)s @ %(lineno)d] %(message)s'

logging.basicConfig(
    format = FORMAT,
    level = logging.DEBUG,
)
log = logging.getLogger('')