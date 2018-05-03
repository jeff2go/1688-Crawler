import requests
from requests.exceptions import ConnectionError
from time import sleep

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;.NET CLR 1.1.4322; .NET CLR2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5(like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
]
proxy_pool_url = 'http://127.0.0.1:5555/random'
proxy = None
max_count = 5


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    global proxy, max_count
    headers = {
        'Cookie': 'cna=JrVoE8ZJpnICAX1wLFvNRBbJ; JSESSIONID=8L78JYZv1-6nbZmNie3IT977N4eA-NnyMKqQ-l4pS; ali_ab=125.112.44.91.1524746036086.3; t=432da7506670e12f3d241952bf1c6180; _tb_token_=7781d5beb7358; _bl_uid=39jv2gs8g4XiF2fOj7UCyqU1g7UR; ctoken=ZeORFq3psTVmabgBTa3Inaga; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJfZXhwaXJlIjoxNTI0ODMyNDUzMDQwLCJfbWF4QWdlIjo4NjQwMDAwMH0=; webp=1; cookie2=1f5c5300c2a943708e5345e962e2b1ce; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1524749336202%7ChomeIdttSAction%3Dtrue; isg=BFJSCSgcXAxv2KP-td53J58Iox70y5FxtsgE_xyrdoXwL_IpBPOmDVhGmosTfs6V; cookie1=BYk5E01IMRgOv9lwa6Q%2F9WEQbcc4WsUiX%2BpLMDqayxo%3D; cookie17=UNcNPbcuK3gM; hng=CN%7Czh-CN%7CCNY; sg=011; csg=9c4655e5; lid=%E4%B9%89%E4%B9%8C2010; __cn_logon__=true; __cn_logon_id__=%E4%B9%89%E4%B9%8C2010; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=3; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=375685501; tbsnid=qLyO3IAfOhOnCFiIl6bLXf8eom1wwAvteXCFzV5Rgnw6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ1zvhIUrY34IWqE1NUiJUbOSnnKfF/EKmUT6JpKURQFRzQyDQRqKjUW+wz6NLz10jFwnSWAw3EYMNHFSYlrqLYigWhihClZrhxnb7+MjupilRdjbwJe08tPFmkyku3yyUEETmUqccb691HchTC+m3ibDFZw+Bj+pm7cWivmjpORmkVZ3FXGXcU8IhUhmvEWZkVU79tFP5M5QRFtQ8zzVZC83KTGdEML8E/rjQt7WGRXuIiM4SWC8Bb2"; login=kFeyVBJLQQI%3D; userID=4xajfL3DQrHncUpnQZX0TYc0vWcisnqH2H6AxmPH6ic6sOlEpJKl9g%3D%3D; _nk_=Y3E2Stm9IjQ6sOlEpJKl9g%3D%3D; userIDNum=jH7Y8ZWD7p1TAhztWl1ziA%3D%3D; last_mid=b2b-375685501ncisr; __last_loginid__=%E4%B9%89%E4%B9%8C2010; _cn_slid_=17PB6qDL%2Bc; _tmp_ck_0=nON%2FXDoC5%2F7aSkrpRM7bhkd9tIGiuAZ7ylxQoqKSPTa3uTy2afq1CtWxVCqwV%2FubdfqikvKFoxIFwPI3cmR2lU1CC3ZYvSUi0ssFJWUJ1OzLyiF9%2BI53M7XWWfvKPJoTl9lQmxp3A9dOeU%2BIWuykryzpMhTtXjjUyhlogA6n5IWCq%2FKNmZr%2FxDsycvkjEZYGigCgBoP6yH6S2VgBl4xM3l2A9bfzLVrfvKMzimyZjS2cLehZFQ5EBoOvyXfhA8Qi3vsnI5%2B5UwnSklBaRcnqd4vajGJ0KastbE1OR5Ixkw0lAVY%2Btk%2BEQeSt3SA7ldVIAlIpKK6%2F2GhYUR0u9sFPDqKDAq1zvMqgB%2BX8glGWk%2FH2K8zd4gB2YYBJd1Y19HrPxdHD%2FkIlH42k8d7A86ozRY%2FCsS5AsKcrnGxKQWiXGL6fEAX1hv1CeGMyjLNBCfj3voysybZmXfqOmzHpldUwK6KryF8rRt6H0H7y33mlpbzS%2B97VMgsvGxkceBjlDck%2F9ts3gGARK9kPx3QwgF5Cng%3D%3D; _csrf_token=1524750096217',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        # 'User-Agent': numpy.random.choice(user_agents),
    }
    print('Try Count', count)
    if count >= max_count:
        print('Tried Too Many Count')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies)
        else:
            response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print(302)
            proxy = get_proxy()
            if proxy:
                print('using proxy with sleep 3 seconds', proxy)
                sleep(3)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)
