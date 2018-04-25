# -*- coding: utf-8 -*-

'''
抓取1688产品数据
'''

import re
import json

import requests
from lxml import html

class Product():
    http = None
    headers = {
        # 'cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=z5pIE+qek0ECATy/9iaD8lki; ali_ab=60.191.246.38.1522642136552.6; hng=CN%7Czh-CN%7CCNY%7C156; h_keys="%u73a9%u5177#bag#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf%u5382"; ad_prefer="2018/04/11 11:37:06"; t=e3985612d6beba055cc8c87d9bcaf964; JSESSIONID=9L78RXlv1-4iXZjxhQnKxP8Hd9w5-YBw6SpQ-3lqL; cookie2=172833be444ae901140322c9b46e6a92; _tb_token_=795b3b153b870; cookie1=BYk5E01IMRgOv9lwa6Q%2F9WEQbcc4WsUiX%2BpLMDqayxo%3D; cookie17=UNcNPbcuK3gM; sg=011; csg=4859e197; lid=%E4%B9%89%E4%B9%8C2010; __cn_logon__=true; __cn_logon_id__=%E4%B9%89%E4%B9%8C2010; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=3; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=375685501; tbsnid=yxG7lxPChsysHgw3sRp8%2F0cjHoY1LZpN%2BlU4bsJavko6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ1zvhIUrY34IWqE1NUiJUbOSnnKfF/EKmUT6JpKURQFRzQyDQRqKjUW+wz6NLz10jFwnSWAw3EYMNHFSYlrqLYigWhihClZrhxnb7+MjupilRdjbwJe08tPFmkyku3yyUEETmUqccb691HchTC+m3ibDFZw+Bj+pm7cWivmjpORmkVZ3FXGXcU8IhUhmvEWZkVU79tFP5M5QRFtQ8zzVZC83KTGdEML8E84z5c93xTUfkaTQMOi5B1J"; login=kFeyVBJLQQI%3D; userID=4xajfL3DQrHncUpnQZX0TYc0vWcisnqH2H6AxmPH6ic6sOlEpJKl9g%3D%3D; _nk_=Y3E2Stm9IjQ6sOlEpJKl9g%3D%3D; userIDNum=jH7Y8ZWD7p1TAhztWl1ziA%3D%3D; last_mid=b2b-375685501ncisr; __last_loginid__=%E4%B9%89%E4%B9%8C2010; _cn_slid_=17PB6qDL%2Bc; _csrf_token=1523944441155; _is_show_loginId_change_block_=b2b-375685501ncisr_false; _show_force_unbind_div_=b2b-375685501ncisr_false; _show_sys_unbind_div_=b2b-375685501ncisr_false; _show_user_unbind_div_=b2b-375685501ncisr_false; __rn_alert__=false; alicnweb=homeIdttS%3D88678849673250246767309355100864982703%7Ctouch_tb_at%3D1523944293613%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010; _tmp_ck_0="4eBTqdpOdrQo3LzwieE841iHlK9A3tqc12mZKFYj%2BNNcBApEqMmUB48tz167764Zw1m%2FH2Wm6Fj4WU70K7T86yRcPM9WhZ8LLeltUXqeSOmsZIk2qDMShYtw5U5FnnepbMBmwlpL%2BrL2LvLCwMdAziWrAYOBAIqopFqIisJo3JJlsBf07LXXuMbhxUTb01YPIcEEV9kGjb1NA%2BZpLUGS3TXHjl29jM8l%2Btweg8bD2BlMgAItPiWGun%2FzTnaZh18waIozWb2H0CaqkR0fqg%2F3Uw9SLXHhMtdrRj4GAYqp0I1RnyloFuFiZJG0Q463W7vYGhAVNRGNEX4rAkYS825dYrA4XFc0%2FXGmN%2FjmF0olCKDzZQmC%2BBbcGkw38kqDS%2FYhSW2ENvAMKHJjy%2BGqhg6iyvvhkJER1noL3U2svp8uOvIKX0X6KOKrbQYixrcpvVRkIau4J1yoruDBeJ87NZLCJWsDjayILfpSJz0%2B0l6crcjTjdicwn%2F9fYpnB4xWopWdgaukPaoQwDDIjo7zI3PzASjurN0te%2Fus"; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914CDC1FCD1AA832C218F2206A38FC55CFB2; isg=BCIigIXzjKiE6pNOZe6nV884c66OdRg-5thUb2y71xVJP8O5VAH5nY2da3vDL54l',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def __fetch_content(self, url):
        # proxy = {
        #     'http': 'http://117.85.105.170:808',
        #     'https': 'https://117.85.105.170:808'
        # }
        # r = self.http.get(url, headers=self.headers, proxies=proxy)
        self.http = self.http or requests.session()
        r = self.http.get(url, headers=self.headers)
        return r.text

    # 过滤产品，可导入义乌购的返回 errcode: 0
    def __filter(self, content):
        content = re.findall("<span>预估生产周期</span>", content)
        if (len(content) > 0):
            return {
                'errcode': 101,
                'errmsg': '此产品为淘工厂类型，暂时无法导入义乌购产品体系'
            }
        return {
            'errcode': 0
        }

    # 基本信息 & SKU
    def __extract_base_and_sku(self, tree):
        script = tree.xpath('//script[contains(., "var iDetailConfig = ")]/text()')[0]

        base_str = re.findall("var iDetailConfig = ({[\s\S]*?});", script)[0].replace("'", '"')
        data = {k:v for k,v in json.loads(base_str).items() if k in ['offerid', 'unit', 'isRangePriceSku', 'isSKUOffer', 'beginAmount', 'refPrice', 'companySiteLink', 'isTp']}
        sku_str = re.findall("var iDetailData = ({[\s\S]*?});", script)[0]
        data.update(json.loads(sku_str.replace("'", '"')))

        return data

    # 阶梯价
    def __extract_price_range(self, tree):
        items = tree.xpath('//td[@data-range]')
        price_range = []
        for item in items:
            price_range_item = json.loads(item.attrib['data-range'])
            price_range.append([int(price_range_item['begin']), float(price_range_item['price'])])
        return price_range
    
    # 阶梯价的可订购数量
    def __extract_can_book_count_based_on_price_range(self, tree):
        text_elements = tree.xpath('//div[contains(@class, "obj-amount")]//span[@class="total"]/text()')
        if (len(text_elements) > 0):
            res = re.findall('\d+', text_elements[0])
            if (len(res) > 0):
                return res[0]
        return 100

    # 标题
    def __extract_title(self, tree):
        return tree.xpath('//h1[@class="d-title"]/text()')[0]

    # 图片
    def __extract_images(self, tree):
        image_elements = tree.xpath('//div[@id="dt-tab"]//li[contains(@class, "tab-trigger")]')
        return list(map(lambda img_element: json.loads(img_element.attrib['data-imgs'])['original'], image_elements))

    # 规格参数
    def __extract_attributes(self, tree):
        attribute_features = tree.xpath('//td[@class="de-feature"]/text()')
        attribute_values = tree.xpath('//td[@class="de-value"]/text()')
        return list(map(lambda feature, value: {'feature': feature, 'value': value}, attribute_features, attribute_values))

    # 详情描述
    def __extract_description(self, tree):
        description_request_url = tree.xpath('//div[@id="desc-lazyload-container"]')[0].attrib['data-tfs-url']
        content = self.__fetch_content(description_request_url)
        content = content[30:-3].replace('\\', '')
        content = re.sub('href[^>]+', 'href="#none"', content)
        return content

    def go(self, url):
        content = self.__fetch_content(url)

        # 过滤不符合义乌购加个体系的产品
        filterResult = self.__filter(content)
        if filterResult['errcode'] != 0:
            return filterResult

        tree = html.fromstring(content)

        product = self.__extract_base_and_sku(tree)
        if (product['isSKUOffer'] == 'false'):
            # 抓取 阶梯价
            price_range = self.__extract_price_range(tree)
            if (len(price_range) > 0):
                product['isRangePriceSku'] = 'true'
                canBookCount = self.__extract_can_book_count_based_on_price_range(tree)
                product['sku'] = {"priceRange": price_range, "skuProps": [], "canBookCount": str(canBookCount)}

        product['title'] = self.__extract_title(tree)
        product['images'] = self.__extract_images(tree)
        product['attributes'] = self.__extract_attributes(tree)
        product['description'] = self.__extract_description(tree)

        return product

# product = Product()
# PRODUCT_URL = 'https://detail.1688.com/offer/523969536038.html'
# content = product.go(PRODUCT_URL)
# print(content)