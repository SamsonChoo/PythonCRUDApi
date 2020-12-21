from . import api
from flask import jsonify, request, url_for, abort
from ..models.diamond import Diamond
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/diamonds/<int:diamond_id>', methods=['GET'])
@token_auth.login_required
def get_diamond(diamond_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Diamond.query.filter_by(user_id=user_id, diamond_id=diamond_id).one().to_dict())


@api.route('/diamonds/<int:diamond_id>/area', methods=['GET'])
@token_auth.login_required
def get_diamond_area(diamond_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Diamond.query.filter_by(user_id=user_id, diamond_id=diamond_id).one().get_area())


@api.route('/diamonds/<int:diamond_id>/perimeter', methods=['GET'])
@token_auth.login_required
def get_diamond_perimeter(diamond_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Diamond.query.filter_by(user_id=user_id, diamond_id=diamond_id).one().get_perimeter())


@api.route('/diamonds', methods=['POST'])
@token_auth.login_required
def create_diamond():
    user_id = token_auth.current_user().user_id
    data = request.get_json() or {}
    if 'diagonal1' not in data or 'diagonal2' not in data:
        return bad_request('must include diagonal1 and diagonal2 fields')
    if type(data['diagonal1']) != int or type(data['diagonal2']) != int:
        return bad_request('diagonal1 and diagonal2 must be integers')
    if data['diagonal1'] <= 0 or data['diagonal2'] <= 0:
        return bad_request('diagonal1 and diagonal2 must be positive')
    diamond = Diamond()
    diamond.from_dict(data, user_id)
    db.session.add(diamond)
    db.session.commit()
    response = jsonify(diamond.to_dict())
    response.status_code = 201
    response.headers['Location'] = [url_for(
        'api.get_diamond', diamond_id=diamond.diamond_id)]
    return response


@api.route('/diamonds/<int:diamond_id>', methods=['PUT'])
@token_auth.login_required
def update_diamond(diamond_id):
    user_id = token_auth.current_user().user_id
    diamond = Diamond.query.filter_by(
        user_id=user_id, diamond_id=diamond_id).one()
    data = request.get_json() or {}
    if 'diagonal1' in data and type(data['diagonal1']) != int or 'diagonal2' in data and type(data['diagonal2']) != int:
        return bad_request('diagonal1 and diagonal2 must be integers')
    if 'diagonal1' in data and data['diagonal1'] <= 0 or 'diagonal2' in data and data['diagonal2'] <= 0:
        return bad_request('diagonal1 and diagonal2 must be positive')
    diamond.from_dict(data, user_id)
    db.session.commit()
    return jsonify(diamond.to_dict())


@api.route('/diamonds/<int:diamond_id>', methods=['DELETE'])
@token_auth.login_required
def del_diamond(diamond_id):
    user_id = token_auth.current_user().user_id
    db.session.delete(Diamond.query.filter_by(
        user_id=user_id, diamond_id=diamond_id).one())
    db.session.commit()
    return '', 204
