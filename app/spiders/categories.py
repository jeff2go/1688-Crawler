"""
抓取1688产品分类列表(及商铺)数据 TODO
"""

import re

from lxml import html

from app.spiders.spider import get_html

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'cna=6B2NFMQceWkCATy/9iZmJ/r2; ali_ab=60.191.246.38.1543910908671.4; lid=%E4%B9%89%E4%B9%8C2010; __last_userid__=375685501; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16b40021a50161-08fe1f8fb068e8-37657e03-1fa400-16b40021a51abb; ali_apache_id=11.15.106.128.1564454978766.321081.5; h_keys="%u7537%u68c9%u670d#%u73a9%u5177#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf#%u91d1%u5b9d%u8d1d#%u4e00%u6db5%u5236%u7ebf#2017%u5723%u8bde%u9996%u9970#%u5723%u8bde%u9996%u9970#%u9996%u9970#%u7ea2%u85af#%u4e49%u4e4c%u817e%u535a%u793c%u54c1"; ad_prefer="2019/08/08 09:38:58"; ali_beacon_id=60.191.246.38.1566810215744.002451.6; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=2; taklid=9d140935ba3b4a8f9c20e255b4a99dd0; _csrf_token=1569548292989; cookie2=11e8d4b69091a1157b038c714385c9a6; t=4c47e32627e4d9d5c08008789ed65a34; _tb_token_=ab7d81831375; uc4=id4=0%40UgDLKslxx%2F5KKbIzCKEbS9CpADM%3D&nk4=0%40s5u8VZNrKh1Ipk4a6%2FKiHZj80A%3D%3D; __cn_logon__=false; alicnweb=homeIdttS%3D99025414611281355176293308315884802540%7Ctouch_tb_at%3D1569548305483%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010%7Cshow_inter_tips%3Dfalse; l=cBMFFQcuvPgtaQebKOfalurza77T5IRb4sPzaNbMiICP_j1y5CQAWZCBm382CnGVp626R3zP_tquBeYBc1bnLjDSik2H9; isg=BNTUjkpcdQqEKuDNKwS17J7fpRRMK8akMa0MD261lt_jWXSjlj_fp6CTWRHkoTBv',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

class Categories:
    def __extract_categories(self, tree):
        link_elements = tree.xpath(
            '//div[contains(@class, "grid-sub")]//div[@class="m-content"]//a[contains(@href, "page/offerlist_")]')

        categories = []
        sub_categories = []
        for item in link_elements:
            href = item.attrib['href']
            ids = re.findall('_(([\d-]+)_?(\d+)*)\.htm', href)[0]
            category = {
                'id': ids[1],
                'pid': ids[2],
                'name': item.text_content().strip(),
                'sub': []
            }
            if category['pid'] == '':
                categories.append(category)
            else:
                sub_categories.append(category)

        for sub_cat in sub_categories:
            for cat in categories:
                if cat['id'] == sub_cat['pid']:
                    cat['sub'].append(sub_cat)
                    break

        return categories

    def __extract_shop_info(self, tree):
        shop_url_element = tree.xpath('//div[contains(@class, "base-info")]//a')[0]
        shop_url = shop_url_element.get('href')
        id = re.findall('https?://(.+)\.1688', shop_url)[0]
        title_element = shop_url_element.xpath('//div[@class="company-name"]')[0]
        title = title_element.get('title')

        # 联系人
        contactor = ''
        contactor_element = tree.xpath('//a[@class="membername"]/text()')
        if len(contactor_element) > 0:
            contactor = contactor_element[0].strip()

        # 电话
        telephone = ''
        telephone_element = tree.xpath('//dl/dt[starts-with(text(), "电")]/following-sibling::dd/text()')
        if len(telephone_element) > 0:
            telephone = telephone_element[0].strip()

        # 移动电话
        mobile = ''
        mobile_element = tree.xpath('//dl/dt[contains(text(), "移动电话")]/following-sibling::dd/text()')
        if len(mobile_element) > 0:
            mobile = mobile_element[0].strip()

        # 地址
        address = self.__extract_shop_address(tree)

        return {
            'id': id,
            'title': title,
            'contactor': contactor,
            'telephone': telephone,
            'mobile': mobile,
            'address': address
        }

    def __extract_shop_address(self, tree):
        address_text = tree.xpath('//span[@class="address_title"]/text()')[0]
        address_text = re.findall('地址：\s+(.+)', address_text)[0]
        address_text = address_text.replace('  ', ' ')
        address_list = address_text.split(' ')
        if len(address_list) == 3:
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
        content = get_html(url, headers)
        tree = html.fromstring(content)

        data = {
            'data': self.__extract_categories(tree),
            'shop': self.__extract_shop_info(tree)
        }

        return data
