from pymongo import MongoClient
import os

#[Environment]::SetEnvironmentVariable("KEY", "VALUE", "[MACHINE, USER, PROCESS]")

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")

def get_database():
    
    conn = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@homenet-asia-mongodb-de.4sgvde0.mongodb.net'
    client = MongoClient(conn)

    return client['mothershipdb']
