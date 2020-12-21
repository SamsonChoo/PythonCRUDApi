from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, errors, tokens, rectangles, squares, triangles, diamonds  # nopep8
