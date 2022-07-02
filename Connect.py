"""
Samira Omerovic
CYBR-260-40
Week 7: Final Project
July 1, 2022

This class is used to make the connection with the database.
"""

import configparser
import mysql.connector
import os
from mysql.connector import MySQLConnection

configFile = os.path.dirname(os.path.abspath(__file__)) + "/config.cfg"

# Database and sql initialized
db = ""
sql = None


def getSQL() -> MySQLConnection:
    """
    This function returns the sql object with the connection.
    :return: MySQLConnection instance
    """
    return sql


def connect_exists() -> bool:
    """
    This function returns whether a connection with the database is active.
    :return: True if connection is active, False otherwise
    """
    return sql is not None and sql.cursor() is not None


def connect() -> None:
    """
    Connects to SQL database with credentials of the configuration file.
    :raise: Exception e
    :return: None
    """
    global db
    global sql

    print("SQL: Connecting...")

    config = configparser.ConfigParser()
    config.read(configFile)

    # Get information needed from configuration file.
    host = config['SQL']['host']
    user = config['SQL']['user']
    db = config['SQL']['database']

    try:
        # Make SQL connection
        sql = mysql.connector.connect(
            host=host,
            user=user,
            password=config['SQL']['password']
        )
        print("SQL: Connected to [{0}@{1}]!".format(user, host))
    except Exception as e:
        # If anything goes wrong, raise the same received exception
        raise e


def close() -> None:
    """
    This function closes the connection with the SQL database if it exists.
    :return: None
    """
    global sql

    if connect_exists():
        sql.cursor().close()
        sql.close()
        sql = None
    print("SQL: Connection closed!")


def setup_database() -> None:
    """
    This function creates the database and tables in case they do not already exist.
    :return: None
    """
    global sql

    if connect_exists():
        mycursor = sql.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS %s" % db)
        mycursor.execute("USE %s" % db)

        # Create the login table
        mycursor.execute('CREATE TABLE IF NOT EXISTS login (%s, %s, %s)' %
            ("email VARCHAR(255) PRIMARY KEY", "hash VARCHAR(255) NOT NULL", "salt VARCHAR(255) NOT NULL"))

        # Create the results table
        mycursor.execute('CREATE TABLE IF NOT EXISTS results (%s, %s, %s, %s, %s);' %
            ("id INT AUTO_INCREMENT PRIMARY KEY", "email VARCHAR(255)", "result VARCHAR(255)", "time VARCHAR(255)", "FOREIGN KEY(email) REFERENCES login(email)"))

        sql.commit()


def drop_database() -> None:
    """
    This function deletes the database from the database.
    :return:
    """
    global sql

    if connect_exists():
        mycursor = sql.cursor()
        mycursor.execute("DROP DATABASE {0};".format(db))
        sql.commit()
