"""
Admin module for the Student Achievement & Portfolio Management System.

This file contains reusable functions for admin login and basic student
management tasks.
"""

from mysql.connector import Error

from backend.db import connect_db


def admin_login(username, password):
    """Return admin details if username and password are correct."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return None

        cursor = connection.cursor()

        query = """
        SELECT Username
        FROM Admin
        WHERE Username = %s AND Password = %s
        """

        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

        if admin is not None:
            print("Admin login successful.")
            return admin

        print("Invalid admin username or password.")
        return None

    except Error as error:
        print("Error while logging in as admin:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def view_all_students():
    """Return all registered students sorted by Student_ID."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Student_ID, Full_Name, Student_Class, Section, Email, Phone, Career_Interest
        FROM Students
        ORDER BY Student_ID
        """
        cursor.execute(query)
        students = cursor.fetchall()

        return students

    except Error as error:
        print("Error while fetching students:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def delete_student(student_id):
    """Delete a student and that student's linked portfolio records."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()

        # All five portfolio tables have a foreign key to Students. Delete the
        # selected student's related rows first so a reused ID never carries
        # data from the deleted student.
        connection.start_transaction()
        cursor.execute(
            "SELECT Student_ID FROM Students WHERE Student_ID = %s FOR UPDATE",
            (student_id,),
        )
        if cursor.fetchone() is None:
            connection.rollback()
            print("Student not found.")
            return False

        for table_name in ("Academics", "Activities", "Achievements", "Volunteer", "Goals"):
            cursor.execute(f"DELETE FROM {table_name} WHERE Student_ID = %s", (student_id,))

        cursor.execute("DELETE FROM Students WHERE Student_ID = %s", (student_id,))
        connection.commit()

        print("Student deleted successfully.")
        return True

    except Error as error:
        if connection is not None:
            connection.rollback()
        print("Error while deleting student:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_students():
    """Return the total number of registered students."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Students"
        cursor.execute(query)
        total_students = cursor.fetchone()

        if total_students is not None:
            return total_students[0]

        return 0

    except Error as error:
        print("Error while counting students:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def average_marks():
    """Return the average academic marks."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0.0

        cursor = connection.cursor()

        query = "SELECT AVG(Marks_Obtained) FROM Academics"
        cursor.execute(query)
        average = cursor.fetchone()

        if average is not None and average[0] is not None:
            return float(average[0])

        return 0.0

    except Error as error:
        print("Error while calculating average marks:", error)
        return 0.0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_all_activities():
    """Return the total number of activities."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Activities"
        cursor.execute(query)
        total_activities = cursor.fetchone()

        if total_activities is not None:
            return total_activities[0]

        return 0

    except Error as error:
        print("Error while counting activities:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_all_achievements():
    """Return the total number of achievements."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Achievements"
        cursor.execute(query)
        total_achievements = cursor.fetchone()

        if total_achievements is not None:
            return total_achievements[0]

        return 0

    except Error as error:
        print("Error while counting achievements:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def total_volunteer_hours():
    """Return the total volunteer hours."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT SUM(Hours) FROM Volunteer"
        cursor.execute(query)
        total_hours = cursor.fetchone()

        if total_hours is not None and total_hours[0] is not None:
            return total_hours[0]

        return 0

    except Error as error:
        print("Error while counting volunteer hours:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def count_completed_goals():
    """Return the total number of completed goals."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return 0

        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM Goals WHERE Status = 'Completed'"
        cursor.execute(query)
        total_goals = cursor.fetchone()

        if total_goals is not None:
            return total_goals[0]

        return 0

    except Error as error:
        print("Error while counting completed goals:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def update_student_email(student_id, new_email):
    """Update only the Email field for a student."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()

        query = "UPDATE Students SET Email = %s WHERE Student_ID = %s"
        cursor.execute(query, (new_email, student_id))
        connection.commit()

        print("Student email updated successfully.")
        return True

    except Error as error:
        print("Error while updating student email:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Testing admin login:")
    admin_login("admin", "admin123")

    print("All registered students:")
    print(view_all_students())
