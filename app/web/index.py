from flask import g, request, jsonify, render_template, flash, redirect, url_for

from . import web
from app.cache.redis import RedisClient
from app.forms.proxy import ProxyCookieForm


def get_redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@web.route('/', methods=['GET'])
def index():
    return '<h1 style="text-align: center; margin-top: 100px;">1688-Crawler based on Flask</h1>'


@web.route('/proxy-cookies/add', methods=['GET', 'POST'])
def add_proxy_cookies():
    form = ProxyCookieForm(request.form)
    if request.method == 'POST' and form.validate():
        # conn = get_redis_conn()
        # is_success = conn.add(request.form.get('cookie'))
        flash('录入成功')
        return redirect(url_for('web.add_proxy_cookies'))
    return render_template('index.html', form=form)
