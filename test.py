import requests

url1 = 'http://127.0.0.1:5000/forgot_pw_check'
url = 'http://127.0.0.1:5000/forgot_password'
myobj = {  "user" : "dimecorp" , }
myotp = {"otp"  : 33835}
x = requests.post(url1  , json=myotp , headers={"x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJhOTZkZmVlYi03ZDI1LTQ2MGQtYjc1Zi01NWM4ZDEyMTE5YzIiLCJleHAiOjE2NDcwODEzMDB9.IhduZHOf9XN0wETrgRecO1jpBcr2R-GJJ66Q0t7jwOg" , "user_id" : "dimecorp"})

print(x.text , x.status_code)

