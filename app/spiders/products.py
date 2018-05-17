"""
抓取1688产品列表数据
"""

import re

from lxml import html

from app.spiders.spider import get_html


class Products:
    # 分页数据
    def __extract_pagination(self, tree):
        pagination_html = tree.xpath('//div[contains(@class, "wp-paging-unit")]')
        if len(pagination_html) > 0:
            pagination_html = pagination_html[0]
        else:
            return {
                'total': len(self.__extract_product_info(tree)),
                'current_page': 1,
                'last_page': 1,
                'per_page': 20,
                'data': []
            }
        if 'new-pagination' in pagination_html.get('class'):
            current_page = int(pagination_html.xpath('.//li[@class="pagination"]/a[@class="current"]/text()')[0])
            last_page = int(pagination_html.xpath('.//em[@class="page-count"]/text()')[0])
            per_page = 16
            total = 16 * last_page
            return {
                'total': total,
                'current_page': current_page,
                'last_page': last_page,
                'per_page': per_page,
                'notice': '此分页产品总数total不一定准确',
                'data': []
            }
        else:
            total = int(pagination_html.xpath('.//em[@class="offer-count"]/text()')[0])
            current_page = int(pagination_html.xpath('.//li[@class="pagination"]/a[@class="current"]/text()')[0])
            last_page = int(pagination_html.xpath('.//em[@class="page-count"]/text()')[0])
        per_page = 20
        return {
            'total': total,
            'current_page': current_page,
            'last_page': last_page,
            'per_page': per_page,
            'data': []
        }

    # 产品数据
    def __extract_product_info(self, tree):
        product_items = tree.xpath(
            '//div[contains(@class, "wp-offerlist-windows")]//ul[contains(@class, "offer-list-row")]/li[@*]')
        products = []
        for product_item in product_items:
            price_element = product_item.xpath('.//div[contains(@class, "price")]//em/text()')
            if price_element and '价格' not in price_element[0]:
                base_element = product_item.xpath('.//a[@class="title-link"]')[0]
                url = base_element.get('href')
                products.append({
                    'id': int(re.findall('offer/(\d+)', url)[0]),
                    'title': base_element.get('title'),
                    'price': float(price_element[0]),
                    'url': url
                })

        return products

    def __extract_shop_info(self, tree):
        shop_url_element = tree.xpath('//div[contains(@class, "base-info")]//a')[0]
        shop_url = shop_url_element.get('href')
        id = re.findall('https?://(.+)\.1688', shop_url)[0]
        title_element = shop_url_element.xpath('//div[@class="company-name"]')[0]
        title = title_element.get('title')

        # 联系人
        contactor = ''
        contactor_element = tree.xpath('//a[@class="membername"]/text()')
        if len(contactor_element) > 0:
            contactor = contactor_element[0].strip()

        # 电话
        telephone = ''
        telephone_element = tree.xpath('//dl/dt[starts-with(text(), "电")]/following-sibling::dd/text()')
        if len(telephone_element) > 0:
            telephone = telephone_element[0].strip()

        # 移动电话
        mobile = ''
        mobile_element = tree.xpath('//dl/dt[contains(text(), "移动电话")]/following-sibling::dd/text()')
        if len(mobile_element) > 0:
            mobile = mobile_element[0].strip()

        # 地址
        address = self.__extract_shop_address(tree)

        return {
            'id': id,
            'title': title,
            'contactor': contactor,
            'telephone': telephone,
            'mobile': mobile,
            'address': address
        }

    def __extract_shop_address(self, tree):
        address_array = tree.xpath('//span[@class="address_title"]/text()')
        if len(address_array) == 0:
            return {
                'country': '',
                'state': '',
                'city': '',
                'detail': '',
            }
        address_tuple = re.findall('地址：\s+(.+)\s+(.+)\s+(.+)\s+(.+)\S', address_array[0])[0]
        address = {
            'city': address_tuple[2],
            'detail': address_tuple[3]
        }
        if address_tuple[0] == ' ':
            address.update({
                'country': address_tuple[1],
                'state': address_tuple[2],
            })
        else:
            address.update({
                'country': address_tuple[0],
                'state': address_tuple[1],
            })
        return address

    def go(self, url):
        content = get_html(url)
        tree = html.fromstring(content)

        products = {
            'total': 0,
            'current_page': 1,
            'last_page': 1,
            'per_page': 20,
            'data': []
        }

        products.update(self.__extract_pagination(tree))
        products['data'] = self.__extract_product_info(tree)
        products['shop'] = self.__extract_shop_info(tree)

        return products
