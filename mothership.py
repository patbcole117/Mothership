from fastapi import FastAPI
from pydantic import BaseModel
from mdc import get_database, insert_document

class Squid(BaseModel):
    id: str
    name: str
    hostname: str
    mac: int
    date_created: str

    def to_mongo(self):
        return {"_id": self.id, "name": self.name, "hostname": self.hostname, "mac": self.mac, "date_created": self.date_created}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MOTHERSHIP"}

@app.get("/home")
def home():
    return {"message": "HOME"}

@app.post("/register/")
def register_squid(squid: Squid):
    response = insert_document("squids", squid)
    print(response)

