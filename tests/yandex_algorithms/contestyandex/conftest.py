from typing import Union
from unittest.mock import MagicMock, Mock, patch

import pytest

from . import api_response


def mock_constructor(mock: Mock, status: int, read: Union[bytes, None] = None, side_effect: Union[list[Exception], None] = None):
    mock_response = MagicMock()
    if side_effect:
        mock.return_value.__enter__.side_effect = side_effect
    else:
        mock.return_value.__enter__.return_value = mock_response
        mock_response.read.return_value = read
        mock_response.status = status
        mock_response.headers = {}
    return mock_response


@pytest.fixture
def urlopen_mock():
    with patch('urllib.request.urlopen') as mock:
        yield mock


@pytest.fixture(scope='package')
def token() -> str:
    return 'y0__ASnlaADSSJDkabh79gabsduH8ahsda8sd0da=aj9abjufaGHK'


@pytest.fixture(scope='package')
def contest_id() -> int:
    return 12345


@pytest.fixture()
def submission_info() -> dict:
    return api_response.submission_info.copy()


@pytest.fixture(scope='package')
def problems() -> dict:
    return api_response.problems


@pytest.fixture(scope='package')
def file_content() -> str:
    return api_response.file_content
