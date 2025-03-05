import requests
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
receiver_emails = os.getenv("RECEIVER_EMAIL").split(",")
password = os.getenv("EMAIL_PASSWORD")
session_url = os.getenv("SESSION_URL")

def send_email_notificacion():
    for receiver_email in receiver_emails:
        logging.info("Enviado notificacion por email...")
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Notificacion de cierre de sesion"
        body = "La sesion de WhatsApp del emisor del tarot y la numerologia se ha cerrado"
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info("Notificacion enviada.")

def check_session():
    logging.info("Verificando el estado de la sesion")
    headers = {
        "Origin": os.getenv("ORIGIN_URL"),
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }
    try:
        response= requests.get(session_url, headers=headers)
        logging.info(f"Codigo de estado: {response.status_code}")
        print(response)
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Respuesta del servidor: {data}")
            print(data)
            if not data.get("clients"):
                logging.info("La lista de clientes esta vacia. Enviando notificacion")
                send_email_notificacion()
        else:
            logging.warning("Codigo de estado de error. Enviando Notificacion")
            send_email_notificacion()
    except requests.exceptions.RequestException as e:
        logging.error(f"Excepcion en la solicitud: {e}. Enviando Notificacion")
        send_email_notificacion()

import time

while True:
    check_session()
    time.sleep(1800)