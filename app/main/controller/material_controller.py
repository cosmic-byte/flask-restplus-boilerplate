from flask import request
from flask_restplus import Resource

from ..util.dto import MaterialDto
from ..service.material_service import save_new_material, get_all_materials, get_a_material
from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = MaterialDto.api
_material = MaterialDto.material

@api.route('/')
class MaterialList(Resource):
    @api.doc('list_of_materials')
    @api.marshal_list_with(_material, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_materials()

    @api.expect(_material, validate=True)
    # @token_required
    @api.response(201, 'Material successfully created.')
    @api.doc('create a new material')
    def post(self):
        """Create a new Material"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'#user['data']['user_id']
        return save_new_material(data)

@api.route('/<public_id>')
@api.param('public_id', 'The material identifier')
@api.response(404, 'Material not found.')
class Material(Resource):
    @api.doc('get a material')
    @api.marshal_with(_material)
    def get(self, public_id):
        """get a material given its identifier"""
        material = get_a_material(public_id)
        if not material:
            api.abort(404)
        else:
            return material
