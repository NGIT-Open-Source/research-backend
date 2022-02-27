# imports

import flask

from datetime import datetime
from pymongo import MongoClient
from flask_mail import Mail, Message
from flask import Flask, request, jsonify, make_response , redirect



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
from genetics import server