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
        'cookie': 'cna=NpBlE7lEqTcCATy/9ib8d8oo; __guid=224050958.1212828614124787200.1524539782982.7976; UM_distinctid=162f5a6f8a5153-0788a8359a0018-5d4e211f-1fa400-162f5a6f8a6716; _uab_collina=152453978644952962231172; h_keys="%u5c0f%u5f69%u65d7%u4e09%u89d2%u4e32%u65d7%u6279%u53d1%u6ce2%u70b9%u6761%u7eb9%u4e09%u89d2%u5f69%u65d7%u6302%u65d7%u751f%u65e5%u805a%u4f1a%u88c5%u9970%u5e03%u7f6e%u5c0f%u5f69%u65d7#%u5c0f%u5f69%u65d7%u4e09%u89d2%u4e32%u65d7%u6279%u53d1"; ad_prefer="2018/04/26 13:33:45"; JSESSIONID=9L78nA0l1-u7eZbuOl9TGMxYb0AC-WdczqqQ-l8m; cookie1=AimTjV1%2FgvQJja3uvjYAtL%2Bu4RydO3TZ3F7qzBugjxU%3D; cookie2=1fb7138c9d8df8588513d43c6d6f7107; cookie17=VAFaBJbrh60%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=a8d0e4e96cf719de5e026f541d81fa84; _tb_token_=737d51b3836b3; sg=640; csg=422c8b4d; lid=finish6; __cn_logon__=true; __cn_logon_id__=finish6; ali_apache_track=c_mid=b2b-7057694494368|c_lid=finish6|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=18V24XcyVSzethFogMEp4cuZDw1dLEpILkPqdy2ELXcogBSl%2FbuCDg%3D%3D; unb=70576944; tbsnid=p0feYpqaUs1V829zbO0RU6uOhEilaFVOpAtZy5Mx0rA6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ2mhbrAT3QQFAUSHnWaeMZ0Q1C7GpXrQ/NBS3kkF3T51S6Wkx8VfdJ/Hlcwqx30d1ic0DPfN2SJ24MaPOHmGf5QOOMAjt4pFsAK2Cg54a2bLjIgamhKA7mtLqYsdAqYYyD6rfe7OjlmXVSJtvlDmPx6OEOWPqVvjHX8yuBX+8GtEt/8iUt2f9E7odIiApMPPH+90w0pt6yokC0XBdcOgM26OIpAqUQYNLKtdNZw0Ej+UTWMwrJzd5GA"; login=kFeyVBJLQQI%3D; userID=ZgxwBH12u%2FOoAlszFbdFfutzD7OXE%2BxZM8f38ZEs%2FZk6sOlEpJKl9g%3D%3D; _nk_=d%2BbMzCQGGKs%3D; userIDNum=MY%2FP49oGkZ46sOlEpJKl9g%3D%3D; last_mid=b2b-7057694494368; __last_loginid__=finish6; _cn_slid_=HHlIUexzZZ; _csrf_token=1525228125080; _is_show_loginId_change_block_=b2b-7057694494368_false; _show_force_unbind_div_=b2b-7057694494368_false; _show_sys_unbind_div_=b2b-7057694494368_false; _show_user_unbind_div_=b2b-7057694494368_false; ali_ab=60.191.246.38.1524720797991.9; monitor_count=1; CNZZDATA1253659577=2009504684-1524535952-https%253A%252F%252Fs383161.1688.com%252F%7C1525226398; __rn_alert__=false; _tmp_ck_0="FuQMUPGBwdedHvygrQUi5Wq2jbkkIKRBRTFkefqmir%2FD%2B%2B4fP07wiuwgRVfbpoVqt3G93X%2BbMcRVGzlQT3giBdqkA17b58wDsGTYq949S%2Bk93CQFPK2XTWYz6g5F3LmtZLLvzTfmteCccKNrdSGb%2Fz2W9hMxXlwTWowQpi8%2Fr8Ogc7C1jiZwENIMijgNFEznk7ss%2BxL2YH9qrjcHgZVKjq6PjjkX0yXdy%2FCFF%2Bke7rmErlzV0wJet7U0s0lIYwJ%2FgrM94aTz9Hbrn5hmx6iLvZp9ZJxi2x8tgCKBiNxrqX96QEX7dk79F4kcrvCBOJVn%2BUcIu5IywD%2ByAxNmOBMrV2AbzSTZwac12Y0CVQkYSWMjbHAJU4XW626HAFJJONO2GNaPYRcMKH8R6fuxgo%2FuJEmzZs12xTudbzxD%2BJwpvV94JYM1pn760vm93pNp4AGesPl62RLuNsq%2FbZxyncEZCcTMCn9PcBJw%2BfRAX7w4YzqpNViaMvaV4VE%2BO7VHbQ3B9NSDdpRSFmnXE2LzhXz3LluJpjDMgcYR"; isg=BPLyIvS9_OR5EcDvTWV7oJXXQzjehciDysD5vrzLGqWQT5JJpBNGLfiNO-tzP261; _umdata=CBCF5C0AD3B0C709B3C31BDCA089FD3BFAE1B9837FE0C2A959228F7C533C4A7C88CABE60A2A104D9CD43AD3E795C914CC90681324F8DF4312C7C48A3629F759A; alicnweb=touch_tb_at%3D1525227868649%7ChomeIdttS%3D36336759672238656903336167765388000097%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3Dfinish6',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def __fetch_content(self, url):
        self.http = self.http or requests.session()
        # proxy = {
        #     'http': 'http://221.130.253.135:8090',
        # }
        # r = self.http.get(url, headers=self.headers, proxies=proxy)
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
        data = {k:v for k,v in json.loads(base_str).items() if k in ['offerid', 'unit', 'isRangePriceSku', 'isSKUOffer', 'beginAmount', 'refPrice', 'companySiteLink', 'isTp', 'mkcActivityId']}
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