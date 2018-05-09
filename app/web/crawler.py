from flask import jsonify, request

from . import web
from app.spiders.product import Product
from app.spiders.products import Products
from app.spiders.categories import Categories


@web.route('/crawlers/categories', methods=['GET'])
def crawl_categories():
    categories = Categories()
    categories = categories.go(request.args.get('url'))
    return jsonify(categories)


@web.route('/crawlers/products', methods=['GET'])
def crawl_products():
    products = Products()
    products = products.go(request.args.get('url'))
    return jsonify(products)


@web.route('/crawlers/product', methods=['GET'])
def crawl_product():
    product = Product()
    product = product.go(request.args.get('url'))
    return jsonify(product)
