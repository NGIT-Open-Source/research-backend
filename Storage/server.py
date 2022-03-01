
from flask import jsonify, send_file, send_from_directory, session , request , make_response
from functools import wraps
from dotenv import load_dotenv
from itsdangerous import json
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
    try:
        file = request.files["filee"]
        filename= str(uuid.uuid4()) + ".dcm"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
        return jsonify(uploaded="success" , file_id = filename) , 200
    except :
        return jsonify(uploaded="fail" , file_id = None) , 403

@app.route("/download" , methods =['GET'])
# @API_required
def dowload():
    args = request.args
    id = args.get('id')
    print(id , app.config["UPLOAD_FOLDER"]  + "\\"  + id + ".dcm")

    print(os.path.isfile(rf"C:\\tai_jutsu\\GENETICS\\FILES\\{id}.dcm"))
    try:
        response = make_response(send_file(app.config["UPLOAD_FOLDER"] + "\\" + id + ".dcm", as_attachment=True))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e :
        print(e)
        return jsonify(file_error = True) , 403

