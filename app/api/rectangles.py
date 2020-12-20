from . import api
from flask import jsonify, request, url_for, abort
from ..models.rectangle import Rectangle
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/rectangles/<int:user_id>/<int:rectangle_id>', methods=['GET'])
@token_auth.login_required
def get_rectangles(user_id, rectangle_id):
    if token_auth.current_user().user_id != user_id:
        abort(403)
    return jsonify(Rectangle.query.filter_by(user_id=user_id, rectangle_id=rectangle_id).one().to_dict())
