"""
Admin reports window for the Student Achievement & Portfolio Management System.

This file creates a simple Tkinter window to display summary reports.
"""

import tkinter as tk

from backend.admin import (
    average_marks,
    count_all_achievements,
    count_all_activities,
    count_completed_goals,
    count_students,
    total_volunteer_hours,
)
from gui import navigation
from gui import theme

# Decorative font used only for the on-screen heading (theme.py untouched).
FONT_HEADING_ROUGE_SM = ("Rouge Script", 26, "bold")


def center_window(window, width, height):
    """Center the reports window on the screen."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def create_header(window):
    """Create the cherry-red header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F4CA  Student Reports", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def create_report_details(window):
    """Create the report summary labels."""

    total_students = count_students()
    average_mark = average_marks()
    total_activities = count_all_activities()
    total_achievements = count_all_achievements()
    total_hours = total_volunteer_hours()
    completed_goals = count_completed_goals()

    report_items = [
        ("\U0001F9D1\u200D\U0001F393 Total registered students", total_students),
        ("\U0001F4D8 Average academic marks", average_mark),
        ("\U0001F3AF Total activities", total_activities),
        ("\U0001F3C6 Total achievements", total_achievements),
        ("\U0001F91D Total volunteer hours", total_hours),
        ("\u2705 Total completed goals", completed_goals),
    ]

    outer = tk.Frame(window, bg=theme.BG)
    outer.pack(pady=20)

    card = theme.create_section_card(outer)
    card.pack()

    info_frame = tk.Frame(card, bg=theme.CARD_BG)
    info_frame.pack(padx=40, pady=26)

    for item_name, item_value in report_items:
        row = tk.Frame(info_frame, bg=theme.CARD_BG)
        row.pack(fill="x", pady=6)

        tk.Label(row, text=item_name, bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY).pack(side="left")
        tk.Label(row, text=str(item_value), bg=theme.CARD_BG, fg=theme.BUTTON_HOVER, font=("Instrument Serif", 14, "bold")).pack(side="right")


def create_close_button(parent, admin_details=None):
    """Create a Back to Dashboard button for the reports page."""

    button_frame = tk.Frame(parent, bg=theme.BG)
    button_frame.pack(pady=20)

    def close_button_pressed():
        if admin_details is not None:
            navigation.open_admin_dashboard(admin_details)
        else:
            navigation.clear_content()
            navigation.show_main_sidebar()

    theme.RoundedButton(
        button_frame,
        text="\U0001F519 Back to Dashboard",
        command=close_button_pressed,
        width=230,
        height=48,
        parent_bg=theme.BG,
    ).pack()


def show_admin_reports_page(parent, admin_details=None):
    """Render the admin reports UI inside the supplied parent frame."""
    if admin_details is not None:
        navigation.set_active_admin_page("View Reports")
        navigation.show_admin_sidebar(admin_details)
    body = navigation.prepare_content(parent)

    create_header(body)
    create_report_details(body)
    create_close_button(body, admin_details)