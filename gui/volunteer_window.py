"""
Volunteer work tracker window for the Student Achievement & Portfolio Management System.

This file creates a Tkinter frontend for adding, viewing, searching, and
summarizing student volunteer work records.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from backend.volunteer import (
    add_volunteer_record,
    get_volunteer_records,
    search_by_organization,
    calculate_total_hours,
    count_volunteer_events,
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
    """Close the volunteer work tracker window."""

    window.destroy()


def create_header(window):
    """Create the header section."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F91D  Volunteer Work Tracker", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_records(student_id, records_table):
    """Load volunteer records into the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    try:
        records = get_volunteer_records(student_id)

        for record in records:
            records_table.insert(
                "",
                "end",
                values=(record[0], record[2], record[3], record[4], record[5])
            )

    except Exception as error:
        messagebox.showerror("Error", "Unable to load volunteer records.")
        print(error)


def load_search_results(records_table, records):
    """Display search results in the table."""

    for item in records_table.get_children():
        records_table.delete(item)

    for record in records:
        records_table.insert(
            "",
            "end",
            values=(record[0], record[2], record[3], record[4], record[5])
        )


def update_summary(student_id, hours_label, events_label):
    """Update the volunteer summary labels."""

    try:
        total_hours = calculate_total_hours(student_id)
    except Exception:
        total_hours = 0

    try:
        total_events = count_volunteer_events(student_id)
    except Exception:
        total_events = 0

    hours_label.config(text="Total Volunteer Hours: " + str(total_hours))
    events_label.config(text="Total Volunteer Events: " + str(total_events))


def clear_entries(
    organization_entry,
    role_entry,
    hours_entry,
    volunteer_date_entry
):
    """Clear all entry boxes after adding a volunteer record."""

    organization_entry.delete(0, tk.END)
    role_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    volunteer_date_entry.delete(0, tk.END)


def add_volunteer_button_clicked(
    student_id,
    organization_entry,
    role_entry,
    hours_entry,
    volunteer_date_entry,
    records_table,
    hours_label,
    events_label
):
    """Collect form data and add a new volunteer record."""

    try:
        organization = organization_entry.get()
        role = role_entry.get()
        hours = int(hours_entry.get())
        volunteer_date = volunteer_date_entry.get()

        success = add_volunteer_record(
            student_id,
            organization,
            role,
            hours,
            volunteer_date
        )

        if success:
            messagebox.showinfo("Success", "Volunteer record added successfully.")
            clear_entries(
                organization_entry,
                role_entry,
                hours_entry,
                volunteer_date_entry
            )
            load_records(student_id, records_table)
            update_summary(student_id, hours_label, events_label)
        else:
            messagebox.showerror("Error", "Could not add volunteer record.")

    except ValueError:
        messagebox.showerror("Error", "Hours must be a valid number.")

    except Exception as error:
        messagebox.showerror("Error", "Something went wrong.")
        print(error)


def search_organization_button_clicked(student_id, organization_entry, records_table):
    """Search volunteer records by organization."""

    try:
        organization = organization_entry.get()
        records = search_by_organization(student_id, organization)
        load_search_results(records_table, records)

    except Exception as error:
        messagebox.showerror("Error", "Unable to search by organization.")
        print(error)


def create_add_section(
    window,
    student_id,
    records_table,
    hours_label,
    events_label
):
    """Create the add volunteer record form."""

    card = theme.create_section_card(window)
    card.pack(pady=15, padx=30, fill="x")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(pady=18, padx=20)

    small_heading(form_frame, "Add Volunteer Record").grid(row=0, column=0, columnspan=4, pady=(0, 12), sticky="w")

    theme.field_label(form_frame, "Organization").grid(row=1, column=0, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Role").grid(row=1, column=1, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Hours").grid(row=1, column=2, padx=8, pady=5, sticky="w")
    theme.field_label(form_frame, "Volunteer Date").grid(row=1, column=3, padx=8, pady=5, sticky="w")

    organization_entry = theme.styled_entry(form_frame, width=24)
    organization_entry.grid(row=2, column=0, padx=8, pady=5, ipady=3)

    role_entry = theme.styled_entry(form_frame, width=22)
    role_entry.grid(row=2, column=1, padx=8, pady=5, ipady=3)

    hours_entry = theme.styled_entry(form_frame, width=16)
    hours_entry.grid(row=2, column=2, padx=8, pady=5, ipady=3)

    volunteer_date_entry = theme.styled_entry(form_frame, width=18)
    volunteer_date_entry.grid(row=2, column=3, padx=8, pady=5, ipady=3)

    def add_volunteer_button_pressed():
        add_volunteer_button_clicked(
            student_id,
            organization_entry,
            role_entry,
            hours_entry,
            volunteer_date_entry,
            records_table,
            hours_label,
            events_label
        )

    add_button = theme.RoundedButton(
        form_frame,
        text="Add Volunteer Record",
        command=add_volunteer_button_pressed,
        width=260,
        height=46,
        parent_bg=theme.CARD_BG,
    )
    add_button.grid(row=3, column=0, columnspan=4, pady=14)


def create_search_section(window, student_id, records_table):
    """Create organization search controls."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    search_frame = tk.Frame(card, bg=theme.CARD_BG)
    search_frame.pack(pady=16, padx=20)

    organization_entry = theme.styled_entry(search_frame, width=26)
    organization_entry.grid(row=0, column=0, padx=6, ipady=3)

    def search_button_pressed():
        search_organization_button_clicked(student_id, organization_entry, records_table)

    theme.RoundedButton(
        search_frame, text="Search Organization", command=search_button_pressed,
        width=200, height=42, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=0, column=1, padx=6)

    def show_all_button_pressed():
        load_records(student_id, records_table)

    theme.RoundedButton(
        search_frame, text="Show All", command=show_all_button_pressed,
        width=120, height=42, bg_color="#FFEFED", hover_color="#FFDEDA",
        fg_color=theme.ACCENT, font=theme.FONT_BUTTON_SM, parent_bg=theme.CARD_BG,
    ).grid(row=0, column=2, padx=6)


def create_records_table(window):
    """Create the volunteer records table."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="both")

    table_frame = tk.Frame(card, bg=theme.CARD_BG)
    table_frame.pack(pady=16, padx=20, fill="both", expand=True)

    small_heading(table_frame, "Volunteer Records").pack(anchor="w", pady=(0, 8))

    columns = (
        "Volunteer ID",
        "Organization",
        "Role",
        "Hours",
        "Volunteer Date"
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
    """Create the volunteer summary section."""

    card = theme.create_section_card(window)
    card.pack(pady=10, padx=30, fill="x")

    summary_frame = tk.Frame(card, bg=theme.CARD_BG)
    summary_frame.pack(pady=16, padx=20)

    small_heading(summary_frame, "Volunteer Summary").pack()

    hours_label = tk.Label(summary_frame, text="Total Volunteer Hours: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    hours_label.pack(pady=2)

    events_label = tk.Label(summary_frame, text="Total Volunteer Events: 0", bg=theme.CARD_BG, fg=theme.ACCENT, font=theme.FONT_BODY)
    events_label.pack(pady=2)

    return hours_label, events_label


def create_back_button(window):
    """Create the back button."""
    def close_button_pressed():
        close_window(window)

    theme.RoundedButton(
        window, text="Back", command=close_button_pressed,
        width=160, height=44, parent_bg=theme.BG,
    ).pack(pady=8)


def show_volunteer_page(parent, student_details):
    """Render the volunteer tracker UI inside the supplied parent frame.

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
        navigation.set_active_student_page("Volunteer Work")
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

    title = tk.Label(body, text="\U0001F91D Volunteer Work Tracker", bg=navigation.CONTENT_BG, fg=theme.ACCENT, font=FONT_HEADING_ROUGE_SM)
    title.pack(anchor="w", padx=30, pady=(16, 6))

    records_table = create_records_table(body)
    hours_label, events_label = create_summary_section(body)
    create_add_section(
        body,
        student_id,
        records_table,
        hours_label,
        events_label
    )
    create_search_section(body, student_id, records_table)

    load_records(student_id, records_table)
    update_summary(student_id, hours_label, events_label)
    theme.RoundedButton(
        body, text="Back to Dashboard",
        command=lambda: navigation.back_to_student_dashboard(body),
        width=220, height=46,
        bg_color="#FFEFED", hover_color="#FFDEDA", fg_color=theme.ACCENT,
        font=theme.FONT_BUTTON_SM, parent_bg=theme.BG,
    ).pack(pady=(10, 20))


def open_volunteer_window(student_id):
    """Compatibility wrapper: open volunteer tracker in a standalone window."""

    window = tk.Tk()
    window.title("Volunteer Work Tracker")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    show_volunteer_page(window, student_id)

    window.mainloop()


if __name__ == "__main__":
    open_volunteer_window(1)