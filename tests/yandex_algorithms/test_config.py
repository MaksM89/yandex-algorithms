import configparser
from pathlib import Path

import pytest

from yandex_algorithms.config import load_config, store_config

_filename = '.pwd'
_section_name = 'section'
_exp = {
    'prompt_in': '<<<',
    'prompt_out': '>>>',
    'infilevar': 'input_file',
    'outfilevar': 'output_file'
}


@pytest.fixture
def cfg_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    file = tmp_path / _filename
    monkeypatch.setattr('yandex_algorithms.config._SECTION_NAME', _section_name)
    monkeypatch.setattr('yandex_algorithms.config._CONFIG_FILE', file)
    return file


@pytest.fixture
def non_empty_file(cfg_file: Path):
    parser = configparser.ConfigParser()
    parser[_section_name] = _exp
    with open(cfg_file, 'w') as f:
        parser.write(f)
    return cfg_file


def test_store_config_create_file(cfg_file: Path):
    assert not cfg_file.exists(), 'Error in test setup'
    store_config(**_exp, file=cfg_file)
    assert cfg_file.exists(), 'File did not created'
    parser = configparser.ConfigParser()
    assert len(parser.read(cfg_file)), "Can\'t parse config file"
    assert _section_name in parser.sections()
    assert _exp == dict(parser[_section_name])


def test_load_config_return_valid_config(non_empty_file: Path):
    config = load_config(non_empty_file)
    assert isinstance(config, dict)
    assert config.keys() == _exp.keys()


def test_load_config_raise_error(cfg_file: Path):
    with pytest.raises(AssertionError):
        load_config(cfg_file)
    cfg_file.touch()
    with pytest.raises(AssertionError):
        load_config(cfg_file)
