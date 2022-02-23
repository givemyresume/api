import os
import smtplib

def sendmail(to, url, name):
    sender = "subhayu@givemyresume.tech"
    password = os.getenv("EMAIL_PASS")
    subject = "Hooray!!! Your resume has been created"
    smtpserver = smtplib.SMTP("smtp.givemyresume.tech:587")
    smtpserver.login(sender, password)
    header = f'To:{to}\nFrom:{sender}\nSubject:{subject}\n'
    print(to, url, name)
    msg = header + f'\n Hello, {name}\n\n You can now view your resume at {url}\n\n'
    smtpserver.sendmail(sender, to, msg)
    smtpserver.close()
