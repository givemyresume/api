import os, json, re
from src.md_to_html_and_pdf import make_html, write_pdf


def write_to_file(data):
    md = f"""{personal(data)}

{skill(data)}

{education(data)}

{experience(data)}

{project(data)}
"""


    givemyresume_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'givemyresume.github.io')
    user_dir = f"{givemyresume_folder}/{data['user']}"

    if not os.path.isdir(f"{user_dir}"):
        try:
            os.mkdir(f"{user_dir}")
        except:
            print(f"cannot create '{user_dir}'!")
    
    mdfile = f"{user_dir}/resume.md"
    with open(mdfile, "w+") as f:
        f.write(md)

    with open(f"{user_dir}/data.json", "w") as j:
        json.dump(data, j)

    prefix = f"{user_dir}/index"

    html = make_html(md, prefix=prefix, css_path=f"{os.path.dirname(__file__)}/resume.css")

    with open(prefix + ".html", "w", encoding="utf-8") as htmlfp:
        htmlfp.write(html)

    if os.getenv("CHROME_ENABLED")=="yes":
        write_pdf(html, prefix=prefix, chrome="")
    else:
        print("Chrome is not enabled... PDF cannot be generated!")

    with open(f"{givemyresume_folder}/index.html", "r") as htmlfp:
        html_content = htmlfp.read()

    with open(f"{givemyresume_folder}/README.md", "r") as readme:
        readme_content = readme.read()
    
    if not re.search(f"'{data['user']}'", html_content) and not re.search(f"/{data['user']}\)", readme_content):
        with open(f"{givemyresume_folder}/index.html", "w") as htmlfp:
            content_to_add = f"    <a href='{data['user']}'>{data['full_name']}'s resume</a>"
            html_content = html_content.split("\n")
            html_content.insert(-2, content_to_add)
            htmlfp.write("\n".join(html_content))

        with open(f"{givemyresume_folder}/README.md", "a") as readme:
            content_to_add = f"  - [{data['full_name']}](https://givemyresume.github.io/{data['user']})\n"
            readme.write(content_to_add)



def personal(data):
    res = f"""# {data["full_name"]}

- <{data["email"]}>
"""
    if data["phone"]:
       res += f"""- {data["phone"]}
"""
    if data["website"]:
        res += f"""- [{re.sub("(https?://|/.*$)", "", data["website"])}]({data["website"]})
"""
    if data["address"]:
       res += f"""- {data["address"]}
"""
    if data["summary"]:
       res += f"""
{data["summary"]}
"""
    return res


def skill(data):
    res = """## Skills
"""
    for i in data["skills"].split("\n"):
        if not i=="":
            res += f"""  - {i}
"""
    return res


def experience(data):
    res = """## Experience
"""
    for i in data["job"]:
        if not data["job"][i]["position"]=="":
            res += f"""
### <span>{data["job"][i]["position"]}, {data["job"][i]["employer"]}</span> <span>{data["job"][i]["start"]} -- {data["job"][i]["end"]}</span>

"""
        for j in data["job"][i]["details"].split("\n"):
            if not j=="":
                res += f"""  - {j}
"""
    return res


def education(data):
    res = """## Education
"""
    for i in data["education"]:
        if not data["education"][i]["school"]=="":
            res += f"""
### <span>{data["education"][i]["school"]}</span> <span>{data["education"][i]["start"]} -- {data["education"][i]["end"]}</span>

"""
        for j in data["education"][i]["details"].split("\n"):
            if not j=="":
                res += f"""  - {j}
"""
    return res


def project(data):
    res = """## Projects
"""
    for i in data["project"]:
        if not data["project"][i]["name"]=="":
            res += f"""
### <span>{data["project"][i]["name"]}</span> <span>{data["project"][i]["end"]}</span>

"""
        for j in data["project"][i]["details"].split("\n"):
            if not j=="":
                res += f"""  - {j}
"""
    return res
