import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState


def post_btn(label: str) -> rx.Component:
    return rx.button(
        rx.cond(DashboardState.is_posting,
                rx.hstack(rx.spinner(size="2"),
                          rx.text("Posting...", font_family="'DM Mono', monospace",
                                  font_size="0.78rem", color="#060608", font_weight="700"),
                          spacing="2", align="center"),
                rx.text(label, font_family="'DM Mono', monospace", font_size="0.78rem", font_weight="700", color="#060608")),
        on_click=DashboardState.submit_post, background="#00FFB2", border_radius="8px",
        padding_x="1.8em", padding_y="0.7em", cursor="pointer",
        box_shadow="0 0 18px rgba(0,255,178,0.18)",
        _hover={"background": "#00e6a0",
                "box_shadow": "0 0 28px rgba(0,255,178,0.3)"},
        transition="all 0.2s ease", disabled=DashboardState.is_posting,
    )


def unschedule_btn(label: str) -> rx.Component:
    return rx.button(
        rx.cond(DashboardState.is_posting,
                rx.hstack(
                rx.spinner(size="2"),
                rx.text("Processing...", font_family="'DM Mono', monospace",
                        font_size="0.78rem", color="#060608", font_weight="700"),
                        spacing="2", align="center"
                ),
                rx.text(label, font_family="'DM Mono', monospace", font_size="0.78rem", font_weight="700", color="#060608")),
                on_click=DashboardState.unschedule_post, background="#FF4D4D", border_radius="8px",
                padding_x="1.8em", padding_y="0.7em", cursor="pointer",
                box_shadow="0 0 18px rgba(255,77,77,0.18)",
                _hover={"background": "#ff1a1a",
                "box_shadow": "0 0 28px rgba(255,77,77,0.3)"},
                transition="all 0.2s ease", disabled=DashboardState.is_posting,
    )

def refresh_posts_btn() -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon("refresh-cw", size=11, color="#060608"),
            rx.text(
                rx.cond(DashboardState.is_refreshing, "Refreshing...", "Refresh"),
                font_family="'DM Mono', monospace",
                font_size="0.72rem",
                color="#060608",
                font_weight="600",
            ),
            spacing="2",
            align="center",
        ),
        on_click=DashboardState.load_posts,
        background="#7fd8ff",
        border_radius="6px",
        padding_x="1.1em",
        padding_y="0.5em",
        cursor="pointer",
        box_shadow="0 0 15px rgba(127, 216, 255, 0.25)",
        _hover={
            "background": "#3ecfff",
            "box_shadow": "0 0 25px rgba(62, 207, 255, 0.45)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
    )
