"""
Student dashboard window for the Student Achievement & Portfolio Management System.

This file creates a simple Tkinter dashboard screen. Backend connections for
summary data and navigation modules will be added later.
"""

import tkinter as tk
from tkinter import messagebox

from backend.academics import calculate_average_marks
from backend.achievements import count_achievements
from backend.activities import count_activities
from backend.goals import count_completed_goals
from backend.volunteer import calculate_total_hours
from gui.academic_window import show_academic_page
from gui.activity_window import show_activity_page
from gui.achievement_window import show_achievement_page
from gui.volunteer_window import show_volunteer_page
from gui.goals_window import show_goals_page
from gui.reports_window import show_reports_page
from gui.leaderboard_window import show_leaderboard_page
from gui.manage_students_window import show_manage_students_page
from gui.admin_reports_window import show_admin_reports_page
from gui import navigation
from gui import theme
from gui.login_window import show_login_page


def show_pending_message():
    """Show a message for modules that will be added later."""

    messagebox.showinfo("Information", "This module will be implemented next.")


def logout(window):
    """Close the dashboard window."""

    window.destroy()

def handle_navigation(button_name, student_details, parent):
    """Open the selected dashboard module inside the supplied parent frame."""

    if button_name == "Academic Tracker":
        show_academic_page(parent, student_details)

    elif button_name == "Activities":
        show_activity_page(parent, student_details)

    elif button_name == "Achievements":
        show_achievement_page(parent, student_details)

    elif button_name == "Volunteer Work":
        show_volunteer_page(parent, student_details)

    elif button_name == "Goals":
        show_goals_page(parent, student_details)

    elif button_name == "Reports":
        show_reports_page(parent, student_details)

    elif button_name == "Leaderboard":
        show_leaderboard_page(parent, student_details)

    else:
        show_pending_message()

def center_window(window, width, height):
    """Center the dashboard window on the screen."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def create_header(window, student_details):
    """Create the dashboard header (shared by every student page)."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")

    text_col = tk.Frame(header_frame, bg=theme.ACCENT)
    text_col.pack(side="left", padx=30, pady=(24, 22))

    welcome_text = "\U0001F44B Welcome, " + student_details["Full_Name"]

    welcome_label = tk.Label(
        text_col,
        text=welcome_text,
        bg=theme.ACCENT,
        fg="white",
        font=theme.FONT_HEADING_SM
    )
    welcome_label.pack(anchor="w")

    title_label = tk.Label(
        text_col,
        text="\U0001F352 Student Achievement & Portfolio Management System",
        bg=theme.ACCENT,
        fg="#FFD7D3",
        font=theme.FONT_SUBHEADING
    )
    title_label.pack(anchor="w", pady=(4, 0))

    # Logout button on header (works both for embedded content and standalone)
    try:
        import gui.navigation as nav
        logout_btn = theme.RoundedButton(
            header_frame,
            text="\U0001F6AA  Logout",
            command=lambda: nav.logout_student(header_frame.winfo_toplevel()),
            width=150,
            height=46,
            bg_color="#FFFFFF",
            hover_color="#FFE3E0",
            fg_color=theme.ACCENT,
            font=("Instrument Serif", 13, "bold"),
            parent_bg=theme.ACCENT,
        )
        logout_btn.pack(side="right", padx=26, pady=22)
    except Exception:
        pass


def create_profile_section(window, student_details):
    """Display basic student profile details."""

    profile_frame = tk.Frame(window, bg=theme.BG)
    profile_frame.pack(fill="x", padx=40, pady=(25, 10))

    heading_label = tk.Label(
        profile_frame,
        text="\U0001F464 Student Profile",
        bg=theme.BG,
        fg=theme.ACCENT,
        font=theme.FONT_HEADING_SM
    )
    heading_label.pack(anchor="w")

    card = theme.create_section_card(profile_frame)
    card.pack(anchor="w", pady=12, fill="x")

    profile_text = (
        "Name: " + student_details["Full_Name"] + "     "
        "Class: " + student_details["Student_Class"] + "     "
        "Section: " + student_details["Section"] + "     "
        "Email: " + student_details["Email"]
    )

    details_label = tk.Label(
        card,
        text=profile_text,
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=theme.FONT_BODY
    )
    details_label.pack(anchor="w", padx=20, pady=16)


def create_summary_card(parent, title, value):
    """Create one dashboard summary card."""

    card_frame = tk.Frame(
        parent,
        bg=theme.CARD_BG,
        width=180,
        height=100,
        highlightbackground=theme.CARD_BORDER,
        highlightthickness=1
    )
    card_frame.pack(side="left", padx=8)
    card_frame.pack_propagate(False)

    title_label = tk.Label(
        card_frame,
        text=title,
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=("Hina Mincho", 11, "bold")
    )
    title_label.pack(pady=(20, 8))

    value_label = tk.Label(
        card_frame,
        text=value,
        bg=theme.CARD_BG,
        fg=theme.BUTTON_HOVER,
        font=theme.FONT_VALUE
    )
    value_label.pack()


def create_summary_section(window, student_id):
    """Create the five summary cards with backend values."""

    summary_frame = tk.Frame(window, bg=theme.BG)
    summary_frame.pack(pady=20)

    # Each value is loaded safely so the GUI does not crash.
    try:
        average = calculate_average_marks(student_id)
    except Exception:
        average = 0

    try:
        activity_count = count_activities(student_id)
    except Exception:
        activity_count = 0

    try:
        achievement_count = count_achievements(student_id)
    except Exception:
        achievement_count = 0

    try:
        volunteer_hours = calculate_total_hours(student_id)
    except Exception:
        volunteer_hours = 0

    try:
        completed_goals = count_completed_goals(student_id)
    except Exception:
        completed_goals = 0

    create_summary_card(summary_frame, "Academic Average", str(average) + "%")
    create_summary_card(summary_frame, "Total Activities", str(activity_count))
    create_summary_card(summary_frame, "Achievements", str(achievement_count))
    create_summary_card(summary_frame, "Volunteer Hours", str(volunteer_hours))
    create_summary_card(summary_frame, "Completed Goals", str(completed_goals))


def create_navigation_buttons(parent, student_details):
    """Create dashboard navigation buttons inside parent."""
    student_id = student_details["Student_ID"]
    # This function is no longer used; sidebar is created inside show_dashboard.
    pass


def show_dashboard(parent, student_details):
    """Render the student dashboard inside the supplied parent frame."""
    # Render dashboard content in the main content area (sidebar is managed by navigation)
    for w in parent.winfo_children():
        w.destroy()
    # Ensure student sidebar is present and highlight Dashboard
    try:
        navigation.set_active_student_page("Dashboard")
        navigation.show_student_sidebar(student_details)
    except Exception:
        pass

    body = navigation.prepare_content(parent)

    create_header(body, student_details)
    create_profile_section(body, student_details)
    create_summary_section(body, student_details["Student_ID"])


def open_dashboard(student_details):
    """Compatibility wrapper: open dashboard in a standalone window."""

    window = tk.Tk()
    window.title("Student Dashboard")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_dashboard(window, student_details)

    window.mainloop()


if __name__ == "__main__":
    sample_student = {
        "Student_ID": 1,
        "Full_Name": "Aarav Sharma",
        "Student_Class": "12",
        "Section": "A",
        "Email": "aarav@example.com",
    }

    open_dashboard(sample_student)
