from . import api
from flask import jsonify, request, url_for, abort
from ..models.square import Square
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/squares/<int:rectangle_id>', methods=['GET'])
@token_auth.login_required
def get_square(rectangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Square.query.filter_by(user_id=user_id, rectangle_id=rectangle_id).one().to_dict())


@api.route('/squares', methods=['POST'])
@token_auth.login_required
def create_square():
    user_id = token_auth.current_user().user_id
    data = request.get_json() or {}
    if 'length' not in data:
        return bad_request('must include length field')
    if type(data['length']) != int:
        return bad_request('length must be an integer')
    if data['length'] <= 0:
        return bad_request('length must be positive')
    square = Square()
    square.from_dict(data, user_id)
    db.session.add(square)
    db.session.commit()
    response = jsonify(square.to_dict())
    response.status_code = 201
    response.headers['Location'] = [url_for(
        'api.get_square', rectangle_id=square.rectangle_id)]
    return response


@api.route('/squares/<int:rectangle_id>', methods=['PUT'])
@token_auth.login_required
def update_square(rectangle_id):
    user_id = token_auth.current_user().user_id
    square = Square.query.filter_by(
        user_id=user_id, rectangle_id=rectangle_id).one()
    data = request.get_json() or {}
    if 'length' in data and type(data['length']) != int:
        return bad_request('length must be an integer')
    if 'length' in data and data['length'] <= 0:
        return bad_request('length must be positive')
    square.from_dict(data, user_id)
    db.session.commit()
    return jsonify(square.to_dict())


@api.route('/squares/<int:rectangle_id>', methods=['DELETE'])
@token_auth.login_required
def del_square(rectangle_id):
    user_id = token_auth.current_user().user_id
    db.session.delete(Square.query.filter_by(
        user_id=user_id, rectangle_id=rectangle_id).one())
    db.session.commit()
    return '', 204
