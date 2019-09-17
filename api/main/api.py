from flask import Blueprint
from flask import Flask
from flask_restplus import Api

from .users import user_controller
from .auth import auth_controller

from .config import config_by_name
from .database import db
from .users.user_model import flask_bcrypt

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='TradeReveal HTTP RESTful API',
          version='0.5',
          description='Digital assets trading for professionals'
          )

api.add_namespace(user_controller.ns)
api.add_namespace(auth_controller.ns)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
