"""
Main window for the Student Achievement & Portfolio Management System.

This file creates the first screen of the desktop application using Tkinter.
Backend modules and database connections will be added later.
"""

import tkinter as tk
from tkinter import messagebox

from gui.login_window import show_login_page
from gui.register_window import show_register_page
from gui.admin_login_window import show_admin_login_page
from gui import navigation
from gui import theme


def show_pending_message():
    """Show a message for modules that will be added later."""

    messagebox.showinfo("Information", "This module will be implemented next.")


def exit_application(window):
    """Ask the user before closing the application."""

    answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")

    if answer:
        window.destroy()


def center_window(window, width, height):
    """Center the application window on the screen."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(str(width) + "x" + str(height) + "+" + str(x_position) + "+" + str(y_position))


def create_footer(window):
    """Create the footer text."""

    footer_label = tk.Label(
        window,
        text="\U0001F352 Developed using Python, Tkinter and MySQL",
        bg=theme.BG,
        fg=theme.MUTED_TEXT,
        font=theme.FONT_LABEL
    )
    footer_label.pack(side="bottom", pady=16)


def main():
    """Create and run the main application window."""
    window = tk.Tk()
    window.title("Student Achievement & Portfolio Management System")
    window.configure(bg=theme.BG)
    navigation.apply_theme_style()
    window_width = navigation.APP_WIDTH
    window_height = navigation.APP_HEIGHT
    center_window(window, window_width, window_height)
    window.resizable(False, False)

    # Left sidebar - only shown once a student or admin is logged in.
    sidebar = tk.Frame(window, bg=navigation.SIDEBAR_BG, width=navigation.SIDEBAR_WIDTH)

    # Content frame where pages will be loaded
    content = tk.Frame(window, bg=navigation.CONTENT_BG)
    content.pack(side="right", expand=True, fill="both")

    # Register the content and sidebar frames with navigation helper
    navigation.set_content_frame(content)
    navigation.set_sidebar_frame(sidebar)

    # No side navigation before login - just show the login page.
    navigation.show_main_sidebar()
    show_login_page(content)

    create_footer(window)

    window.mainloop()


if __name__ == "__main__":
    main()
