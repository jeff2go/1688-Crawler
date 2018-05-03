from . import web


@web.route('/', methods=['GET'])
def index():
    a = 1/0
    return '<h1 style="text-align: center; margin-top: 100px;">1688-Crawler based on Flask</h1>'
