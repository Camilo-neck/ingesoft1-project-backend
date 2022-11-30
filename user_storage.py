import uuid
import firebase_admin
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from firebase_admin import auth
from firebase_admin import credentials
cred = credentials.Certificate('INSERTAR KEY')

default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# emailInput = "test4@gmail.com"
# passwordInput = "1234567"

user = auth.create_user(email = emailInput, password = passwordInput)

userData = user.__dict__
db.collection('users').document().set(userData["_data"])


