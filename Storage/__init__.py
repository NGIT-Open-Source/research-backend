from flask import Flask
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)
app.config['UPLOAD_FOLDER'] = rf"C:\tai_jutsu\GENETICS\FILES"
from Storage import server