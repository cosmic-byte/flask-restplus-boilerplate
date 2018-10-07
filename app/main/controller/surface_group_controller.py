from flask import request
from flask_restplus import Resource

from ..util.dto import SurfaceGroupDto
from ..service.surface_group_service import save_new_surface_group, \
                                            get_all_surface_groups, \
                                            get_a_surface_group
from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = SurfaceGroupDto.api
_surface_groups = SurfaceGroupDto.surface_group


@api.route('/')
class SurfaceGroupList(Resource):
    @api.doc('list of surface groups')
    @api.marshal_list_with(_surface_groups, envelope='data')
    def get(self):
        """List all surface groups"""
        api_response, success = get_all_surface_groups()
        print(api_response)
        if success:
            return api_response['surface_groups']
        else:
            return api_response, 409

    @api.expect(_surface_groups, validate=True)
    # @token_required
    @api.response(201, 'Surface group successfully created.')
    @api.doc('create a new surface group')
    def post(self):
        """Create a new HoneybeeSurface"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'  # user['data']['user_id']
        return save_new_surface_group(data)


@api.route('/<id>')
@api.param('id', 'The surface group identifier')
@api.response(404, 'Surface Group not found.')
class HoneybeeSurface(Resource):
    @api.doc('get a surface group')
    @api.marshal_with(_surface_groups)
    def get(self, id):
        """get a material given its identifier"""
        api_response, success = get_a_surface_group(id)
        if not success:
            api.abort(404)
        else:
            return api_response['surface_group']
