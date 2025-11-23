from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.index import index
from dotenv import load_dotenv
import os

cp = CSRFProtect()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['WTF_CSRF_SSL_STRICT'] = False
    app.register_blueprint(index)
    cp.init_app(app)
    return app
