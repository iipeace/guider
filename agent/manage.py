import os

from flask_script import Manager
from app import create_app

# if FLASK_MODE path is not set dev env run
app = create_app(os.getenv('FLASK_MODE') or 'dev')

app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    pass


if __name__ == '__main__':
    manager.run()
