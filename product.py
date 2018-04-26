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
        'cookie': 'cna=z5pIE+qek0ECATy/9iaD8lki; ali_ab=60.191.246.38.1522642136552.6; hng=CN%7Czh-CN%7CCNY%7C156; h_keys="%u73a9%u5177#bag#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf%u5382"; lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; JSESSIONID=9L78wBil1-f1LZKfIhcHtv0vWGm4-8JvvIqQ-3Au31; t=e3985612d6beba055cc8c87d9bcaf964; cookie2=1cdcca41ca8072bf2c0ee9a453507cda; _tb_token_=eb7df8dee7e7f; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie17=WvX8NQn9COLZ; sg=%E5%8E%820a; csg=ca5184ec; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; _nk_=thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D; userIDNum=I1GdGME70WvmkdAiNY8Cqw%3D%3D; _csrf_token=1524724826187; ctoken=zQVVTDcsBBsZL4Xp01rPcoco; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; alicnweb=homeIdttS%3D88678849673250246767309355100864982703%7Ctouch_tb_at%3D1524724814621%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582%7Cshow_inter_tips%3Dfalse; ad_prefer="2018/04/26 14:40:37"; _tmp_ck_0="LUGYM4%2BaK%2FUxsqQv66Q7M%2FfaKh%2B2PrsMLhZGGpO0iDnMGHK06PtZG6boY1k9MwdFxqQLOUrzFpS8NX1%2FAuCNbMxXUM%2F0qpwRATtI4%2Fb4mv8bmRFVzj%2FBo3MITJSPEp6cWyzjtN%2BwhHEBQNWBioJUTZm9viHl8Jb6Tv2Tka0Fg6t5Pq1a%2FLgcHxvLA0NNUbVTNPLLYpU6nWCra1ot0Zzguc9oBbJTw56v8OV4SiyThA51yUGawKcdXU28lU5CPTQp3PbR3dCe6IZS93cMv82SHzHmNbUg3FkYRw8ABQav85krv9ynmMaOgtUBqnxgqS1CcmqeVCDImEbQGnYQTN76DCNBCrribPOoRotOUk6u2PDggtwtA81lpyCozfopRGBc01g86YNSmEDHolByQ%2Fo50MFBKM25%2FWXifsg8Wj2SKhS5sVerWMFq4eIcwO5CNTGSZCm8HpvrZokhm8Fr1hSxuQjGqZU56RcmMJnDDB5snmdIeUcXf%2BRMjYroOmsPVwI2xWSkFsr53yQgGR6LviWILNP0ZXyMrRzM"; _sync_time_=1524724849968; cn_tmp=Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDN2qeNR+pPYI/MjhUAySl5n3f41uTF+gIz1BHbUn1l7cxNcO4IjZYanVFaB3FfNA223oZVTkdfMWkwtzl61zjgag==; cn_m_s=V26OO6JZqvVHuX/5v4XvBotJHEUq1VWNmEIrZLG/7SnwJwpf+YxFem6bpBr4zTmx; ali_apache_track="c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82"; tbsnid=wgTOJPS1+SjKh+ECGT4mX2hxu1v5JaAbLC9a+k2UXqI6sOlEpJKl9g==; ali-ss=eyJtZW1iZXJJZCI6Inlpd3V5aWhhbiIsInVzZXJJZCI6Ijk1MjQzNDc1MCIsImxvZ2luSWQiOiLkuIDmtrXliLbnur/ljoIiLCJzaWQiOiIxY2RjY2E0MWNhODA3MmJmMmMwZWU5YTQ1MzUwN2NkYSIsImVjb2RlIjoiIiwibG9naW5TdGF0dXNSZXRNc2ciOm51bGwsImxvZ2luTWVzc2FnZUVycm9yIjpudWxsLCJsb2dpbkVycm9yVXNlck5hbWUiOm51bGwsImNoZWNrY29kZSI6bnVsbCwic2VjcmV0IjoiOGhvZHMwRHZXeVBmMjk2V2s2eTBoNzF5IiwiX2V4cGlyZSI6MTUyNDgxMTI0OTk3MSwiX21heEFnZSI6ODY0MDAwMDB9; webp=1; _m_h5_tk=e9b7bc14f5861637e39fb2b8fe7337b3_1524727281307; _m_h5_tk_enc=3b2ee0bcad7a0d7b9eeecbed01e0fe7b; isg=BEVFtMb2syXHE5T3Tp-o_kQZVId1BMcn9Enr4EeqAXyL3mVQD1IJZNOc7AQonhFM',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def __fetch_content(self, url):
        self.http = self.http or requests.session()
        proxy = {
            'http': 'http://221.130.253.135:8090',
        }
        r = self.http.get(url, headers=self.headers, proxies=proxy)
        # r = self.http.get(url, headers=self.headers)
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

product = Product()
PRODUCT_URL = 'https://detail.1688.com/offer/523969536038.html'
content = product.go(PRODUCT_URL)
print(content)