from app.cache.redis import RedisClient
import requests
from requests.exceptions import ConnectionError
from app.settings import MAX_REQUEST_COUNT

redis = RedisClient()
cookie = redis.random() or 'cna=JrVoE8ZJpnICAX1wLFvNRBbJ; JSESSIONID=bYyYmJj-WQnZB2bhNm02SE4CkF-AkjlUtQ-buVN; ali_ab=60.191.246.38.1527648098283.2; cookie2=1e8df116199db8703304a09b4259dd5d; t=a8e1d92dd57f9940cdd2297d44c89665; _tb_token_=5a8160539b5be; lid=%E4%B9%89%E4%B9%8C2010; __cn_logon__=false; _tmp_ck_0=repzlpczqMsCyFXw%2Bu3vIS2x9vA7LfQ0aEUkQOjgQSz9vKXptrC1YQeXxsHVu3loiES3AVg%2BJxzjKDbVw1ODz5BP0q85dubLqDDUw5nuGOplPrm%2Bt7Ziwsr137JT4CITSeoxN3Be4AdeWmJeyiALt3E6%2Fvd5n3gOfkWxVEEYacfs%2BumTtn6VRV%2BUFLxOuV5N97nlGKi5L76R5%2BhTLJRyhUR2P0%2BKrbV0QrNDRkYlp3NpCGpDJQl7DNuIH4JWFSetH0cAA7inUrXQludCunYXFxOeEO%2BhcCrVo4WA%2B4eYb45ZGDKbD2eq%2F5p8gnTPK7kIiOetu2hOu5dxH6oMFwJzLlNOknv908oJpnaDd3ZotMVx53vx6xSZnmkBzOm%2FFF%2Bkhz858oZn%2F4w%3D; _bl_uid=8Rj2hh1ts4qigs8byig0cCLcjFjO; alicnweb=homeIdttS%3D45913072957084221467214121330697404248%7Ctouch_tb_at%3D1527648101275%7ChomeIdttSAction%3Dtrue; isg=BBwcvh9YqyH9Ql0cX8gBpSWm7TzEk_4MbC54nfYdKYfqQbzLHqWQT5Lzpam5SfgX'


def get_html(url, count=1):
    global cookie, redis
    max_count = int(MAX_REQUEST_COUNT)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
        'cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'upgrade-insecure-requests': '1',
    }
    print('Try count', count)
    if count >= max_count:
        print('Tried Too Many Count, canceled')
        return None
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('request 302')
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
