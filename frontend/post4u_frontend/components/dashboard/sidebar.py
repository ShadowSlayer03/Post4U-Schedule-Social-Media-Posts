import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState

# # # # # #
# SIDEBAR
# # # # # #


def tab_item(icon_name: str, label: str, tab_id: str) -> rx.Component:
    active = DashboardState.active_tab == tab_id
    return rx.box(
        rx.hstack(
            rx.icon(icon_name, size=13, color=rx.cond(
                active, "#00FFB2", "rgba(255,255,255,0.26)")),
            rx.text(label, font_family="'DM Mono', monospace", font_size="0.74rem",
                    font_weight=rx.cond(active, "600", "400"),
                    color=rx.cond(active, "white", "rgba(255,255,255,0.26)"), letter_spacing="0.03em"),
            spacing="3", align="center",
        ),
        padding_x="0.85em", padding_y="0.62em", border_radius="8px",
        background=rx.cond(active, "rgba(0,255,178,0.07)", "transparent"),
        border=rx.cond(active, "1px solid rgba(0,255,178,0.13)",
                       "1px solid transparent"),
        cursor="pointer", width="100%",
        on_click=DashboardState.set_tab(tab_id),
        _hover={"background": rx.cond(
            active, "rgba(0,255,178,0.07)", "rgba(255,255,255,0.02)")},
        transition="all 0.15s ease",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="7px", height="7px", background="#00FFB2",
                       border_radius="50%", box_shadow="0 0 10px #00FFB2"),
                rx.text("POST4U", font_family="'DM Mono', monospace",
                        font_size="0.86rem", font_weight="700", letter_spacing="0.18em", color="white"),
                spacing="2", align="center",
            ),
            rx.text("Dashboard", font_family="'DM Mono', monospace", font_size="0.6rem",
                    color="rgba(255,255,255,0.17)", letter_spacing="0.1em", margin_bottom="1.5em"),
            rx.vstack(
                tab_item("calendar", "Schedule Post", "schedule"),
                tab_item("send", "Post Now", "post_now"),
                tab_item("trash-2", "Unschedule Post", "unschedule"),
                tab_item("list", "History", "history"),
                spacing="1", width="100%",
            ),
            rx.spacer(),
        ),
        width="205px", height="100%", min_height="100vh",
        background="rgba(255,255,255,0.05)",
        border_right="1px solid rgba(255,255,255,0.1)",
        padding="1.8em 1.1em",
        flex_shrink="0",
        display=rx.breakpoints(initial="none", md="flex"),
    )
