"""
Admin dashboard page for the Student Achievement & Portfolio Management System.

This module renders admin dashboard content inside the shared application
content frame. It does not create new Tk windows or call mainloop().
"""

import tkinter as tk
from tkinter import messagebox

from gui.admin_reports_window import show_admin_reports_page
from gui.leaderboard_window import show_leaderboard_page
from gui.manage_students_window import show_manage_students_page
from gui import navigation
from gui import theme


def create_header(parent, admin_details):
    """Create the cherry-red header section."""

    theme.create_page_header(
        parent,
        icon="\U0001F6E1\uFE0F",
        title_text="Welcome, Admin",
        subtitle_text="Student Achievement & Portfolio Management System",
    )


def create_admin_information(parent, admin_details):
    """Create the admin information section."""

    info_frame = tk.Frame(parent, bg=theme.BG)
    info_frame.pack(pady=24)

    card = theme.create_section_card(info_frame)
    card.pack()

    inner = tk.Frame(card, bg=theme.CARD_BG)
    inner.pack(padx=30, pady=18)

    username_label = tk.Label(
        inner,
        text="Username: " + str(admin_details[0]),
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=theme.FONT_BODY
    )
    username_label.pack(anchor="w", pady=3)

    role_label = tk.Label(
        inner,
        text="Role: Administrator",
        bg=theme.CARD_BG,
        fg=theme.ACCENT,
        font=theme.FONT_BODY
    )
    role_label.pack(anchor="w", pady=3)


def create_navigation_buttons(parent, admin_details):
    """Create navigation buttons for the admin dashboard."""
    button_frame = tk.Frame(parent, bg=theme.BG)
    button_frame.pack(pady=20)

    inner = tk.Frame(button_frame, bg=theme.BG)
    inner.pack()

    items = [
        ("\U0001F9D1\u200D\U0001F393 Manage Students", lambda: show_manage_students_page(navigation.content_frame, admin_details)),
        ("\U0001F4CA View Reports", lambda: show_admin_reports_page(navigation.content_frame, admin_details)),
        ("\U0001F451 View Leaderboard", lambda: show_leaderboard_page(navigation.content_frame, admin_details)),
    ]

    for label, cmd in items:
        theme.RoundedButton(
            inner,
            text=label,
            command=cmd,
            width=340,
            height=52,
            parent_bg=theme.BG,
        ).pack(pady=8)

    def do_logout():
        navigation.clear_content()
        navigation.show_main_sidebar()
        try:
            from gui.admin_login_window import show_admin_login_page
            show_admin_login_page(navigation.content_frame)
        except Exception:
            pass

    theme.RoundedButton(
        inner,
        text="\U0001F6AA Logout",
        command=do_logout,
        width=340,
        height=52,
        bg_color=theme.ACCENT,
        hover_color=theme.ACCENT_SOFT,
        fg_color="white",
        font=("Instrument Serif", 14, "bold"),
        parent_bg=theme.BG,
    ).pack(pady=(18, 8))


def show_admin_dashboard(parent, admin_details):
    """Render the admin dashboard inside the supplied parent frame."""
    body = navigation.prepare_content(parent)

    create_header(body, admin_details)
    create_admin_information(body, admin_details)
    create_navigation_buttons(body, admin_details)
