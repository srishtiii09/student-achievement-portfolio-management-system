"""
Student login window for the Student Achievement & Portfolio Management System.

This file creates a simple Tkinter login screen and uses the backend
login_student() function to verify student login details.
"""

import tkinter as tk
from tkinter import messagebox

from backend.login import login_student
from gui import navigation
from gui import theme

# Decorative fonts used only for on-screen headings (theme.py untouched).
FONT_HEADING_ROUGE = ("Rouge Script", 32, "bold")
FONT_HEADING_ROUGE_SIDEBAR = ("Rouge Script", 24, "bold")
FONT_SUBHEADING_FELIPA = ("Felipa", 13)
FONT_SECTION_FELIPA = ("Felipa", 15, "bold")


def handle_login(parent_frame, email_entry, password_entry):
    """Get login details from entry boxes and check student login."""

    email = email_entry.get()
    password = password_entry.get()

    student_details = login_student(email, password)

    if student_details is not None:
        # On success, directly open the dashboard inside the main content frame.
        navigation.open_dashboard(student_details)
    else:
        messagebox.showerror("Login", "Invalid email or password")


def close_window(window):
    """Close the login window."""

    window.destroy()


def create_header(parent):
    """Create the cherry-red header section inside the supplied parent frame."""

    header_frame = tk.Frame(parent, bg=theme.ACCENT)
    header_frame.pack(fill="x")

    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))

    title_label = tk.Label(
        inner,
        text="\U0001F510  Student Login",
        bg=theme.ACCENT,
        fg="white",
        font=FONT_HEADING_ROUGE,
    )
    title_label.pack()

    subtitle_label = tk.Label(
        inner,
        text="Student Achievement & Portfolio Management System",
        bg=theme.ACCENT,
        fg="#FFD7D3",
        font=FONT_SUBHEADING_FELIPA,
    )
    subtitle_label.pack(pady=(4, 0))


def create_side_navigation(parent):
    """Show quick links to Student Login, Registration, and Admin Login.

    Uses the same sidebar frame/style as the rest of the app so the visitor
    can jump between the three entry pages without a Back button.
    """

    sidebar = navigation.sidebar_frame

    if sidebar is None:
        return

    for w in sidebar.winfo_children():
        w.destroy()

    sidebar.configure(bg=theme.ACCENT)
    sidebar.pack_forget()
    sidebar.pack(side="left", fill="y")

    accent = tk.Frame(sidebar, bg="#FF9DBB", height=3)
    accent.pack(fill="x", side="top")

    title = tk.Label(
        sidebar,
        text="\u2728 Student Portfolio",
        bg=theme.ACCENT,
        fg="white",
        font=FONT_HEADING_ROUGE_SIDEBAR,
        wraplength=navigation.SIDEBAR_WIDTH - 30,
        justify="center",
    )
    title.pack(pady=(24, 18))

    target = navigation.content_frame if navigation.content_frame is not None else parent

    def go_login():
        show_login_page(parent)

    def go_register():
        from gui.register_window import show_register_page
        show_register_page(target)

    def go_admin():
        from gui.admin_login_window import show_admin_login_page
        show_admin_login_page(target)

    nav_items = [
        ("\U0001F511 Student Login", go_login, True),
        ("\U0001F4DD Student Registration", go_register, False),
        ("\U0001F6E1\uFE0F Admin Login", go_admin, False),
    ]

    for label, cmd, is_active in nav_items:
        bg_color = "#6B1B10" if is_active else "#7A231A"
        wrapper = tk.Frame(sidebar, bg=theme.ACCENT)
        wrapper.pack(pady=4, padx=16, fill="x")

        theme.RoundedButton(
            wrapper,
            text=label,
            command=cmd,
            width=navigation.SIDEBAR_WIDTH - 32,
            height=44,
            radius=14,
            bg_color=bg_color,
            hover_color="#8A2E22",
            fg_color="white",
            font=theme.FONT_BUTTON_SM,
            parent_bg=theme.ACCENT,
        ).pack(fill="x")


def create_login_form(parent):
    """Create labels, entry boxes, and buttons for the login form."""

    outer = tk.Frame(parent, bg=theme.BG)
    outer.pack(expand=True, fill="both", pady=50)

    card = theme.create_section_card(outer)
    card.pack(anchor="center")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(padx=50, pady=40)

    tk.Label(
        form_frame,
        text="Welcome back!",
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=FONT_SECTION_FELIPA,
    ).pack(anchor="w", pady=(0, 18))

    email_label = theme.field_label(form_frame, "Email")
    email_label.pack(anchor="w")

    email_entry = theme.styled_entry(form_frame, width=32)
    email_entry.pack(pady=(6, 20), ipady=4)

    password_label = theme.field_label(form_frame, "Password")
    password_label.pack(anchor="w")

    password_entry = theme.styled_entry(form_frame, width=32, show="*")
    password_entry.pack(pady=(6, 26), ipady=4)

    def login_button_pressed():
        handle_login(parent, email_entry, password_entry)

    login_button = theme.RoundedButton(
        form_frame,
        text="\U0001F511 Login",
        command=login_button_pressed,
        width=260,
        height=50,
        parent_bg=theme.CARD_BG,
    )
    login_button.pack(pady=8)


def center_window(window, width, height):
    """Center a top-level window on the screen (kept for compatibility)."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def show_login_page(parent):
    """Place the student login interface inside the supplied parent frame."""
    create_side_navigation(parent)
    body = navigation.prepare_content(parent)

    create_header(body)
    create_login_form(body)


def open_login_window():
    """Compatibility wrapper: open a standalone login window."""

    window = tk.Tk()
    window.title("Student Login")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    create_header(window)
    create_login_form(window)

    window.mainloop()


if __name__ == "__main__":
    open_login_window()