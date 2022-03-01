from importlib.metadata import files
import json
from pydantic import Json
import requests

url1 = 'http://127.0.0.1:5000/get_Data'
url = 'http://127.0.0.1:5000/forgot_password'
url3 = "http://192.168.214.190:80/download?id=9136950c-2992-4776-ab12-4d29ed3661c9"
url4 = "https://storage.jayendramadara.repl.co/upload"

myobj = {  "user" : "dimecorp" , }


myotp = {"otp"  : 33835}



filee = {
    "filee" : open(rf"C:\Users\jayendra\Downloads\CT0012.fragmented_no_bot_jpeg_baseline.51 (1).dcm" , "rb") 
}
upload = {
    "patient_name" : "mikasa" ,
    "body_part"    : "head",
    "label"        : "hypertension_1",
    "file"  : url1
}

x = requests.post(url4 , files=filee)

print(x.text , x.status_code)



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