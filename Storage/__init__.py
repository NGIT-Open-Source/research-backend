from flask import Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = rf"C:\tai_jutsu\GENETICS\FILES"
from Storage import server