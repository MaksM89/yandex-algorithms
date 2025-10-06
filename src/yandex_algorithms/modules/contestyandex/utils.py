import http.server
import json
import os
import random
import string
import urllib.error
import urllib.request
from collections.abc import Iterable
from multiprocessing.pool import ThreadPool
from typing import Callable, TypeVar, Union

_auth_code = None
_state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code

        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)

        if parsed_path.path == '/callback' and 'code' in query:
            _auth_code = query['code'][0]
            state_rcv = query.get('state', [None])[0]

            if state_rcv != _state:
                self.send_response(400)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('<h1>Ошибка</h1><p>Неверный параметр state.</p>'.encode())
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('''
            <h1>✅ Успешно!</h1>
            <p>Вы авторизованы через Yandex ID. Теперь можно закрыть это окно.</p>
            '''.encode())
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<h1>400 Ошибка</h1><p>Неизвестный путь.</p>'.encode())

    def log_message(self, format, *args):
        pass  # Отключаем логи сервера

# === Вспомогательная функция для отправки POST-запросов через urllib ===


def _make_post_request(url, data=None, headers=None, encode=True) -> tuple[dict, int]:
    """
    Универсальная функция для POST-запроса через urllib
    """
    if data and encode:
        data = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers or {}, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            return json.loads(body), response.status
    except urllib.error.HTTPError as e:
        return {'error': e.msg}, e.code


# === Вспомогательная функция для GET-запросов через urllib ===
def _make_get_request(url, headers=None, return_json=True) -> tuple[Union[dict, str], int]:
    """
    Универсальная функция для GET-запроса через urllib
    """
    req = urllib.request.Request(url, headers=headers or {}, method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return {'error': str(e)}, e.code
    except UnicodeDecodeError as e:
        return {'error': str(e)}, 500
    if return_json:
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            return {'error': str(e)}, 500
    return body, response.status


def general_headers(token: str, accept: str = 'application/json') -> dict[str, str]:
    return {
        'Authorization': f'OAuth {token}',
        'accept': accept,
    }


R = TypeVar('R')


# def map_in_thread(func: Callable[P, R], params: Iterable[P]) -> list[R]:
def map_in_thread(func: Callable[..., R], params: Iterable[tuple]) -> list[R]:
    with ThreadPool(os.cpu_count() or 1) as pool:
        result = pool.starmap(func, params)
    return result
