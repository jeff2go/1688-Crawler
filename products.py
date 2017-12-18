# -*- coding: utf-8 -*-

'''
抓取1688产品列表数据
'''

import re
import json

import requests
from lxml import html

class Products():
    http = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
        'Cookie':'ali_beacon_id=60.191.246.41.1472092574174.121211.5; l=Ari41S0sYzMO4Y0DLKZtRdKtCGhLQByw; __guid=224050958.4129828784400486000.1501575451180.7642; _uab_collina=150157545673451089484192; CNZZDATA1261052687=760213936-1501638200-https%253A%252F%252Fdetail.1688.com%252F%7C1501638200; ali_apache_track="c_ms=1|c_mid=b2b-467363274|c_lid=%E5%93%88%E4%BA%8B%E5%90%84"; UM_distinctid=15f47bc63db2bb-08d93fe730b364-5d4e211f-100200-15f47bc63dc25c; cna=jSsfEFS+gScCAX1wvWtLLM7h; h_keys="%u5361%u7eb8%u753b#%u9053%u6734%u7eb8#%u7259%u7b7e#%u84dd%u7259%u8033%u673a#%u53a8%u623f%u5200#%u87ba%u4e1d%u673a#%u65b9%u5dfe#%u6bdb%u5dfe#%u53a8%u623f%u6302%u67b6#%u8db3%u6d74%u76c6"; ad_prefer="2017/10/24 09:02:04"; Hm_lvt_97c875c5e5d9f579abee666c38327aee=1508737051,1509351507; JSESSIONID=dnzY0Ec-mEgYh3CQt2VB7h4at8-lX7KLaQ-p32; cookie1=VFPrftrDkQN4HRVN5uKe5a7o8Qz4gwXoTyRFU3km8yM%3D; cookie2=11a90adce22a70334b1d850d1645d8f8; cookie17=VypX7OXb%2Bqmg; hng=CN%7Czh-CN%7CCNY%7C156; uss=AnWaQPvGOtjnMdfE0y7XuL%2F%2FASlpMQ2yWQmuoTRCDPbpqM7T9NgMuhFzBQ%3D%3D; t=14d9dd418806e4d7ef6df57ad459661f; _tb_token_=63b31150e3cb; sg=%E5%90%844a; __cn_logon__=true; __cn_logon_id__=%E5%93%88%E4%BA%8B%E5%90%84; ali_apache_tracktmp="c_w_signed=Y"; cn_tmp="Z28mC+GqtZ1f6I+6hPp15KcgoH9jp94vr5lyUwmRnIt+nxAcxhN6vxHNk5fgDzTTJGwB87LzjYEDhV8TbXHKIzttMproEX+1mKpPUWm0ShjuHvjjZlnmTaBju0MKVKGtAG1D21adC3YQqOXAM2B/nIUuWiPTOvzuuCtR5nUWDT3t9/pCYEpMWHkPMKDN4c0VSscdpN2oZVvVSzTK1KPZqf+9Vigf+2fxI7li0glwxDk="; _cn_slid_="%2Fe7WsDxbjz"; tbsnid=diYNjoGFiX8wDs0Ahh1iKEV0p%2F5TzSfnqOAFLCBjgHA6sOlEpJKl9g%3D%3D; LoginUmid="%2F%2F6U95LyO53uP8WfpGnW%2BBOG7fx%2BMF97%2Br6BxF4XS3Yyp8JBi5lr6w%3D%3D"; userID="nMmuAOiAGU07zAKwqNcy7mKhz3jZ9sMPUrJKv3iiMJ46sOlEpJKl9g%3D%3D"; last_mid=b2b-467363274; unb=467363274; __last_loginid__="%E5%93%88%E4%BA%8B%E5%90%84"; login="kFeyVBJLQQI%3D"; _csrf_token=1510102012750; ali_ab=60.191.246.41.1486713481476.9; _is_show_loginId_change_block_=b2b-467363274_false; _show_force_unbind_div_=b2b-467363274_false; _show_sys_unbind_div_=b2b-467363274_false; _show_user_unbind_div_=b2b-467363274_false; monitor_count=3; CNZZDATA1253659577=823052292-1501573495-%7C1510098241; __rn_alert__=false; _umdata=535523100CBE37C3139C60D67F3AA08899AE63FC336C1E3B218982C81FB2C66BD43AF69D35F89216CD43AD3E795C914C6CDA35B865DF8F70407820361FDBCE4C; alicnweb=touch_tb_at%3D1510102034102%7Clastlogonid%3D%25E5%2593%2588%25E4%25BA%258B%25E5%2590%2584; _ITBU_IS_FIRST_VISITED_=*xC-i2FHLMGc4vG80MGkT%3Apm0jjhmokk%7C*xC-i2FvWvGvSvFkyvmcYZFgLMgTT%3Apm0jjhn1qd; userIDNum="Aqt%2Fjdu2G2YDBPJBu4sTUQ%3D%3D"; _nk_="AukEgnGQNb4%3D"; _tmp_ck_0="LUGYM4%2BaK%2FXNO2g1QcArZsvppziep7QmZ31P6o78AUV1Z4wLqzlLbKXQ3bdhle2j7%2FBFxN4mlBC6dVS9VdDshlkfZmNU4aN35MkDCC8Aqn1a0YVC%2FgXWDawt0IeuAi9b3wcGwlx24ONjemtanber3RUgw3a2SHnBf9Jhpi67tjfy9rU8FTcoSjIEd16c5tYin9fgZ58KhidXmHl%2FYR7eqmUS9c6N%2FRrDIAilhgFl0iV6qNV4Eq6HOQP8XwCnvWKtqNB5OssBwKS%2F0m7NCblt6vfWdoROSfkWkD%2FStCvsQ5lMVVx1eTPGmhSr0Cgqopu6g6M1DdpHji9%2BOdFNU8pmKfwGydvu3M%2BRQMJD14iQ7rI9GdwSUtWdDOefFoJEQYLEcpgKb9jyKU2nSnp8MCOWpPlZ0J9FcN28gWm8UOcEj8KZwFVKU%2BDfAEeQsNbTvnIX7VOzBsEq5MKVBZQYKt889ReLAeNuATkhc3XsKZ4AOGtD1x6jb3g5ZHWAsPmoc1vlfVDnYvxA0URufjOs7ctIyA%3D%3D"; isg=AlBQD6zjPtFQAOBKiJ1C0vimIZ5isSo8tLqbmEogC6t-hfAv8ykE86b_KUKx'
    }

    def __fetch_content(self, url):
        self.http = self.http or requests.session()
        r = self.http.get(url, headers=self.headers)
        return r.text

    # 分页数据
    def __extract_pagination(self, tree):
        pagination_htmls = tree.xpath('//div[@class="wp-paging-unit"]/ul')
        if (len(pagination_htmls) > 0):
            pagination_html = pagination_htmls[0]
        else:
            return {
                'total': len(self.__extract_product_info(tree)),
                'current_page': 1,
                'last_page': 1,
                'per_page': 20,
                'data': []
            }
        total = int(tree.xpath('//em[@class="offer-count"]/text()')[0])
        current_page = int(tree.xpath('//li[@class="pagination"]/a[@class="current"]/text()')[0])
        last_page = int(tree.xpath('//em[@class="page-count"]/text()')[0])
        per_page = 20
        return {
            'total': total,
            'current_page': current_page,
            'last_page': last_page,
            'per_page': per_page,
            'data': []
        }

    # 产品数据
    def __extract_product_info(self, tree):
        price_elements = tree.xpath('//div[@class="wp-offerlist-windows"]//li[@data-prop]//div[@class="price"]/em/text()')
        base_elements = tree.xpath('//div[@class="wp-offerlist-windows"]//li[@data-prop]//div[@class="title"]/a')

        def extract_product(price, other):
            url = other.get('href')
            return {
                'id': int(re.findall('offer/(\d+)', url)[0]),
                'title': other.get('title'),
                'price': float(price),
                'url': url
            }

        return list(map(extract_product, price_elements, base_elements))

    def __extract_shop_info(self, tree):
        shop_url_element = tree.xpath('//div[contains(@class, "base-info")]//a')[0]
        shop_url = shop_url_element.get('href')
        id = re.findall('https?://(.+)\.1688', shop_url)[0]
        title_element = shop_url_element.xpath('//div[@class="company-name"]')[0]
        title = title_element.get('title')

        # 联系人
        contactor = ''
        contactor_element = tree.xpath('//a[@class="membername"]/text()')
        if (len(contactor_element) > 0):
            contactor = contactor_element[0].strip()

        # 电话
        telphone = ''
        telphone_element = tree.xpath('//dl/dt[starts-with(text(), "电")]/following-sibling::dd/text()')
        if (len(telphone_element) > 0):
            telphone = telphone_element[0].strip()
        
        # 移动电话
        mobile = ''
        mobile_element = tree.xpath('//dl/dt[contains(text(), "移动电话")]/following-sibling::dd/text()')
        if (len(mobile_element) > 0):
            mobile = mobile_element[0].strip()

        # 地址
        address = self.__extract_shop_address(tree)

        return {
            'id': id,
            'title': title,
            'contactor': contactor,
            'telphone': telphone,
            'mobile': mobile,
            'address': address
        }

    def __extract_shop_address(self, tree):
        address_text = tree.xpath('//span[@class="address_title"]/text()')[0]
        address_text = re.findall('地址：\s+(.+)', address_text)[0]
        address_text = address_text.replace('  ', ' ')
        address_list = address_text.split(' ')
        if (len(address_list) == 3):
            address = {
                'country': address_list[0],
                'state': address_list[1],
                'city': '',
                'detail': address_list[2]
            }
        else:
            address = {
                'country': address_list[0],
                'state': address_list[1],
                'city': address_list[2],
                'detail': address_list[3]
            }
        return address

    def go(self, url):
        content = self.__fetch_content(url)
        tree = html.fromstring(content)

        products = {
            'total': 0,
            'current_page': 1,
            'last_page': 1,
            'per_page': 20,
            'data': []
        }

        pagination = self.__extract_pagination(tree)
        products.update(self.__extract_pagination(tree))
        products['data'] = self.__extract_product_info(tree)
        products['shop'] = self.__extract_shop_info(tree)

        return products

# products = Products()
# PRODUCT_URL = 'https://hanshuhanshu.1688.com/page/offerlist.htm?spm=a2615.2177701.0.0.3916fb2aYydGj4'
# print(products.go(PRODUCT_URL))
