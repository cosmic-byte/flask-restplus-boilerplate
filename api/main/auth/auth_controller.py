from flask import request
from flask_restplus import Namespace, Resource, fields

from .auth_helper import Auth
from .auth_dto import auth_dto

ns = Namespace('auth', description='authentication related operations')
ns.add_model(auth_dto.name, auth_dto)


@ns.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """

    @ns.doc('user login')
    @ns.expect(auth_dto, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@ns.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @ns.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
