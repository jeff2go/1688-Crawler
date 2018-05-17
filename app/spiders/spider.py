from app.cache.redis import RedisClient
import requests
from requests.exceptions import ConnectionError
from app.settings import MAX_REQUEST_COUNT

redis = RedisClient()
cookie = redis.random()


def get_html(url, count=1):
    global cookie, redis
    max_count = int(MAX_REQUEST_COUNT)
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'upgrade-insecure-requests': 1,
    }
    print('Try Count', count)
    if count >= max_count:
        print('Tried Too Many Count')
        return None
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            redis.decrease(cookie)
            cookie = redis.random()
            if cookie:
                print('using proxy cookie')
                count += 1
                return get_html(url, count)
            else:
                print('Get Proxy Cookie Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        cookie = redis.random()
        count += 1
        return get_html(url, count)
