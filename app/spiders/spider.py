from app.cache.redis import RedisClient
import requests
from requests.exceptions import ConnectionError

redis = RedisClient()
cookie = redis.random() or 'cna=SkXXEeTNmyUCATy/9iZ5q4MR; ptid=SkXXEeTNmyUCATy/9iZ5q4MR; JSESSIONID=XK0ZEOm-8iXZHZOyg9JkwDart7-Y0C2QrQ-xL8u1; cookie2=12ffccd9dfde6ddab53f3b3d6e105e0b; hng=CN%7Czh-CN%7CCNY%7C156; t=e41d229beff1dae2873a1bde061d9cd1; _tb_token_=e513668773ee3; lid=txf19882006; __cn_logon__=false; _tmp_ck_0=qgnHlOkUZ7V2v%2FPPouI2ZpJklZg%2BkoylPdWzxxiDoTK6wVqMHG3HpkLTjoD4faIPcHiwlBjZ19emPhRPfoVBJPHLTCqXzPEHJtEhdokLcdtyAYfQ4Di0yqhCYU00lHLrhNv5LyBcL61CdC4HkhmM5%2FeuyWJS9%2B9ZBOY63Ie4lKA6ClwrDycrf26vPGT8Qa1LO5Muq%2B7FJOwBgRtmQsv2IK7RNsxZQOZAWTRGdAybom2AhY4fkVTsnM2lS7QAnSg9JBRcTJBZy4XGNB9YEdDxIp1bubbfAnJRgrcUa0oFW5yX7y%2BFacrt%2B97CBgmVKBQgzDCHhNeyCtwYZpvZ0e2V0s19UzMWZW%2F5NQ62c%2BbISB7o0BOKhJnJAJo9mMfH8Qdj; alicnweb=touch_tb_at%3D1525745873782; isg=BJ2dpKbam81DTX_hx9zj_Ok4rHmdvO-7rHqf-l9i2fQjFr1IJgrh3GuMRAoQ1unE; ali_ab=60.191.246.38.1525745875468.9'


def get_html(url, count=1):
    global cookie, redis
    max_count = 10
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cache-control': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
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
