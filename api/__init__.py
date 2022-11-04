from flask import Flask

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("api/key.json")
default_app = firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 
    from .userAPI import userAPI
    app.register_blueprint(userAPI, url_prefix="/user")

    @app.route('/')
    def hello_world():
    	return '<h1>Hello, World!</h1>'

    if __name__ == '__main__':
    	app.run(debug=True)

    return app
