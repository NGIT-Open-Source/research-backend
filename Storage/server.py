
from flask import jsonify, send_file, send_from_directory, session , request
from functools import wraps
from dotenv import load_dotenv
from Storage import app
import os
import uuid

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

@app.route("/upload" , methods =['POST'])
@API_required
def upload():
    file = request.files["filee"]
    filename= str(uuid.uuid4()) + ".dcm"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
    return filename 

@app.route("/download" , methods =['GET'])
# @API_required
def dowload():
    args = request.args
    id = args.get('id')
    print(id , app.config["UPLOAD_FOLDER"] + id + ".dcm")

    return send_file(app.config["UPLOAD_FOLDER"] + "\\" + id + ".dcm", as_attachment=True)
