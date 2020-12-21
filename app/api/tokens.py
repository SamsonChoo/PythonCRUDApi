from flask import jsonify
from .. import db
from . import api
from .auth import basic_auth, token_auth


@api.route('/login', methods=['GET'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})


@api.route('/logout', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
