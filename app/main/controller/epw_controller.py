from flask import request
from flask_restplus import Resource

from ..util.dto import EPWDto
from ..service.epw_service import save_new_epw, get_all_epws, get_an_epw
from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = EPWDto.api
_epw = EPWDto.epw


@api.route('/')
class EPWList(Resource):
    @api.doc('list of epws')
    @api.marshal_list_with(_epw, envelope='data')
    def get(self):
        """List all epws"""
        return get_all_epws()

    @api.expect(_epw, validate=True)
    # @token_required
    @api.response(201, 'Epw successfully created.')
    @api.doc('create a new epw')
    def post(self):
        """Create a new EPW"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'  # user['data']['user_id']
        return save_new_epw(data)


@api.route('/<public_id>')
@api.param('public_id', 'The epw identifier')
@api.response(404, 'EPW not found.')
class Material(Resource):
    @api.doc('get an epw')
    @api.marshal_with(_epw)
    def get(self, public_id):
        """get an epw given its identifier"""
        epw = get_an_epw(public_id)
        if not epw:
            api.abort(404)
        else:
            return epw
