"""
抓取go2产品数据
http://www.go2.cn/
"""

import re
import json

from lxml import html
from app.spiders.spider import get_html

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.2025120374.1560389345; _gid=GA1.2.1069169606.1569546754; Hm_lvt_d632121f6fa73f8db725c6dfcb8cf041=1567673313,1568797742,1569546754; Hm_lvt_80e798ed6dd8a1596a3a77ceb1ee88ae=1567673313,1568797742,1569546754; Hm_lvt_c474c6da0ac1239117a1f6abbbc48d32=1567673313,1568797742,1569546754; Hm_lvt_fa5da7a6f80ec2247f5c8de677f76041=1567673313,1568797742,1569546754; aliyungf_tc=AQAAAOwrTW7uOgIAJva/PA5oubT7rwny; PHPSESSID=u37skuht0sinh0djqj8nfeh7a6; __51cke__=; _alicdn_sec__=5d8d743eb4daa758c25c0425617df7c737ed7e00; go2_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%221a8c07d37c550a999a2870425f2fed4a%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2260.191.246.38%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_14_6%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F77.0.3865.90+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1569551481%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D6944b42bb17651596225a0ee44272894; __tins__4621821=%7B%22sid%22%3A%201569551422302%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201569553394540%7D; __51laig__=16; Hm_lvt_e838809e282b973abda9a75260600a0f=1569547675,1569551489,1569551507,1569551596; Hm_lpvt_e838809e282b973abda9a75260600a0f=1569551596; Hm_lpvt_d632121f6fa73f8db725c6dfcb8cf041=1569551596; Hm_lvt_f6cad666dd7696b74db974d3d5aab4f3=1569547675,1569551494,1569551504,1569551596; Hm_lpvt_f6cad666dd7696b74db974d3d5aab4f3=1569551596; Hm_lvt_9d0abdf1f48a92c8ad9b5078b24ed864=1569547675,1569551489,1569551504,1569551596; Hm_lpvt_9d0abdf1f48a92c8ad9b5078b24ed864=1569551596; Hm_lpvt_80e798ed6dd8a1596a3a77ceb1ee88ae=1569551596; Hm_lvt_966bafbde46979d2c64b80725ec1fbb3=1569547677,1569551489,1569551504,1569551596; Hm_lpvt_966bafbde46979d2c64b80725ec1fbb3=1569551596; Hm_lvt_dd6c5448d9747b21983d4d4db20831a0=1569547676,1569551489,1569551504,1569551596; Hm_lpvt_dd6c5448d9747b21983d4d4db20831a0=1569551596; Hm_lpvt_c474c6da0ac1239117a1f6abbbc48d32=1569551596; Hm_lvt_d2ede7bff5cdac94f9cc9d8ce9b27277=1569547676,1569551490,1569551504,1569551597; Hm_lpvt_d2ede7bff5cdac94f9cc9d8ce9b27277=1569551597; Hm_lvt_62b3cf2b6595100cabc31cda24169e39=1569547676,1569551490,1569551505,1569551597; Hm_lpvt_62b3cf2b6595100cabc31cda24169e39=1569551597; Hm_lvt_b943c4774942276062c9b2dfcff5f0b1=1569547677,1569551490,1569551504,1569551597; Hm_lpvt_b943c4774942276062c9b2dfcff5f0b1=1569551597; Hm_lpvt_fa5da7a6f80ec2247f5c8de677f76041=1569551597; Hm_lvt_726778d4d8b40b8c83bc2a1367cfd7d6=1569547676,1569551489,1569551504,1569551597; Hm_lpvt_726778d4d8b40b8c83bc2a1367cfd7d6=1569551597',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

class Go2Product:

    # 标题
    def __extract_title(self, tree):
        titleElements = tree.xpath('//div[@class="product-details"]//h6/text()')
        if len(titleElements) > 0:
            return titleElements[0]
        goodsNumElements = tree.xpath('//div[@class="product-details"]//span[@class="ft-bold"]/text()')
        if len(goodsNumElements) > 0:
            return '商品货号：' + goodsNumElements[0]
        return '未获取标题'

    # 图片
    def __extract_images(self, tree):
        image_elements = tree.xpath('//img[@big]/@big')
        return image_elements

    # 详情描述
    def __extract_description(self, content):
        # <img class="lazy" src="/images/loading.png" data-url="http://go2.i.ximgs.net/4/493394/20190410/20190410548282001_750.jpg" />
        # <img src="http://img1.yiwugou.com/i004/2019/06/13/85/9e66eddbfef02821a48d9f4ca5bae293.jpg@800w_1o" alt="" />
        res = re.findall("<!--商品详情-->([\\s\\S]+)<!--拿货咨询-->", content)
        return '<meta name="referrer" content="no-referrer">' + res[0].replace('class="lazy"', '').replace('src="/images/loading.png"', '').replace('data-url', 'src')

    # 提取价格
    def __extract_price(self, tree):
        priceElements = tree.xpath('//meta[@property="og:product:price"]/@content')
        if len(priceElements):
            return priceElements[0]
        return '0.00'

    def __extract_sku_props(self, tree):
        res1 = tree.xpath('//div[@class="properties-box"]//li[@title]/@title')
        res2 = tree.xpath('//div[@class="properties-box-c"]//li[@title]/@title')
        list1 = list(map(lambda item: dict(name=item), res1))
        list2 = list(map(lambda item: dict(name=item), res2))
        return [dict(prop='尺码', value=list1), dict(prop='颜色', value=list2)]

    def go(self, url):
        content = get_html(url, headers)

        print('content', content)

        tree = html.fromstring(content)

        product = dict(isRangePriceSku='true', isSKUOffer='false', unit='双', attributes=[])

        product['title'] = self.__extract_title(tree)
        product['images'] = self.__extract_images(tree)
        product['description'] = self.__extract_description(content)
        product['sku'] = dict(canBookCount='9999')
        price = self.__extract_price(tree)
        product['sku']['priceRange'] = [[1, float(price)]]
        product['sku']['skuProps'] = self.__extract_sku_props(tree)

        return product
