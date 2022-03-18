
from pymongo import MongoClient
from flask_mail import Mail
from flask import Flask
from dotenv import load_dotenv
import os

#inits
load_dotenv()
app = Flask(__name__)
mail = Mail(app)
client = MongoClient(os.getenv("MONGO_URL"))

#configs
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] =False
app.config['MAIL_SERVER']=os.getenv("MAIL_SERVER")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")

#decorator to verify jwt in requests
from genetics import server
from genetics import file_upload