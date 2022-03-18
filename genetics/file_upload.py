from datetime import datetime
import jwt
import os
from dotenv import load_dotenv
from genetics import app,client
from pymongo import MongoClient
from flask import jsonify, session
from functools import wraps
import pprint
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response , redirect
# import matplotlib.pyplot as plt
# import pydicom.data



app.config['UPLOAD_FOLDER'] = os.getcwd() + "\\test_phase2"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        # print("mawaaa")

    
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message' : 'Token is missing !!'})), 401

        # jwt validation
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'] , algorithms=["HS256"])
            db = client['research']
            collection = db["research_auth"]
            current_user = collection.find_one({"_id":data["public_id"]})
        except Exception as e:
            print(e ,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message' : 'Token is invalid !!'
            })), 401

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
            return make_response(jsonify({'message' : 'APIKEY is missing !!'})), 401
        if str(api_key) == str(os.getenv('API_KEY')):
            # print("thank god")
            pass
        else:
            return make_response(jsonify({
                'message' : 'Token is invalid !!'
            })), 401

        # returns the current logged in users contex to the routes
        return  f( *args, **kwargs)
    return decorated



@app.route("/file_upload" , methods =['POST' ])
@API_required
@token_required
def file_upload(current_user):
    # print(request.get_json(force=True))

    data = request.get_json()
    # print(type(data))
    # input()
    patient  , body_label , label , filee = data["patient_name"] ,data["body_part"],data["label"],data["file_id"]
    # print()
    # print(current_user)
    if not patient or not body_label or not label or not filee:
        return make_response(jsonify({"messgae" : "invalid labeling or empty labeling"})) , 401
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
    del current_user["password"]
    return current_user , 200


@app.route("/get_Data" , methods =['GET' ])
@API_required
@token_required
def get_Data(current_user):
    del current_user["password"] 
    return make_response(current_user) , 200

load_dotenv()





