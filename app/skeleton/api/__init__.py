from flask_restplus import Api
from flask import Blueprint

from .auth import api as auth_ns
from .user import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTFUL API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restful web service'
          )

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(user_ns, path='/user')

