import os, json
from src.md_to_html_and_pdf import make_html, write_pdf


def write_to_file(data):
    md = f"""{personal(data)}

{skill(data)}

{education(data)}

{experience(data)}

{project(data)}
"""

    script_dir = os.path.dirname(__file__)
    saved_data_folder = '/'.join(script_dir.split('/')[:-2])+'/saved_data'
    user_dir = f"{saved_data_folder}/{data['user']}"

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

    html = make_html(md, prefix=prefix, css_path=f"{script_dir}/resume.css")

    with open(prefix + ".html", "w", encoding="utf-8") as htmlfp:
        htmlfp.write(html)

    write_pdf(html, prefix=prefix, chrome="")





def personal(data):
    res = f"""# {data["full_name"]}

- <{data["email"]}>
"""
    if data["phone"]:
       res += f"""- {data["phone"]}
"""
    if data["website"]:
        res += f"""- [{data["website"]}]({data["website"]})
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
        res += f"""  - {i}
"""
    return res


def experience(data):
    res = """## Experience
"""
    for i in data["job"]:
        res += f"""
### <span>{data["job"][i]["position"]}, {data["job"][i]["employer"]}</span> <span>{data["job"][i]["start"]} -- {data["job"][i]["end"]}</span>

"""
        for j in data["job"][i]["details"].split("\n"):
            res += f"""  - {j}
"""
    return res


def education(data):
    res = """## Education
"""
    for i in data["education"]:
        res += f"""
### <span>{data["education"][i]["school"]}</span> <span>{data["education"][i]["start"]} -- {data["education"][i]["end"]}</span>

"""
        for j in data["education"][i]["details"].split("\n"):
            res += f"""  - {j}
"""
    return res


def project(data):
    res = """## Projects
"""
    for i in data["project"]:
        res += f"""
### <span>{data["project"][i]["name"]}</span> <span>{data["project"][i]["end"]}</span>

"""
        for j in data["project"][i]["details"].split("\n"):
            res += f"""  - {j}
"""
    return res
