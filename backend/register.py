"""
Student registration module for the Student Achievement & Portfolio Management System.

This file contains a reusable function to validate student details and
register a new student in the Students table.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.student_ids import get_smallest_available_student_id
from backend.validation import (
    validate_email,
    validate_empty_field,
    validate_password,
    validate_phone,
)


def register_student(
    full_name,
    student_class,
    section,
    email,
    phone,
    career_interest,
    password
):
    """Validate student details and register the student in the database."""
    # Basic field validations with clear messages
    if not validate_empty_field(full_name):
        return False, "Full Name cannot be empty."

    if not validate_empty_field(student_class):
        return False, "Class cannot be empty."

    try:
        sc_int = int(student_class)
        if sc_int < 11 or sc_int > 12:
            return False, "Class must be between 11 and 12."
    except Exception:
        return False, "Class must be a number between 11 and 12."

    if not validate_empty_field(section):
        return False, "Section cannot be empty."

    if not validate_empty_field(email) or not validate_email(email):
        return False, "Email format is invalid."

    if not validate_empty_field(phone) or not validate_phone(phone):
        return False, "Phone number must contain exactly 10 digits."

    if not validate_empty_field(password) or not validate_password(password):
        return False, "Password must contain at least 6 characters."

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            return False, "Database connection failed."

        cursor = connection.cursor()

        # Allocate and insert the ID as one transaction.
        connection.start_transaction()

        check_query = "SELECT Student_ID, Full_Name, Student_Class, Section, Email FROM Students WHERE Email = %s"
        cursor.execute(check_query, (email,))
        existing_student = cursor.fetchone()

        if existing_student is not None:
            connection.rollback()
            return False, "Email already exists."

        # AUTO_INCREMENT cannot fill gaps in the middle of the ID sequence.
        # Select the existing IDs and explicitly insert the first missing one.
        cursor.execute("SELECT Student_ID FROM Students ORDER BY Student_ID FOR UPDATE")
        existing_ids = [row[0] for row in cursor.fetchall()]
        student_id = get_smallest_available_student_id(existing_ids)

        insert_query = """
        INSERT INTO Students
        (Student_ID, Full_Name, Student_Class, Section, Email, Phone, Career_Interest, Password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        student_data = (
            student_id,
            full_name,
            student_class,
            section,
            email,
            phone,
            career_interest,
            password,
        )

        cursor.execute(insert_query, student_data)
        connection.commit()

        student_details = {
            "Student_ID": student_id,
            "Full_Name": full_name,
            "Student_Class": student_class,
            "Section": section,
            "Email": email,
        }

        return True, student_details

    except Error as error:
        if connection is not None:
            connection.rollback()
        return False, f"Error while registering student: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    register_student(
        "Aarav Sharma",
        "12",
        "A",
        "aarav@example.com",
        "9876543210",
        "Computer Science",
        "pass123"
    )
