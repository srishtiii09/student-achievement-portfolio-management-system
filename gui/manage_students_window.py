"""
Manage students window for the Student Achievement & Portfolio Management System.
"""

import tkinter as tk
from tkinter import messagebox

from backend.admin import delete_student, view_all_students
from gui import navigation
from gui import theme

# Decorative font used only for the on-screen heading (theme.py untouched).
FONT_HEADING_ROUGE_SM = ("Rouge Script", 26, "bold")


def center_window(window, width, height):
    """Center the window."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def create_header(window):
    """Create the header."""

    header_frame = tk.Frame(window, bg=theme.ACCENT)
    header_frame.pack(fill="x")
    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))
    tk.Label(
        inner, text="\U0001F9D1\u200D\U0001F393  Manage Students", bg=theme.ACCENT, fg="white",
        font=FONT_HEADING_ROUGE_SM,
    ).pack()


def load_student_list(listbox):
    """Load students from database."""

    listbox.delete(0, tk.END)

    students = view_all_students()

    if not students:
        listbox.insert(tk.END, "No students found.")
        return

    listbox.insert(
        tk.END,
        "ID      Name                           Class     Section"
    )

    for student in students:
        student_id = student[0]
        name = student[1]
        student_class = student[2]
        section = student[3]

        listbox.insert(
            tk.END,
            f"{student_id:<6}{name:<30}{student_class:<10}{section}"
        )


def create_student_table(window):
    """Create student list."""

    card = theme.create_section_card(window)
    card.pack(pady=20, padx=30, fill="both")

    frame = tk.Frame(card, bg=theme.CARD_BG)
    frame.pack(pady=20, padx=20)

    listbox = tk.Listbox(
        frame,
        width=72,
        height=15,
        font=("Instrument Serif", 12),
        bg="#FFFBFA",
        fg=theme.ACCENT,
        selectbackground="#FFC9C4",
        selectforeground=theme.ACCENT,
        highlightbackground=theme.CARD_BORDER,
        highlightthickness=1,
        bd=0
    )

    listbox.pack()

    load_student_list(listbox)

    return listbox


def refresh_student_list(listbox):
    load_student_list(listbox)


def delete_selected_student(listbox):
    """Delete selected student."""

    selected = listbox.curselection()

    if not selected:
        messagebox.showinfo(
            "Information",
            "Please select a student."
        )
        return

    text = listbox.get(selected[0])

    if text.startswith("ID") or text == "No students found.":
        return

    try:
        student_id = int(text.split()[0])
    except Exception:
        messagebox.showerror(
            "Error",
            "Invalid selection."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Delete selected student?"
    )

    if not confirm:
        return

    if delete_student(student_id):
        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )
        refresh_student_list(listbox)
    else:
        messagebox.showerror(
            "Error",
            "Unable to delete student."
        )


def create_buttons(parent, listbox, admin_details=None):
    """Create action buttons for the manage students page."""

    frame = tk.Frame(parent, bg=theme.BG)
    frame.pack(pady=15)

    theme.RoundedButton(
        frame,
        text="\U0001F504 Refresh",
        command=lambda: refresh_student_list(listbox),
        width=260,
        height=48,
        parent_bg=theme.BG,
    ).pack(pady=6)

    theme.RoundedButton(
        frame,
        text="\U0001F5D1\uFE0F Delete Selected Student",
        command=lambda: delete_selected_student(listbox),
        width=260,
        height=48,
        bg_color=theme.ACCENT,
        hover_color=theme.ACCENT_SOFT,
        fg_color="white",
        font=("Instrument Serif", 13, "bold"),
        parent_bg=theme.BG,
    ).pack(pady=6)

    def back_to_dashboard():
        if admin_details is not None:
            navigation.open_admin_dashboard(admin_details)
        else:
            navigation.clear_content()
            navigation.show_main_sidebar()

    theme.RoundedButton(
        frame,
        text="\U0001F519 Back to Dashboard",
        command=back_to_dashboard,
        width=260,
        height=48,
        bg_color="#FFEFED",
        hover_color="#FFDEDA",
        fg_color=theme.ACCENT,
        parent_bg=theme.BG,
    ).pack(pady=6)


def show_manage_students_page(parent, admin_details=None):
    """Render the manage students page inside the supplied parent frame."""
    if admin_details is not None:
        navigation.set_active_admin_page("Manage Students")
        navigation.show_admin_sidebar(admin_details)
    body = navigation.prepare_content(parent)

    create_header(body)
    listbox = create_student_table(body)
    create_buttons(body, listbox, admin_details)