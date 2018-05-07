"""
抓取1688产品分类列表(及商铺)数据 TODO
"""

import re

from lxml import html

from app.libs.spider import get_html


class Categories:
    def __extract_categories(self, tree):
        link_elements = tree.xpath(
            '//div[contains(@class, "grid-sub")]//div[@class="m-content"]//a[contains(@href, "page/offerlist_")]')

        categories = []
        sub_categories = []
        for item in link_elements:
            href = item.attrib['href']
            ids = re.findall('_(([\d-]+)_?(\d+)*)\.htm', href)[0]
            category = {
                'id': ids[1],
                'pid': ids[2],
                'name': item.text_content().strip(),
                'sub': []
            }
            if category['pid'] == '':
                categories.append(category)
            else:
                sub_categories.append(category)

        for sub_cat in sub_categories:
            for cat in categories:
                if cat['id'] == sub_cat['pid']:
                    cat['sub'].append(sub_cat)
                    break

        return categories

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
            'telphone': telephone,
            'mobile': mobile,
            'address': address
        }

    def __extract_shop_address(self, tree):
        address_text = tree.xpath('//span[@class="address_title"]/text()')[0]
        address_text = re.findall('地址：\s+(.+)', address_text)[0]
        address_text = address_text.replace('  ', ' ')
        address_list = address_text.split(' ')
        if len(address_list) == 3:
            address = {
                'country': address_list[0],
                'state': address_list[1],
                'city': '',
                'detail': address_list[2]
            }
        else:
            address = {
                'country': address_list[0],
                'state': address_list[1],
                'city': address_list[2],
                'detail': address_list[3]
            }
        return address

    def go(self, url):
        content = get_html(url)
        tree = html.fromstring(content)

        data = {
            'data': self.__extract_categories(tree),
            'shop': self.__extract_shop_info(tree)
        }

        return data
