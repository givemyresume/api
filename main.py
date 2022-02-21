import os
from fastapi import FastAPI, Request
from faunadb import query as q
from faunadb.client import FaunaClient
from src.json_to_md import write_to_file


app = FastAPI()
FAUNA_DB_KEY = os.getenv("FAUNA_DB_KEY")


client = FaunaClient(secret=FAUNA_DB_KEY)
indexes = client.query(q.paginate(q.indexes()))


@app.get("/")
async def root():
    info = {
    "availabe_routes": 
    {
        "/schema": "JSON schema to send at /savedata", 
        "/savedata": "save your data to the databasse", 
        "/resume/{user}": "replace {user} with the username you used to register or save data"
    }
}
    return 


@app.get("/schema")
async def send_schema():
    schema = {
    "user": "foo-bar",
    "full_name": "foo-bar",
    "address": "foo-bar",
    "phone": "foo-bar",
    "email": "foo-bar",
    "website": "foo-bar",
    "summary": "foo-bar",
    "skills": "foo-bar",
    "education": {
        "1": {
            "school": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "2": {
            "school": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "3": {
            "school": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        }
    },
    "job": {
        "1": {
            "employer": "foo-bar",
            "position": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "2": {
            "employer": "foo-bar",
            "position": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "3": {
            "employer": "foo-bar",
            "position": "foo-bar",
            "start": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        }
    },
    "project": {
        "1": {
            "name": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "2": {
            "name": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        },
        "3": {
            "name": "foo-bar",
            "end": "foo-bar",
            "details": "foo-bar"
        }
    },
    "references": "foo-bar"
}
    return schema


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
                "message": f"Visit https://givemyresume.github.io/{data['user']} to download your resume"
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

