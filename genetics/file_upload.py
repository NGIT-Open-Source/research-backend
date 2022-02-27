from datetime import datetime
import jwt
import os
from dotenv import load_dotenv
from genetics import app,client
from pymongo import MongoClient
from flask import jsonify, session
from functools import wraps
import pprint
from firebase_admin import credentials, initialize_app, storage
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response , redirect
import matplotlib.pyplot as plt
import pydicom.data

#creds 
cred = credentials.Certificate(rf"jayendra-madaram-firebase-adminsdk-p6rxo-603c7c7cad.json")
initialize_app(cred, {'storageBucket': 'jayendra-madaram.appspot.com'})


app.config['UPLOAD_FOLDER'] = rf"C:\tai_jutsu\GENETICS\test_phase2"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        # print("mawaaa")

    
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        # jwt validation
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'] , algorithms=["HS256"])
            db = client['research']
            collection = db["research_auth"]
            current_user = collection.find_one({"_id":data["public_id"]})
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401

        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
    return decorated

def API_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # jwt is passed in the request header
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        if not api_key:
            return jsonify({'message' : 'APIKEY is missing !!'}), 401
        if str(api_key) == str(os.getenv('API_KEY')):
            # print("thank god")
            pass
        else:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401

        # returns the current logged in users contex to the routes
        return  f( *args, **kwargs)
    return decorated



@app.route("/file_upload" , methods =['POST', "GET" ])
@API_required
@token_required
def file_upload(current_user):
    # print(request.get_json(force=True))

    data = request.get_json()
    # print(type(data))
    # input()
    patient  , body_label , label , filee = data["patient_name"] ,data["body_part"],data["label"],data["file"]
    # print()
    # print(current_user)
    if patient in current_user["patients"].keys():

        if body_label in current_user["patients"][patient].keys():

            if label in current_user["patients"][patient][body_label].keys():

                current_user["patients"][patient][body_label][label].append((filee , datetime.utcnow()))
            
            else:
                current_user["patients"][patient][body_label][label] = [(filee , datetime.utcnow())]
        
        else:
            current_user["patients"][patient][body_label] = {
                [label] : [(filee , datetime.utcnow())]
            }
    else:
        
        current_user["patients"][patient] = {body_label : {
            label : [(filee , datetime.utcnow())]
        }}
        # print(type(current_user["patients"]))
    db = client['research']
    collection = db["research_auth"]
    collection.update_one({"_id" : current_user["_id"]} , {"$set" : {"patients" : current_user["patients"]}})
    return "hoillaaaa"
load_dotenv()





