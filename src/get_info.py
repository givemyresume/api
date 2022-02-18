import requests

def push_to_github(path, repo):
    url="https://api.github.com/repos/"+repo+"/contents/"+path

    data = requests.get(url, headers = {"Accept": "application/vnd.github.v3+json"}).json()
    print(data)

path="saved_data/subhayu99/data.json"
repo = "subhayu99/resume_builder_api"

push_to_github(path, repo)

