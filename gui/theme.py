"""
Shared visual theme for the Student Achievement & Portfolio Management System.

This module holds every colour, font and reusable widget used across the
GUI files so that all pages look consistent. Nothing in here talks to the
database or changes any backend behaviour - it is presentation only.
"""

import tkinter as tk

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
BG = "#FFFFFF"              # page background (white)
ACCENT = "#470500"          # cherry red - headings, sidebar, text on light bg
ACCENT_SOFT = "#6B1B10"     # slightly lighter accent for hover states on dark bg
BUTTON = "#FF908A"          # primary button colour
BUTTON_HOVER = "#FF6F66"    # button hover colour
BUTTON_TEXT = "#470500"     # text on buttons
CARD_BG = "#FFFFFF"         # card background
CARD_BORDER = "#FFC9C4"     # light cherry border for cards
LOGOUT = "#470500"          # logout button (big + visible)
LOGOUT_HOVER = "#6B1B10"
LOGOUT_TEXT = "#FFFFFF"
MUTED_TEXT = "#8A5B55"

# ---------------------------------------------------------------------------
# Fonts
# Tkinter silently falls back to a default font if a named font isn't
# installed on the machine, so these are safe to reference even if the
# fonts aren't present - install "Bitcount Ink", "Instrument Serif" and
# "Hina Mincho" for the exact intended look.
# ---------------------------------------------------------------------------
FONT_HEADING = ("Bitcount Ink", 30, "bold")
FONT_HEADING_SM = ("Bitcount Ink", 20, "bold")
FONT_SUBHEADING = ("Hina Mincho", 13)
FONT_LABEL = ("Hina Mincho", 11)
FONT_BUTTON = ("Instrument Serif", 14)
FONT_BUTTON_SM = ("Instrument Serif", 12)
FONT_BODY = ("Instrument Serif", 13)
FONT_VALUE = ("Instrument Serif", 16)


# ---------------------------------------------------------------------------
# Rounded button widget
# ---------------------------------------------------------------------------
class RoundedButton(tk.Canvas):
    """A clean, rounded-corner button drawn on a Canvas.

    Exposes a small subset of tk.Button's interface (configure, command)
    so it can be dropped in wherever a tk.Button used to be.
    """

    def __init__(
        self,
        parent,
        text="",
        command=None,
        width=200,
        height=46,
        radius=20,
        bg_color=BUTTON,
        hover_color=BUTTON_HOVER,
        fg_color=BUTTON_TEXT,
        font=FONT_BUTTON,
        parent_bg=None,
        **kwargs
    ):
        resolved_bg = parent_bg
        if resolved_bg is None:
            try:
                resolved_bg = parent["bg"]
            except Exception:
                resolved_bg = BG

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=resolved_bg,
            highlightthickness=0,
            bd=0,
            **kwargs
        )

        self.command = command
        self.width = width
        self.height = height
        self.radius = radius
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.font = font
        self.text = text
        self._enabled = True

        self._render(self.bg_color)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _render(self, color):
        self.delete("all")
        self._round_rect(1, 1, self.width - 1, self.height - 1, self.radius, fill=color, outline=color)
        self.create_text(
            self.width / 2,
            self.height / 2,
            text=self.text,
            fill=self.fg_color,
            font=self.font,
        )

    def _on_click(self, _event):
        if self._enabled and self.command:
            self.command()

    def _on_enter(self, _event):
        if self._enabled:
            self._render(self.hover_color)
            self.configure(cursor="hand2")

    def _on_leave(self, _event):
        if self._enabled:
            self._render(self.bg_color)

    def configure_text(self, text):
        self.text = text
        self._render(self.bg_color)

    def set_enabled(self, enabled):
        self._enabled = enabled
        self._render(self.bg_color if enabled else "#F0D9D6")


# ---------------------------------------------------------------------------
# Shared layout helpers
# ---------------------------------------------------------------------------
def create_page_header(parent, icon, title_text, subtitle_text=None):
    """Create the standard cherry-red header used at the top of every page."""

    header_frame = tk.Frame(parent, bg=ACCENT)
    header_frame.pack(fill="x")

    inner = tk.Frame(header_frame, bg=ACCENT)
    inner.pack(pady=(22, 18))

    title_label = tk.Label(
        inner,
        text=(icon + "  " if icon else "") + title_text,
        bg=ACCENT,
        fg="white",
        font=FONT_HEADING_SM,
    )
    title_label.pack()

    if subtitle_text:
        subtitle_label = tk.Label(
            inner,
            text=subtitle_text,
            bg=ACCENT,
            fg="#FFD7D3",
            font=FONT_SUBHEADING,
        )
        subtitle_label.pack(pady=(4, 0))

    return header_frame


def create_section_card(parent, min_width=None):
    """A soft white card with a light cherry border used to group content."""

    card = tk.Frame(
        parent,
        bg=CARD_BG,
        highlightbackground=CARD_BORDER,
        highlightthickness=1,
        bd=0,
    )
    if min_width:
        card.configure(width=min_width)
    return card


def section_heading(parent, text):
    """Small serif section heading (e.g. 'Add Achievement')."""

    return tk.Label(
        parent,
        text=text,
        bg=CARD_BG,
        fg=ACCENT,
        font=("Hina Mincho", 15, "bold"),
    )


def field_label(parent, text, bg=CARD_BG):
    return tk.Label(parent, text=text, bg=bg, fg=MUTED_TEXT, font=FONT_LABEL)


def styled_entry(parent, width=22, show=None):
    kwargs = {}
    if show:
        kwargs["show"] = show
    return tk.Entry(
        parent,
        width=width,
        font=FONT_BODY,
        bg="#FFFBFA",
        fg=ACCENT,
        insertbackground=ACCENT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=CARD_BORDER,
        highlightcolor=ACCENT,
        **kwargs
    )
