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
        'cookie': '_uab_collina=151151417932957227926525; CNZZDATA1253659577=1338067901-1520570405-%7C1521445346; cna=JrVoE8ZJpnICAX1wLFvNRBbJ; ali_ab=125.112.44.91.1524746036086.3; hng=CN%7Czh-CN%7CCNY%7C156; JSESSIONID=5e9Zopf-18eZuOuJGUftGNmQg4-8yTxqqQ-pUV; cookie2=149bc39dfa15e6938caf2e94e7a5a5e1; t=432da7506670e12f3d241952bf1c6180; _tb_token_=ee373d7d3887f; __cn_logon__=true; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; ctoken=QVO5JqMxPXts5ULtYlfFnaga; cn_m_s=D6j4EflXCl5bq5cskw6AxRWLu9W0l7/sqBKCCPTh39j1byNOqQsQCSJLzol0mvF0; ali-ss=eyJtZW1iZXJJZCI6Inlpd3V5aWhhbiIsInVzZXJJZCI6Ijk1MjQzNDc1MCIsImxvZ2luSWQiOiLkuIDmtrXliLbnur/ljoIiLCJzaWQiOiIxNDliYzM5ZGZhMTVlNjkzOGNhZjJlOTRlN2E1YTVlMSIsImVjb2RlIjoiIiwibG9naW5TdGF0dXNSZXRNc2ciOm51bGwsImxvZ2luTWVzc2FnZUVycm9yIjpudWxsLCJsb2dpbkVycm9yVXNlck5hbWUiOm51bGwsImNoZWNrY29kZSI6bnVsbCwic2VjcmV0IjoiVEM5aWxOVEpGRGNBRllmQ1FrV1l3QnUwIiwiX2V4cGlyZSI6MTUyNTMxNDAxNzcyNywiX21heEFnZSI6ODY0MDAwMDB9; webp=1; _m_h5_tk=70b125e2d19a4e735f32a64a22f50a07_1525229689623; _m_h5_tk_enc=db1c3a888ddea51ca0bb04d9d6ad37bb; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C16249D7C076616EAAE7C2424C638FEE2; ad_prefer="2018/05/02 14:48:55"; h_keys="%u73a9%u5177"; cookie1=BYk5E01IMRgOv9lwa6Q%2F9WEQbcc4WsUiX%2BpLMDqayxo%3D; cookie17=UNcNPbcuK3gM; sg=011; csg=42d051cf; lid=%E4%B9%89%E4%B9%8C2010; __cn_logon_id__=%E4%B9%89%E4%B9%8C2010; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=3; unb=375685501; tbsnid=qc%2Fp6A90PYpzfhqbSCUKNMwBvj6COLpBKP%2BKLUitS%2B06sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ1zvhIUrY34IWqE1NUiJUbOSnnKfF/EKmUT6JpKURQFRzQyDQRqKjUW+wz6NLz10jFwnSWAw3EYMNHFSYlrqLYigWhihClZrhxnb7+MjupilRdjbwJe08tPFmkyku3yyUEETmUqccb691HchTC+m3ibDFZw+Bj+pm7cWivmjpORmkVZ3FXGXcU8IhUhmvEWZkVU79tFP5M5QRFtQ8zzVZC83KTGdEML8E+EaccZZFWmOILZHmIbATJN"; login=kFeyVBJLQQI%3D; userID=4xajfL3DQrHncUpnQZX0TYc0vWcisnqH2H6AxmPH6ic6sOlEpJKl9g%3D%3D; _nk_=Y3E2Stm9IjQ6sOlEpJKl9g%3D%3D; userIDNum=jH7Y8ZWD7p1TAhztWl1ziA%3D%3D; last_mid=b2b-375685501ncisr; __last_loginid__=%E4%B9%89%E4%B9%8C2010; _cn_slid_=17PB6qDL%2Bc; _csrf_token=1525243749827; _is_show_loginId_change_block_=b2b-375685501ncisr_false; _show_force_unbind_div_=b2b-375685501ncisr_false; _show_sys_unbind_div_=b2b-375685501ncisr_false; _show_user_unbind_div_=b2b-375685501ncisr_false; __rn_alert__=false; alicnweb=homeIdttS%3D78994739529372997155561416241427710433%7Ctouch_tb_at%3D1525243732696%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010; _tmp_ck_0="zbfvknZrLpt0%2BbV28tu%2FTuBJUtQWNntNKrDMnqg1FVe0XQVX6Sr5akWfZsPpCBzvNlif6Eg64iPKgMLP5xGfBjD%2FLyDwJjV3U%2B%2BcBIEwgWBbvfLuzJ4BI0B7Cy%2FEhW7o8uqlcHxOoXvOwIJ7IRcDjrZEn1p8FxzcnLZnjhPaJY%2Bf6BN2mHGNRlfQTRbETSoUZcUKPf%2Bm7YcEL8VblHc%2Bqa3cLCqP2k38qYsxoq3DTj84hv73Iz%2FJJ2UPACBZJJ%2F8GrcnWIPkL28YJyyQe4MFMR4kWd5RPQzraaoWRFyX0T6Btvgmvp5tHhWrhcUJ%2BPhdxONO17zW0hCCyLGgoW2VPzt%2FuamzM4mHgTf9DklKppRXDcWFAxFwYtNMB6l24prawu5WCo02SOn1s4Zn1bgjDMRT4F8JGFN1l1Gunz1mdPYO23EsGdT2h6bzpQaDCjG67GrtmFUNxBSptvDQzTXV6IrDm4sm%2F50A4%2F%2F6itYbM%2BVK7VFi3VxtujuWedi6cYcbEpZVW0rFnUWUBL4NcXOdlJkjZqZggc4k41ZhZTV9iA3QolssZ53YGQ%3D%3D"; isg=BH19Hihw-3V0jFyfVrfw1syxjN99HI_fheFbnj_CvlQBdp2oB2rBPEsEJKowdskk',
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
