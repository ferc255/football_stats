"""
The tools that allow to communicate with google sheets through API.
"""
import logging


def get_logger(name):
    formatter = logging.Formatter(
        '%(asctime)s %(process)d:%(levelname)s:%(name)s:%(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
