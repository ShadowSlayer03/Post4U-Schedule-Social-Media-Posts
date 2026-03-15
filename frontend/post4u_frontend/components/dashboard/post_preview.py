import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState

MONO = "'DM Mono', monospace"
SANS = "'DM Sans', sans-serif"
_DIM = "rgba(255,255,255,0.3)"


# Shared Components

def _avatar(label: str, bg: str, size: str = "34px", icon: str | None = None) -> rx.Component:
    """Circular avatar — shows an icon if provided, otherwise a text label."""
    inner = (
        rx.icon(icon, size=13, color="white")
        if icon
        else rx.text(label, font_size="0.65rem", font_weight="700", color="white", font_family=MONO)
    )
    return rx.box(
        inner,
        width=size, height=size, border_radius="50%",
        background=bg, flex_shrink="0",
        display="flex", align_items="center", justify_content="center",
    )


def _content_text(color: str = "white") -> rx.Component:
    """Reactive content body — same across all platforms."""
    return rx.text(
        DashboardState.content,
        font_family=SANS, font_size="0.88rem", color=color,
        white_space="pre-wrap", line_height="1.55", width="100%",
    )


def _action_item(icon: str, label: str) -> rx.Component:
    return rx.hstack(
        rx.icon(icon, size=14, color=_DIM),
        rx.text(label, font_size="0.72rem", color=_DIM, font_family=MONO),
        spacing="1", align="center",
    )


def _card_shell(bg: str, border: str, *children: rx.Component) -> rx.Component:
    """Outer card wrapper with uniform border-radius, padding, overflow."""
    return rx.box(
        rx.vstack(*children, spacing="3", align="start", width="100%", padding="1.1em"),
        background=bg, border=border,
        border_radius="14px", width="100%", overflow="hidden",
    )


def _og_embed_card(accent: str = "rgba(255,255,255,0.07)") -> rx.Component:
    """Standard OG embed block — used by X, Reddit, Telegram."""
    return rx.cond(
        DashboardState.og_url,
        rx.box(
            rx.vstack(
                rx.cond(
                    DashboardState.og_image,
                    rx.image(
                        src=DashboardState.og_image,
                        width="100%",
                        height="160px",
                        object_fit="cover",
                        border_radius="6px 6px 0 0",
                    ),
                ),
                rx.vstack(
                    rx.cond(
                        DashboardState.is_fetching_og,
                        rx.hstack(
                            rx.spinner(
                                size="1", color="rgba(255,255,255,0.3)"),
                            rx.text("Fetching preview…", font_family=MONO,
                                    font_size="0.65rem", color="rgba(255,255,255,0.3)"),
                            spacing="2", align="center",
                        ),
                        rx.vstack(
                            rx.text(
                                DashboardState.og_title,
                                font_weight="600",
                                font_size="0.82rem",
                                color="white",
                                font_family=SANS,
                                line_limit=2,
                            ),
                            rx.text(
                                DashboardState.og_description,
                                font_size="0.73rem",
                                color="rgba(255,255,255,0.45)",
                                font_family=SANS,
                                line_limit=2,
                            ),
                            rx.text(
                                DashboardState.og_url,
                                font_size="0.62rem",
                                color="rgba(255,255,255,0.25)",
                                font_family=MONO,
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                width="100%",
                            ),
                            spacing="1",
                            align="start",
                            width="100%",
                        ),
                    ),
                    padding="0.65em 0.8em",
                    align="start",
                    width="100%",
                ),
                spacing="0",
                align="stretch",
                width="100%",
            ),
            border=f"1px solid {accent}", border_radius="8px",
            overflow="hidden", background="rgba(0,0,0,0.25)",
            width="100%", margin_top="0.6em",
        ),
    )


def _discord_og_embed() -> rx.Component:
    """Discord-specific left-border embed style."""
    return rx.cond(
        DashboardState.og_url,
        rx.box(
            rx.hstack(
                rx.box(width="4px", background="#5865F2", border_radius="3px",
                       align_self="stretch", flex_shrink="0"),
                rx.vstack(
                    rx.cond(
                        DashboardState.is_fetching_og,
                        rx.text("Fetching embed…", font_family=MONO, font_size="0.65rem", color=_DIM),
                        rx.vstack(
                            rx.text(DashboardState.og_title, font_weight="600",
                                    font_size="0.82rem", color="#00AFF4",
                                    font_family=SANS, line_limit=2),
                            rx.text(DashboardState.og_description, font_size="0.75rem",
                                    color="rgba(255,255,255,0.45)", font_family=SANS, line_limit=3),
                            rx.cond(
                                DashboardState.og_image,
                                rx.image(src=DashboardState.og_image, width="100%",
                                         max_height="200px", object_fit="cover",
                                         border_radius="4px", margin_top="0.4em"),
                            ),
                            spacing="1", align="start", width="100%",
                        ),
                    ),
                    padding="0.5em 0.8em", align="start", width="100%",
                ),
                spacing="0", align="stretch", width="100%",
            ),
            background="rgba(0,0,0,0.2)", border_radius="4px",
            overflow="hidden", margin_top="0.4em", width="100%",
        ),
    )


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CARDS FOR POST - DIFFERENT SOCIAL MEDIA PLATFORMS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def x_preview_card() -> rx.Component:
    header = rx.hstack(
        _avatar("P4", "linear-gradient(135deg,#00FFB2,#0099FF)", size="36px"),
        rx.vstack(
            rx.text("Post4U", font_weight="700", font_size="0.85rem", color="white", font_family=SANS),
            rx.text("@post4u_app", font_size="0.72rem", color="rgba(255,255,255,0.4)", font_family=MONO),
            spacing="0", align="start",
        ),
        rx.spacer(),
        rx.text("𝕏", font_size="1.1rem", color="white", font_weight="700"),
        spacing="2", align="center", width="100%",
    )
    footer = rx.hstack(
        _action_item("heart", "100"),
        _action_item("message-circle", "120"),
        _action_item("repeat-2", "10"),
        _action_item("bar-chart-2", "12.5k"),
        spacing="5", margin_top="0.4em",
    )
    return _card_shell(
        "#0F1923", "1px solid rgba(255,255,255,0.1)",
        header, _content_text(), _og_embed_card("rgba(255,255,255,0.1)"), footer,
    )


def reddit_preview_card() -> rx.Component:
    header = rx.hstack(
        _avatar("r/", "#FF4500", size="30px"),
        rx.vstack(
            rx.text("r/post4u", font_weight="700", font_size="0.78rem", color="white", font_family=SANS),
            rx.text("Posted by u/post4u_app · just now", font_size="0.65rem",
                    color="rgba(255,255,255,0.35)", font_family=MONO),
            spacing="0", align="start",
        ),
        spacing="2", align="center", width="100%",
    )
    footer = rx.hstack(
        rx.hstack(
            rx.icon("arrow-up", size=14, color="rgba(255,255,255,0.35)"),
            rx.text("1", font_size="0.72rem", color="rgba(255,255,255,0.45)", font_family=MONO),
            rx.icon("arrow-down", size=14, color="rgba(255,255,255,0.35)"),
            spacing="1", align="center",
            padding_x="0.5em", padding_y="0.25em",
            border_radius="20px", background="rgba(255,255,255,0.06)",
        ),
        _action_item("message-square", "Comment"),
        _action_item("share-2", "Share"),
        spacing="3", margin_top="0.4em",
    )
    return _card_shell(
        "#1A1A1B", "1px solid rgba(255,255,255,0.08)",
        header, _content_text("rgba(255,255,255,0.9)"),
        _og_embed_card("rgba(255,69,0,0.25)"), footer,
    )


def telegram_preview_card() -> rx.Component:
    channel_bar = rx.hstack(
        _avatar("", "linear-gradient(135deg,#229ED9,#1A7FC4)", size="32px", icon="send"),
        rx.text("Post4U Channel", font_weight="700", font_size="0.82rem",
                color="white", font_family=SANS),
        spacing="2", align="center",
        padding="0.7em 1em", width="100%",
        background="rgba(0,0,0,0.3)",
        border_bottom="1px solid rgba(255,255,255,0.06)",
    )
    bubble = rx.box(
        rx.vstack(
            _content_text(),
            _og_embed_card("rgba(34,158,217,0.3)"),
            rx.text("12:00", font_size="0.6rem", color="rgba(255,255,255,0.35)",
                    font_family=MONO, align_self="end"),
            spacing="2", align="start", width="100%",
        ),
        background="#2B5278", border_radius="4px 14px 14px 14px",
        padding="0.8em 1em", max_width="90%", margin="0.8em 1em 1em",
    )
    return rx.box(
        rx.vstack(channel_bar, bubble, spacing="0", align="start", width="100%"),
        background="#17212B", border="1px solid rgba(255,255,255,0.08)",
        border_radius="14px", width="100%", overflow="hidden",
    )


def discord_preview_card() -> rx.Component:
    channel_bar = rx.hstack(
        rx.icon("hash", size=14, color="rgba(255,255,255,0.4)"),
        rx.text("general", font_family=MONO, font_size="0.78rem",
                color="rgba(255,255,255,0.5)", font_weight="600"),
        padding="0.6em 1em",
        background="rgba(0,0,0,0.2)",
        border_bottom="1px solid rgba(255,255,255,0.05)",
        width="100%", spacing="1", align="center",
    )
    message_row = rx.hstack(
        _avatar("P", "linear-gradient(135deg,#5865F2,#4752C4)", size="38px"),
        rx.vstack(
            rx.hstack(
                rx.text("Post4U", font_weight="700", font_size="0.84rem",
                        color="white", font_family=SANS),
                rx.text("Today at 12:00", font_size="0.62rem",
                        color="rgba(255,255,255,0.3)", font_family=MONO),
                spacing="2", align="baseline",
            ),
            _content_text("rgba(255,255,255,0.88)"),
            _discord_og_embed(),
            spacing="1", align="start", width="100%",
        ),
        spacing="3", align="start", padding="0.8em 1em", width="100%",
    )
    return rx.box(
        rx.vstack(channel_bar, message_row, spacing="0", align="start", width="100%"),
        background="#36393F", border="1px solid rgba(255,255,255,0.07)",
        border_radius="14px", width="100%", overflow="hidden",
    )


# # # # # # # # # # # # # # #  # # #
# PREVIEW STICKY PANEL - TOWARDS SIDE
# # # # # # # # # # # # # # # # # # #

def platform_previews_panel() -> rx.Component:
    """Shows a card for every selected platform. Empty box when none selected."""
    return rx.cond(
        DashboardState.platforms.length() > 0,
        rx.vstack(
            rx.text("Preview", font_family=MONO, font_size="0.67rem",
                    color="rgba(0,255,178,0.5)", letter_spacing="0.14em",
                    text_transform="uppercase", margin_bottom="0.2em"),
            rx.cond(DashboardState.platforms.contains("x"), x_preview_card()),
            rx.cond(DashboardState.platforms.contains("reddit"), reddit_preview_card()),
            rx.cond(DashboardState.platforms.contains("telegram"), telegram_preview_card()),
            rx.cond(DashboardState.platforms.contains("discord"), discord_preview_card()),
            spacing="6", align="start", width="100%",
        ),
        rx.box(),
    )