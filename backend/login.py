"""
Student login module for the Student Achievement & Portfolio Management System.

This file contains a reusable function to validate student login details
and check them with the Students table.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_email, validate_password


def login_student(email, password):
    """Validate login details and return student information if login succeeds."""

    if not validate_email(email):
        print("Please enter a valid email address.")
        return None

    if not validate_password(password):
        print("Password must have at least 6 characters.")
        return None

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return None

        cursor = connection.cursor()

        # Search for the student using the email address.
        query = """
        SELECT Student_ID, Full_Name, Student_Class, Section, Email, Password
        FROM Students
        WHERE Email = %s
        """
        cursor.execute(query, (email,))
        student = cursor.fetchone()

        if student is None:
            print("User not found.")
            return None

        saved_password = student[5]

        if password != saved_password:
            print("Incorrect password.")
            return None

        student_details = {
            "Student_ID": student[0],
            "Full_Name": student[1],
            "Student_Class": student[2],
            "Section": student[3],
            "Email": student[4],
        }

        print("Login successful.")
        return student_details

    except Error as error:
        print("Error while logging in:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    login_student("aarav@example.com", "pass123")
