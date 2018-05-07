import requests
from requests.exceptions import ConnectionError
from time import sleep

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
        'Cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; hng=CN%7Czh-CN%7CCNY%7C156; webp=1; _m_h5_tk=70b125e2d19a4e735f32a64a22f50a07_1525229689623; _m_h5_tk_enc=db1c3a888ddea51ca0bb04d9d6ad37bb; h_keys="%u73a9%u5177"; ad_prefer="2018/05/03 15:48:58"; JSESSIONID=8L78WELv1-18eZMusont66u0InZ8-DUvBKrQ-sEl4; cookie2=1610f527c3af6b862fe791489c4da285; t=432da7506670e12f3d241952bf1c6180; _tb_token_=fa09155f66417; ali_apache_tracktmp=c_w_signed=Y; tbsnid=veKaErNct5vGcnB%2FwdTbwV%2F1rl7ErXqebSyqfFo%2BzY06sOlEpJKl9g%3D%3D; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C850194D46E88321466F4CD81A0528791; __rn_alert__=false; cookie1=BYk5E01IMRgOv9lwa6Q%2F9WEQbcc4WsUiX%2BpLMDqayxo%3D; cookie17=UNcNPbcuK3gM; sg=011; csg=57e2d824; lid=%E4%B9%89%E4%B9%8C2010; __cn_logon__=true; __cn_logon_id__=%E4%B9%89%E4%B9%8C2010; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=3; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=375685501; cn_tmp="Z28mC+GqtZ1zvhIUrY34IWqE1NUiJUbOSnnKfF/EKmUT6JpKURQFRzQyDQRqKjUW+wz6NLz10jFwnSWAw3EYMNHFSYlrqLYigWhihClZrhxnb7+MjupilRdjbwJe08tPFmkyku3yyUEETmUqccb691HchTC+m3ibDFZw+Bj+pm7cWivmjpORmkVZ3FXGXcU8IhUhmvEWZkVU79tFP5M5QRFtQ8zzVZC83KTGdEML8E9yXw9xeUXJCitWA3lZuPPv"; login=kFeyVBJLQQI%3D; userID=4xajfL3DQrHncUpnQZX0TYc0vWcisnqH2H6AxmPH6ic6sOlEpJKl9g%3D%3D; _nk_=Y3E2Stm9IjQ6sOlEpJKl9g%3D%3D; userIDNum=jH7Y8ZWD7p1TAhztWl1ziA%3D%3D; last_mid=b2b-375685501ncisr; __last_loginid__=%E4%B9%89%E4%B9%8C2010; _cn_slid_=17PB6qDL%2Bc; _csrf_token=1525670274817; _is_show_loginId_change_block_=b2b-375685501ncisr_false; _show_force_unbind_div_=b2b-375685501ncisr_false; _show_sys_unbind_div_=b2b-375685501ncisr_false; _show_user_unbind_div_=b2b-375685501ncisr_false; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1525670262574%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010%7Cshow_inter_tips%3Dfalse; _tmp_ck_0="nON%2FXDoC5%2F5X1cNg18b8vaA4a5P%2FjKr5B2kyyqCAAf70KUDZFVdQLDxFNzn3AofE%2BcfK0di%2Be8aDMdyaxgUvZNFjfv6ccCJ%2BGzhZeWYImsz%2ByoOP%2FXAbHRtyxuBaF%2Fj%2BqV18bCf079synNXknB%2B%2FAW84hy3tQW6IJJTNevXdCKNs6OR4g662ij4mLE7Rjr11XTR2%2F%2BGGh0VF5RPHSefQHmr24OGPOX6gnYJZI3CGuNeCG2H3saFhTlxKNRM%2FNodgzKxSbZa2f2FsZpTuuvMgj1%2Fcbrq88ij1YCvJ4GvDyn5%2BmDFNaMRBYNkJw7vHxlmkihPVpjOGErXQgoy%2BBJqCnWkjlZUBldAFUyJYbYCqPj8DUTc1ALjSLMNunhxHTtLQx67JLtl23sGD5kYqT0NFMuDowNPhp41kpMXHYRsH1HPbA%2BjeGgS57yjtoG%2Bvv1lwNTLmwO4mhDUhDG7jsPpgKUSyfnNxBdVXi4wAr0r%2BpcNZzJu%2Frtva0n%2F8qwxbyvKB7Q3YQmNZ%2FYWSIhjDSAgX5laSC%2Bub78tY"; isg=BMHBKfEPf_8uiJDLagP0Kigt0AvR6AtTyntxPyMWt0glCuDcazvlsVwg6H5MAs0Y',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
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
