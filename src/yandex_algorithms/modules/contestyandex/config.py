import configparser
from pathlib import Path
from typing import TypedDict, Union

from .contest_api import ProblemInfo

_CONFIG_FILE = Path('.cfg')
_SECTION_NAME = 'contest.yandex.ru'
_PROBLEM_PREFIX = 'problem.'


class Config(TypedDict):
    token: str
    contest_id: int
    problems: dict[str, ProblemInfo]


def load_config(
        file: Path = _CONFIG_FILE
) -> Config:
    cfg = configparser.ConfigParser()
    if len(cfg.read(file)) == 0:
        return Config(token='', contest_id=-1, problems={})
    if _SECTION_NAME in cfg.sections():
        raw_conf: dict[str, Union[str, int]] = dict(cfg[_SECTION_NAME])
    else:
        raise NotImplementedError(f'No section {_SECTION_NAME} in config file')
    assert len(raw_conf.keys() - Config.__annotations__.keys()) == 0, \
        f'Need [{_SECTION_NAME}] section with params "{"".join(Config.__annotations__.keys() - "problems")}"'
    try:
        raw_conf['contest_id'] = int(raw_conf['contest_id'])
    except ValueError:
        raise ValueError('Invalid contest_id value in config file')
    conf = Config(problems={}, **raw_conf)  # type: ignore # есть проверки
    for name in cfg.sections():
        if name.startswith(_PROBLEM_PREFIX):
            info = dict(cfg[name])
            assert len(info.keys() - ProblemInfo.__annotations__.keys()) == 0, \
                f'Need [{name}] section with params "{"".join(ProblemInfo.__annotations__.keys() - "problems")}"'
            conf['problems'][name.split('.', 1)[1]] = ProblemInfo(
                **info)  # type: ignore[typeddict-item] # есть все проверки
    return conf  # type: ignore # есть все проверки


def store_config(
    token: Union[str, None],
    contest_id: Union[int, None],
    problems_info: list[dict[str, ProblemInfo]],
    file: Path = _CONFIG_FILE,
):
    prev = load_config(file)
    cfg = configparser.ConfigParser()
    cfg[_SECTION_NAME] = {
        'token': token or prev['token'],
        'contest_id': str(contest_id) or str(prev['contest_id'])
    }
    prev['problems'].update({p: v for d in problems_info for p, v in d.items()})
    for problem, info in prev['problems'].items():
        cfg[_PROBLEM_PREFIX + problem] = info  # type: ignore[assignment] # конвертируется
    with open(file, 'w') as f:
        cfg.write(f)

# def merge_config(
#         token: Union[str, None] = None,
#         contest_id: Union[int, None] = None,
#         file: Path = _CONFIG_FILE
# ) -> dict:
#     cfg = configparser.ConfigParser()
#     cfg.read(file)
#     if _SECTION_NAME in cfg.sections():
#         prev = dict(cfg[_SECTION_NAME])
#     else:
#         # raise NotImplementedError(f'No section {_SECTION_NAME} in config file')
#         prev = {}
#     conf = {
#             'token' : token or prev.get('token', ''),
#             'contest_id' : contest_id or prev.get('contest_id'),
#         }
#     return conf

# def store_config(
#     token: Union[str, None],
#     contest_id: Union[int, None],
#     # problems: Union[List[Dict[str, ProblemInfo]], None],
#     file: Path = _CONFIG_FILE,
# ):
#     conf = merge_config(token, contest_id, file)
#     cfg = configparser.ConfigParser()
#     with open(file, 'w') as f:
#         cfg.write(f)
