from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MOTHERSHIP"}

app.get("/home")
def home():
    return {"message": "HOME"}

class SquidInstruction():

    def __init__(self):
        # TODO