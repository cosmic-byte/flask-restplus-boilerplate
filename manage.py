import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.skeleton.api import blueprint as api_blueprint

from app.skeleton import create_app, db
from app.skeleton.models import user, blacklist


basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app(os.getenv('SKELETON_ENV') or 'dev')

app.register_blueprint(api_blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()