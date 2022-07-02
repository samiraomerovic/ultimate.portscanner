"""
Samira Omerovic
CYBR-260-40
Week 7: Final Project
July 1, 2022

This class is used to send emails with customised bodies.
"""

import configparser
import os
import smtplib
from email.message import EmailMessage

server = None
configFile = os.path.dirname(os.path.abspath(__file__)) + "/config.cfg"
email = ""


def connect() -> None:
    """
    This function makes a connection with the e-mail server by making use of the credentials from the config file.
    :return: None
    """
    global email
    global server

    config = configparser.ConfigParser()
    config.read(configFile)

    # Get the information needed from the configuration file
    server = config['MAIL']['server']
    port = config['MAIL']['port']
    email = config['MAIL']['email']
    password = config['MAIL']['password']

    # Setup connection through SMTP
    server = smtplib.SMTP(server, int(port))
    server.starttls()
    server.ehlo()
    server.login(email, password)


def connection_exists() -> bool:
    """
    This function returns whether a connection is active with the e-mail server.
    :return: True if connection exists, False otherwise
    """
    return server is not None


def sendemail(message: str, target: str) -> None:
    """
    This function sends an e-mail to the target e-mail with a custom message as the body.
    The function makes use of the existing server connection, for which a check is in place.
    :param message: Message to be placed in the body of the e-mail
    :param target: target e-mail
    :return: None
    """
    global email
    global server
    if connection_exists():
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = "Ultimate Port Scanner results!"
        msg["From"] = email
        msg["To"] = target
        server.send_message(msg)


def close() -> None:
    """
    Closes the connection with the server if a connection exists.
    :return:
    """
    global server

    if connection_exists():
        server.quit()
