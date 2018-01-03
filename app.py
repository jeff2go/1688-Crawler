from flask import Flask
from flask import jsonify
from flask import request

from products import Products
from product import Product
from categories import Categories

import json

app = Flask(__name__)

@app.route('/crawlers/categories', methods=['GET'])
def crawl_categories():
    try:
        categories = Categories()
        categories = categories.go(request.args.get('url'))
        return jsonify(categories)
    except Exception as e:
        resp = jsonify({'errcode': 500, 'errmsg': '抓取分类列表异常: ' + str(e)})
        resp.status_code = 500
        return resp

@app.route('/crawlers/products', methods=['GET'])
def crawl_products():
    try:
        products = Products()
        products = products.go(request.args.get('url'))
        return jsonify(products)
    except Exception as e:
        resp = jsonify({'errcode': 500, 'errmsg': '抓取产品列表异常: ' + str(e)})
        resp.status_code = 500
        return resp

@app.route('/crawlers/product', methods=['GET'])
def crawl_product():
    try:
        product = Product()
        product = product.go(request.args.get('url'))
        return jsonify(product)
    except Exception as e:
        resp = jsonify({'errcode': 500, 'errmsg': '抓取产品异常: ' + str(e)})
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run()
