"""
Navigation helper to manage the single application content frame and
provide shared layout helpers used across all pages.

Pages should call `prepare_content(parent)` to get a centered content
frame that follows the application's spacing and alignment rules.
"""

import tkinter as tk
from tkinter import ttk

from gui import theme

# Application layout constants
APP_WIDTH = 1500
APP_HEIGHT = 900
SIDEBAR_WIDTH = 280
SIDEBAR_BG = theme.ACCENT
CONTENT_BG = theme.BG
DEFAULT_FONT = theme.FONT_BODY

content_frame = None
sidebar_frame = None
current_student = None
current_admin = None
active_student_page = None
active_admin_page = None


def apply_theme_style():
    """Configure ttk widgets (tables) to match the cherry red Y2K theme.

    Call this once after the main Tk window is created.
    """
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "Treeview.Heading",
        background=theme.ACCENT,
        foreground="white",
        font=("Hina Mincho", 10, "bold"),
        relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", theme.ACCENT_SOFT)])

    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=theme.ACCENT,
        font=theme.FONT_BODY,
        rowheight=28,
        borderwidth=0
    )
    style.map(
        "Treeview",
        background=[("selected", "#FFD7D3")],
        foreground=[("selected", theme.ACCENT)]
    )


def set_content_frame(frame):
    global content_frame
    content_frame = frame


def set_sidebar_frame(frame):
    global sidebar_frame
    sidebar_frame = frame


def set_active_student_page(name):
    """Set the active student page and refresh the sidebar highlighting."""
    global active_student_page
    active_student_page = name
    if current_student is not None and sidebar_frame is not None:
        show_student_sidebar(current_student)


def set_active_admin_page(name):
    """Set the active admin page and refresh the sidebar highlighting."""
    global active_admin_page
    active_admin_page = name
    if current_admin is not None and sidebar_frame is not None:
        show_admin_sidebar(current_admin)


def return_to_student_dashboard():
    """Return the embedded student view to its dashboard."""
    if current_student is not None:
        open_dashboard(current_student)


def back_to_student_dashboard(source=None):
    """Return to the student dashboard, or close a compatibility window."""
    if current_student is not None and content_frame is not None:
        open_dashboard(current_student)
    elif source is not None:
        source.winfo_toplevel().destroy()


def return_to_admin_dashboard():
    """Return the embedded admin view to its dashboard."""
    if current_admin is not None:
        open_admin_dashboard(current_admin)


def logout_student(window):
    """Logout a student: return main app to login/register view.

    If running inside the single-window layout (content_frame set), clear
    content and show the main sidebar/login. If the page is a standalone
    top-level, destroy it and also reset the main content if available.
    """
    try:
        top = window.winfo_toplevel()
    except Exception:
        top = None

    global current_student
    current_student = None

    # If main navigation is available, restore main view
    if content_frame is not None and sidebar_frame is not None:
        clear_content()
        show_main_sidebar()
        try:
            from gui.login_window import show_login_page
            show_login_page(content_frame)
        except Exception:
            pass

    # If this was a standalone window, destroy it
    try:
        if top is not None and content_frame is not None:
            main_top = content_frame.winfo_toplevel()
            if top != main_top:
                top.destroy()
        elif top is not None and content_frame is None:
            top.destroy()
    except Exception:
        pass


def clear_content():
    if content_frame is None:
        return
    for w in content_frame.winfo_children():
        w.destroy()


def open_dashboard(student_details):
    """Show the student dashboard inside the registered content frame."""
    if content_frame is None:
        return
    # Update the left sidebar to show student navigation, then render dashboard
    show_student_sidebar(student_details)
    from gui import dashboard
    dashboard.show_dashboard(content_frame, student_details)


def _make_sidebar_button(parent, key, label, cmd, active_key, on_select):
    """A rounded sidebar navigation button, darkened when active."""

    is_active = (active_key == key)
    bg_color = "#6B1B10" if is_active else "#7A231A"
    hover_color = "#8A2E22"

    wrapper = tk.Frame(parent, bg=theme.ACCENT)
    wrapper.pack(pady=4, padx=16, fill="x")

    btn = theme.RoundedButton(
        wrapper,
        text=label,
        command=lambda: (on_select(key), cmd()),
        width=SIDEBAR_WIDTH - 32,
        height=44,
        radius=14,
        bg_color=bg_color,
        hover_color=hover_color,
        fg_color="white",
        font=theme.FONT_BUTTON_SM,
        parent_bg=theme.ACCENT,
    )
    btn.pack(fill="x")
    return btn


def _make_logout_button(parent, command):
    """The logout button - deliberately large and easy to spot."""

    wrapper = tk.Frame(parent, bg=theme.ACCENT)
    wrapper.pack(side="bottom", pady=(10, 26), padx=16, fill="x")

    divider = tk.Frame(parent, bg="#FF9DBB", height=2)
    divider.pack(side="bottom", fill="x", padx=16, pady=(0, 6))

    btn = theme.RoundedButton(
        wrapper,
        text="\U0001F6AA  Logout",
        command=command,
        width=SIDEBAR_WIDTH - 32,
        height=56,
        radius=16,
        bg_color="#FFFFFF",
        hover_color="#FFE3E0",
        fg_color=theme.ACCENT,
        font=("Instrument Serif", 16, "bold"),
        parent_bg=theme.ACCENT,
    )
    btn.pack(fill="x")
    return btn


def show_student_sidebar(student_details):
    """Populate the registered sidebar_frame with student navigation buttons."""
    if sidebar_frame is None or content_frame is None:
        return

    global current_student
    current_student = student_details

    sidebar_frame.pack_forget()
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.configure(bg=theme.ACCENT)

    for w in sidebar_frame.winfo_children():
        w.destroy()

    accent = tk.Frame(sidebar_frame, bg="#FF9DBB", height=3)
    accent.pack(fill="x", side="top")

    title = tk.Label(
        sidebar_frame,
        text="\u2728 " + student_details.get("Full_Name", "Student"),
        bg=theme.ACCENT,
        fg="white",
        font=theme.FONT_HEADING_SM,
        wraplength=SIDEBAR_WIDTH - 30,
        justify="center"
    )
    title.pack(pady=(24, 18))

    # Import page show functions locally to avoid circular imports
    from gui.academic_window import show_academic_page
    from gui.activity_window import show_activity_page
    from gui.achievement_window import show_achievement_page
    from gui.volunteer_window import show_volunteer_page
    from gui.goals_window import show_goals_page
    from gui.reports_window import show_reports_page
    from gui.leaderboard_window import show_leaderboard_page

    def on_select(key):
        global active_student_page
        active_student_page = key

    items = [
        ("Dashboard", "\U0001F3E0 Dashboard", lambda: open_dashboard(student_details)),
        ("Academic Tracker", "\U0001F4D8 Academic Tracker", lambda: show_academic_page(content_frame, student_details)),
        ("Activities", "\U0001F3AF Activities", lambda: show_activity_page(content_frame, student_details)),
        ("Achievements", "\U0001F3C6 Achievements", lambda: show_achievement_page(content_frame, student_details)),
        ("Volunteer Work", "\U0001F91D Volunteer Work", lambda: show_volunteer_page(content_frame, student_details)),
        ("Goals", "\u2705 Goals", lambda: show_goals_page(content_frame, student_details)),
        ("Reports", "\U0001F4CA Reports", lambda: show_reports_page(content_frame, student_details)),
        ("Leaderboard", "\U0001F451 Leaderboard", lambda: show_leaderboard_page(content_frame, student_details)),
    ]

    for key, label, cmd in items:
        _make_sidebar_button(sidebar_frame, key, label, cmd, active_student_page, on_select)

    _make_logout_button(sidebar_frame, lambda: logout_student(sidebar_frame.winfo_toplevel()))


def show_admin_sidebar(admin_details):
    """Populate the registered sidebar_frame with admin navigation buttons."""
    if sidebar_frame is None or content_frame is None:
        return

    global current_admin
    current_admin = admin_details

    sidebar_frame.pack_forget()
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.configure(bg=theme.ACCENT)

    for w in sidebar_frame.winfo_children():
        w.destroy()

    accent = tk.Frame(sidebar_frame, bg="#FF9DBB", height=3)
    accent.pack(fill="x", side="top")

    title = tk.Label(
        sidebar_frame,
        text="\U0001F6E1\uFE0F Admin",
        bg=theme.ACCENT,
        fg="white",
        font=theme.FONT_HEADING_SM,
    )
    title.pack(pady=(24, 18))

    from gui import admin_dashboard
    from gui.manage_students_window import show_manage_students_page
    from gui.admin_reports_window import show_admin_reports_page
    from gui.leaderboard_window import show_leaderboard_page

    def on_select(key):
        global active_admin_page
        active_admin_page = key

    items = [
        ("Dashboard", "\U0001F3E0 Dashboard", lambda: admin_dashboard.show_admin_dashboard(content_frame, admin_details)),
        ("Manage Students", "\U0001F9D1\u200D\U0001F393 Manage Students", lambda: show_manage_students_page(content_frame, admin_details)),
        ("View Reports", "\U0001F4CA View Reports", lambda: show_admin_reports_page(content_frame, admin_details)),
        ("Leaderboard", "\U0001F451 Leaderboard", lambda: show_leaderboard_page(content_frame, admin_details)),
    ]

    for key, label, cmd in items:
        _make_sidebar_button(sidebar_frame, key, label, cmd, active_admin_page, on_select)

    def admin_logout_pressed():
        global current_admin
        current_admin = None
        clear_content()
        show_main_sidebar()
        try:
            from gui.login_window import show_login_page
            show_login_page(content_frame)
        except Exception:
            pass

    _make_logout_button(sidebar_frame, admin_logout_pressed)


def show_main_sidebar():
    """Hide the sidebar entirely - there is no side navigation before login."""
    global current_student, current_admin, active_student_page, active_admin_page
    current_student = None
    current_admin = None
    active_student_page = None
    active_admin_page = None

    if sidebar_frame is None:
        return

    for w in sidebar_frame.winfo_children():
        w.destroy()

    sidebar_frame.pack_forget()


def open_admin_dashboard(admin_details):
    """Show the admin dashboard inside the registered content frame."""
    if content_frame is None:
        return

    global current_student, current_admin, active_student_page, active_admin_page
    current_student = None
    current_admin = admin_details
    active_student_page = None
    active_admin_page = "Dashboard"

    if sidebar_frame is not None:
        show_admin_sidebar(admin_details)

    from gui import admin_dashboard
    admin_dashboard.show_admin_dashboard(content_frame, admin_details)


def prepare_content(parent):
    """Clear ``parent`` and return a vertically scrollable page body.

    The body fills the entire available width so pages never show an
    empty white gap down the middle of the window.
    """

    for w in parent.winfo_children():
        w.destroy()

    parent.configure(bg=CONTENT_BG)

    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(expand=True, fill="both")

    scrollbar = tk.Scrollbar(container, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    canvas = tk.Canvas(container, bg=CONTENT_BG, highlightthickness=0,
                       yscrollcommand=scrollbar.set)
    canvas.pack(side="left", expand=True, fill="both")
    scrollbar.config(command=canvas.yview)

    body = tk.Frame(canvas, bg=CONTENT_BG)
    body_window = canvas.create_window((0, 0), window=body, anchor="nw")

    def update_scroll_region(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def fit_body_width(event):
        canvas.itemconfigure(body_window, width=event.width)

    def on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(-int(event.delta / 120), "units")
        elif event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    body.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", fit_body_width)
    # The page is replaced as a unit, so this binding is safely replaced on
    # every route and allows the wheel to work over any nested form/table.
    parent.winfo_toplevel().bind_all("<MouseWheel>", on_mousewheel)
    parent.winfo_toplevel().bind_all("<Button-4>", on_mousewheel)
    parent.winfo_toplevel().bind_all("<Button-5>", on_mousewheel)

    return body