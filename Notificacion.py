import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = "mensajeriaap2025@gmail.com"
receiver_email = "aagudelo.investigacion@andrespublicidadtg.com"
password = os.getenv("EMAIL_PASSWORD")
session_url = os.getenv("SESSION_URL")

def send_email_notificacion():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Notificacion de cierre de sesion"

    body = "La sesion de WhatsApp del emisor del tarot y la numerologia se ha cerrado"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def check_session():
    headers = {
        "Origin": os.getenv("ORIGIN_URL"),
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }
    try:
        response= requests.get(session_url, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if not data.get("clients"):
                send_email_notificacion()
        else:
            send_email_notificacion()
    except requests.exceptions.RequestException as e:
        send_email_notificacion()

import time

while True:
    check_session()
    time.sleep(1800)