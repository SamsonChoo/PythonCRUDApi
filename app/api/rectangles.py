from .auth import token_auth


@api.route('/rectangles', methods=['GET'])
@token_auth.login_required
def get_rectangles():
    # code to fetch all rectangles by user
    pass
