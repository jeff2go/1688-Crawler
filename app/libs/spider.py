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
        'Cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; hng=CN%7Czh-CN%7CCNY%7C156; webp=1; _m_h5_tk=70b125e2d19a4e735f32a64a22f50a07_1525229689623; _m_h5_tk_enc=db1c3a888ddea51ca0bb04d9d6ad37bb; h_keys="%u73a9%u5177"; ad_prefer="2018/05/03 15:48:58"; JSESSIONID=8L78WELv1-18eZMusont66u0InZ8-DUvBKrQ-sEl4; cookie2=1610f527c3af6b862fe791489c4da285; t=432da7506670e12f3d241952bf1c6180; _tb_token_=fa09155f66417; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie17=WvX8NQn9COLZ; sg=%E5%8E%820a; csg=c32782ec; lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_track=c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82|c_ms=2|c_mt=3; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; tbsnid=veKaErNct5vGcnB%2FwdTbwV%2F1rl7ErXqebSyqfFo%2BzY06sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDNHCeDv14o/+LCoT6M9eIna5nTvYDOiuKU7HgB4cYksfXOHinVz/VkOdM/xbjJkvF/3dEXc60g53bjih00YaeDFa56L8rnsMa+B36fltyGDBEUo9QCuC6+fN5dm4vw0DRzYoptLsGxHHfwUof6eBaAgTppWzJKIjUYMKUYEZDPqjc0+fusazbrJhKXTepbSN0a09UZUt+iL4Q="; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; _nk_=thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D; userIDNum=I1GdGME70WvmkdAiNY8Cqw%3D%3D; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; _csrf_token=1525659541153; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1525659542984%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582%7Cshow_inter_tips%3Dfalse; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C850194D46E88321466F4CD81A0528791; _tmp_ck_0="LUGYM4%2BaK%2FXV1CgGHE43bjDSHdKM6CiPWs7a7UDHy%2FnMTeiTXVeZyjLbr%2ByxcJKaeUVeIiZSVMojisx18h3cfRxIjuQ1XxOkR8je6k8uCd%2B1MCWlYCJT%2BEyzEpOa5xvjKQQQsmNjyxnlW%2F0ccwthfrPm%2BGEEko7ieLBc6Q2ukYP889%2B1G2G%2B%2FF1idX8h1uFrO3cd%2Fxp04Agl14hHAOy%2Fr2o3pXrIhoLdI41nzqhFAvj0ON2kFrsR7o5O35b%2B9mPuQ6Dpc5NHSDghPIGlSdIEc9%2Fk8dF8ZozO7QGo1CVhqBQEYmwyZA93ldxsMPBhgkNe2WWuEZ1uk1S4bR%2FLlpKvECSAT6EWKdzbMflHOB%2FTqtUnZn3oINoDgenkgBn2b4YtQTs%2BDP2sR0toDXWH2tfIkOwPOwnq8n7q%2BKyoTJut4cI%2F1EKgL0jt4%2Baob4OMwBEyWW4hwl4vSDAksJTOX%2FsT2y5U5Knx%2FzhnB98bDhWeMgtBnoAdalezOPPE2sTAO6U6ftPh%2BF9S7wQKQV49MY2U62gTQcNLiMto"; isg=BFJSEwnYXAIPcqP-td53J58Iox4-ZWhOHX7i6hyrVIXwL_IpBPOmDVhlm4sTX86V',
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
