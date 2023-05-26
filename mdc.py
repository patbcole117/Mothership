from pymongo import MongoClient
from pymongo import errors
import os

#[Environment]::SetEnvironmentVariable("KEY", "VALUE", "[MACHINE, USER, PROCESS]")

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_URL = os.environ.get("MONGO_URL")

def get_database():
    
    conn = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_URL}-mongodb-de.4sgvde0.mongodb.net'
    client = MongoClient(conn)

    return client['mothershipdb']


def insert_document(collection_name, document):
    mothershipdb = get_database()
    collection = mothershipdb[collection_name]

    try:
        collection.insert_one(document)
        return f'MONGO INSERTED: {document}'
    except errors.DuplicateKeyError as err:
        return f'MONGO DUPLICATE KEY ERROR IN {document}'

def find_document(collection_name, key, value):
    mothershipdb = get_database()
    collection = mothershipdb[collection_name]

    document = collection.find_one({key: value})
    return document