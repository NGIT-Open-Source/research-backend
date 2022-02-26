# imports

import uuid
import os
import re
import json
import random 
import jwt
import email 
import smtplib,ssl
from datetime import datetime
import flask

from flask import jsonify, session
from functools import wraps
from dotenv import load_dotenv
from pymongo import MongoClient
from email.mime.base import MIMEBase
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from itsdangerous import NoneAlgorithm
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, make_response , redirect
from  werkzeug.security import generate_password_hash, check_password_hash



#inits

app = Flask(__name__)
mail = Mail(app)
client = MongoClient('mongodb://localhost:27017')

#configs
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['SECRET_KEY'] = 'heyypeepssyougottahavethiskey'
app.config['MAIL_USERNAME'] = 'freelacerhiring@gmail.com'

#decorator to verify jwt in requests
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        print("mawaaa")

    
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





@app.route('/signup', methods =['POST' , "GET"])
def signup():

    #data aquired from requests
    data = request.json
    try:
        email , user = data["email"] , data["user"]
        pw = data["pw"]
        if not user or not email or not pw:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )

        #Bson object for mongo insertions
        auth_obj =  { 
            "_id" : str(uuid.uuid4()),
            "name" : user,
            "email" : email,
            "password" : generate_password_hash(pw)
            }
        
        #connecting to mongo client
        db = client['research']
        collection = db["research_auth"]
        user_obj = collection.find_one({"email":email})

        #validation and edgecase handlining
        if  user_obj != None :
            return jsonify({"email_exits" : True , "token" : None}) , 401
        collection.insert_one(auth_obj)

        #jwt generation
        token = jwt.encode({
            'public_id':auth_obj["_id"],
            'exp' : datetime.utcnow() + timedelta(weeks = 2)
        }, app.config['SECRET_KEY'] , algorithms=["HS256"])


        return make_response(jsonify({"email_exits" : False , 'token' : token}), 201)


    except:
        return  make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )




@app.route('/login', methods =['POST' , "GET"])
def login():

    #data from requests
    data = request.json
    try:
        user =  data["user"]
        pw = data["pw"]

        #user and pw validation
        if not user  or not pw:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )

        #connecting to mongo instance
        db = client['research']
        collection = db["research_auth"]
        user_obj = collection.find_one({"name":user})

        #user object validation
        if  user_obj == None:
            return jsonify({"user_exits" : False ,login : False, "token" : None}) , 401
        
        # password validation and jwt generation
        if check_password_hash(user_obj["password"] , pw):
            token = jwt.encode({
            'public_id':user_obj["_id"],
            'exp' : datetime.utcnow() + timedelta(weeks = 2)
            }, app.config['SECRET_KEY'])


        return make_response(jsonify({"login" : True ,"user_exits" : True ,  'token' : token}), 201)
    except:
        return  make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )


#default route called when app is initialized 
@app.route('/test')
@token_required
def test(current_user):
    print(current_user)
    return "reyy"

#default testing route
@app.route("/")
def default():
    return redirect("/signup")

# route for forgot pw
@app.route("/forgot_password" ,  methods =['POST' , "GET"])
def forgot_password():

    #data from requests and connecting to mongo instace
    data = request.json
    user =  data["user"]
    db = client['research']
    collection = db["research_auth"]

    #chekin is user already exits
    user_obj = collection.find_one({"name":user})
    if  user_obj == None:
        return jsonify({"user_exits" : False ,login : False, "token" :  None}) , 401
    
    #smtp server initialization and otp generation
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "freelacerhiring@gmail.com"  # Enter your address
    receiver_email = "dimebeatengreen8@gmail.com"  # Enter receiver address
    password = os.getenv("EMAIL_PASSWORD")
    SUBJECT = "NOREPLY"
    random_otp = random.randint(10000,99999)

    # sending otp emails 
    TEXT = "Verification email for your authentication : {}".format(random_otp)
    mail_txt = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    context = ssl.create_default_context()

    #initialising smtp server
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, mail_txt)
    f = None

    # storing generated otp in new collection which is indexed with ttl
    db = client['research']
    collection = db["otp_client"]
    collection.create_index("createdAt", expireAfterSeconds=600)
    collection.insert_one({"createdAt": datetime.utcnow(),
   "user": user,
   "otp": random_otp})

    # storing otp 
    return "sent"

#otp validation part
@app.route("/forgot_pw_check" ,  methods =['POST' , "GET"])
def forgot_password_validity():

    #retrive otp from requests
    otp = request.json["otp"]
    user = request.headers["user_id"]
    
    #edge cases
    if not otp or not user:
        return jsonify({"otp_verified" : False ,login : False, "token" :  None}) , 401

    #connecting to mongo client
    db = client['research']
    collection = db["otp_client"]
    user_obj = collection.find_one({"user" : user})
    auth_obj = db["research_auth"].find_one({"name" : user})

    #validatioin and jwt generation
    if user_obj and user_obj["otp"] == otp:
        print(auth_obj["_id"])
        token = jwt.encode({
            'public_id':auth_obj["_id"],
            'exp' : datetime.utcnow() + timedelta(weeks = 2) 
        }, app.config['SECRET_KEY'] )
        print(token)

        #resopnse
        return flask.jsonify(otp_verified = True , login = True , token = token)
    return flask.jsonify(otp_verified = False , login = False , token = None)

load_dotenv()
app.run(debug = True)

