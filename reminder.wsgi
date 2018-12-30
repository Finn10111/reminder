import os
import sys
sys.path.insert(1, os.path.dirname(__file__))
from app import create_app

def application(environ, start_response):
    os.environ['SECRET_KEY'] = environ.get('SECRET_KEY') 
    app = create_app()
    return app(environ, start_response)
