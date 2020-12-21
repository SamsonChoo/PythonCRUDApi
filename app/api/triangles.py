from . import api
from flask import jsonify, request, url_for, abort
from ..models.triangle import Triangle
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/triangles/<int:triangle_id>', methods=['GET'])
@token_auth.login_required
def get_triangle(triangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Triangle.query.filter_by(user_id=user_id, triangle_id=triangle_id).one().to_dict())


@api.route('/triangles/<int:triangle_id>/area', methods=['GET'])
@token_auth.login_required
def get_triangle_area(triangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Triangle.query.filter_by(user_id=user_id, triangle_id=triangle_id).one().get_area())


@api.route('/triangles/<int:triangle_id>/perimeter', methods=['GET'])
@token_auth.login_required
def get_triangle_perimeter(triangle_id):
    user_id = token_auth.current_user().user_id
    return jsonify(Triangle.query.filter_by(user_id=user_id, triangle_id=triangle_id).one().get_perimeter())


@api.route('/triangles', methods=['POST'])
@token_auth.login_required
def create_triangle():
    user_id = token_auth.current_user().user_id
    data = request.get_json() or {}
    if 'length1' not in data or 'length2' not in data or 'length3' not in data:
        return bad_request('must include length1, length2, and length3 fields')
    if (type(data['length1']) != int and type(data['length1']) != float or
        type(data['length2']) != int and type(data['length2']) != float or
            type(data['length3']) != int and type(data['length3']) != float):
        return bad_request('length must be numbers')
    if data['length1'] <= 0 or data['length2'] <= 0 or data['length3'] <= 0:
        return bad_request('length must be positive')
    triangle = Triangle()
    triangle.from_dict(data, user_id)
    db.session.add(triangle)
    db.session.commit()
    response = jsonify(triangle.to_dict())
    response.status_code = 201
    response.headers['Location'] = [url_for(
        'api.get_triangle', triangle_id=triangle.triangle_id)]
    return response


@api.route('/triangles/<int:triangle_id>', methods=['PUT'])
@token_auth.login_required
def update_triangle(triangle_id):
    user_id = token_auth.current_user().user_id
    triangle = Triangle.query.filter_by(
        user_id=user_id, triangle_id=triangle_id).one()
    data = request.get_json() or {}
    if ('length1' in data and type(data['length1']) != int and type(data['length1']) != float or
        'length2' in data and type(data['length2']) != int and type(data['length2']) != float or
            'length3' in data and type(data['length3']) != int and type(data['length3']) != float):
        return bad_request('length must be numbers')
    if 'length1' in data and data['length1'] <= 0 or 'length2' in data and data['length2'] <= 0 or 'length3' in data and data['length3'] <= 0:
        return bad_request('length must be positive')
    triangle.from_dict(data, user_id)
    db.session.commit()
    return jsonify(triangle.to_dict())


@api.route('/triangles/<int:triangle_id>', methods=['DELETE'])
@token_auth.login_required
def del_triangle(triangle_id):
    user_id = token_auth.current_user().user_id
    db.session.delete(Triangle.query.filter_by(
        user_id=user_id, triangle_id=triangle_id).one())
    db.session.commit()
    return '', 204
