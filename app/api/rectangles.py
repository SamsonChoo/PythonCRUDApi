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


# @api.route('/rectangles/<int:user_id>', methods=['POST'])
# @token_auth.login_required
# def create_rectangle(user_id):
#     if token_auth.current_user().user_id != user_id:
#         abort(403)
#     data = request.get_json() or {}
#     if 'length' not in data or 'width' not in data:
#         return bad_request('must include length and width fields')

#     if User.query.filter_by(user_name=data['user_name']).first():
#         return bad_request('please use a different username')
#     if 'email' in data:
#         email_valid = validate_email(
#             email_address=data['email'], check_regex=True, check_mx=False)
#         if not email_valid:
#             return bad_request('please enter a valid email address')
#         if User.query.filter_by(email=data['email']).first():
#             return bad_request('please use a different email address')
#     password_strength = safe.check(data['password'])
#     if not password_strength.valid:
#         return bad_request('please enter a stronger password')
#     user = User()
#     user.from_dict(data, new_user=True)
#     db.session.add(user)
#     db.session.commit()
#     response = jsonify(user.to_dict())
#     response.status_code = 201
#     response.headers['Location'] = [url_for(
#         'api.get_user_by_user_name', user_name=user.user_name), url_for(
#         'api.get_user_by_user_id', user_id=user.user_id)]
#     return response
