import reflex as rx


def nav_link(text: str, href: str) -> rx.Component:
    return rx.link(
        text,
        href=href,
        font_family="'DM Mono', monospace",
        font_size="0.78rem",
        font_weight="500",
        letter_spacing="0.08em",
        color="rgba(255,255,255,0.4)",
        text_transform="uppercase",
        text_decoration="none",
        _hover={"color": "#00FFB2", "transition": "color 0.2s ease"},
        transition="color 0.2s ease",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    background="#00FFB2",
                    border_radius="50%",
                    box_shadow="0 0 12px #00FFB2, 0 0 24px rgba(0,255,178,0.4)",
                ),
                rx.text(
                    "POST4U",
                    font_family="'DM Mono', monospace",
                    font_size="0.95rem",
                    font_weight="700",
                    letter_spacing="0.2em",
                    color="white",
                ),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                nav_link("Features", "#features"),
                nav_link("Platforms", "#platforms"),
                nav_link("Setup", "#setup"),
                spacing="7",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("github", size=13, color="rgba(255,255,255,0.5)"),
                        rx.text(
                            "Star",
                            font_family="'DM Mono', monospace",
                            font_size="0.73rem",
                            letter_spacing="0.06em",
                            color="rgba(255,255,255,0.5)",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    href="https://github.com",
                    text_decoration="none",
                    padding_x="1em",
                    padding_y="0.5em",
                    border="1px solid rgba(255,255,255,0.08)",
                    border_radius="6px",
                    _hover={
                        "border_color": "rgba(0,255,178,0.3)",
                        "background": "rgba(0,255,178,0.03)",
                    },
                    transition="all 0.2s ease",
                ),
                rx.link(
                    rx.text(
                        "Dashboard →",
                        font_family="'DM Mono', monospace",
                        font_size="0.73rem",
                        letter_spacing="0.06em",
                        color="#060608",
                        font_weight="700",
                    ),
                    href="/dashboard",
                    text_decoration="none",
                    padding_x="1.2em",
                    padding_y="0.5em",
                    background="#00FFB2",
                    border_radius="6px",
                    _hover={
                        "background": "#00e6a0",
                        "box_shadow": "0 0 24px rgba(0,255,178,0.4)",
                    },
                    transition="all 0.2s ease",
                ),
                spacing="3",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5em", md="2.5em"),
        ),
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="100",
        padding_y="1.1em",
        background="rgba(6,6,8,0.85)",
        backdrop_filter="blur(24px)",
        border_bottom="1px solid rgba(255,255,255,0.04)",
    )