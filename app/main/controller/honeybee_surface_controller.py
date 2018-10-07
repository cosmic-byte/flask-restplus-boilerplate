from flask import request
from flask_restplus import Resource

from ..util.dto import HoneybeeSurfaceDto
from ..service.honeybee_surface_service import save_new_honeybee_surface, \
                                               get_all_honeybee_surfaces, \
                                               get_a_honeybee_surface
from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = HoneybeeSurfaceDto.api
_honeybee_surface = HoneybeeSurfaceDto.honeybee_surface


@api.route('/')
class HoneybeeSurfaceList(Resource):
    @api.doc('list of honeybee surfaces')
    @api.marshal_list_with(_honeybee_surface, envelope='data')
    def get(self):
        """List all honeybee surfaces"""
        api_response, success = get_all_honeybee_surfaces()
        if success:
            return api_response['honeybee_surfaces']
        else:
            return api_response, 409

    @api.expect(_honeybee_surface, validate=True)
    # @token_required
    @api.response(201, 'Honeybee surface successfully created.')
    @api.doc('create a new honeybee surface')
    def post(self):
        """Create a new HoneybeeSurface"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'#user['data']['user_id']
        return save_new_honeybee_surface(data)


@api.route('/<id>')
@api.param('id', 'The material identifier')
@api.response(404, 'Material not found.')
class HoneybeeSurface(Resource):
    @api.doc('get a honeybee surface')
    @api.marshal_with(_honeybee_surface)
    def get(self, id):
        """get a material given its identifier"""
        api_response, success = get_a_honeybee_surface(id)
        if not success:
            api.abort(404)
        else:
            return api_response['honeybee_surface']
