"""
Reports module for the Student Achievement & Portfolio Management System.

This file creates a simple student portfolio summary by reusing functions
from other project modules.
"""

from backend.academics import (
    calculate_average_marks,
    get_highest_score,
    get_lowest_score,
)
from backend.achievements import count_achievements
from backend.activities import count_activities
from backend.goals import count_completed_goals, count_pending_goals
from backend.volunteer import calculate_total_hours, count_volunteer_events


def generate_student_summary(student_id):
    """Return a dictionary containing the student's portfolio summary."""

    summary = {
        "Average Marks": calculate_average_marks(student_id),
        "Highest Score": get_highest_score(student_id),
        "Lowest Score": get_lowest_score(student_id),
        "Total Activities": count_activities(student_id),
        "Total Achievements": count_achievements(student_id),
        "Total Volunteer Hours": calculate_total_hours(student_id),
        "Total Volunteer Events": count_volunteer_events(student_id),
        "Completed Goals": count_completed_goals(student_id),
        "Pending Goals": count_pending_goals(student_id),
    }

    return summary


def display_student_summary(student_id):
    """Print the student's portfolio summary neatly."""

    summary = generate_student_summary(student_id)

    print("==============================")
    print("STUDENT PORTFOLIO SUMMARY")
    print("==============================")
    print("Average Marks :", summary["Average Marks"])
    print("Highest Score :", summary["Highest Score"])
    print("Lowest Score :", summary["Lowest Score"])
    print("Activities :", summary["Total Activities"])
    print("Achievements :", summary["Total Achievements"])
    print("Volunteer Hours :", summary["Total Volunteer Hours"])
    print("Volunteer Events :", summary["Total Volunteer Events"])
    print("Completed Goals :", summary["Completed Goals"])
    print("Pending Goals :", summary["Pending Goals"])


def save_report(student_id, filename):
    """Save the student's portfolio summary in a text file."""

    try:
        summary = generate_student_summary(student_id)

        report_text = "==============================\n"
        report_text = report_text + "STUDENT PORTFOLIO SUMMARY\n"
        report_text = report_text + "==============================\n\n"
        report_text = report_text + "Average Marks : " + str(summary["Average Marks"]) + "\n"
        report_text = report_text + "Highest Score : " + str(summary["Highest Score"]) + "\n"
        report_text = report_text + "Lowest Score : " + str(summary["Lowest Score"]) + "\n"
        report_text = report_text + "Activities : " + str(summary["Total Activities"]) + "\n"
        report_text = report_text + "Achievements : " + str(summary["Total Achievements"]) + "\n"
        report_text = report_text + "Volunteer Hours : " + str(summary["Total Volunteer Hours"]) + "\n"
        report_text = report_text + "Volunteer Events : " + str(summary["Total Volunteer Events"]) + "\n"
        report_text = report_text + "Completed Goals : " + str(summary["Completed Goals"]) + "\n"
        report_text = report_text + "Pending Goals : " + str(summary["Pending Goals"]) + "\n"

        with open(filename, "w") as report_file:
            report_file.write(report_text)

        print("Report saved successfully.")
        return True

    except OSError as error:
        print("Error while saving report:", error)
        return False


if __name__ == "__main__":
    display_student_summary(1)
    save_report(1, "student_report.txt")
