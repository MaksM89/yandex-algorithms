import logging
import sys

from .cli import main
from .utils import init_logger


def handle_uncaught(exc_type, exc_value, exc_tb):
    logger = logging.getLogger()  # root
    # logger = logging.getLogger('yalgo')
    logger.critical('Program stopped by exception', exc_info=(exc_type, exc_value, exc_tb))
    sys.exit(1)


def run_main():
    sys.excepthook = handle_uncaught
    if sys.path[0] != '':  # запущен как скрипт
        sys.path.insert(0, '')
    listner = init_logger()
    main()
    listner.stop()


if __name__ == '__main__':
    run_main()
