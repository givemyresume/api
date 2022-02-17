import requests
import base64
import json

def push_to_github(filename, path, repo, branch, token):
    url="https://api.github.com/repos/"+repo+"/contents/"+path

    base64content=base64.b64encode(open(filename,"rb").read())

    data = requests.get(url, headers = {"Authorization": "token "+token, "Accept": "application/vnd.github.v3+json"}).json()
    print(data)
    sha = data['sha']

    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message":"update",
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")

token = "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"
filename="/home/subhayu/Downloads/ResumeBuilder/api/saved_data/subhayu99/data.json"
path="subhayu99/data.json"
repo = "subhayu99/saved_resumes"
branch="main"

push_to_github(filename, path, repo, branch, token)

