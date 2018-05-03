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
        'Cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; hng=CN%7Czh-CN%7CCNY%7C156; webp=1; _m_h5_tk=70b125e2d19a4e735f32a64a22f50a07_1525229689623; _m_h5_tk_enc=db1c3a888ddea51ca0bb04d9d6ad37bb; h_keys="%u73a9%u5177"; lid=%E4%B9%89%E4%B9%8C2010; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=3; last_mid=b2b-375685501ncisr; __last_loginid__=%E4%B9%89%E4%B9%8C2010; _cn_slid_=17PB6qDL%2Bc; JSESSIONID=Ur4Zmla-MZeZZduQ6qGseH7MX7-GCq8yqQ-rvu8; cookie2=142a73065584bae443704d83fdaadf6e; t=432da7506670e12f3d241952bf1c6180; _tb_token_=f330ef3e0ebf3; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1525333721798%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010; ad_prefer="2018/05/03 15:48:58"; cookie1=BYk5E01IMRgOv9lwa6Q%2F9WEQbcc4WsUiX%2BpLMDqayxo%3D; cookie17=UNcNPbcuK3gM; sg=011; csg=448d5df9; __cn_logon__=true; __cn_logon_id__=%E4%B9%89%E4%B9%8C2010; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=375685501; tbsnid=%2B4CVjRkMKaQWOjMPWpaD1zrN%2BlubKw7JjPRzYe%2Fbago6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ1zvhIUrY34IWqE1NUiJUbOSnnKfF/EKmUT6JpKURQFRzQyDQRqKjUW+wz6NLz10jFwnSWAw3EYMNHFSYlrqLYigWhihClZrhxnb7+MjupilRdjbwJe08tPFmkyku3yyUEETmUqccb691HchTC+m3ibDFZw+Bj+pm7cWivmjpORmkVZ3FXGXcU8IhUhmvEWZkVU79tFP5M5QRFtQ8zzVZC83KTGdEML8E/rPa0DvMiB1QyDHvjF0DZT"; login=kFeyVBJLQQI%3D; userID=4xajfL3DQrHncUpnQZX0TYc0vWcisnqH2H6AxmPH6ic6sOlEpJKl9g%3D%3D; _nk_=Y3E2Stm9IjQ6sOlEpJKl9g%3D%3D; userIDNum=jH7Y8ZWD7p1TAhztWl1ziA%3D%3D; _csrf_token=1525333745872; _is_show_loginId_change_block_=b2b-375685501ncisr_false; _show_force_unbind_div_=b2b-375685501ncisr_false; _show_sys_unbind_div_=b2b-375685501ncisr_false; _show_user_unbind_div_=b2b-375685501ncisr_false; __rn_alert__=false; _tmp_ck_0="Dy8PRM0AS5%2BQuS5c4ZHuW2TeE%2B0ayhy8cVZQMMgwWlyFmj%2FL3SvTU%2FaZA%2F03%2BxxkNpwC2hEka3hhyuUN0YGkek4cBUQ6amQy5MPXJvIP0F2gHzwuNiYjdoDmSJP60lI4PIyFNwVFs5fPwbNtFriBy6EUlRM%2FmxwWEqn2%2FfuOQG%2F%2FCIV9UD92ApdcaWd32hEU4CBIsBmjkQIuEIkLFdsUL2OhUNNd0ztwWMfXagX%2F8zqIaNwi3eSotr2XKWTO80cEJHb8o8%2Fj3mwTU55k0ScebmyPs1Va9%2F%2B3qXoitHq8j%2BdR9hVj5P2PkoBI84y1frBcRBrcfp6ckOxKaaojnDx6UTP7YAQBKiDtkUD9xh0cfIB0Gi9rNlOXtbLCv838vEwEBfMH%2BjaGmduW2x5t3YpE0E6pnRJSMhuzMjOgBbL5Yi8CIJg8hcD%2FsyPxXCkX2UttvXbqPeQ4Tc%2BjED3Sbo1NU99Zd8Au1I0xJl86EJlIv4%2FtbWfMWNPgmvoXllshRZEYZwbzenwxlArCF1Jq5nn2D19m2V8jZY%2Fv"; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C3F03E7187C0A6DCC018DCA4B0B5FDAC7; isg=BAgI__8JxsFBESlAi2zdIZka2XAQt1II2wzo9MK5XQN2nagHasE8S563EXXtrSST',
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
