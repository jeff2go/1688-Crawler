"""
抓取go2产品数据
http://www.go2.cn/
"""

import re
import json

from lxml import html
from app.spiders.spider import get_html


class Go2Product:

    # 标题
    def __extract_title(self, tree):
        return tree.xpath('//div[@class="product-details"]//h6/text()')[0]

    # 图片
    def __extract_images(self, tree):
        image_elements = tree.xpath('//img[@big]/@big')
        return image_elements

    # 详情描述
    def __extract_description(self, content):
        # <img class="lazy" src="/images/loading.png" data-url="http://go2.i.ximgs.net/4/493394/20190410/20190410548282001_750.jpg" />
        # <img src="http://img1.yiwugou.com/i004/2019/06/13/85/9e66eddbfef02821a48d9f4ca5bae293.jpg@800w_1o" alt="" />
        res = re.findall("<!--商品详情-->([\\s\\S]+)<!--拿货咨询-->", content)
        return res[0].replace('class="lazy"', '').replace('src="/images/loading.png"', '').replace('data-url', 'src')

    # 提取价格
    def __extract_price(self, tree):
        res = tree.xpath('//meta[@property="og:product:price"]/@content')[0]
        return res

    def __extract_sku_props(self, tree):
        res1 = tree.xpath('//div[@class="properties-box"]//li[@title]/@title')
        res2 = tree.xpath('//div[@class="properties-box-c"]//li[@title]/@title')
        list1 = list(map(lambda item: dict(name=item), res1))
        list2 = list(map(lambda item: dict(name=item), res2))
        return [dict(prop='尺码', value=list1), dict(prop='颜色', value=list2)]

    def go(self, url):
        content = get_html(url)

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
