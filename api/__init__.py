from flask import Flask

import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Obtener credenciales de las variables de entorno
cred = credentials.Certificate({
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
})

default_app = firebase_admin.initialize_app(cred)


def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 
    from .chazaAPI import chazaAPI
    from .comentarioAPI import comentarioAPI
    from .reporteAPI import reporteAPI
    from .usuarioAPI import usuarioAPI
    #from .userAPI import userAPI

    # Asigna el blueprint de chaza a la aplicación principal
    app.register_blueprint(chazaAPI, url_prefix="/chaza")
    app.register_blueprint(comentarioAPI, url_prefix="/comentario")
    app.register_blueprint(reporteAPI, url_prefix="/reporte")
    app.register_blueprint(usuarioAPI, url_prefix="/usuario")
    

    @app.route('/')
    def hello_world():
        return '<h1>Hello, World!</h1>'

    if __name__ == '__main__':
        app.run(debug=True)

    return app