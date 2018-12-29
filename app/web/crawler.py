from flask import jsonify, request
import traceback

from . import web
from app.spiders.product import Product
from app.spiders.products import Products
from app.spiders.categories import Categories


@web.route('/crawlers/categories', methods=['GET'])
def crawl_categories():
    try:
        categories = Categories()
        categories = categories.go(request.args.get('url'))
        return jsonify(categories)
    except Exception as e:
        traceback.print_exc()
        resp = jsonify({'errcode': 500, 'errmsg': '抓取商铺分类异常: ' + str(e)})
        resp.status_code = 500
        return resp


@web.route('/crawlers/products', methods=['GET'])
def crawl_products():
    try:
        products = Products()
        products = products.go(request.args.get('url'))
        return jsonify(products)
    except Exception as e:
        traceback.print_exc()
        resp = jsonify({'errcode': 500, 'errmsg': '抓取产品列表异常: ' + str(e)})
        resp.status_code = 500
        return resp


@web.route('/crawlers/product', methods=['GET'])
def crawl_product():
    try:
        product = Product()
        product = product.go(request.args.get('url'))
        return jsonify(product)
    except Exception as e:
        traceback.print_exc()
        resp = jsonify({'errcode': 500, 'errmsg': '抓取产品异常: ' + str(e)})
        resp.status_code = 500
        return resp
