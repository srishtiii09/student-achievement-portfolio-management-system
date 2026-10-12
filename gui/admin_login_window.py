"""
Admin login window for the Student Achievement & Portfolio Management System.

This file creates a simple Tkinter admin login screen and uses the backend
admin_login() function to verify admin login details.
"""

import tkinter as tk
from tkinter import messagebox

from backend.admin import admin_login
from gui import navigation
from gui import theme

# Decorative fonts used only for on-screen headings (theme.py untouched).
FONT_HEADING_ROUGE = ("Rouge Script", 32, "bold")
FONT_SUBHEADING_FELIPA = ("Felipa", 13)
FONT_SECTION_FELIPA = ("Felipa", 15, "bold")


def center_window(window, width, height):
    """Center the admin login window on the screen."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def create_header(parent):
    """Create the cherry-red header section inside the supplied parent frame.

    Matches the student login header exactly (size, font, positioning).
    """

    header_frame = tk.Frame(parent, bg=theme.ACCENT)
    header_frame.pack(fill="x")

    inner = tk.Frame(header_frame, bg=theme.ACCENT)
    inner.pack(pady=(22, 18))

    tk.Label(
        inner,
        text="\U0001F6E1\uFE0F  Admin Login",
        bg=theme.ACCENT,
        fg="white",
        font=FONT_HEADING_ROUGE,
    ).pack()

    tk.Label(
        inner,
        text="Student Achievement & Portfolio Management System",
        bg=theme.ACCENT,
        fg="#FFD7D3",
        font=FONT_SUBHEADING_FELIPA,
    ).pack(pady=(4, 0))


def create_login_form(parent):
    """Create labels, entry boxes, and buttons for the admin login form."""

    outer = tk.Frame(parent, bg=theme.BG)
    outer.pack(expand=True, fill="both", pady=50)

    card = theme.create_section_card(outer)
    card.pack(anchor="center")

    form_frame = tk.Frame(card, bg=theme.CARD_BG)
    form_frame.pack(padx=50, pady=40)

    tk.Label(
        form_frame,
        text="Administrator Access",
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=FONT_SECTION_FELIPA,
    ).pack(anchor="w", pady=(0, 18))

    username_label = theme.field_label(form_frame, "Username")
    username_label.pack(anchor="w")

    username_entry = theme.styled_entry(form_frame, width=32)
    username_entry.pack(pady=(6, 20), ipady=4)

    password_label = theme.field_label(form_frame, "Password")
    password_label.pack(anchor="w")

    password_entry = theme.styled_entry(form_frame, width=32, show="*")
    password_entry.pack(pady=(6, 26), ipady=4)

    login_button = theme.RoundedButton(
        form_frame,
        text="\U0001F511 Login",
        command=None,
        width=260,
        height=50,
        parent_bg=theme.CARD_BG,
    )
    login_button.pack(pady=8)

    return username_entry, password_entry, login_button


def handle_admin_login(parent_frame, username_entry, password_entry):
    """Read admin login details and check them using the backend function."""

    username = username_entry.get()
    password = password_entry.get()

    admin_details = admin_login(username, password)

    if admin_details is not None:
        # Open the admin dashboard inside the application's content frame
        navigation.open_admin_dashboard(admin_details)
    else:
        messagebox.showerror("Login", "Invalid username or password")


def close_window(window):
    """Close the admin login window (kept for compatibility)."""

    window.destroy()


def show_admin_login_page(parent):
    """Place the admin login UI inside the supplied parent frame."""
    body = navigation.prepare_content(parent)

    create_header(body)
    username_entry, password_entry, login_button = create_login_form(body)

    def handle_login_click():
        handle_admin_login(body, username_entry, password_entry)

    login_button.command = handle_login_click


def open_admin_login_window():
    """Compatibility wrapper: open a standalone admin login window."""

    window = tk.Tk()
    window.title("Admin Login")
    window.configure(bg=theme.BG)

    center_window(window, navigation.APP_WIDTH, navigation.APP_HEIGHT)
    window.resizable(False, False)

    username_entry, password_entry, login_button = create_login_form(window)

    def handle_login_click():
        handle_admin_login(window, username_entry, password_entry)

    login_button.command = handle_login_click

    window.mainloop()

if __name__ == "__main__":
    open_admin_login_window()