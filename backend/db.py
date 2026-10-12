"""
Database connection module for the Student Achievement & Portfolio Management System.

This file contains a reusable function to connect the Python project with
the MySQL database named student_portfolio.
"""

import mysql.connector
from mysql.connector import Error


def connect_db():
    """
    Connect to the student_portfolio MySQL database.

    Returns:
        connection: MySQL connection object if the connection is successful.
        None: If the connection fails.
    """

    try:
        # Create a connection with the MySQL database.
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="student_portfolio"
        )

        # Check whether the connection was successful.
        if connection.is_connected():
            print("Connected to MySQL successfully.")
            return connection

    except Error as error:
        # Display a simple error message if connection fails.
        print("Error while connecting to MySQL:", error)

    return None


if __name__ == "__main__":
    db_connection = connect_db()

    if db_connection is not None:
        db_connection.close()
        print("MySQL connection closed.")
