"""Check if the database contains data in the right spot.
If there is no data, inject the seed-dataset.
"""

import os
import json
from typing import Dict
from pymongo import MongoClient

print ("SEEEEEDER111")

IP=os.environ["MONGO_IP"]
Port=int(os.environ["MONGO_PORT"])
User=os.environ["MONGO_USER"]
Password=os.environ["MONGO_PASSWORD"]
Database=os.environ["MONGO_DB"]
Collection=os.environ["MONGO_COLLECTION"]

print (IP)
print (Password)
print (os.getcwd())

# TODO: das muss durch urllib.parse.quote_plus gehen!
client = MongoClient (host=IP, port=Port,username=User, password=Password )

db = client [Database]
collection = db[Collection]




def readData (filePath: str) -> Dict:
    with open (filePath, encoding="utf-8") as dataFile:
        data = json.load(dataFile)
        return data

data = readData ("/app/data.json")
print (data)


for item in data:
    print (str(item))
    collection.insert_one(item)