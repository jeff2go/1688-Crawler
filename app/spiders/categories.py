"""
抓取1688产品分类列表(及商铺)数据 TODO
"""

import re

from lxml import html

from app.spiders.spider import get_html

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
    'cookie': 'cna=d75WG6RzSSQCAXPnX+K/Yq4w; leftMenuLastMode=EXPEND; mtop_partitioned_detect=1; _m_h5_tk=5c8dc5b5cf4303b5db2e96a8eaa68e66_1734682707964; _m_h5_tk_enc=1d7c54a1d4e44d71c2ab114329cc0dfc; t=315e2a753bcc3448e8db676b131e1327; __cn_logon__=false; cookie2=16fbf9e79a5d0d856dc19b92721d144d; _tb_token_=e3876b96b477d; xlly_s=1; leftMenuModeTip=shown; taklid=2ac36427180d4818b6427a4d58ef65e1; _csrf_token=1734674328982; arms_uid=264e3bac-bd0b-4353-aad3-a91aada1a085; x5sec=7b226b796c696e3b32223a226234646132303838626234633064626338393166373930633566656133346137434f65516c4c7347454c6262796f372b2f2f2f2f2f7745776a5a61746c666a2f2f2f2f2f41513d3d222c22733b32223a2263303337633738646539643665636531227d; _bl_uid=OFmak4kmwmhcObfOXkdgx0esR9Uq; _user_vitals_session_data_={"user_line_track":true,"ul_session_id":"ugb69s2a7t","last_page_id":"shop319593x241661.1688.com%2Fpxcjvz8lv2"}; tfstk=g0JiNXsL3waWwUY8WeWsgrUe-FGd5l6f_EeAktQqTw7QXP31BZRc-iV4u--VoEYdREfjfZQVoEK26DH-eht1ht8myYHRdOenFFjN_5oVLiS-vGPrvnRchtu-JcAbrG6XPCCMjF-ExiIzgi8Vg6zFfwS4_t8V86SP0RWV3Eoh8gs0uZyNuMyFVw7V3t82YDjx_z2VrKJBLVEsGkTJLqpVj1bybN-9AplO_5tG--y2KBX1zxQ33-JhfHpD0dwZEwR9gdBeQ2zAL3Op7MXonojHZHWNjEM7CO-yYI5MnjE5lBxew6AQXcsHI3vcq6l4kZCkLdB6t42RzBt2n6-sr7spg3p9iF3Q3NdkYefJpyeRLdYMQ6XP4VNUaWTbhMovLSNf_Mshy9KZx3APbpFoxDVS11SCX4nnxSZO_MshyDm3No5NAG3R.; isg=BIyMWG6gB7rvVBPjrg6yjaV9Xey-xTBvgR8ekeZNKjfycS57C9V3_wqDEXnJOWjH',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

class Categories:
    def __extract_categories(self, tree):
        link_elements = tree.xpath(
            '//li[contains(@class, "cat")]//a[contains(@href, "page/offerlist_")]')

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

    def __extract_shop_info(self, tree, url):
        shop_url_element = tree.xpath('//div[@id="site_footer-box"]//div[@class="m-content"]//p[@class="info"]//span')[0]
        id = re.findall('https?://(.+)\.1688', url)[0]
        title = shop_url_element.text_content().strip()

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
        content = get_html(url, headers)
        print("content", content)
        tree = html.fromstring(content)

        data = {
            'data': self.__extract_categories(tree),
            'shop': self.__extract_shop_info(tree, url)
        }

        return data
