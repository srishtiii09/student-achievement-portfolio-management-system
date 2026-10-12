"""
Achievements module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to add, view, search, and count
student achievement records.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_empty_field


def add_achievement(
    student_id,
    title,
    competition,
    position,
    organization,
    achievement_date
):
    """Add a new achievement record for a student."""

    if not validate_empty_field(title):
        print("Title cannot be empty.")
        return False

    if not validate_empty_field(competition):
        print("Competition cannot be empty.")
        return False

    if not validate_empty_field(position):
        print("Position cannot be empty.")
        return False

    if not validate_empty_field(organization):
        print("Organization cannot be empty.")
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
        INSERT INTO Achievements
        (Student_ID, Title, Competition, Position, Organization, Achievement_Date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            student_id,
            title,
            competition,
            position,
            organization,
            achievement_date,
        )

        cursor.execute(query, values)
        connection.commit()

        print("Achievement added successfully.")
        return True

    except Error as error:
        print("Error while adding achievement:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_achievements(student_id):
    """Return all achievements for a student as a list of tuples."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Achievement_ID, Student_ID, Title, Competition, Position,
               Organization, Achievement_Date
        FROM Achievements
        WHERE Student_ID = %s
        ORDER BY Achievement_Date DESC
        """
        cursor.execute(query, (student_id,))
        achievements = cursor.fetchall()

        return achievements

    except Error as error:
        print("Error while fetching achievements:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_achievements_by_position(student_id, position):
    """Return achievements that match the given position for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Achievement_ID, Student_ID, Title, Competition, Position,
               Organization, Achievement_Date
        FROM Achievements
        WHERE Student_ID = %s AND Position = %s
        ORDER BY Achievement_Date DESC
        """
        cursor.execute(query, (student_id, position))
        achievements = cursor.fetchall()

        return achievements

    except Error as error:
        print("Error while searching achievements by position:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_achievements_by_organization(student_id, organization):
    """Return achievements from the given organization for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Achievement_ID, Student_ID, Title, Competition, Position,
               Organization, Achievement_Date
        FROM Achievements
        WHERE Student_ID = %s AND Organization = %s
        ORDER BY Achievement_Date DESC
        """
        cursor.execute(query, (student_id, organization))
        achievements = cursor.fetchall()

        return achievements

    except Error as error:
        print("Error while searching achievements by organization:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_achievements(student_id):
    """Return the total number of achievements for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Achievements WHERE Student_ID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    except Error as error:
        print("Error while counting achievements:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Adding sample achievement:")
    add_achievement(
        1,
        "First Prize in Coding",
        "Inter School Coding Contest",
        "First",
        "ABC Public School",
        "2026-07-07"
    )

    print("All achievements:")
    print(get_achievements(1))

    print("Achievements by position:")
    print(search_achievements_by_position(1, "First"))

    print("Achievements by organization:")
    print(search_achievements_by_organization(1, "ABC Public School"))

    print("Total achievement count:")
    print(count_achievements(1))
