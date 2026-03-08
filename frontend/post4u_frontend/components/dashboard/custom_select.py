import reflex as rx
from typing import Optional
from post4u_frontend.states.dashboard_state import DashboardState

class SelectDropdownState(rx.State):
    """Manages the open/close state of the custom select dropdown."""
    open: bool = False

    @rx.event
    def toggle(self):
        self.open = not self.open

    @rx.event
    def close(self):
        self.open = False


def custom_select(
    options,
    value=None,
    on_change=None,
    placeholder: str = "Select...",
    width: str = "100%",
    font_family: str = "'DM Mono', monospace",
    font_size: str = "0.7rem",
    color: str = "white",
    background: str = "#18181b",
    border: str = "1px solid #232329",
    border_radius: str = "8px",
    padding: str = "0.72em 1em",
    **kwargs
) -> rx.Component:
    """
    A fully custom, dark-themed select dropdown built on Reflex primitives.
    - `options`: a Var (list of str) or plain list
    - `value`: the currently selected value Var (from parent state)
    - `on_change`: the parent event handler to call when an option is chosen
    """

    def select_item(opt):
        return rx.box(
            rx.text(
                opt,
                font_family=font_family,
                font_size=font_size,
                color=color,
                padding="0.6em 1em",
                background=rx.cond(value == opt, "rgba(255,255,255,0.07)", background),
                border_radius="6px",
                cursor="pointer",
                width="100%",
                transition="background 0.15s",
            ),
            width="100%",
            _hover={"background": "rgba(255,255,255,0.05)", "border_radius": "6px"},
            on_click=[on_change(opt), SelectDropdownState.close],
            cursor="pointer",
        )

    return rx.box(
        # Trigger button
        rx.box(
            rx.hstack(
                rx.text(
                    rx.cond(value, value, placeholder),
                    font_family=font_family,
                    font_size=font_size,
                    color=rx.cond(value, color, "rgba(255,255,255,0.25)"),
                    overflow="hidden",
                    white_space="nowrap",
                    text_overflow="ellipsis",
                    flex="1",
                ),
                rx.icon(
                    "chevron-down",
                    size=14,
                    color="rgba(255,255,255,0.3)",
                    style={
                        "transition": "transform 0.2s",
                        "transform": rx.cond(
                            SelectDropdownState.open,
                            "rotate(180deg)",
                            "rotate(0deg)"
                        ),
                    },
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            background=background,
            border=border,
            border_radius=border_radius,
            padding=padding,
            width=width,
            cursor="pointer",
            on_click=SelectDropdownState.toggle,
            style={"userSelect": "none"},
            _hover={"border": "1px solid #3a3a3f"},
            transition="border 0.15s",
        ),
        # Dropdown list
        rx.cond(
            SelectDropdownState.open,
            rx.box(
                rx.vstack(
                    rx.foreach(options, select_item),
                    spacing="0",
                    width="100%",
                ),
                background=background,
                border=border,
                border_radius="8px",
                box_shadow="0 8px 32px rgba(0,0,0,0.5)",
                position="absolute",
                z_index="1000",
                width=width,
                margin_top="0.3em",
                padding_y="0.3em",
                padding_x="0.3em",
                style={"maxHeight": "220px", "overflowY": "auto"},
            ),
        ),
        position="relative",
        width=width,
        **kwargs
    )
