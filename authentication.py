import uuid
import firebase_admin
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from firebase_admin import auth
from firebase_admin import credentials
cred = credentials.Certificate('api/key.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# email = "test59@gmail.com"
# password = "1234567"
# user = auth.create_user(email = email, password = password)
# uniqueId = user.uid

# db.collection('users').document(uniqueId).set({
#     nombre: "x",
#     tipoUsuario: "x",
#     urlFotoPerfil: "x",
#     password: "x",
#     chazasPropias: "x"
# })