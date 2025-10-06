import configparser
import importlib
from urllib.parse import urlparse

_known_parsers = {
    'contest.yandex.ru': 'contestyandex'
}


def init_module(url: str, **params):
    parsed = urlparse(url)
    if parsed.hostname not in _known_parsers:
        raise NotImplementedError(f'Can\'t extract from {url}')
    module_name = _known_parsers[parsed.hostname]
    module = importlib.import_module(f'{__package__}.{module_name}')
    module.init(url, **params)
    return module


def get_module():
    cfg = configparser.ConfigParser()
    cfg.read('.cfg')
    for section in cfg.sections():
        if section in _known_parsers:
            module_name = _known_parsers[section]
            module = importlib.import_module(f'{__package__}.{module_name}')
            return module
    raise Exception('No known parser present in config file')
