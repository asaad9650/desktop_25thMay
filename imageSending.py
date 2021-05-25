import pyrebase
import os
import datetime, time
from firebase_admin import db


config = {
    "apiKey": "AIzaSyDuJBIy74DlZod-3u3EbuR1nFBb19yOsGg",
    "authDomain": "fingerprintdoorlock-8bb72.firebaseapp.com",
    "databaseURL": "https://fingerprintdoorlock-8bb72.firebaseio.com",
    "projectId": "fingerprintdoorlock-8bb72",
    "storageBucket": "fingerprintdoorlock-8bb72.appspot.com",
    "messagingSenderId": "462227919420",
    "appId": "1:462227919420:web:87fb3f149c465f8e7b2939",
    "measurementId": "G-JJLHWCR9PR"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()
auth = firebase.auth()
email = "k.shahzaib2019@gmail.com"
password = "shariq0667111"
user = auth.sign_in_with_email_and_password(email, password)
def imageSend(name):
    ref = db.reference('/image')
    my_image = name
    temp  = ''
    if (temp != name):
        print("sadsdasd")
        # Upload Image
        temp = name
        storage.child(my_image).put(my_image)

        # Download Image
        storage.child(my_image).download(filename="myself.jpg", path=name)

        # Get url of image

        url = storage.child(my_image).get_url(user['idToken'])
        print(url)
        x = datetime.datetime.now().strftime("%H:%M:%S  , %b %d,%Y")
        ref.push({'date':x,'imgUrl':url})
    else:
        print("sss")
