import requests

url = 'http://127.0.0.1:5000/forgot_password'
myobj = {  "user" : "dimecorp" , }

x = requests.post(url  , json=myobj , headers={"x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJhOTZkZmVlYi03ZDI1LTQ2MGQtYjc1Zi01NWM4ZDEyMTE5YzIiLCJleHAiOjE2NDcwODEzMDB9.IhduZHOf9XN0wETrgRecO1jpBcr2R-GJJ66Q0t7jwOg"})

print(x.text , x.status_code)

