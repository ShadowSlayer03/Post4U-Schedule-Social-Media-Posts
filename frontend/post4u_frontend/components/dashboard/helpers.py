import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState

# # # # #
# HELPERS
# # # # #


def slabel(text: str) -> rx.Component:
    return rx.text(text, font_family="'DM Mono', monospace", font_size="0.67rem",
                   color="rgba(0,255,178,0.5)", letter_spacing="0.14em", text_transform="uppercase", margin_bottom="0.4em")


def flabel(text: str) -> rx.Component:
    return rx.text(text, font_family="'DM Mono', monospace", font_size="0.69rem",
                   color="rgba(255,255,255,0.3)", letter_spacing="0.05em", margin_bottom="0.3em")


def input_style() -> dict:
    return {
        "font_family": "'DM Mono', monospace", "font_size": "0.8rem", "color": "white",
        "background": "rgba(255,255,255,0.025)", "border": "1px solid rgba(255,255,255,0.07)",
        "border_radius": "8px", "padding": "0.72em 1em", "width": "100%",
        "_placeholder": {"color": "rgba(255,255,255,0.18)"},
        "_focus": {"border_color": "rgba(255,255,255,1)", "outline": "none"},
    }


def content_area() -> rx.Component:
    return rx.vstack(
        rx.text_area(
            placeholder="What are you shipping today?",
            value=DashboardState.content,
            on_change=DashboardState.set_content,
            font_family="'DM Sans', sans-serif", font_size="0.86rem", color="white",
            background="rgba(255,255,255,0.025)", border="1px solid rgba(255,255,255,0.07)",
            border_radius="10px", padding="1em", min_height="120px", resize="vertical", width="100%",
            _placeholder={"color": "rgba(255,255,255,0.17)"},
            _focus={"border_color": "rgba(0,255,178,0.26)", "outline": "none",
                    "box_shadow": "0 0 0 3px rgba(0,255,178,0.05)"}
        ),
        rx.hstack(
            rx.text("Char limit exceeded for: ", font_family="'DM Mono', monospace", font_size="0.67rem", color="rgba(255,255,255,0.3)"),
            rx.foreach(
                DashboardState.char_limits,
                lambda info: rx.cond(
                    info["is_over"],
                    rx.text(
                        info["platform"].capitalize(),
                        color="#FF4D4D", font_size="0.65rem", font_family="'DM Mono', monospace"
                    ),
                    None
                )
            ),
            rx.spacer(),
            rx.text(
                f"{DashboardState.content.length()} / {DashboardState.max_characters} chars",
                font_family="'DM Mono', monospace",
                font_size="0.67rem",
                color=rx.cond(
                    DashboardState.content.length() > DashboardState.max_characters,
                    "#FF4D4D",
                    "rgba(255,255,255,0.3)"
                )
            ),
            width="100%", align="center", margin_top="0.3em"
        ),
        width="100%", align="end"
    )


def ptoggle(icon_name: str, label: str, pid: str, color: str) -> rx.Component:
    s = DashboardState.platforms.contains(pid)
    return rx.box(
        rx.hstack(
            rx.icon(icon_name, size=13, color=rx.cond(
                s, color, "rgba(255,255,255,0.26)")),
            rx.text(label, font_family="'DM Mono', monospace", font_size="0.72rem",
                    color=rx.cond(s, "white", "rgba(255,255,255,0.3)"), letter_spacing="0.04em"),
            spacing="2", align="center",
        ),
        padding_x="0.95em", padding_y="0.52em", border_radius="8px",
        background=rx.cond(s, "rgba(0,255,178,0.06)",
                           "rgba(255,255,255,0.02)"),
        border=rx.cond(s, "1px solid rgba(0,255,178,0.2)",
                       "1px solid rgba(255,255,255,0.07)"),
        cursor="pointer", on_click=DashboardState.toggle_platform(pid),
        _hover={"border_color": "rgba(0,255,178,0.2)"}, transition="all 0.15s ease",
    )


def prow() -> rx.Component:
    return rx.hstack(
        ptoggle("twitter", "X", "x", "#1DA1F2"),
        ptoggle("message-circle", "Reddit", "reddit", "#FF4500"),
        ptoggle("send", "Telegram", "telegram", "#229ED9"),
        ptoggle("hash", "Discord", "discord", "#5865F2"),
        spacing="3", flex_wrap="wrap",
    )
