import logging
import sys


__all__ = [
    'get_sprintapi_logger',
    'set_global_level_to_debug',
    'set_global_level_to_info'
]


_log_formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


_stdout_handler = logging.StreamHandler(sys.stdout)
_stdout_handler.setFormatter(_log_formatter)
_stdout_handler.setLevel(logging.DEBUG)
_stdout_filter = logging.Filter()
_stdout_filter.filter = lambda record: record.levelno <= logging.INFO
_stdout_handler.addFilter(_stdout_filter)

_stderr_handler = logging.StreamHandler(sys.stderr)
_stderr_handler.setFormatter(_log_formatter)
_stderr_handler.setLevel(logging.WARNING)
_stderr_filter = logging.Filter()
_stderr_filter.filter = lambda record: record.levelno > logging.INFO


_managed_loggers: dict[str, logging.Logger] = {}
_current_level = logging.INFO


def get_sprintapi_logger(name: str):
    logger = _managed_loggers.get(name, None)
    if logger is not None:
        return logger

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(_current_level)
    logger.addHandler(_stdout_handler)
    logger.addHandler(_stderr_handler)
    _managed_loggers[name] = logger

    return logger


_logger = get_sprintapi_logger('LogCtrl')


def _set_global_level(level: int):
    global _current_level
    _current_level = level

    for logger in _managed_loggers.values():
        _logger.info(f'Logger "{logger.name} set to level: {level}."')
        logger.setLevel(_current_level)


def set_global_level_to_debug():
    _set_global_level(logging.DEBUG)


def set_global_level_to_info():
    _set_global_level(logging.INFO)
