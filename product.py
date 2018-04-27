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
        'cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJfZXhwaXJlIjoxNTI0ODMyNDUzMDQwLCJfbWF4QWdlIjo4NjQwMDAwMH0=; webp=1; hng=CN%7Czh-CN%7CCNY; JSESSIONID=Q02Zz5n-w1LZM3cuILbaeONEk7-4n8lNqQ-lqik; cookie2=1cae888d7e2f3eb7d19b53d82d412258; t=432da7506670e12f3d241952bf1c6180; _tb_token_=3e85756be393; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C2F6671F98D860D1439EE53CA51AC43BF; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie17=WvX8NQn9COLZ; sg=%E5%8E%820a; csg=48763d37; lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_track=c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82|c_ms=2|c_mt=3; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; tbsnid=O0jl9z61hoEKv%2F2pQs60BrYI2N%2FNWB1vuLxkc0LRXko6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDNHCeDv14o/+LCoT6M9eIna5nTvYDOiuKU7HgB4cYksfXOHinVz/VkOdM/xbjJkvF/3dEXc60g53bjih00YaeDFa56L8rnsMa+B36fltyGDBEUo9QCuC6+fN5dm4vw0DRzYoptLsGxHHfwUof6eBaAgTppWzJKIjUYMKUYEZDPqjc0+fusazbrJrwUdqwXEiGC/AtkAR9GK4I="; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; _nk_=thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D; userIDNum=I1GdGME70WvmkdAiNY8Cqw%3D%3D; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; _csrf_token=1524798679409; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1524796127406%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582; _tmp_ck_0="zbfvknZrLpuKnfpwzzv2s2q5H7CcokUimmyC9rNn529TvvXrtwgyWBlHZKk9CHQDyEZgi1dI2BC4v9IqheBtx7U8C71fJ5Sw66Wmp%2FEOgWtQmsDSP7AfPLT8czp6hW0mUJm1%2BBb797Y8pTL%2BoyUxHa3c3tmtjadQsneLDaK6mX2Qn%2BJDMrPMXDDyo6U9RD2%2FCYaGpDAXzaVbv7RYajVfZgh7PMfbSSQyIsXdwiF40H9JvX%2BZJF16cm%2BrFNlmn9vqSnohTtXfXX4G1gNC%2BEEWCrmvTKzhWdd2rzDEyy8PO3OBliyISJgtjtbgGmhVzidmHvFkdWTwSKkrS%2BIvT5%2BpK7WyrblndbKUzWjJI1KL%2Bkklo6H3r%2BiWEdk%2F4FpI3Sgj0dBLQHeX%2BqXyofCNxCEEvF2iCPgIGUYMOW%2FGZYLFRcIMbe%2BxNXkQ%2FOsdEAvALEFbg1kqesqXlB72Z2L77ajl49LYYOkAbHFLg3Z%2BGBJDHZqhroS2p5J%2BeLxlOX5da5jZawTeFUA76g5llc6ARCgzw1N0H2h3qURJ"; isg=BDo6SYYaNFf0PLu2jWbPb3cwi2ZW7YB2DsB8t0Qz4U2YN9pxLHsO1QBtg8PrpzZd',
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