from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.material_controller import api as material_ns
from .main.controller.honeybee_surface_controller import api as\
    honeybee_surface_ns
from .main.controller.analysis_grid_controller import api as analysis_grid_ns
from .main.controller.surface_group_controller import api as surface_group_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Ladybug Tools CRUD API ',
          version='1.0',
          description='a crud api for ladybug tools objects'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(material_ns, path='/material')
api.add_namespace(honeybee_surface_ns, path='/honeybee_surface')
api.add_namespace(analysis_grid_ns, path='/analysis_grid')
api.add_namespace(surface_group_ns, path='/surface_group')
