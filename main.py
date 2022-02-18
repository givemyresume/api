import os
from fastapi import FastAPI, Request
from faunadb import query as q
from faunadb.client import FaunaClient
from src.json_to_md import write_to_file


app = FastAPI()
FAUNA_DB_KEY = os.getenv("FAUNA_DB_KEY")


client = FaunaClient(secret=FAUNA_DB_KEY)
indexes = client.query(q.paginate(q.indexes()))


@app.get("/resume/{user}")
async def create_resume(user: str):
    try:
        is_signed_up = client.query(q.get(q.match(q.index("users_index"), user)))
        try:
            try:
                data = client.query(q.get(q.match(q.index("resume_index"), user)))["data"]
            except:
                return {
                    "status": "FAILED",
                    "message": "No data found. Try saving your data by sending it to the '/savedata' endpoint."
                }
            try:
                write_to_file(data)
            except:
                return {
                    "status": "FAILED",
                    "message": "Resume creation failed!"
                }
            os.system("./push.sh")
            return {
                "status": "SUCCESS",
                "message": f"Visit https://givemyresume.github.io/{data['user']}/index.pdf to download your resume"
            }
        except:
            return {
                "status": "FAILED",
                "message": "Oops! Something went wrong..."
            }
    except:
        return {
            "status": "FAILED",
            "message": "User not found with the given username. Have you signed up yet?"
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

