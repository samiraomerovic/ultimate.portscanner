"""
Samira Omerovic
CYBR-260-40
Week 7: Final Project
July 1, 2022

This class is used for the account functionality
"""

import hashlib
import uuid
from datetime import date
import Connect
import Queries


def generate_salt() -> str:
    """
    This function generates a salt
    :return: String object of the generated salt
    """
    return uuid.uuid4().hex


def hash(password: str, salt: str) -> str:
    """
    This function hashes the password with a given salt and returns the result.
    :param password: The password to be hashed.
    :param salt: The salt to be used for the hashing process.
    :return: Hashed password
    """
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()


def email_exists(email: str) -> bool:
    """
    This function checks whether an entry of this email already exists in the database
    :param email: The email to be checked
    :return: True if email already exists, False otherwise
    """
    if email is None or email == "":
        return True

    query = "SELECT COUNT(*) FROM {0}.login WHERE email = %s;".format(Connect.db)
    result = Queries.get_single_query(query, email)

    # Returns true if result caused an error
    return bool(result) if query is not None else True


def register(email: str, password: str) -> bool:
    """
    Inserts account into database after validation
    :param email: The email to be inserted
    :param password: The password to be inserted
    :return: True if insertion is successful, False otherwise
    """
    if Connect.connect_exists() and email is not None and password is not None and email != "" and password != "":
        if email_exists(email):
            print("Error: Email already exists!")
            return False

        # Salt and hash the password
        salt = generate_salt()
        hashed_pass = hash(password, salt)

        # Insert into database
        query = "INSERT INTO {0}.login VALUES (%s, %s, %s);".format(Connect.db)
        tuple = (email, hashed_pass, salt)
        Queries.execute_query(query, tuple)

        return True

    return False


def login(email: str, password: str) -> bool:
    """
    This function checks whether the password matches the password in the database with the given email.
    :param email: The email to be checked
    :param password: The password to be checked
    :return: True if the two passwords are equal, False otherwise
    """
    if Connect.connect_exists() and email is not None and password is not None and email != "" and password != "":
        if not email_exists(email):
            return False

        query_salt = "SELECT salt FROM {0}.login WHERE email = %s;".format(Connect.db)
        salt = Queries.get_single_query(query_salt, email)
        query_pass = "SELECT hash FROM {0}.login WHERE email = %s;".format(Connect.db)
        hashed_pass = Queries.get_single_query(query_pass, email)

        return True if hashed_pass == hash(password, salt) else False

    return False


def store_results(email: str, message: str) -> None:
    """
    This function stores the result with the email entry in the results table
    :param email: The email to be used
    :param message: the message to be stored
    :return: None
    """
    if Connect.connect_exists() and email is not None:
        query = "INSERT INTO {0}.results VALUES (%s, %s, %s, %s);".format(Connect.db)
        tuple = (None, email, message, str(date.today()))
        Queries.execute_query(query, tuple)


def get_results(email: str) -> [] or None:
    """
    This function gets all the results from the database with the given email.
    :param email: The email to be used to get the results.
    :return: Array of results or None if there is no entries
    """
    if Connect.connect_exists() and email is not None:
        query = "SELECT result, time FROM {0}.results WHERE email = %s;".format(Connect.db)
        return Queries.get_all_query(query, email)
