import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import json
import os

from keys import gen
from keys import birthdate

#firebase
cred = credentials.Certificate(os.getcwd() + "\\sAK.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
db_doc_name = "floop-keys"

# Get the keys from the database
def createkey_fb(userid, key, days):
    keys_doc = db.collection(db_doc_name).document(key)
    data = ({
        'adminuid': userid,
        'date-of-creation': birthdate(), 
        'date-of-expiration': "",
        'length': days,
        'useruid': "",
    })
    keys_doc.set(data)


# Generate the keys

# input how many days
days = int(input("How many days? "))
# input how many keys
keys = int(input("How many keys? "))

for i in range(keys):
    key = gen(days)
    print(key)
    createkey_fb("5261828597", key, days)

print("Done")