"""
Achievement tracker window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for adding, viewing, and counting
student achievement records.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.achievements import (
    add_achievement,
    get_achievements,
    count_achievements,
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
    """Close the achievement tracker window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F3C6  Achievement Tracker", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_records(student_id, records_table):
    """Load achievement records into the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    try:
        records = get_achievements(student_id)

        for record in records:
            records_table.insert(
                "",
                "end",
                values=(record[0], record[2], record[3], record[4], record[5], record[6])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load achievement records.")
        print(error)


def update_summary(student_id, count_label):
    """Update the achievement summary count."""

    try:
        total_achievements = count_achievements(student_id)
    except Exception:
        total_achievements = 0

    count_label.config(text="Total Achievements: " + str(total_achievements))


def clear_entries(
    title_entry,
    competition_entry,
    position_entry,
    organization_entry,
    achievement_date_entry
):
    """Clear all entry boxes after adding an achievement."""

    title_entry.delete(0, tk.END)
    competition_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)
    organization_entry.delete(0, tk.END)
    achievement_date_entry.delete(0, tk.END)


def add_achievement_button_clicked(
    student_id,
    title_entry,
    competition_entry,
    position_entry,
    organization_entry,
    achievement_date_entry,
    records_table,
    count_label
):
    """Collect form data and add a new achievement record."""

    try:
        title = title_entry.get()
        competition_name = competition_entry.get()
        position = position_entry.get()
        organization = organization_entry.get()
        achievement_date = achievement_date_entry.get()

        success = add_achievement(
            student_id,
            title,
            competition_name,
            position,
            organization,
            achievement_date
        )

        if success:
            messagebox.showinfo("Success", "Achievement added successfully.")
            clear_entries(
                title_entry,
                competition_entry,
                position_entry,
                organization_entry,
                achievement_date_entry
            )
            load_records(student_id, records_table)
            update_summary(student_id, count_label)
        else:
            messagebox.showerror("Error", "Could not add achievement.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def create_add_section(window, student_id, records_table, count_label):
    """Create the add achievement form."""

    card = theme.create_section_card(window)
    card.pack(pady=15, padx=30, fill="x")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(pady=18, padx=20)

    small_heading(form_frame, "Add Achievement").grid(row=0, column=0, columnspan=5, pady=(0, 12), sticky="w")

    theme.field_label(form_frame, "Achievement Title").grid(row=1, column=0, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Competition Name").grid(row=1, column=1, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Position / Rank").grid(row=1, column=2, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Issuing Organization").grid(row=1, column=3, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Achievement Date").grid(row=1, column=4, padx=6, pady=5, sticky="w")

    title_entry = theme.styled_entry(form_frame, width=20)
    title_entry.grid(row=2, column=0, padx=6, pady=5, ipady=3)

    competition_entry = theme.styled_entry(form_frame, width=20)
    competition_entry.grid(row=2, column=1, padx=6, pady=5, ipady=3)

    position_entry = theme.styled_entry(form_frame, width=16)
    position_entry.grid(row=2, column=2, padx=6, pady=5, ipady=3)

    organization_entry = theme.styled_entry(form_frame, width=20)
    organization_entry.grid(row=2, column=3, padx=6, pady=5, ipady=3)

    achievement_date_entry = theme.styled_entry(form_frame, width=16)
    achievement_date_entry.grid(row=2, column=4, padx=6, pady=5, ipady=3)

    def add_achievement_button_pressed():
        add_achievement_button_clicked(
            student_id,
            title_entry,
            competition_entry,
            position_entry,
            organization_entry,
            achievement_date_entry,
            records_table,
            count_label
        )

    add_button = theme.RoundedButton(
        form_frame,
        text="Add Achievement",
        command=add_achievement_button_pressed,
        width=220,
        height=46,
        parent_bg=theme.CARD_BG,
    )
    add_button.grid(row=3, column=0, columnspan=5, pady=14)


def create_records_table(window):
    """Create the achievement records table."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="both")

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=16, padx=20, fill="both", expand=True)

    small_heading(table_frame, "Achievement Records").pack(anchor="w", pady=(0, 8))

    columns = (
        "Achievement ID",
        "Title",
        "Competition",
        "Position",
        "Organization",
        "Date"
    )

    records_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    column_widths = (120, 170, 170, 120, 180, 120)

    for index, column in enumerate(columns):
        records_table.heading(column, text=column)
        records_table.column(column, width=column_widths[index] + 80, anchor="center", stretch=True)

    records_table.pack(fill="both", expand=True)

    return records_table


def create_summary_section(window):
    """Create the achievement summary section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    summary_frame = tk.Frame(card, bg=theme.CARD_BG)
    summary_frame.pack(pady=16, padx=20)

    count_label = tk.Label(
        summary_frame,
        text="Total Achievements: 0",
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=("Hina Mincho", 13, "bold")
    )
    count_label.pack()

    return count_label


def create_back_button(window):
    """Create the back button."""
    def close_button_pressed():
        close_window(window)

    theme.RoundedButton(
        window, text="Back", command=close_button_pressed,
        width=160, height=44, parent_bg=theme.BG,
    ).pack(pady=8)


def show_achievement_page(parent, student_details):
    """Render the achievement tracker UI inside the supplied parent frame.

    Accepts either a student details dict or a student_id for compatibility.
    """
    if isinstance(student_details, dict):
        sd = student_details
        student_id = sd.get("Student_ID")
    else:
        sd = None
        student_id = student_details

    from gui import dashboard as _dashboard

    # Ensure sidebar and active highlighting
    try:
        navigation.set_active_student_page("Achievements")
        if isinstance(student_details, dict):
            navigation.show_student_sidebar(student_details)
        else:
            navigation.show_student_sidebar({"Full_Name": "Student"})
    except Exception:
        pass

    body = navigation.prepare_content(parent)

    if sd is not None:
        _dashboard.create_header(body, sd)
    else:
        _dashboard.create_header(body, {"Full_Name": "Student"})

    title = tk.Label(body, text="\U0001F3C6 Achievement Tracker", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(anchor="w", padx=30, pady=(16, 6))

    records_table = create_records_table(body)
    count_label = create_summary_section(body)
    create_add_section(body, student_id, records_table, count_label)

    load_records(student_id, records_table)
    update_summary(student_id, count_label)
    theme.RoundedButton(
        body, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(body),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=theme.BG,
    ).pack(pady=(10, 20))


def open_achievement_window(student_id):
    """Compatibility wrapper: open achievement tracker in a standalone window."""

    window = tk.Tk()
    window.title("Achievement Tracker")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_achievement_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_achievement_window(1)