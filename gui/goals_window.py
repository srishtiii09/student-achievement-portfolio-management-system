"""
Goal tracker window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for adding, viewing, updating, and
counting student goals.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.goals import (
    add_goal,
    get_goals,
    update_goal_status,
    count_completed_goals,
    count_pending_goals
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
    """Close the goal tracker window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\u2705  Goal Tracker", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_records(student_id, records_table):
    """Load goal records into the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    try:
        records = get_goals(student_id)

        for record in records:
            records_table.insert(
                "",
                "end",
                values=(record[0], record[2], record[3], record[4])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load goal records.")
        print(error)


def update_summary(student_id, completed_label, pending_label):
    """Update the goal summary labels."""

    try:
        completed_goals = count_completed_goals(student_id)
    except Exception:
        completed_goals = 0

    try:
        pending_goals = count_pending_goals(student_id)
    except Exception:
        pending_goals = 0

    completed_label.config(text="Completed Goals: " + str(completed_goals))
    pending_label.config(text="Pending Goals: " + str(pending_goals))


def clear_entries(goal_title_entry, status_entry, deadline_entry):
    """Clear all entry boxes after adding a goal."""

    goal_title_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)


def clear_status_entries(goal_id_entry, new_status_entry):
    """Clear status update entry boxes."""

    goal_id_entry.delete(0, tk.END)
    new_status_entry.delete(0, tk.END)


def add_goal_button_clicked(
    student_id,
    goal_title_entry,
    status_entry,
    deadline_entry,
    records_table,
    completed_label,
    pending_label
):
    """Collect form data and add a new goal record."""

    try:
        goal_title = goal_title_entry.get()
        status = status_entry.get()
        deadline = deadline_entry.get()

        success = add_goal(
            student_id,
            goal_title,
            status,
            deadline
        )

        if success:
            messagebox.showinfo("Success", "Goal added successfully.")
            clear_entries(goal_title_entry, status_entry, deadline_entry)
            load_records(student_id, records_table)
            update_summary(student_id, completed_label, pending_label)
        else:
            messagebox.showerror("Error", "Could not add goal.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def update_status_button_clicked(
    student_id,
    goal_id_entry,
    new_status_entry,
    records_table,
    completed_label,
    pending_label
):
    """Collect status update data and update a goal status."""

    try:
        goal_id = int(goal_id_entry.get())
        new_status = new_status_entry.get()

        success = update_goal_status(goal_id, new_status)

        if success:
            messagebox.showinfo("Success", "Goal status updated successfully.")
            clear_status_entries(goal_id_entry, new_status_entry)
            load_records(student_id, records_table)
            update_summary(student_id, completed_label, pending_label)
        else:
            messagebox.showerror("Error", "Could not update goal status.")

    except ValueError:
        messagebox.showerror("Error", "Goal ID must be a valid number.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def create_summary_section(window):
    """Create the goals summary section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    summary_frame = tk.Frame(card, bg=theme.CARD_BG)
    summary_frame.pack(pady=16, padx=20)

    small_heading(summary_frame, "Goals Summary").pack()

    completed_label = tk.Label(summary_frame, text="Completed Goals: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    completed_label.pack(pady=2)

    pending_label = tk.Label(summary_frame, text="Pending Goals: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    pending_label.pack(pady=2)

    return completed_label, pending_label


def create_add_section(
    window,
    student_id,
    records_table,
    completed_label,
    pending_label
):
    """Create the add goal form."""

    card = theme.create_section_card(window)
    card.pack(pady=15, padx=30, fill="x")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(pady=18, padx=20)

    small_heading(form_frame, "Add Goal").grid(row=0, column=0, columnspan=3, pady=(0, 12), sticky="w")

    theme.field_label(form_frame, "Goal Title").grid(row=1, column=0, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Status").grid(row=1, column=1, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Deadline").grid(row=1, column=2, padx=8, pady=5, sticky="w")

    goal_title_entry = theme.styled_entry(form_frame, width=30)
    goal_title_entry.grid(row=2, column=0, padx=8, pady=5, ipady=3)

    status_entry = theme.styled_entry(form_frame, width=22)
    status_entry.grid(row=2, column=1, padx=8, pady=5, ipady=3)

    deadline_entry = theme.styled_entry(form_frame, width=20)
    deadline_entry.grid(row=2, column=2, padx=8, pady=5, ipady=3)

    def add_goal_button_pressed():
        add_goal_button_clicked(
            student_id,
            goal_title_entry,
            status_entry,
            deadline_entry,
            records_table,
            completed_label,
            pending_label
        )

    add_button = theme.RoundedButton(
        form_frame,
        text="Add Goal",
        command=add_goal_button_pressed,
        width=220,
        height=46,
        parent_bg=theme.CARD_BG,
    )
    add_button.grid(row=3, column=0, columnspan=3, pady=14)


def create_status_update_section(
    window,
    student_id,
    records_table,
    completed_label,
    pending_label
):
    """Create the goal status update section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    update_frame = tk.Frame(card, bg=theme.CARD_BG)
    update_frame.pack(pady=18, padx=20)

    small_heading(update_frame, "Update Goal Status").grid(row=0, column=0, columnspan=3, pady=(0, 12), sticky="w")

    theme.field_label(update_frame, "Goal ID").grid(row=1, column=0, padx=8, pady=5, sticky="w")
    theme.field_label(update_frame, "New Status").grid(row=1, column=1, padx=8, pady=5, sticky="w")

    goal_id_entry = theme.styled_entry(update_frame, width=18)
    goal_id_entry.grid(row=2, column=0, padx=8, pady=5, ipady=3)

    new_status_entry = theme.styled_entry(update_frame, width=24)
    new_status_entry.grid(row=2, column=1, padx=8, pady=5, ipady=3)

    def update_status_button_pressed():
        update_status_button_clicked(
            student_id,
            goal_id_entry,
            new_status_entry,
            records_table,
            completed_label,
            pending_label
        )

    theme.RoundedButton(
        update_frame,
        text="Update Status",
        command=update_status_button_pressed,
        width=200,
        height=44,
        parent_bg=theme.CARD_BG,
    ).grid(row=2, column=2, padx=8, pady=5)


def create_records_table(window):
    """Create the goals records table."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="both")

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=16, padx=20, fill="both", expand=True)

    small_heading(table_frame, "Goal Records").pack(anchor="w", pady=(0, 8))

    columns = (
        "Goal ID",
        "Goal Title",
        "Status",
        "Deadline"
    )

    records_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=7
    )

    column_widths = (120, 330, 180, 180)

    for index, column in enumerate(columns):
        records_table.heading(column, text=column)
        records_table.column(column, width=column_widths[index] + 80, anchor="center", stretch=True)

    records_table.pack(fill="both", expand=True)

    return records_table


def create_back_button(window):
    """Create the back button."""
    def close_button_pressed():
        close_window(window)

    theme.RoundedButton(
        window, text="Back", command=close_button_pressed,
        width=160, height=44, parent_bg=theme.BG,
    ).pack(pady=8)


def show_goals_page(parent, student_details):
    """Render the goals UI inside the supplied parent frame.

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
        navigation.set_active_student_page("Goals")
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

    title = tk.Label(body, text="\u2705 Goal Tracker", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(anchor="w", padx=30, pady=(16, 6))

    records_table = create_records_table(body)
    completed_label, pending_label = create_summary_section(body)
    create_add_section(
        body,
        student_id,
        records_table,
        completed_label,
        pending_label
    )
    create_status_update_section(
        body,
        student_id,
        records_table,
        completed_label,
        pending_label
    )

    load_records(student_id, records_table)
    update_summary(student_id, completed_label, pending_label)
    theme.RoundedButton(
        body, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(body),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=theme.BG,
    ).pack(pady=(10, 20))


def open_goals_window(student_id):
    """Compatibility wrapper: open goals in a standalone window."""

    window = tk.Tk()
    window.title("Goal Tracker")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_goals_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_goals_window(1)