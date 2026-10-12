"""
Student registration window for the Student Achievement & Portfolio Management System.

This file creates a simple Tkinter registration screen and uses the backend
register_student() function to register a new student.
"""

import tkinter as tk
from tkinter import messagebox

from backend.register import register_student
from gui import navigation
from gui import theme

# Decorative fonts used only for on-screen headings (theme.py untouched).
FONT_HEADING_ROUGE = ("Rouge Script", 32, "bold")
FONT_SUBHEADING_FELIPA = ("Felipa", 13)
FONT_SECTION_FELIPA = ("Felipa", 15, "bold")


def close_window(window):
    """Close the registration window (kept for compatibility)."""

    window.destroy()


def clear_entries(entries):
    """Clear all registration entry boxes."""

    for entry in entries:
        entry.delete(0, tk.END)


def handle_register(parent, entries):
    """Read registration details and register the student."""

    full_name = entries[0].get()
    student_class = entries[1].get()
    section = entries[2].get()
    email = entries[3].get()
    phone = entries[4].get()
    password = entries[5].get()

    success, result = register_student(
        full_name,
        student_class,
        section,
        email,
        phone,
        "Not specified",
        password
    )

    if success:
        # result contains student details dict
        student_details = result

        # If this form was opened in a standalone window, close it and
        # open the dashboard inside the main application (if available).
        # import here to avoid circular module import issues
        from gui import navigation
        from gui import dashboard as _dashboard

        try:
            top = parent.winfo_toplevel()
        except Exception:
            top = None

        main_top = None
        try:
            if navigation.content_frame is not None:
                main_top = navigation.content_frame.winfo_toplevel()
        except Exception:
            main_top = None

        # Close standalone register window if it's not the main app window
        if top is not None and main_top is not None and top != main_top:
            try:
                top.destroy()
            except Exception:
                pass

        # Show student sidebar and dashboard in the main content frame if available
        try:
            if navigation.content_frame is not None and navigation.sidebar_frame is not None:
                navigation.show_student_sidebar(student_details)
                _dashboard.show_dashboard(navigation.content_frame, student_details)
            else:
                # Embedded parent (clear and show dashboard)
                for w in parent.winfo_children():
                    w.destroy()
                navigation.show_student_sidebar(student_details)
                _dashboard.show_dashboard(parent, student_details)
        except Exception:
            pass

    else:
        # result contains an error message
        messagebox.showerror("Registration Failed", result)


def create_header(parent):
    """Create the cherry-red header section inside the supplied parent frame."""

    header_frame = tk.Frame(parent, bg=theme.ACCENT)
    header_frame.pack(fill="x")

    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))

    tk.Label(
        inner,
        text="\U0001F4DD  Student Registration",
        bg=theme.ACCENT,
        fg="white",
        font=FONT_HEADING_ROUGE,
    ).pack()

    tk.Label(
        inner,
        text="Create your student portfolio account",
        bg=theme.ACCENT,
        fg="#FFD7D3",
        font=FONT_SUBHEADING_FELIPA,
    ).pack(pady=(4, 0))


def create_registration_form(parent):
    """Create labels, entry boxes, and buttons for the registration form."""

    outer = tk.Frame(parent, bg=theme.BG)
    outer.pack(expand=True, fill="both", pady=30)

    card = theme.create_section_card(outer)
    card.pack(anchor="center")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(padx=50, pady=30)

    tk.Label(
        form_frame,
        text="Tell us about yourself",
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=FONT_SECTION_FELIPA,
    ).pack(anchor="w", pady=(0, 14))

    entries = []

    labels = [
        "Full Name",
        "Class",
        "Section",
        "Email",
        "Phone Number",
        "Password"
    ]

    for label_text in labels:
        label = theme.field_label(form_frame, label_text)
        label.pack(anchor="w")

        if label_text == "Password":
            entry = theme.styled_entry(form_frame, width=32, show="*")
        else:
            entry = theme.styled_entry(form_frame, width=32)

        entry.pack(pady=(5, 12), ipady=3)
        entries.append(entry)

    def register_button_pressed():
        handle_register(parent, entries)

    register_button = theme.RoundedButton(
        form_frame,
        text="\u2728 Register",
        command=register_button_pressed,
        width=260,
        height=50,
        parent_bg=theme.CARD_BG,
    )
    register_button.pack(pady=8)


def center_window(window, width, height):
    """Center a top-level window on the screen (kept for compatibility)."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def show_register_page(parent):
    """Place the registration UI inside the supplied parent frame."""
    body = navigation.prepare_content(parent)
    create_header(body)
    create_registration_form(body)


def open_register_window():
    """Compatibility wrapper: open a standalone registration window."""

    window = tk.Tk()
    window.title("Student Registration")
    window.configure(bg=theme.BG)

    center_window(window, 560, 760)
    window.resizable(False, False)

    create_header(window)
    create_registration_form(window)

    window.mainloop()


if __name__ == "__main__":
    open_register_window()