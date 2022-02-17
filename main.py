from email import message
import os
from fastapi import FastAPI, Request
from faunadb import query as q
from faunadb.client import FaunaClient
from src.json_to_md import write_to_file


app = FastAPI()
client = FaunaClient(secret="fnAEffAgzSACTABvMpg2lOwlPquGo_oNvuN1XHbA")
indexes = client.query(q.paginate(q.indexes()))


@app.get("/resume/{user}")
async def read_item(user: str):
    try:
        is_signed_up = client.query(q.get(q.match(q.index("users_index"), user)))
        try:
            data = client.query(q.get(q.match(q.index("resume_index"), user)))["data"]
            write_to_file(data)
            os.system("./push.sh")
            return {
                "status": "SUCCESS",
                "message": "Done"
            }
        except:
            return {
                "status": "FAILED",
                "message": "No data found. Try saving your data by sending it to the '/savedata' endpoint."
            }
    except:
        return {
            "status": "FAILED",
            "context": "User not found with the given username. Have you signed up yet?"
        }


@app.post("/savedata")
async def savedata(signupData : Request):
    data = await signupData.json()
    try:
        resume = client.query(q.get(q.match(q.index("resume_index"), data["user"])))
        quiz = client.query(q.update(q.ref(q.collection("Resume_Info"),resume["ref"].id()), {
            "data": data
        }))

        return {
            "status" : "SUCCESS",
            "message": "Data Updated"
        }

    except:
        quiz = client.query(q.create(q.collection("Resume_Info"), {
            "data": data
        }))

        return {
            "status" : "SUCCESS",
            "message": "Data Created"
        }

