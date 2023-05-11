from pymongo import MongoClient
from pymongo import errors
import os

#[Environment]::SetEnvironmentVariable("KEY", "VALUE", "[MACHINE, USER, PROCESS]")

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")

def get_database():
    
    conn = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@homenet-asia-mongodb-de.4sgvde0.mongodb.net'
    client = MongoClient(conn)

    return client['mothershipdb']


def insert_document(collection_name, document):
    mothershipdb = get_database()
    collection = mothershipdb[collection_name]

    try:
        collection.insert_one(document.to_mongo())
        return f'MONGO INSERTED: {document.to_mongo()}'
    except errors.DuplicateKeyError as err:
        return f'MONGO DUPLICATE KEY ERROR: {document.to_mongo()}'