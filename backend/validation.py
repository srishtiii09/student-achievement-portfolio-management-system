"""
Validation module for the Student Achievement & Portfolio Management System.

This file contains reusable functions to check user input before it is used
in the project.
"""


def validate_empty_field(value):
    """Return True if the value is not empty after removing extra spaces."""

    if value.strip() != "":
        return True
    return False


def validate_email(email):
    """Return True if the email has one @ symbol and a dot after it."""

    if email.count("@") != 1:
        return False

    parts = email.split("@")
    domain = parts[1]

    if "." in domain:
        return True
    return False


def validate_phone(phone):
    """Return True if the phone number contains exactly 10 digits."""

    if phone.isdigit() and len(phone) == 10:
        return True
    return False


def validate_marks(obtained, maximum):
    """Return True if obtained marks are valid for the maximum marks."""

    if obtained >= 0 and maximum > 0 and obtained <= maximum:
        return True
    return False


def validate_password(password):
    """Return True if the password has at least 6 characters."""

    if len(password) >= 6:
        return True
    return False


def validate_goal_status(status):
    """Return True if the goal status is one of the accepted values."""

    valid_statuses = ["Pending", "In Progress", "Completed"]

    if status in valid_statuses:
        return True
    return False


if __name__ == "__main__":
    print("Empty field validation:", validate_empty_field("Rakesh"))
    print("Email validation:", validate_email("student@example.com"))
    print("Phone validation:", validate_phone("9876543210"))
    print("Marks validation:", validate_marks(85, 100))
    print("Password validation:", validate_password("secret1"))
    print("Goal status validation:", validate_goal_status("Pending"))
