import configparser
from pathlib import Path
from typing import TypedDict, Union

# _PROMPT_IN = '-->'
# _PROMPT_OUT = '<--'

_CONFIG_FILE = Path('.cfg')
_SECTION_NAME = 'default'


class Config(TypedDict):
    prompt_in: str
    prompt_out: str
    infilevar: str
    outfilevar: str


def store_config(
    prompt_in: Union[str, None],
    prompt_out: Union[str, None],
    infilevar: Union[str, None],
    outfilevar: Union[str, None],
    file: Path = _CONFIG_FILE,
):
    cfg = configparser.ConfigParser()
    cfg.read(file)
    if _SECTION_NAME in cfg.sections():
        default = dict(cfg[_SECTION_NAME])
    else:
        default = {}
    default = {
        'prompt_in': prompt_in or default.get('prompt_in', '-->'),
        'prompt_out': prompt_out or default.get('prompt_out', '<--'),
        'infilevar': infilevar or default.get('infilevar', ''),
        'outfilevar': outfilevar or default.get('outfilevar', '')
    }
    cfg[_SECTION_NAME] = default
    with open(file, 'w') as f:
        cfg.write(f)


def load_config(file: Path = _CONFIG_FILE) -> Config:
    cfg = configparser.ConfigParser()
    cfg.read(file)
    if _SECTION_NAME in cfg.sections():
        default = dict(cfg[_SECTION_NAME])
    else:
        default = {}
    assert default.keys() == Config.__annotations__.keys(), \
        f'Need [{_SECTION_NAME}] section with params "{"".join(list(Config.__annotations__.keys()))}"'
    return Config(**default)  # type: ignore[typeddict-item]  # есть проверка на ключи
