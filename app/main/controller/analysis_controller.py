from app.main.util.dto import AnalysisDto
from flask_restx import Resource
from app.main.core.DlLinerRegression import DlLinerRegression

from flask import request

api = AnalysisDto.api

analysis_request = AnalysisDto.analysis_request


@api.route('/linear_regression')
class Analysis(Resource):
    """
        Analysis Method
    """
    @api.doc('use model to analysis')
    @api.expect(analysis_request, validate=True)
    def post(self):
        post_data = request.json

        lr = DlLinerRegression(post_data['dataSetUrl'], "rs.txt")
        lr.readData()
        lr.run()
        lr.output()
        with open("rs.txt") as f:
            content = f.read()
        return {"content": content}
