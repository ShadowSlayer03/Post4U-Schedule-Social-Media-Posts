import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState
from .components.dashboard.sidebar import sidebar
from .components.dashboard.tabs import (
    schedule_tab,
    post_now_tab,
    history_tab,
    unschedule_tab,
)

# # # # # # #
# MAIN PAGE
# # # # # # #


def dashboard() -> rx.Component:
    return rx.box(
        rx.toast.provider(
            position="bottom-right",
            duration=5000,
            rich_colors=True,
        ),
        rx.html(
            """<style>
            @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500;600&family=DM+Sans:wght@400;500&display=swap');
            *{box-sizing:border-box}body{margin:0;padding:0;background:#060608}
            ::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:#060608}
            ::-webkit-scrollbar-thumb{background:rgba(0,255,178,0.17);border-radius:2px}

            /* Dark theme for Toasts */
            [data-sonner-toast] {
                background: #1B1212 !important;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 12px !important;
                font-family: 'DM Mono', monospace !important;
                backdrop-filter: blur(10px) !important;
            }
            [data-sonner-toast][data-type="success"] {
                color: #00FFB2 !important;
                border: 1px solid rgba(0, 255, 178, 0.2) !important;
            }
            [data-sonner-toast][data-type="error"] {
                color: #FF4D4D !important;
                border: 1px solid rgba(255, 77, 77, 0.2) !important;
            }
            [data-sonner-toast][data-type="warning"] {
                color: #FFB400 !important;
                border: 1px solid rgba(255, 180, 0, 0.2) !important;
            }
            [data-sonner-toast] [data-close-button] {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                color: white !important;
            }
            </style>"""
        ),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            background="#00FFB2",
                            border_radius="50%",
                            box_shadow="0 0 8px #00FFB2",
                        ),
                        rx.text(
                            "POST4U",
                            font_family="'DM Mono', monospace",
                            font_size="0.8rem",
                            font_weight="700",
                            letter_spacing="0.18em",
                            color="white",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        *[
                            rx.text(
                                t,
                                font_family="'DM Mono', monospace",
                                font_size="0.67rem",
                                color=rx.cond(
                                    DashboardState.active_tab == k,
                                    "#00FFB2",
                                    "rgba(255,255,255,0.26)",
                                ),
                                cursor="pointer",
                                on_click=DashboardState.set_tab(k),
                            )
                            for t, k in [
                                ("Sched", "schedule"),
                                ("Now", "post_now"),
                                ("Hist", "history"),
                                ("Unsch", "unschedule"),
                            ]
                        ],
                        spacing="4",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    padding_bottom="1.4em",
                    border_bottom="1px solid rgba(255,255,255,0.05)",
                    margin_bottom="2em",
                    display=rx.breakpoints(initial="flex", md="none"),
                ),
                rx.cond(
                    DashboardState.active_tab == "schedule",
                    schedule_tab(),
                    rx.cond(
                        DashboardState.active_tab == "post_now",
                        post_now_tab(),
                        rx.cond(
                            DashboardState.active_tab == "unschedule",
                            unschedule_tab(),
                            history_tab(),
                        ),
                    ),
                ),
                flex="1",
                padding=rx.breakpoints(initial="1.5em", md="2.8em"),
                height="100vh",
                overflow_y="auto",
            ),
            spacing="0",
            align="stretch",
            width="100%",
            height="100dvh",
            min_height="100dvh",
        ),
        background="#060608",
        width="100%",
        height="100dvh",
        min_height="100dvh",
    )
