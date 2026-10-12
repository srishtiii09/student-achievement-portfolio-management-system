"""
Leaderboard module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to display top students based on
academic performance, activities, achievements, and volunteer hours.
"""

from mysql.connector import Error

from backend.db import connect_db


def get_top_students_by_average_marks():
    """Return students sorted by average academic percentage."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        # Average percentage is calculated from all academic records.
        query = """
        SELECT Students.Student_ID, Students.Full_Name,
               ROUND(AVG((Academics.Marks_Obtained / Academics.Maximum_Marks) * 100), 2)
        FROM Students
        JOIN Academics
        ON Students.Student_ID = Academics.Student_ID
        GROUP BY Students.Student_ID, Students.Full_Name
        ORDER BY ROUND(AVG((Academics.Marks_Obtained / Academics.Maximum_Marks) * 100), 2) DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching marks leaderboard:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_top_students_by_activities():
    """Return students sorted by total number of activities."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Students.Student_ID, Students.Full_Name,
               COUNT(Activities.Activity_ID)
        FROM Students
        JOIN Activities
        ON Students.Student_ID = Activities.Student_ID
        GROUP BY Students.Student_ID, Students.Full_Name
        ORDER BY COUNT(Activities.Activity_ID) DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching activities leaderboard:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_top_students_by_achievements():
    """Return students sorted by total number of achievements."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Students.Student_ID, Students.Full_Name,
               COUNT(Achievements.Achievement_ID)
        FROM Students
        JOIN Achievements
        ON Students.Student_ID = Achievements.Student_ID
        GROUP BY Students.Student_ID, Students.Full_Name
        ORDER BY COUNT(Achievements.Achievement_ID) DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching achievements leaderboard:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_top_students_by_volunteer_hours():
    """Return students sorted by total volunteer hours."""

    connection = None
    cursor = None

    try:
        connection = connect_db()

        if connection is None:
            print("Database connection failed.")
            return []

        cursor = connection.cursor()

        query = """
        SELECT Students.Student_ID, Students.Full_Name,
               SUM(Volunteer.Hours)
        FROM Students
        JOIN Volunteer
        ON Students.Student_ID = Volunteer.Student_ID
        GROUP BY Students.Student_ID, Students.Full_Name
        ORDER BY SUM(Volunteer.Hours) DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        return records

    except Error as error:
        print("Error while fetching volunteer hours leaderboard:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_activity_leaderboard():
    """Return the activity leaderboard."""

    return get_top_students_by_activities()


def get_volunteer_leaderboard():
    """Return the volunteer hours leaderboard."""

    return get_top_students_by_volunteer_hours()


def get_achievement_leaderboard():
    """Return the achievement leaderboard."""

    return get_top_students_by_achievements()


if __name__ == "__main__":
    print("Top students by average marks:")
    print(get_top_students_by_average_marks())

    print("Top students by activities:")
    print(get_top_students_by_activities())

    print("Top students by achievements:")
    print(get_top_students_by_achievements())

    print("Top students by volunteer hours:")
    print(get_top_students_by_volunteer_hours())
