import smtplib

def sendmail(to, url, name):
    sender = "subhayu@givemyresume.tech"
    with open("./cred.txt") as c:
        password = c.readline()
        print(password)
    subject = "Hooray!!! Your resume has been created"
    smtpserver = smtplib.SMTP("smtp.givemyresume.tech:587")
    smtpserver.login(sender, password)
    header = f'To:{to}\nFrom:{sender}\nSubject:{subject}\n'
    msg = header + f'\n Hello, {name}\n\n You can now view your resume at {url}\n\n'
    smtpserver.sendmail(sender, to, msg)
    smtpserver.close()
