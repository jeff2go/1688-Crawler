# -*- coding: utf-8 -*-

'''
我是一名爬取工人
'''

from product import Product

product = Product()
PRODUCT_URL = 'https://detail.1688.com/offer/1152061078.html?spm=a2615.7691456.0.0.584f5c07YDUNfs'
print(product.go(PRODUCT_URL))
