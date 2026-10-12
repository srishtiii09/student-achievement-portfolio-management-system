"""
Reports window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for viewing and saving a student
portfolio summary report.
"""

import tkinter as tk
from tkinter import messagebox

from backend.reports import (
    generate_student_summary,
    save_report
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
    """Close the reports window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F4CA  Student Portfolio Report", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def get_summary_value(summary, key):
    """Return a safe display value from the summary dictionary."""

    value = summary.get(key)

    if value is None:
        return "0"

    return str(value)


def refresh_report(student_id, summary_labels):
    """Reload all report summary values."""

    try:
        summary = generate_student_summary(student_id)

        for key in summary_labels:
            summary_labels[key].config(text=get_summary_value(summary, key))

    except Exception as error:
        messagebox.showerror("Error", "Unable to load report summary.")
        print(error)


def save_report_button_clicked(student_id, filename_entry):
    """Save the report using the entered filename."""

    try:
        filename = filename_entry.get()

        if filename == "":
            filename = "student_report.txt"

        success = save_report(student_id, filename)

        if success:
            messagebox.showinfo("Success", "Report saved successfully.")
        else:
            messagebox.showerror("Error", "Could not save report.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def create_summary_card(parent, row, column, title):
    """Create one report summary card."""

    card_frame = tk.Frame(
        parent,
        bg=theme.CARD_BG,
        highlightbackground=theme.CARD_BORDER,
        highlightthickness=1,
        bd=0,
        width=250,
        height=80
    )
    card_frame.grid(row=row, column=column, padx=10, pady=8)
    card_frame.grid_propagate(False)

    title_label = tk.Label(
        card_frame,
        text=title,
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=("Hina Mincho", 11, "bold")
    )
    title_label.pack(pady=(12, 4))

    value_label = tk.Label(
        card_frame,
        text="0",
        bg=theme.CARD_BG,
        fg=theme.BUTTON_HOVER,
        font=theme.FONT_VALUE
    )
    value_label.pack()

    return value_label


def create_summary_section(window):
    """Create the report summary card layout."""

    summary_frame = tk.Frame(window, bg=theme.BG)
    summary_frame.pack(pady=15)

    small_heading(summary_frame, "Portfolio Summary").pack()

    summary_labels = {}

    summary_items = (
        "Average Marks",
        "Highest Score",
        "Lowest Score",
        "Total Activities",
        "Total Achievements",
        "Total Volunteer Hours",
        "Total Volunteer Events",
        "Completed Goals",
        "Pending Goals"
    )

    for index, item in enumerate(summary_items):
        row = (index // 3) + 1
        column = index % 3
        summary_labels[item] = create_summary_card(
            summary_frame,
            row,
            column,
            item
        )

    return summary_labels


def create_save_section(window, student_id, summary_labels):
    """Create report filename, save, and refresh controls."""

    card = theme.create_section_card(window)
    card.pack(pady=10)

    save_frame = tk.Frame(card, bg=theme.CARD_BG)
    save_frame.pack(pady=16, padx=20)

    theme.field_label(save_frame, "Report Filename").grid(row=0, column=0, padx=8, pady=5, sticky="w")

    filename_entry = theme.styled_entry(save_frame, width=30)
    filename_entry.grid(row=1, column=0, padx=8, pady=5, ipady=3)
    filename_entry.insert(0, "student_report.txt")

    def save_button_pressed():
        save_report_button_clicked(student_id, filename_entry)

    theme.RoundedButton(
        save_frame, text="\U0001F4BE Save Report", command=save_button_pressed,
        width=190, height=44, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=1, column=1, padx=8, pady=5)

    def refresh_button_pressed():
        refresh_report(student_id, summary_labels)

    theme.RoundedButton(
        save_frame, text="\U0001F504 Refresh Report", command=refresh_button_pressed,
        width=190, height=44, bg_color="#FFEFED", hover_color="#FFDEDA",
        fg_color=theme.ACCENT, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=1, column=2, padx=8, pady=5)


def create_back_button(window):
    """Create the back button."""
    def close_button_pressed():
        close_window(window)

    theme.RoundedButton(
        window, text="Back", command=close_button_pressed,
        width=160, height=44, parent_bg=theme.BG,
    ).pack(pady=8)


def show_reports_page(parent, student_details):
    """Render the reports UI inside the supplied parent frame.

    Accepts either a student details dict or a student_id for compatibility.
    """
    if isinstance(student_details, dict):
        sd = student_details
        student_id = sd.get("Student_ID")
    else:
        sd = None
        student_id = student_details

    from gui import dashboard as _dashboard

    # Show sidebar and mark Reports active
    try:
        navigation.set_active_student_page("Reports")
        if sd is not None:
            navigation.show_student_sidebar(sd)
        else:
            navigation.show_student_sidebar({"Full_Name": "Student"})
    except Exception:
        pass

    body = navigation.prepare_content(parent)

    if sd is not None:
        _dashboard.create_header(body, sd)
    else:
        _dashboard.create_header(body, {"Full_Name": "Student"})

    # Centered full-width summary area
    title = tk.Label(body, text="\U0001F4CA Student Portfolio Report", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(pady=(16, 12))

    container = tk.Frame(body, bg=navigation.CONTENT_BG)
    container.pack(expand=True, fill="both")

    summary_frame = tk.Frame(container, bg=navigation.CONTENT_BG)
    summary_frame.pack(expand=True, fill="both", padx=60, pady=10)

    # Configure three equal columns
    for c in range(3):
        summary_frame.grid_columnconfigure(c, weight=1)

    summary_labels = {}
    summary_items = (
        "Average Marks",
        "Highest Score",
        "Lowest Score",
        "Total Activities",
        "Total Achievements",
        "Total Volunteer Hours",
        "Total Volunteer Events",
        "Completed Goals",
        "Pending Goals"
    )

    for index, item in enumerate(summary_items):
        row = (index // 3)
        column = index % 3
        card = tk.Frame(summary_frame, bg=theme.CARD_BG, highlightbackground=theme.CARD_BORDER, highlightthickness=1, bd=0, width=380, height=110)
        card.grid(row=row, column=column, padx=16, pady=12, sticky="nsew")
        card.grid_propagate(False)

        lbl_title = tk.Label(card, text=item, bg=theme.CARD_BG, fg=theme.ACCENT, font=("Hina Mincho", 12, "bold"))
        lbl_title.pack(pady=(16, 6))
        lbl_value = tk.Label(card, text="0", bg=theme.CARD_BG, fg=theme.BUTTON_HOVER, font=theme.FONT_VALUE)
        lbl_value.pack()

        summary_labels[item] = lbl_value

    # Save/Refresh controls aligned center beneath cards
    save_card = theme.create_section_card(container)
    save_card.pack(pady=14)

    save_frame = tk.Frame(save_card, bg=theme.CARD_BG)
    save_frame.pack(padx=20, pady=16)

    theme.field_label(save_frame, "Report Filename").grid(row=0, column=0, padx=8, pady=5, sticky="w")

    filename_entry = theme.styled_entry(save_frame, width=36)
    filename_entry.grid(row=1, column=0, padx=8, pady=5, ipady=3)
    filename_entry.insert(0, "student_report.txt")

    theme.RoundedButton(
        save_frame, text="\U0001F4BE Save Report",
        command=lambda: save_report_button_clicked(student_id, filename_entry),
        width=190, height=44, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=1, column=1, padx=8, pady=5)

    theme.RoundedButton(
        save_frame, text="\U0001F504 Refresh Report",
        command=lambda: refresh_report(student_id, summary_labels),
        width=190, height=44, bg_color="#FFEFED", hover_color="#FFDEDA",
        fg_color=theme.ACCENT, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=1, column=2, padx=8, pady=5)

    refresh_report(student_id, summary_labels)
    theme.RoundedButton(
        container, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(container),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=navigation.CONTENT_BG,
    ).pack(pady=(0, 20))


def open_reports_window(student_id):
    """Compatibility wrapper: open reports in a standalone window."""

    window = tk.Tk()
    window.title("Student Portfolio Report")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_reports_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_reports_window(1)