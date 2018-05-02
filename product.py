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
        'cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; hng=CN%7Czh-CN%7CCNY%7C156; JSESSIONID=5e9Zopf-18eZuOuJGUftGNmQg4-8yTxqqQ-pUV; cookie2=149bc39dfa15e6938caf2e94e7a5a5e1; t=432da7506670e12f3d241952bf1c6180; _tb_token_=ee373d7d3887f; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1525227580212%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie17=WvX8NQn9COLZ; sg=%E5%8E%820a; csg=f33f43ec; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; _nk_=thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D; userIDNum=I1GdGME70WvmkdAiNY8Cqw%3D%3D; _csrf_token=1525227603441; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; ctoken=QVO5JqMxPXts5ULtYlfFnaga; _sync_time_=1525227617467; cn_tmp=Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDNtBBCepO71yWAFaah9Qccd21MkFTXyGIhSqt+AkpPG8QDkGQV2T9kErcppNf+bqwVLI0QCNLBQpFB1DO4RaQv+w==; cn_m_s=D6j4EflXCl5bq5cskw6AxRWLu9W0l7/sqBKCCPTh39j1byNOqQsQCSJLzol0mvF0; ali_apache_track="c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82"; tbsnid=qc/p6A90PYpzfhqbSCUKNMwBvj6COLpBKP+KLUitS+06sOlEpJKl9g==; ali-ss=eyJtZW1iZXJJZCI6Inlpd3V5aWhhbiIsInVzZXJJZCI6Ijk1MjQzNDc1MCIsImxvZ2luSWQiOiLkuIDmtrXliLbnur/ljoIiLCJzaWQiOiIxNDliYzM5ZGZhMTVlNjkzOGNhZjJlOTRlN2E1YTVlMSIsImVjb2RlIjoiIiwibG9naW5TdGF0dXNSZXRNc2ciOm51bGwsImxvZ2luTWVzc2FnZUVycm9yIjpudWxsLCJsb2dpbkVycm9yVXNlck5hbWUiOm51bGwsImNoZWNrY29kZSI6bnVsbCwic2VjcmV0IjoiVEM5aWxOVEpGRGNBRllmQ1FrV1l3QnUwIiwiX2V4cGlyZSI6MTUyNTMxNDAxNzcyNywiX21heEFnZSI6ODY0MDAwMDB9; webp=1; _m_h5_tk=70b125e2d19a4e735f32a64a22f50a07_1525229689623; _m_h5_tk_enc=db1c3a888ddea51ca0bb04d9d6ad37bb; _tmp_ck_0="LUGYM4%2BaK%2FUXEUVPC4dDZ4IxjRb5JlDuyVv1oPRxlTgCfqrzeLgFS1xgk%2BuznVfWrNWi28xGeGpFqaj%2BmSwGk3gSC1nuy75naTOGvgqBbi9jVXuvK%2FCy8O82tNcClfhYhZU6vAxfAjvwO8cX9RKltJIftOt%2B7Ay4TFBxotKxCnj%2F9hFy7abhwk2wK0u%2F432E30Su7i6bcdTAKW5U61%2B6vTcJ0fDcRUwAQ40zgffaTz%2F1wtmI5kwuBvFb7XiVqzOb%2BsTltRSYd4ulIruws86GLULaFhMEs0dOIL3SdBflMSXhv8ruzxPmHrDTA6cAGaFxSTsqabDCGERJQ1pvPaLMnmJb%2F2HGWSY%2B5%2FUZIj6AiFw3EASVJvx9N%2F6cA5GuF%2BpAxhep3j6PmbtCkGSxt6JjQfvFdTnSzlV4b5Mh%2FdvqibHFmXhrkpVFxBRiRGeo52q6P5JaTRasN0kINKmge9X44pxVomGxu1iSQPoxPMIKYJi2iDiFxhErvMXnE08PMpZw%2FW%2BfHOh4EHCD72zJXonTWYDZ5xfrQ7rc"; isg=BMLCrkuSLHSIcjMuxY7Hd69YE84ulfgeRjj0Dwzb6DXgX2LZ9CMWvUi1C1sjDz5F; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C16249D7C076616EAAE7C2424C638FEE2',
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