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
        'Cookie':'_uab_collina=151151417932957227926525; ali_ab=60.191.246.38.1511514156593.1; cna=WURTEsHQWHACATy/9iaDsnE3; h_keys="%u65b0%u95fb%u7eb8#%u7537%u5f0f%u536b%u8863#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf%u5382#%u4e49%u4e4c%u4e00%u6db5%u5236%u7ebf#%u4e00%u6db5%u5236%u7ebf#%u5154%u5b50%u840c%u732b%u4fbf%u643a%u5f0f%u591c%u706f#%u5361%u901a%u53ee%u5f53%u521b%u610f%u793c%u7269USB#%u4e0a%u6d77#%u7537%u5f0f%u5939%u514b#%u73a9%u5177"; last_mid=yiwuyihan; __last_loginid__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; _cn_slid_=IUcoR%2BQ80F; UM_distinctid=161f9e7f46641f-055de36abea91-32667b04-1fa400-161f9e7f46794; JSESSIONID=E37ZHYg-bBIZdMtp6C5ETNnKK9-3UvYhmQ-Zbx; alicnweb=touch_tb_at%3D1521424763440%7Clastlogonid%3D%25E4%25B8%2580%25E6%25B6%25B5%25E5%2588%25B6%25E7%25BA%25BF%25E5%258E%2582%7ChomeIdttS%3D62194053257600413129641851863569534442%7ChomeIdttSAction%3Dtrue%7Cshow_inter_tips%3Dfalse; ad_prefer="2018/03/19 10:02:49"; cookie1=Vqssh7w6jqtme8hBodvNkV7r6%2BugZKoUkpBcB87ej%2Bg%3D; cookie2=192bea66a2d513a43ba14c05969c9cbc; cookie17=WvX8NQn9COLZ; hng=CN%7Czh-CN%7CCNY%7C156; t=e3985612d6beba055cc8c87d9bcaf964; _tb_token_=c3617c7e35be8; sg=%E5%8E%820a; csg=411b1c30; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=cysOIPISIfLblw1%2BC8W%2FOtAmd2wHu0Ta0KrmK37pobFTG4BC5yy9jw%3D%3D; unb=952434750; login=kFeyVBJLQQI%3D; userID=lpWtF%2BwMFeE%2BfEDFLV1gd%2BrSUb5Kar7167hcsMQwkAY6sOlEpJKl9g%3D%3D; _csrf_token=1521424976191; _is_show_loginId_change_block_=yiwuyihan_false; _show_force_unbind_div_=yiwuyihan_false; _show_sys_unbind_div_=yiwuyihan_false; _show_user_unbind_div_=yiwuyihan_false; __rn_alert__=false; CNZZDATA1253659577=1338067901-1520570405-%7C1521420235; _umdata=65F7F3A2F63DF02042CD40C8CB341A75B45FEEB2FA6EFB040032BDD8266423B49B6F37ADA64137D5CD43AD3E795C914C4F8F2E1E63A8B487C0AC7414455611F0; ctoken=JX9Th3K72wUhr5l73VLGnaga; _sync_time_=1521425005326; cn_tmp=Z28mC+GqtZ3r7szDk/CxK5OyKoa7brDN9e/z57U6QUeFY5GMFYx0hBxBpKGlR1TDe19WauSqQpp8aXKcWoh2aZKOqteJqIVNc8HbVSBMDuv/zqOsCjbPdA==; cn_m_s=8jyNbezD+roqDZbSy0F/scEiqnffiULEuV30eCigcKZww68qL7IbvFIQRkI1CXDm; ali_apache_track="c_mid=yiwuyihan|c_lid=%E4%B8%80%E6%B6%B5%E5%88%B6%E7%BA%BF%E5%8E%82"; tbsnid=mRqVqFtzL3O3Hsl5CfR3mN7WIsEMFY9iTuzeKQGhMmg6sOlEpJKl9g==; ali-ss=eyJtZW1iZXJJZCI6Inlpd3V5aWhhbiIsInVzZXJJZCI6Ijk1MjQzNDc1MCIsImxvZ2luSWQiOiLkuIDmtrXliLbnur/ljoIiLCJzaWQiOiIxOTJiZWE2NmEyZDUxM2E0M2JhMTRjMDU5NjljOWNiYyIsImVjb2RlIjoiIiwibG9naW5TdGF0dXNSZXRNc2ciOm51bGwsImxvZ2luTWVzc2FnZUVycm9yIjpudWxsLCJsb2dpbkVycm9yVXNlck5hbWUiOm51bGwsImNoZWNrY29kZSI6bnVsbCwic2VjcmV0IjoiX2lESXhFcUhpQUpRUE04NG03cjY1OC1aIiwiX2V4cGlyZSI6MTUyMTUxMTQwNTQzNywiX21heEFnZSI6ODY0MDAwMDB9; _m_h5_tk=5fdeec1e3a0256993d428242ecb1cb1b_1521427256495; _m_h5_tk_enc=8d875dee8a21e829b51eca4e134ad46f; webp=1; userIDNum="I1GdGME70WvmkdAiNY8Cqw%3D%3D"; _nk_="thwcrK%2Bgi%2F%2BV8dneKHo%2BJQ%3D%3D"; _tmp_ck_0="Us6kfQ%2FxEOOMEb6zd8Wcsxrvecs01gHUzismq1NaKI8knmoZpRyD2QdHw6OFEmw7tRddgPW5r6M5FpwWHsIOUDVcHBuNW1a8ZHEjlXF8fMplY1EfC%2BvIigrQaBYosA4ACdWl8bFcg2TUANLPFmiamAbkU5k3v8ypHH14X%2BoJADdch0DyLMfFjybF%2Fl2sCb2G1HM%2FP5hOftWNaDf0yFHmYhYjWlthT6kZIjGpfY%2Fbz77lqieCRJkM2oq%2B5ZTT30sXqwQFo1Q4nvW3Q%2FMl3Umjw64LZwUISRzG%2BV05br3tQ4f9BQXg6E9PoMoYg%2BKyrEmcUrMFw2P0kC2joPqnLTtvCoTgrQCsIIDVH3rLgjE4QlJ2wGiyhgFaxK19fYFzEOQhyYskrpBAt1Y7ADJPuuSoXnrycQZ4mQIwYTsC%2Bpfxen9Q3rYGTPCKwntsxazmZzLqOCiZmzMDbLpepIosmCVJthoD%2F1ppV2cHawyp%2BSpMVK6XGM4QG0m8Rsct16LXQTh%2FBe5qy8%2B1D66xzmSIyIaGDE8jF7K0ZIzT1AfomZWsS28%3D"; isg=BP39mLDke7Ox7Nwf1jdwVkwxDF_9nA9fqIFFwr9CPtSD9h0oh-pBvMuEpCqw9kmk'
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
# PRODUCT_URL = 'https://detail.1688.com/offer/39685445050.html?smToken=c282e6e9a31649d1946a89ad39edac3e&smSign=t1F6Kae2G2DAAaxV84z65w%3D%3D'
# content = product.go(PRODUCT_URL)
# print(content)