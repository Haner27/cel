from contextlib import contextmanager

__author__ = 'nengfang.han'


@contextmanager
def logger_switch_context(logger, level=None, handler=None):
    old_level = logger.level
    try:
        if level:
            logger.level = level

        if handler:
            logger.addHandler(handler)

        yield logger
    finally:
        logger.level = old_level
        if handler:
            logger.removeHandler(handler)