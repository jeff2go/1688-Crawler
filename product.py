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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
        'Cookie':'cna=hPcbE2Mq+loCATy/9ib7PtGN; ali_apache_track=c_mid=b2b-7057694494368|c_lid=finish6|c_ms=1; UM_distinctid=16209d634120-05a3da9b384eb2-5d4e211f-1fa400-16209d634136b4; JSESSIONID=Xb9ZvCi-EqSZ0iRSbTBfJy3i58-dcEc2oQ-9jYi; cookie1=AimTjV1%2FgvQJja3uvjYAtL%2Bu4RydO3TZ3F7qzBugjxU%3D; cookie2=1f6e40ec26c641e86a69bef3fac7197c; cookie17=VAFaBJbrh60%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=f5af4d8e2ae57b44de90986eae17ddaa; _tb_token_=e7a704f7ee6b5; sg=640; csg=318cc3c5; __cn_logon__=true; __cn_logon_id__=finish6; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=6XRrzdY0G2C5fY0rzrx7RadHRsNRWF%2FMlos59r45MxoQoN5blcC8mQ%3D%3D; unb=70576944; tbsnid=2gHVh977ILtAlbrYcxgx7ACDFM9Ql40XFl4YhBqcSB06sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ2mhbrAT3QQFAUSHnWaeMZ0Q1C7GpXrQ/NBS3kkF3T51S6Wkx8VfdJ/Hlcwqx30d1ic0DPfN2SJ24MaPOHmGf5QOOMAjt4pFsAK2Cg54a2bLjIgamhKA7mtLqYsdAqYYyD6rfe7OjlmXVSJtvlDmPx6OEOWPqVvjHX8yuBX+8GtEt/8iUt2f9E7odIiApMPPH+90w0pt6yokO6FyM7FMKr0HU0uZAIkBkCm2YEFxF9S7Q=="; login=kFeyVBJLQQI%3D; userID=ZgxwBH12u%2FOoAlszFbdFfutzD7OXE%2BxZM8f38ZEs%2FZk6sOlEpJKl9g%3D%3D; last_mid=b2b-7057694494368; __last_loginid__=finish6; _cn_slid_=HHlIUexzZZ; _csrf_token=1522651447165; userIDNum="MY%2FP49oGkZ46sOlEpJKl9g%3D%3D"; _nk_="d%2BbMzCQGGKs%3D"; ali_ab=60.191.246.38.1522651432132.6; _is_show_loginId_change_block_=b2b-7057694494368_false; _show_force_unbind_div_=b2b-7057694494368_false; _show_sys_unbind_div_=b2b-7057694494368_false; _show_user_unbind_div_=b2b-7057694494368_false; __rn_alert__=false; JSESSIONID=18kzylxrmeml71ftumfca54sfw; _tmp_ck_0="LUGYM4%2BaK%2FUy8fMgsR1E1f%2Fz%2BjESQ3GIHVcpuI6fm8thhOzqLtGfvfDNG1UQIJxGV77TJ2ZxNrnVjfMveXEUVsJhR4uASlyiaVZwVpLFaeHeMIiPMjNJzBUgro5EUA8g0C5kcCTfR2sofnTawi4slUMCd4f6s%2Bi6yAv1nUViNOs%2BdkhubH2oTVOxxxY0qwVHXdV%2FiNMdKxiBc59etNbgomeh5vl5I8FvxLmniC2ywRQtPDToutb6PJN1OlJUcXtgTPQM6mDBgktAzticEj%2FJ3AfaTxxfe3oonmf3DcBVy%2FzPbHtUa3M26isKOJc8KY1WAPG%2BgJ3Ua8aLsPoy8ZjKY%2FFzccUUqDFd4XVP0UDjq55qJAMA%2B19jl4Y6Aq545Uhnk9QRr0%2Fb8PfdRPDG%2BVC3g3mbmTyUXczzT%2BYO6wp0%2BBitYSqtkkI69%2Bg5phejMNGuQUifn%2B65dv96l1WsCWBbXIYjTXfHRwiuFO7toVD6v3dquEd8oQlwOJ15CVtD%2BQMJIApH%2B7Rbcs%2FeOhWNufYfcg%3D%3D"; alicnweb=touch_tb_at%3D1522651227946%7Clastlogonid%3Dfinish6%7ChomeIdttS%3D54417069135775114529018015108642185984%7ChomeIdttSAction%3Dtrue; isg=BO7uKXQQOBgkUEwfCtu_lM-uP0S66Yx3JvR1Mhi3ffGs-45VgX8C-ZT1t2cXI6oB'
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