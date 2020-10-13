from app.main.util.dto import AnalysisDto
from flask_restx import Resource

from flask import request

api = AnalysisDto.api

analysis_request = AnalysisDto.analysis_request


@api.route('/')
class Analysis(Resource):
    """
        Analysis Method
    """
    @api.doc('use model to analysis')
    @api.expect(analysis_request, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return {"status":"ok"}
