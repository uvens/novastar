import logging
import os
from logging.handlers import RotatingFileHandler


LOG_FTM: str = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
DATE_FTM: str = "%d/%B/%Y %H:%M:%S"

logging.basicConfig()

logger = logging.getLogger('Bill_of_loading')


def init_my_logging():
    """
    Configuring logging for a SON-like appearance when running locally
    """
    logger.setLevel(logging.DEBUG)
    log_file_name = os.path.splitext(os.path.realpath('logging'))[0] + '.log'
    handler = RotatingFileHandler(log_file_name, maxBytes=1.5 * pow(1024, 2), backupCount=3)
    log_format = "%(asctime)-15s [{}:%(name)s:%(lineno)s:%(funcName)s:%(levelname)s] %(message)s".format(os.getpid())
    handler.setLevel(logging.DEBUG)
    try:
        from colorlog import ColoredFormatter
        formatter = ColoredFormatter(log_format)
    except ImportError:
        formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

init_my_logging()


def get_file_handler(name: str) -> logging.FileHandler:
    log_dir_name: str = f"{get_my_env_var('PATH_TO_DB')}/logging"
    if not os.path.exists(log_dir_name):
        os.mkdir(log_dir_name)
    file_handler: logging.FileHandler = logging.FileHandler(f"{log_dir_name}/{name}.log")
    file_handler.setFormatter(logging.Formatter(LOG_FTM, datefmt=DATE_FTM))
    return file_handler


def get_logger(name: str) -> logging.getLogger:
    logger: logging.getLogger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(get_file_handler(name))
    logger.setLevel(logging.INFO)
    return logger
