"""
Academics module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to add, view, and calculate academic
records for students.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_marks


def add_academic_record(
    student_id,
    subject,
    exam_type,
    marks_obtained,
    maximum_marks
):
    """Add a new academic record for a student."""

    if subject.strip() == "":
        print("Subject cannot be empty.")
        return False

    if exam_type.strip() == "":
        print("Exam type cannot be empty.")
        return False

    if not validate_marks(marks_obtained, maximum_marks):
        print("Marks are not valid.")
        return False

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()

        query = """
        INSERT INTO Academics
        (Student_ID, Subject, Exam_Type, Marks_Obtained, Maximum_Marks)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            student_id,
            subject,
            exam_type,
            marks_obtained,
            maximum_marks,
        )

        cursor.execute(query, values)
        connection.commit()

        print("Academic record added successfully.")
        return True

    except Error as error:
        print("Error while adding academic record:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_academic_records(student_id):
    """Return all academic records for a student as a list of tuples."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Record_ID, Student_ID, Subject, Exam_Type, Marks_Obtained, Maximum_Marks
        FROM Academics
        WHERE Student_ID = %s
        ORDER BY Subject
        """
        cursor.execute(query, (student_id,))
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching academic records:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def calculate_average_marks(student_id):
    """Calculate and return the average percentage for a student."""

    records = get_academic_records(student_id)

    if len(records) == 0:
        return 0

    total_percentage = 0

    for record in records:
        marks_obtained = record[4]
        maximum_marks = record[5]
        percentage = (marks_obtained / maximum_marks) * 100
        total_percentage = total_percentage + percentage

    average = total_percentage / len(records)
    return round(average, 2)


def get_highest_score(student_id):
    """Return the subject with the highest percentage score."""

    records = get_academic_records(student_id)

    if len(records) == 0:
        return None

    highest_record = records[0]
    highest_percentage = (highest_record[4] / highest_record[5]) * 100

    for record in records:
        percentage = (record[4] / record[5]) * 100

        if percentage > highest_percentage:
            highest_percentage = percentage
            highest_record = record

    return highest_record[2], highest_record[4], highest_record[5]


def get_lowest_score(student_id):
    """Return the subject with the lowest percentage score."""

    records = get_academic_records(student_id)

    if len(records) == 0:
        return None

    lowest_record = records[0]
    lowest_percentage = (lowest_record[4] / lowest_record[5]) * 100

    for record in records:
        percentage = (record[4] / record[5]) * 100

        if percentage < lowest_percentage:
            lowest_percentage = percentage
            lowest_record = record

    return lowest_record[2], lowest_record[4], lowest_record[5]


if __name__ == "__main__":
    print("Adding academic record:")
    print(add_academic_record(1, "Computer Science", "Unit Test", 45, 50))

    print("Academic records:")
    print(get_academic_records(1))

    print("Average percentage:")
    print(calculate_average_marks(1))

    print("Highest score:")
    print(get_highest_score(1))

    print("Lowest score:")
    print(get_lowest_score(1))
