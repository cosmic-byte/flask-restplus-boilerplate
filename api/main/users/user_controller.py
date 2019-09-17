from flask import request
from flask_restplus import Namespace, Resource, fields

from .user_service import save_new_user, get_all_users, get_a_user
from ..auth.decorator import admin_token_required
from .user_dto import user_dto

ns = Namespace('users', description='user related operations')
ns.add_model(user_dto.name, user_dto)


@ns.route('/')
class UserList(Resource):
    @ns.doc('list of registered users')
    @admin_token_required
    @ns.marshal_list_with(user_dto, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @ns.expect(user_dto, validate=True)
    @ns.response(201, 'User successfully created.')
    @ns.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@ns.route('/<public_id>')
@ns.param('public_id', 'The User identifier')
@ns.response(404, 'User not found.')
class User(Resource):
    @ns.doc('get a user')
    @ns.marshal_with(user_dto)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            ns.abort(404)
        else:
            return user
