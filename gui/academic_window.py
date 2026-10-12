"""
Academic tracker window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for adding and viewing academic records.
It uses existing backend functions and does not connect directly to MySQL.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.academics import (
    add_academic_record,
    calculate_average_marks,
    get_academic_records,
    get_highest_score,
    get_lowest_score,
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
    """Close the academic tracker window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F4D8  Academic Tracker", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_records(student_id, records_table):
    """Load academic records into the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    try:
        records = get_academic_records(student_id)

        for record in records:
            records_table.insert(
                "",
                "end",
                values=(record[0], record[2], record[3], record[4], record[5])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load academic records.")
        print(error)


def update_summary(student_id, average_label, highest_label, lowest_label):
    """Update the performance summary labels."""

    try:
        average = calculate_average_marks(student_id)
    except Exception:
        average = 0

    try:
        highest_score = get_highest_score(student_id)
    except Exception:
        highest_score = None

    try:
        lowest_score = get_lowest_score(student_id)
    except Exception:
        lowest_score = None

    if highest_score is None:
        highest_text = "0"
    else:
        highest_text = str(highest_score)

    if lowest_score is None:
        lowest_text = "0"
    else:
        lowest_text = str(lowest_score)

    average_label.config(text="Average Percentage: " + str(average) + "%")
    highest_label.config(text="Highest Score: " + highest_text)
    lowest_label.config(text="Lowest Score: " + lowest_text)


def clear_entries(subject_entry, exam_type_entry, marks_entry, maximum_entry):
    """Clear all entry boxes after adding a record."""

    subject_entry.delete(0, tk.END)
    exam_type_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    maximum_entry.delete(0, tk.END)


def add_record_button_clicked(
    student_id,
    subject_entry,
    exam_type_entry,
    marks_entry,
    maximum_entry,
    records_table,
    average_label,
    highest_label,
    lowest_label
):
    """Collect form data and add a new academic record."""

    try:
        subject = subject_entry.get()
        exam_type = exam_type_entry.get()
        marks_obtained = int(marks_entry.get())
        maximum_marks = int(maximum_entry.get())

        success = add_academic_record(
            student_id,
            subject,
            exam_type,
            marks_obtained,
            maximum_marks
        )

        if success:
            messagebox.showinfo("Success", "Academic record added successfully.")
            clear_entries(subject_entry, exam_type_entry, marks_entry, maximum_entry)
            load_records(student_id, records_table)
            update_summary(student_id, average_label, highest_label, lowest_label)
        else:
            messagebox.showerror("Error", "Could not add academic record.")

    except ValueError:
        messagebox.showerror("Error", "Marks must be valid numbers.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def create_add_record_section(
    window,
    student_id,
    records_table,
    average_label,
    highest_label,
    lowest_label
):
    """Create the add academic record form."""

    card = theme.create_section_card(window)
    card.pack(pady=15, padx=30, fill="x")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(pady=18, padx=20)

    small_heading(form_frame, "Add Academic Record").grid(row=0, column=0, columnspan=4, pady=(0, 12), sticky="w")

    theme.field_label(form_frame, "Subject").grid(row=1, column=0, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Exam Type").grid(row=1, column=1, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Marks Obtained").grid(row=1, column=2, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Maximum Marks").grid(row=1, column=3, padx=8, pady=5, sticky="w")

    subject_entry = theme.styled_entry(form_frame, width=22)
    subject_entry.grid(row=2, column=0, padx=8, pady=5, ipady=3)

    exam_type_entry = theme.styled_entry(form_frame, width=22)
    exam_type_entry.grid(row=2, column=1, padx=8, pady=5, ipady=3)

    marks_entry = theme.styled_entry(form_frame, width=18)
    marks_entry.grid(row=2, column=2, padx=8, pady=5, ipady=3)

    maximum_entry = theme.styled_entry(form_frame, width=18)
    maximum_entry.grid(row=2, column=3, padx=8, pady=5, ipady=3)

    def add_record_button_pressed():
        add_record_button_clicked(
            student_id,
            subject_entry,
            exam_type_entry,
            marks_entry,
            maximum_entry,
            records_table,
            average_label,
            highest_label,
            lowest_label
        )

    add_button = theme.RoundedButton(
        form_frame,
        text="Add Record",
        command=add_record_button_pressed,
        width=220,
        height=46,
        parent_bg=theme.CARD_BG,
    )
    add_button.grid(row=3, column=0, columnspan=4, pady=14)


def create_records_table(window):
    """Create the academic records table."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="both")

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=16, padx=20, fill="both", expand=True)

    small_heading(table_frame, "Academic Records").pack(anchor="w", pady=(0, 8))

    columns = ("Record ID", "Subject", "Exam Type", "Marks Obtained", "Maximum Marks")

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
    """Create the performance summary section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    summary_frame = tk.Frame(card, bg=theme.CARD_BG)
    summary_frame.pack(pady=16, padx=20)

    small_heading(summary_frame, "Performance Summary").pack()

    average_label = tk.Label(summary_frame, text="Average Percentage: 0%", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    average_label.pack(pady=2)

    highest_label = tk.Label(summary_frame, text="Highest Score: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    highest_label.pack(pady=2)

    lowest_label = tk.Label(summary_frame, text="Lowest Score: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    lowest_label.pack(pady=2)

    return average_label, highest_label, lowest_label


def create_back_button(window):
    """Create the back button."""
    def close_button_pressed():
        close_window(window)

    theme.RoundedButton(
        window,
        text="Back",
        command=close_button_pressed,
        width=160,
        height=44,
        parent_bg=theme.BG,
    ).pack(pady=8)


def show_academic_page(parent, student_details):
    """Render the academic tracker UI inside the supplied parent frame.

    `student_details` may be a dict (from dashboard) or an integer student_id
    for compatibility with standalone windows.
    """

    # Accept either dict or id
    if isinstance(student_details, dict):
        sd = student_details
        student_id = sd.get("Student_ID")
    else:
        sd = None
        student_id = student_details

    from gui import dashboard as _dashboard

    # Ensure sidebar and active highlighting
    try:
        navigation.set_active_student_page("Academic Tracker")
        if isinstance(student_details, dict):
            navigation.show_student_sidebar(student_details)
        else:
            navigation.show_student_sidebar({"Full_Name": "Student"})
    except Exception:
        pass

    body = navigation.prepare_content(parent)

    # Use dashboard header so typography and spacing match exactly
    if sd is not None:
        _dashboard.create_header(body, sd)
    else:
        _dashboard.create_header(body, {"Full_Name": "Student"})

    # Page title aligned with dashboard content
    title = tk.Label(body, text="\U0001F4D8 Academic Tracker", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(anchor="w", padx=30, pady=(16, 6))

    records_table = create_records_table(body)
    average_label, highest_label, lowest_label = create_summary_section(body)

    create_add_record_section(
        body,
        student_id,
        records_table,
        average_label,
        highest_label,
        lowest_label
    )

    load_records(student_id, records_table)
    update_summary(student_id, average_label, highest_label, lowest_label)
    theme.RoundedButton(
        body, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(body),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=theme.BG,
    ).pack(pady=(10, 20))


def open_academic_window(student_id):
    """Compatibility wrapper: open academic tracker in a standalone window."""

    window = tk.Tk()
    window.title("Academic Tracker")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_academic_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_academic_window(1)