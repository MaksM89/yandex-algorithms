import urllib.parse
import urllib.request
from threading import Thread
from unittest.mock import Mock, patch

import pytest

from yandex_algorithms.modules.contestyandex.oauth_api import authenticate_yandex

_REDIRECT_URL = 'http://localhost:8000/callback?{query}'


def mock_open(url: str):
    def post(req: urllib.request.Request):
        # time.sleep(0.1)
        with urllib.request.urlopen(req, timeout=1):
            pass
    parsed_path = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed_path.query)
    if 'state' not in query:
        pytest.fail('Test mock setup error')
    params = {
        'code': 123,
        'state': query['state'][0],
        'cid': 'idontknowwhatitis'
    }
    req = urllib.request.Request(
        _REDIRECT_URL.format(query=urllib.parse.urlencode(params)),
        method='GET'
    )
    Thread(target=post, args=(req,)).start()


@patch('yandex_algorithms.modules.contestyandex.oauth_api._make_post_request')
@patch('webbrowser.open')
def test_authenticate_yandex(mock_wb: Mock, mock_mpr: Mock):
    exp_token = 'y0_123'
    mock_wb.side_effect = mock_open
    mock_mpr.return_value = ({'access_token': exp_token}, 200)
    token = authenticate_yandex('123', '123')
    assert exp_token == token
