from . import api
from flask import jsonify, request, url_for, abort
from validate_email import validate_email
import safe
from ..models import User
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/users/<string:user_name>', methods=['GET'])
@token_auth.login_required
def get_user_by_user_name(user_name):
    if token_auth.current_user().user_name != user_name:
        abort(403)
    return jsonify(User.query.filter_by(user_name=user_name).one().to_dict())


@api.route('/users/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_user_by_id(user_id):
    if token_auth.current_user().user_id != user_id:
        abort(403)
    return jsonify(User.query.get_or_404(user_id).to_dict())


@api.route('/users/register', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'user_name' not in data or 'password' not in data:
        return bad_request('must include user_name and password fields')
    if User.query.filter_by(user_name=data['user_name']).first():
        return bad_request('please use a different username')
    if 'email' in data:
        email_valid = validate_email(
            email_address=data['email'], check_regex=True, check_mx=False)
        if not email_valid:
            return bad_request('please enter a valid email address')
        if User.query.filter_by(email=data['email']).first():
            return bad_request('please use a different email address')
    password_strength = safe.check(data['password'])
    if not password_strength.valid:
        return bad_request('please enter a stronger password')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = [url_for(
        'api.get_user_by_user_name', user_name=user.user_name), url_for(
        'api.get_user_by_id', user_id=user.user_id)]
    return response


@api.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def update_user_by_id(user_id):
    if token_auth.current_user().user_id != user_id:
        abort(403)
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if 'user_name' in data and data['user_name'] != user.user_name and User.query.filter_by(user_name=data['user_name']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@api.route('/users/<string:user_name>', methods=['PUT'])
@token_auth.login_required
def update_user_by_user_name(user_name):
    if token_auth.current_user().user_name != user_name:
        abort(403)
    user = User.query.filter_by(user_name=user_name).one()
    data = request.get_json() or {}
    if 'user_name' in data and data['user_name'] != user.user_name and User.query.filter_by(user_name=data['user_name']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
