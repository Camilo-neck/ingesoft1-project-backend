from flask import Flask

import firebase_admin
from firebase_admin import credentials

import os
from dotenv import load_dotenv
import json

load_dotenv()

#Obtener credenciales de las variables de entorno
cred = credentials.Certificate('api/key.json')

default_app = firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 
    from .chazaAPI import chazaAPI
    from .comentarioAPI import comentarioAPI
    #from .userAPI import userAPI

    # Asigna el blueprint de chaza a la aplicación principal
    app.register_blueprint(chazaAPI, url_prefix="/chaza")
    app.register_blueprint(comentarioAPI, url_prefix="/comentario")
    

    @app.route('/')
    def hello_world():
        return '<h1>Hello, World!</h1>'

    if __name__ == '__main__':
        app.run(debug=True)

    return app