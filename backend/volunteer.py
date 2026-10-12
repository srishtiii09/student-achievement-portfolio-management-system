"""
Volunteer module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to add, view, search, and calculate
student volunteer work records.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_empty_field


def add_volunteer_record(
    student_id,
    organization,
    role,
    hours,
    volunteer_date
):
    """Add a new volunteer record for a student."""

    if not validate_empty_field(organization):
        print("Organization cannot be empty.")
        return False

    if not validate_empty_field(role):
        print("Role cannot be empty.")
        return False

    if hours <= 0:
        print("Hours must be greater than 0.")
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
        INSERT INTO Volunteer
        (Student_ID, Organization, Role, Hours, Volunteer_Date)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            student_id,
            organization,
            role,
            hours,
            volunteer_date,
        )

        cursor.execute(query, values)
        connection.commit()

        print("Volunteer record added successfully.")
        return True

    except Error as error:
        print("Error while adding volunteer record:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_volunteer_records(student_id):
    """Return all volunteer records for a student as a list of tuples."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Volunteer_ID, Student_ID, Organization, Role, Hours, Volunteer_Date
        FROM Volunteer
        WHERE Student_ID = %s
        ORDER BY Volunteer_Date DESC
        """
        cursor.execute(query, (student_id,))
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching volunteer records:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_by_organization(student_id, organization):
    """Return volunteer records from the given organization."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Volunteer_ID, Student_ID, Organization, Role, Hours, Volunteer_Date
        FROM Volunteer
        WHERE Student_ID = %s AND Organization = %s
        ORDER BY Volunteer_Date DESC
        """
        cursor.execute(query, (student_id, organization))
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while searching volunteer records:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def calculate_total_hours(student_id):
    """Return the total volunteer hours for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT SUM(Hours) FROM Volunteer WHERE Student_ID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result is None or result[0] is None:
            return 0

        return int(result[0])

    except Error as error:
        print("Error while calculating volunteer hours:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_volunteer_events(student_id):
    """Return the total number of volunteer events for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Volunteer WHERE Student_ID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    except Error as error:
        print("Error while counting volunteer events:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Adding sample volunteer record:")
    add_volunteer_record(
        1,
        "Community Cleanliness Club",
        "Volunteer",
        5,
        "2026-07-07"
    )

    print("All volunteer records:")
    print(get_volunteer_records(1))

    print("Volunteer records by organization:")
    print(search_by_organization(1, "Community Cleanliness Club"))

    print("Total volunteer hours:")
    print(calculate_total_hours(1))

    print("Total volunteer events:")
    print(count_volunteer_events(1))
