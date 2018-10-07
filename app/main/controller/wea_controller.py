from flask import request
from flask_restplus import Resource

from ..util.dto import WEADto
from ..service.wea_service import save_new_wea, get_all_weas, get_a_wea
from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = WEADto.api
_wea = WEADto.wea


@api.route('/')
class weaList(Resource):
    @api.doc('list of weas')
    @api.marshal_list_with(_wea, envelope='data')
    def get(self):
        """List all weas"""
        return get_all_weas()

    @api.expect(_wea, validate=True)
    # @token_required
    @api.response(201, 'wea successfully created.')
    @api.doc('create a new wea')
    def post(self):
        """Create a new wea"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'  # user['data']['user_id']
        return save_new_wea(data)


@api.route('/<public_id>')
@api.param('public_id', 'The wea identifier')
@api.response(404, 'wea not found.')
class Material(Resource):
    @api.doc('get a wea')
    @api.marshal_with(_wea)
    def get(self, public_id):
        """get a wea given its identifier"""
        wea = get_a_wea(public_id)
        if not wea:
            api.abort(404)
        else:
            return wea
