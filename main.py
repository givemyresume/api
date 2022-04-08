import datetime
import hashlib
import os
import threading
from fastapi import FastAPI, HTTPException, Request, Depends
from faunadb import query as q
from faunadb.client import FaunaClient
import pytz
from src.json_to_md import write_to_file
from src.sendemail import sendmail
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from auth.oauth import get_current_user
from auth.jwttoken import create_access_token
from auth.model import User
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()
FAUNA_DB_KEY = os.getenv("FAUNA_DB_KEY")

client = FaunaClient(secret=FAUNA_DB_KEY)
indexes = client.query(q.paginate(q.indexes()))

config = Config('.env')

oauth = OAuth(config)

@app.get("/")
async def root():
    info = {
        "availabe_routes": {
            "/schema": "shows the JSON schema to POST at /savedata", 
            "/register": "let's you register to the app",
            "/login": "let's you login and get an access token",
            "/savedata": "let's you save your data to the database using the access token", 
            "/resume/{user}": "replace {user} with your registered username to generate your resume"
        }
    }
    return info


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
        user = client.query(q.get(q.match(q.index("users_index"), user)))
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
            except Exception as e:
                return {
                    "status": "FAILED",
                    "message": str(e)
                }
            os.system("./push.sh")
            print("sending email")
            threading.Timer(120, sendmail(data["email"], f"https://givemyresume.tech/{data['user']}", data["full_name"])).start()
            print("email sent")
            return {
                "status": "SUCCESS",
                "message": "We will send you an email with your resume link."
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": str(e)
            }
    except:
        return {
            "status": "FAILED",
            "message": "User not found with the given username. Have you signed up yet?"
        }


@app.post("/register")
def register(request:User):
    try:
        user = client.query(q.get(q.match(q.index("users_index"), request.username)))
    except:
        user = False
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pass = hashlib.sha512(request.password.encode()).hexdigest()
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_object["date"] =  datetime.datetime.now(pytz.UTC)
    user_id = client.query(q.create(q.collection("Users"), {
                "data": user_object 
            }))
    return {"status":"user created"}


@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    try:
        user = client.query(q.get(q.match(q.index("users_index"), request.username)))
    except:
        user = False
    if not user:
       raise HTTPException(status_code=400, detail="Username not registered")
    else:
        if not hashlib.sha512(request.password.encode()).hexdigest() == user["data"]["password"]:
            raise HTTPException(status_code=400, detail="Incorrect Password")
        access_token = create_access_token(data={"sub": user["data"]["username"] })
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/savedata")
async def savedata(signupData : Request, username = Depends(get_current_user)):
    data = await signupData.json()
    data["user"] = username
    try:
        resume = client.query(q.get(q.match(q.index("resume_index"), username)))
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

