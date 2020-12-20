from . import api
from flask import jsonify, request, url_for, abort
from ..models.rectangle import Rectangle
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/rectangles/<int:rectangle_id>', methods=['GET'])
@token_auth.login_required
def get_rectangle(rectangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Rectangle.query.filter_by(user_id=user_id, rectangle_id=rectangle_id).one().to_dict())


@api.route('/rectangles/<int:rectangle_id>/area', methods=['GET'])
@token_auth.login_required
def get_rectangle_area(rectangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Rectangle.query.filter_by(user_id=user_id, rectangle_id=rectangle_id).one().get_area())


@api.route('/rectangles/<int:rectangle_id>/perimeter', methods=['GET'])
@token_auth.login_required
def get_rectangle_perimeter(rectangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Rectangle.query.filter_by(user_id=user_id, rectangle_id=rectangle_id).one().get_perimeter())


@api.route('/rectangles', methods=['POST'])
@token_auth.login_required
def create_rectangle():
    user_id = token_auth.current_user().user_id
    data = request.get_json() or {}
    if 'length' not in data or 'width' not in data:
        return bad_request('must include length and width fields')
    if type(data['length']) != int or type(data['width']) != int:
        return bad_request('length and width must be integers')
    if data['length'] <= 0 or data['width'] <= 0:
        return bad_request('length and width must be positive')
    rectangle = Rectangle()
    rectangle.from_dict(data, user_id, new_rectangle=True)
    db.session.add(rectangle)
    db.session.commit()
    response = jsonify(rectangle.to_dict())
    response.status_code = 201
    response.headers['Location'] = [url_for(
        'api.get_rectangle', rectangle_id=rectangle.rectangle_id)]
    return response
