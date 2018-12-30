from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.index import index

cp = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    app.register_blueprint(index)
    cp.init_app(app)
    return app
