"""
Activities module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to add, view, search, and count
student activity records.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_empty_field


def add_activity(
    student_id,
    activity_name,
    category,
    level,
    organizer,
    activity_date
):
    """Add a new activity record for a student."""

    if not validate_empty_field(activity_name):
        print("Activity name cannot be empty.")
        return False

    if not validate_empty_field(category):
        print("Category cannot be empty.")
        return False

    if not validate_empty_field(level):
        print("Level cannot be empty.")
        return False

    if not validate_empty_field(organizer):
        print("Organizer cannot be empty.")
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
        INSERT INTO Activities
        (Student_ID, Activity_Name, Category, Level, Organizer, Activity_Date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            student_id,
            activity_name,
            category,
            level,
            organizer,
            activity_date,
        )

        cursor.execute(query, values)
        connection.commit()

        print("Activity added successfully.")
        return True

    except Error as error:
        print("Error while adding activity:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_activities(student_id):
    """Return all activities for a student as a list of tuples."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Activity_ID, Student_ID, Activity_Name, Category, Level,
               Organizer, Activity_Date
        FROM Activities
        WHERE Student_ID = %s
        ORDER BY Activity_Date DESC
        """
        cursor.execute(query, (student_id,))
        activities = cursor.fetchall()

        return activities

    except Error as error:
        print("Error while fetching activities:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_activities_by_category(student_id, category):
    """Return activities that match the given category for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Activity_ID, Student_ID, Activity_Name, Category, Level,
               Organizer, Activity_Date
        FROM Activities
        WHERE Student_ID = %s AND Category = %s
        ORDER BY Activity_Date DESC
        """
        cursor.execute(query, (student_id, category))
        activities = cursor.fetchall()

        return activities

    except Error as error:
        print("Error while searching activities by category:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_activities_by_level(student_id, level):
    """Return activities that match the given level for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Activity_ID, Student_ID, Activity_Name, Category, Level,
               Organizer, Activity_Date
        FROM Activities
        WHERE Student_ID = %s AND Level = %s
        ORDER BY Activity_Date DESC
        """
        cursor.execute(query, (student_id, level))
        activities = cursor.fetchall()

        return activities

    except Error as error:
        print("Error while searching activities by level:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_activities(student_id):
    """Return the total number of activities for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Activities WHERE Student_ID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    except Error as error:
        print("Error while counting activities:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Adding sample activity:")
    add_activity(
        1,
        "Debate Competition",
        "Public Speaking",
        "School",
        "ABC Public School",
        "2026-07-07"
    )

    print("All activities:")
    print(get_activities(1))

    print("Activities by category:")
    print(search_activities_by_category(1, "Public Speaking"))

    print("Activities by level:")
    print(search_activities_by_level(1, "School"))

    print("Total activity count:")
    print(count_activities(1))
