"""
Leaderboard window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for viewing activity, volunteer, and
achievement leaderboards.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.leaderboard import (
    get_activity_leaderboard,
    get_volunteer_leaderboard,
    get_achievement_leaderboard,
    get_top_students_by_average_marks,
)
from gui import navigation
from gui import theme

# Decorative fonts used only for on-screen headings (theme.py untouched).
FONT_HEADING_ROUGE_SM = ("Rouge Script", 26, "bold")
FONT_SECTION_FELIPA = ("Felipa", 15, "bold")


def small_heading(parent, text):
    """Section heading label using the Felipa decorative font."""
    return tk.Label(parent, text=text, bg=theme.CARD_BG, fg=theme.ACCENT, font=FONT_SECTION_FELIPA)


def center_window(window, width, height):
    """Center the window on the screen."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def close_window(window):
    """Close the leaderboard window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F451  Leaderboard", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def clear_table(leaderboard_table):
    """Remove all rows from a leaderboard table."""

    for item in leaderboard_table.get_children():
        leaderboard_table.delete(item)


def load_activity_leaderboard(activity_table):
    """Load activity leaderboard records into the table."""

    clear_table(activity_table)

    try:
        records = get_activity_leaderboard()

        for rank, record in enumerate(records, start=1):
            activity_table.insert(
                "",
                "end",
                values=(rank, record[1], record[2])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load activity leaderboard.")
        print(error)


def load_volunteer_leaderboard(volunteer_table):
    """Load volunteer leaderboard records into the table."""

    clear_table(volunteer_table)

    try:
        records = get_volunteer_leaderboard()

        for rank, record in enumerate(records, start=1):
            volunteer_table.insert(
                "",
                "end",
                values=(rank, record[1], record[2])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load volunteer leaderboard.")
        print(error)


def load_achievement_leaderboard(achievement_table):
    """Load achievement leaderboard records into the table."""

    clear_table(achievement_table)

    try:
        records = get_achievement_leaderboard()

        for rank, record in enumerate(records, start=1):
            achievement_table.insert(
                "",
                "end",
                values=(rank, record[1], record[2])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load achievement leaderboard.")
        print(error)


def load_academic_leaderboard(academic_table):
    """Load academic (average marks) leaderboard records into the table."""

    clear_table(academic_table)

    try:
        records = get_top_students_by_average_marks()

        for rank, record in enumerate(records, start=1):
            academic_table.insert(
                "",
                "end",
                values=(rank, record[1], str(record[2]) + "%")
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load academic leaderboard.")
        print(error)


def refresh_leaderboards(activity_table, volunteer_table, achievement_table, academic_table):
    """Reload all leaderboard tables."""

    load_activity_leaderboard(activity_table)
    load_volunteer_leaderboard(volunteer_table)
    load_achievement_leaderboard(achievement_table)
    load_academic_leaderboard(academic_table)


def create_leaderboard_table(parent, heading_text, columns, height):
    """Create one leaderboard table with a section heading."""

    card = theme.create_section_card(parent)
    card.pack(pady=8, padx=6, fill="both", side="left", expand=True)

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=14, padx=16, fill="both", expand=True)

    small_heading(table_frame, heading_text).pack(anchor="w", pady=(0, 8))

    leaderboard_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=height
    )

    for column in columns:
        leaderboard_table.heading(column, text=column)
        leaderboard_table.column(column, width=170, anchor="center", stretch=True)

    leaderboard_table.pack(fill="both", expand=True)

    return leaderboard_table


def create_tables(window):
    """Create all leaderboard tables."""

    tables_frame = tk.Frame(window, bg=theme.BG)
    tables_frame.pack(pady=10, padx=24, fill="both")

    top_row = tk.Frame(tables_frame, bg=theme.BG)
    top_row.pack(fill="both", expand=True)

    bottom_row = tk.Frame(tables_frame, bg=theme.BG)
    bottom_row.pack(fill="both", expand=True, pady=(12, 0))

    activity_columns = ("Rank", "Student Name", "Total Activities")
    volunteer_columns = ("Rank", "Student Name", "Volunteer Hours")
    achievement_columns = ("Rank", "Student Name", "Total Achievements")
    academic_columns = ("Rank", "Student Name", "Average Marks")

    activity_table = create_leaderboard_table(
        top_row,
        "\U0001F3AF Activity Leaderboard",
        activity_columns,
        6
    )

    volunteer_table = create_leaderboard_table(
        top_row,
        "\U0001F91D Volunteer Leaderboard",
        volunteer_columns,
        6
    )

    achievement_table = create_leaderboard_table(
        bottom_row,
        "\U0001F3C6 Achievement Leaderboard",
        achievement_columns,
        6
    )

    academic_table = create_leaderboard_table(
        bottom_row,
        "\U0001F4D8 Academic Leaderboard",
        academic_columns,
        6
    )

    return activity_table, volunteer_table, achievement_table, academic_table


def create_buttons(window, activity_table, volunteer_table, achievement_table, academic_table, admin_details=None):
    """Create refresh and back buttons."""

    button_frame = tk.Frame(window, bg=theme.BG)
    button_frame.pack(pady=16)

    def refresh_button_pressed():
        refresh_leaderboards(activity_table, volunteer_table, achievement_table, academic_table)

    theme.RoundedButton(
        button_frame, text="\U0001F504 Refresh", command=refresh_button_pressed,
        width=170, height=46, parent_bg=theme.BG,
    ).grid(row=0, column=0, padx=8)

    # Return to the dashboard for the active role.
    def back_button_pressed():
        if admin_details is not None:
            navigation.open_admin_dashboard(admin_details)
        else:
            navigation.return_to_student_dashboard()

    theme.RoundedButton(
        button_frame, text="\U0001F519 Back to Dashboard", command=back_button_pressed,
        width=210, height=46, bg_color="#FFEFED", hover_color="#FFDEDA",
        fg_color=theme.ACCENT, parent_bg=theme.BG,
    ).grid(row=0, column=1, padx=8)


def show_leaderboard_page(parent, details=None):
    """Render the leaderboard UI inside the supplied parent frame.
    Accepts optional `details`:
    - dict => student_details (render student dashboard header)
    - other => admin_details (render admin header)
    """
    from gui import dashboard as _dashboard

    body = navigation.prepare_content(parent)

    # Student header when passed a student details dict
    if isinstance(details, dict):
        try:
            navigation.set_active_student_page("Leaderboard")
            navigation.show_student_sidebar(details)
        except Exception:
            pass
        _dashboard.create_header(body, details)
    else:
        # Admin or generic header
        if details is not None:
            navigation.set_active_admin_page("Leaderboard")
            navigation.show_admin_sidebar(details)
        create_header(body)

    activity_table, volunteer_table, achievement_table, academic_table = create_tables(body)
    # Pass admin_details for proper Back to Dashboard behavior when used in admin flows
    create_buttons(
        body, activity_table, volunteer_table, achievement_table, academic_table,
        details if not isinstance(details, dict) else None
    )

    refresh_leaderboards(activity_table, volunteer_table, achievement_table, academic_table)