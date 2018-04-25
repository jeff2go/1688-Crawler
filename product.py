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
        'cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=z5pIE+qek0ECATy/9iaD8lki; ali_ab=60.191.246.38.1522642136552.6; hng=CN%7Czh-CN%7CCNY%7C156; h_keys="%u73a9%u5177#bag#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf%u5382"; ad_prefer="2018/04/11 11:37:06"; t=e3985612d6beba055cc8c87d9bcaf964; JSESSIONID=9L78dvjv1-EhXZI6Aa1BNzXj1Hg5-udogBqQ-adax; cookie2=1f1b1792091de5b7b3d7219f21e28faf; _tb_token_=fe1583e3e553f; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C917069E515B500E3FE6A8F86D90B4E4C; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie17=WvX8NQn9COLZ; sg=%E5%8E%820a; csg=2f342e4d; lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_track=c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82|c_ms=2|c_mt=3; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; tbsnid=4IIVPU3z66sylCQj2e5pzl3K6Gq29qyayGhE1IUb7Hk6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDNHCeDv14o/+LCoT6M9eIna5nTvYDOiuKU7HgB4cYksfXOHinVz/VkOdM/xbjJkvF/3dEXc60g53bjih00YaeDFa56L8rnsMa+B36fltyGDBEUo9QCuC6+fN5dm4vw0DRzYoptLsGxHHfwUof6eBaAgTppWzJKIjUYMKUYEZDPqjc0+fusazbrJm8+C4wvPOKqVLqgK1lVuWg="; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; _csrf_token=1524642411791; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; alicnweb=homeIdttS%3D88678849673250246767309355100864982703%7Ctouch_tb_at%3D1524642254426%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582; userIDNum="I1GdGME70WvmkdAiNY8Cqw%3D%3D"; _nk_="thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D"; _tmp_ck_0="uxKfwS7HQDR1%2Far1lH2QQ3DsjsliNwqzFVe06yZw5RFv7WWxZCEg8BMGILsVorOd4MP7w9qn23ItxF%2FsQL9vhfVtOjV1Txg6A5NiLpsjRfSQ45KXBUeN%2Ba%2FlPtpEAHbqGaZEkzJMeEMuzlhk2Inu0IHyq9Bw2VnM%2FErNhfIGZzKBi%2BYiGmG61buRGXVJ3gezQcobZX5Wz9HNytoxKiTxoiwoit%2BrZjE0cgWo63Ppe3VR6k9NItJCcdifWH7ICeE8ErP6lgLPg0EOjjL9ZTBAUjsdpZdG8ama2nVx%2B34Ip3xfWNsOF4sL4ZiZDqQHKk6z1jaPwl8hfGsl%2BbT%2FLWAYJR674y1iYK3OmpUrd1Z1tnV%2Bb0C1ItiNBBhWWKuvwdIfRM2qIGsY0zLH2acdCiLBn3md71RggIm%2BlnvIxb9IbWfm9kuzj5mQX%2BBLsFB41Zf10eVs2VeoiPJGU8S4V%2FGWLmFWGLU1ClKTtt7rWppL9Xm3wIhCrqH9dkbAbtMyhIfBUBtfkI1uXwNSPC98p0koBM0Nldx3Nf7D"; isg=BNTUlwc4cmfY3OUk52DJHS3epBRMK8akBP7ChW61Z9_gWXSjlj3Ip4r7XVFBoTBv',
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