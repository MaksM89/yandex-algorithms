import http.server
import logging
import random
import socketserver
import string
import urllib.parse
import webbrowser

from .utils import _make_post_request

_AUTH_URL = 'https://oauth.yandex.ru/authorize'
_TOKEN_URL = 'https://oauth.yandex.ru/token'
_REDIRECT_URI = 'http://localhost:8000/callback'

_auth_code = None
_state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

_logger = logging.getLogger(__name__)

# === HTTP-сервер для получения кода авторизации ===


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code

        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)

        if parsed_path.path == '/callback' and 'code' in query:
            _auth_code = query['code'][0]
            state_rcv = query.get('state', [None])[0]

            if state_rcv != _state:
                _logger.debug('Error in states: expected %s, got %s.', _state, state_rcv)
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


def _start_local_server(host: str, port: int, timeout: int = 10):
    """Запускает локальный HTTP-сервер для получения кода авторизации"""
    with socketserver.TCPServer((host, port), OAuthHandler) as server:
        server.timeout = timeout
        _logger.info(
            '🌍 We are awaiting authorization... The server is running on http://localhost:8000/callback.')
        server.handle_request()  # Обрабатываем один запрос


# === Основной процесс авторизации ===
def authenticate_yandex(client_id: str, client_secret: str):

    # 1. Формируем URL для авторизации
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': _REDIRECT_URI,
        'state': _state,
        'scope': 'contest:submit'
    }
    auth_request_url = f'{_AUTH_URL}?{urllib.parse.urlencode(params)}'

    _logger.info('🔗 Opening the browser for authorization...')
    webbrowser.open(auth_request_url)

    # 2. Запускаем локальный сервер для получения кода
    _start_local_server('localhost', 8000)

    if not _auth_code:
        raise Exception(
            '❌ The authorization code was not received. "client_id" and "client_secret" may be missing/incorrect.')
    _logger.info('✅ Authorization code received.')

    # 3. Обмениваем код на токен
    token_data = {
        'grant_type': 'authorization_code',
        'code': _auth_code,
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response, status = _make_post_request(_TOKEN_URL, data=token_data, headers=headers, encode=True)
    if status != 200:
        raise Exception(f'❌ Token receipt error: {token_response}')
    token = token_response['access_token']
    _logger.info('✅ Success! The token was received')
    return token
