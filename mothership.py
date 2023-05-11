from fastapi import FastAPI
from pydantic import BaseModel


class Squid(BaseModel):
    id: str
    date_created: str


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MOTHERSHIP"}

@app.get("/home")
def home():
    return {"message": "HOME"}

@app.post("/register/")
def register_squid(squid: Squid):
    print(squid)