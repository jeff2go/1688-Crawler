from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import index
from app.web import crawler
from app.web import go2
from app.web import errors
