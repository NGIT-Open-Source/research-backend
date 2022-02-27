from importlib.metadata import files
import json
from pydantic import Json
import requests

url1 = 'http://127.0.0.1:5000/file_upload'
url = 'http://127.0.0.1:5000/forgot_password'


myobj = {  "user" : "dimecorp" , }


myotp = {"otp"  : 33835}



filee = {
    "filee" : open(rf"test_data\0002.DCM" , "rb") 
}
upload = {
    "patient_name" : "mikasa" ,
    "body_part"    : "head",
    "label"        : "hypertension_1",
    "file"  : url1
}

x = requests.post(url1 , headers={"x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIwZWQ4MzM3MS01YjljLTQwNTgtYWNhNy1kMmFjMGYyYjQ4YzMiLCJleHAiOjE2NDcxNjYzODZ9.4i4u-Tm1BmmeLrC0_wtQvAGhfaSQxPxuiXxf6Rr97Lc" , "user_id" : "dimecorp" , "X-API-Key" : "Panther"} ,json=upload)

# print(x.text , x.status_code)



# # ---------------
# from firebase_admin import credentials, initialize_app, storage

# cred = credentials.Certificate(rf"jayendra-madaram-firebase-adminsdk-p6rxo-603c7c7cad.json")
# initialize_app(cred, {'storageBucket': 'jayendra-madaram.appspot.com'})

# # Put your local file path 
# fileName = rf"test_data\0002.DCM"
# bucket = storage.bucket()
# blob = bucket.blob(fileName)
# blob.upload_from_filename(fileName)

# # Opt : if you want to make public access from the URL
# blob.make_public()

# print("your file url", blob.public_url)

# # from pydicom import dcmread
# # from pydicom.filebase import DicomBytesIO

# # with open(rf'test_data\osirix-goudurix (1) (1) (1).dcm', 'rb') as fp:
# #     raw = DicomBytesIO(fp.read())
# #     ds = dcmread(raw)
# #     print(raw)

# # with open(rf"test_data\0002.DCM" , "rb") as f:
#     # print(f)