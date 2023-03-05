"""Check if the database contains data in the right spot.
If there is no data, inject the seed-dataset.
"""

import os
import json
from typing import Dict
from pymongo import MongoClient


# Setup db-connection using config from environment
IP=os.environ["MONGO_IP"]
Port=int(os.environ["MONGO_PORT"])
User=os.environ["MONGO_USER"]
Password=os.environ["MONGO_PASSWORD"]
Database=os.environ["MONGO_DB"]
Collection=os.environ["MONGO_COLLECTION"]


client = MongoClient (host=IP, port=Port,username=User, password=Password )
db = client [Database]
collection = db[Collection]

# Only insert data if collection does not have any entries
numberEntries = collection.count_documents ({})

if numberEntries == 0:
    with open ("/app/data.json", encoding="utf-8") as dataFile:
        data = json.load(dataFile)
        collection.insert_many (data)   

        print ("inserted seed-data")     

else:
    print ("database already contains entries, will not insert seed-data")
