"""
Activity tracker window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for adding, viewing, searching, and
counting extracurricular activity records.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.activities import (
    add_activity,
    count_activities,
    get_activities,
    search_activities_by_category,
    search_activities_by_level,
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
    """Close the activity tracker window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F3AF  Extracurricular Activity Tracker", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_records(student_id, records_table):
    """Load all activity records into the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    try:
        records = get_activities(student_id)

        for record in records:
            records_table.insert(
                "",
                "end",
                values=(record[0], record[2], record[3], record[4], record[5], record[6])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load activity records.")
        print(error)


def load_search_results(records_table, records):
    """Display search results in the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    for record in records:
        records_table.insert(
            "",
            "end",
            values=(record[0], record[2], record[3], record[4], record[5], record[6])
        )


def update_activity_count(student_id, count_label):
    """Update the total activity count."""

    try:
        total_activities = count_activities(student_id)
    except Exception:
        total_activities = 0

    count_label.config(text="Total Activities: " + str(total_activities))


def clear_entries(
    activity_name_entry,
    category_entry,
    level_entry,
    organizer_entry,
    activity_date_entry
):
    """Clear all entry boxes after adding an activity."""

    activity_name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    level_entry.delete(0, tk.END)
    organizer_entry.delete(0, tk.END)
    activity_date_entry.delete(0, tk.END)


def add_activity_button_clicked(
    student_id,
    activity_name_entry,
    category_entry,
    level_entry,
    organizer_entry,
    activity_date_entry,
    records_table,
    count_label
):
    """Collect form data and add a new activity record."""

    try:
        activity_name = activity_name_entry.get()
        category = category_entry.get()
        level = level_entry.get()
        organizer = organizer_entry.get()
        activity_date = activity_date_entry.get()

        success = add_activity(
            student_id,
            activity_name,
            category,
            level,
            organizer,
            activity_date
        )

        if success:
            messagebox.showinfo("Success", "Activity added successfully.")
            clear_entries(
                activity_name_entry,
                category_entry,
                level_entry,
                organizer_entry,
                activity_date_entry
            )
            load_records(student_id, records_table)
            update_activity_count(student_id, count_label)
        else:
            messagebox.showerror("Error", "Could not add activity.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def search_category_button_clicked(student_id, category_entry, records_table):
    """Search activities by category."""

    try:
        category = category_entry.get()
        records = search_activities_by_category(student_id, category)
        load_search_results(records_table, records)

    except Exception as error:
        messagebox.showerror("Error", "Unable to search by category.")
        print(error)


def search_level_button_clicked(student_id, level_entry, records_table):
    """Search activities by level."""

    try:
        level = level_entry.get()
        records = search_activities_by_level(student_id, level)
        load_search_results(records_table, records)

    except Exception as error:
        messagebox.showerror("Error", "Unable to search by level.")
        print(error)


def create_add_activity_section(window, student_id, records_table, count_label):
    """Create the add activity form."""

    card = theme.create_section_card(window)
    card.pack(pady=15, padx=30, fill="x")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(pady=18, padx=20)

    small_heading(form_frame, "Add Activity").grid(row=0, column=0, columnspan=5, pady=(0, 12), sticky="w")

    theme.field_label(form_frame, "Activity Name").grid(row=1, column=0, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Category").grid(row=1, column=1, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Level").grid(row=1, column=2, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Organizer").grid(row=1, column=3, padx=6, pady=5, sticky="w")
    theme.field_label(form_frame, "Activity Date").grid(row=1, column=4, padx=6, pady=5, sticky="w")

    activity_name_entry = theme.styled_entry(form_frame, width=20)
    activity_name_entry.grid(row=2, column=0, padx=6, pady=5, ipady=3)

    category_entry = theme.styled_entry(form_frame, width=18)
    category_entry.grid(row=2, column=1, padx=6, pady=5, ipady=3)

    level_entry = theme.styled_entry(form_frame, width=16)
    level_entry.grid(row=2, column=2, padx=6, pady=5, ipady=3)

    organizer_entry = theme.styled_entry(form_frame, width=20)
    organizer_entry.grid(row=2, column=3, padx=6, pady=5, ipady=3)

    activity_date_entry = theme.styled_entry(form_frame, width=16)
    activity_date_entry.grid(row=2, column=4, padx=6, pady=5, ipady=3)

    def add_activity_button_pressed():
        add_activity_button_clicked(
            student_id,
            activity_name_entry,
            category_entry,
            level_entry,
            organizer_entry,
            activity_date_entry,
            records_table,
            count_label
        )

    add_button = theme.RoundedButton(
        form_frame,
        text="Add Activity",
        command=add_activity_button_pressed,
        width=220,
        height=46,
        parent_bg=theme.CARD_BG,
    )
    add_button.grid(row=3, column=0, columnspan=5, pady=14)


def create_search_section(window, student_id, records_table):
    """Create category and level search controls."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    search_frame = tk.Frame(card, bg=theme.CARD_BG)
    search_frame.pack(pady=16, padx=20)

    category_entry = theme.styled_entry(search_frame, width=20)
    category_entry.grid(row=0, column=0, padx=6, ipady=3)

    def search_category_button_pressed():
        search_category_button_clicked(student_id, category_entry, records_table)

    theme.RoundedButton(
        search_frame, text="Search Category", command=search_category_button_pressed,
        width=170, height=42, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=0, column=1, padx=6)

    level_entry = theme.styled_entry(search_frame, width=20)
    level_entry.grid(row=0, column=2, padx=6, ipady=3)

    def search_level_button_pressed():
        search_level_button_clicked(student_id, level_entry, records_table)

    theme.RoundedButton(
        search_frame, text="Search Level", command=search_level_button_pressed,
        width=150, height=42, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=0, column=3, padx=6)

    def show_all_button_pressed():
        load_records(student_id, records_table)

    theme.RoundedButton(
        search_frame, text="Show All", command=show_all_button_pressed,
        width=120, height=42, bg_color="#FFEFED", hover_color="#FFDEDA",
        fg_color=theme.ACCENT, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=0, column=4, padx=6)


def create_records_table(window):
    """Create the activity records table."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="both")

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=16, padx=20, fill="both", expand=True)

    small_heading(table_frame, "Activity Records").pack(anchor="w", pady=(0, 8))

    columns = (
        "Activity ID",
        "Activity Name",
        "Category",
        "Level",
        "Organizer",
        "Activity Date"
    )

    records_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    for column in columns:
        records_table.heading(column, text=column)
        records_table.column(column, width=220, anchor="center", stretch=True)

    records_table.pack(fill="both", expand=True)

    return records_table


def create_summary_section(window):
    """Create the activity summary section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    summary_frame = tk.Frame(card, bg=theme.CARD_BG)
    summary_frame.pack(pady=16, padx=20)

    count_label = tk.Label(
        summary_frame,
        text="Total Activities: 0",
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


def show_activity_page(parent, student_details):
    """Render the activity tracker UI inside the supplied parent frame.

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
        navigation.set_active_student_page("Activities")
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

    title = tk.Label(body, text="\U0001F3AF Extracurricular Activity Tracker", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(anchor="w", padx=30, pady=(16, 6))

    records_table = create_records_table(body)
    count_label = create_summary_section(body)
    create_add_activity_section(body, student_id, records_table, count_label)
    create_search_section(body, student_id, records_table)

    load_records(student_id, records_table)
    update_activity_count(student_id, count_label)
    theme.RoundedButton(
        body, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(body),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=theme.BG,
    ).pack(pady=(10, 20))


def open_activity_window(student_id):
    """Compatibility wrapper: open activity tracker in a standalone window."""

    window = tk.Tk()
    window.title("Activity Tracker")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_activity_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_activity_window(1)