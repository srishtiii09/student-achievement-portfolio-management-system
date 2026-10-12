"""
Goals module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to add, view, update, and count
student goals.
"""

from mysql.connector import Error

from backend.db import connect_db
from backend.validation import validate_empty_field, validate_goal_status


def add_goal(
    student_id,
    goal_title,
    status,
    deadline
):
    """Add a new goal for a student."""

    if not validate_empty_field(goal_title):
        print("Goal title cannot be empty.")
        return False

    if not validate_goal_status(status):
        print("Invalid goal status.")
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
        INSERT INTO Goals
        (Student_ID, Goal_Title, Status, Deadline)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            student_id,
            goal_title,
            status,
            deadline,
        )

        cursor.execute(query, values)
        connection.commit()

        print("Goal added successfully.")
        return True

    except Error as error:
        print("Error while adding goal:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_goals(student_id):
    """Return all goals for a student as a list of tuples."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Goal_ID, Student_ID, Goal_Title, Status, Deadline
        FROM Goals
        WHERE Student_ID = %s
        ORDER BY Deadline
        """
        cursor.execute(query, (student_id,))
        goals = cursor.fetchall()

        return goals

    except Error as error:
        print("Error while fetching goals:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def update_goal_status(goal_id, new_status):
    """Update the status of a goal."""

    if not validate_goal_status(new_status):
        print("Invalid goal status.")
        return False

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()

        query = "UPDATE Goals SET Status = %s WHERE Goal_ID = %s"
        cursor.execute(query, (new_status, goal_id))
        connection.commit()

        print("Goal status updated successfully.")
        return True

    except Error as error:
        print("Error while updating goal status:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_completed_goals(student_id):
    """Return the number of completed goals for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = """
        SELECT COUNT(*)
        FROM Goals
        WHERE Student_ID = %s AND Status = %s
        """
        cursor.execute(query, (student_id, "Completed"))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    except Error as error:
        print("Error while counting completed goals:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_pending_goals(student_id):
    """Return the number of pending or in-progress goals for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = """
        SELECT COUNT(*)
        FROM Goals
        WHERE Student_ID = %s AND (Status = %s OR Status = %s)
        """
        cursor.execute(query, (student_id, "Pending", "In Progress"))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    except Error as error:
        print("Error while counting pending goals:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Adding sample goal:")
    add_goal(1, "Complete Computer Science Project", "Pending", "2026-08-31")

    print("All goals:")
    print(get_goals(1))

    print("Updating goal status:")
    update_goal_status(1, "Completed")

    print("Completed goal count:")
    print(count_completed_goals(1))

    print("Pending goal count:")
    print(count_pending_goals(1))
