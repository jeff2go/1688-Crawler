from flask import jsonify

from . import web


@web.app_errorhandler(404)
def page_not_found(e):
    resp = jsonify({'errcode': 404, 'errmsg': str(e)})
    resp.status_code = 404
    return resp


@web.app_errorhandler(500)
def internal_server_error(e):
    resp = jsonify({'errcode': 500, 'errmsg': str(e)})
    resp.status_code = 500
    return resp
