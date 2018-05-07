import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = '\x0bo\x92\x7f\x0ceW+v\xd2\xb6F\xfe\xea\x00\x92\xbcPf\x0e\x92<m\xf4'
DEBUG = False

REDIS_HOST = os.getenv("REDIS_HOST") or '127.0.0.1'
REDIS_PORT = os.getenv("REDIS_PORT") or 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or ''
REDIS_KEY_FOR_PROXY_COOKIES = os.getenv("REDIS_KEY_FOR_PROXY_COOKIES") or 'redis_key_for_proxy_cookies'

MAX_SCORE = 10
MIN_SCORE = 1
INITIAL_SCORE = 10
