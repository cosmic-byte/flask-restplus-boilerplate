import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from .main import api
from .main.database import db

app = api.create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(api.blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('api', pattern='test*.py', top_level_dir='.')
    result = unittest.TextTestRunner(verbosity=6).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
