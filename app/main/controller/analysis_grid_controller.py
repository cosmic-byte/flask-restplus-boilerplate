from flask import request
from flask_restplus import Resource

from ..util.dto import AnalysisGridDto
from ..service.analysis_grid_service import save_new_analysis_grid, \
                                               get_all_analysis_grids, \
                                               get_an_analysis_grid

from app.main.util.decorator import token_required
from app.main.service.auth_helper import Auth

api = AnalysisGridDto.api
_analysis_grid = AnalysisGridDto.analysis_grid


@api.route('/')
class AnalysisGridList(Resource):
    @api.doc('list of analysis grids')
    @api.marshal_list_with(_analysis_grid, envelope='data')
    def get(self):
        """List all analysis grids"""
        api_response, success = get_all_analysis_grids()
        if success:
            return api_response['analysis_grids']
        else:
            return api_response, 409

    @api.expect(_analysis_grid, validate=True)
    # @token_required
    @api.response(201, 'Analysis grid successfully created.')
    @api.doc('create a new analysis grid')
    def post(self):
        """Create a new analysis grid"""
        user, status = Auth.get_logged_in_user(request)
        data = request.json
        data['user_id'] = 'test'  # user['data']['user_id']
        return save_new_analysis_grid(data)


@api.route('/<id>')
@api.param('id', 'The material identifier')
@api.response(404, 'Material not found.')
class AnalysisGrid(Resource):
    @api.doc('get an analysis grid')
    @api.marshal_with(_analysis_grid)
    def get(self, id):
        """get a material given its identifier"""
        api_response, success = get_an_analysis_grid(id)
        if not success:
            api.abort(404)
        else:
            return api_response['analysis_grid']
