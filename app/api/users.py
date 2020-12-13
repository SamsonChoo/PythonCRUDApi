from . import api
from flask import jsonify, request, url_for, abort
from ..models import User
from .errors import bad_request
from .. import db
from .auth import token_auth


@api.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users', methods=['GET'])
def get_users():
    pass


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'user_name' not in data or 'password' not in data:
        return bad_request('must include user_name and password fields')
    if User.query.filter_by(user_name=data['user_name']).first():
        return bad_request('please use a different username')
    if 'email' in data and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.user_id)
    return response


@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'user_name' in data and data['user_name'] != user.user_name and User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
