import smtplib
import os

def sendmail(to, url, name):
    sender = "subhayu@givemyresume.tech"
    password = os.getenv("EMAIL_PASS")
    subject = "Your resume has been created"
    smtpserver = smtplib.SMTP("smtp.givemyresume.tech:587")
    smtpserver.login(sender, password)
    header = f'To:{to}\nFrom:{sender}\nSubject:{subject}\n'
    msg = header + f'''
Hello, {name}

Your resume has been created and will be live in a minute at {url}

Here are some things you should know:
To download your resume as pdf
    On PC
        - Press `Ctrl + P` keys or right click on the page and select `Print...`
        - Select `Save as PDF`
        - Click `Save`
    On Mobile Phones
        - From the browser menu select `Share`
        - Now select the `Print` option
        - Set your desired paper configurations
        - Click the icon with PDF download sign on it 
        - Select where to save and click `Save`
    - In both cases remember to turn off Headers & Footers

Additionaly, you can share the link to share your resume with others

Thank you for using givemyresume.tech
'''
    smtpserver.sendmail(sender, to, msg)
    smtpserver.close()
