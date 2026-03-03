import reflex as rx

# # # # # # # #
# HERO SECTION
# # # # # # # #

def hero_section() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute", top="0", left="0", right="0", bottom="0",
            background="radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,255,178,0.07) 0%, transparent 70%)",
            pointer_events="none",
        ),
        rx.box(
            position="absolute", top="0", left="0", right="0", bottom="0",
            background_image=(
                "linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),"
                "linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px)"
            ),
            background_size="60px 60px",
            pointer_events="none",
        ),
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.box(width="5px", height="5px", background="#00FFB2", border_radius="50%", box_shadow="0 0 6px #00FFB2"),
                    rx.text("Open Source · Self-Hosted · No Subscriptions",
                        font_family="'DM Mono', monospace", font_size="0.68rem",
                        letter_spacing="0em", color="rgba(0,255,178,0.8)", font_weight="500"),
                    spacing="2", align="center",
                ),
                padding_x="1.2em", padding_y="0.45em",
                background="rgba(0,255,178,0.05)",
                border="1px solid rgba(0,255,178,0.15)",
                border_radius="100px",
            ),
            rx.html("""<h1 style="
                font-family: 'Syne', sans-serif;
                font-size: clamp(5rem, 6vw, 5.2rem);
                font-weight: 700;
                line-height: 1.05;
                letter-spacing: -0.03em;
                margin: 0.4em 0 0.2em 0;
                color: white;
                text-align: center;
            ">Post once.<br/>
            <span style="background: linear-gradient(135deg, #00FFB2 0%, #00C8FF 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                Reach everywhere.</span></h1>"""
            ),
            rx.text(
                "Schedule and cross-post to X, Reddit, Telegram, and Discord from a single API. Deploy in 60 seconds with Docker.",
                font_family="'DM Sans', sans-serif",
                font_size=rx.breakpoints(initial="0.95rem", md="1.05rem"),
                color="rgba(255,255,255,0.35)",
                text_align="center", max_width="520px", line_height="1.75",
            ),
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("terminal", size=14, color="#060608"),
                        rx.text("docker-compose up", font_family="'DM Mono', monospace",
                            font_size="0.8rem", font_weight="700", color="#060608"),
                        spacing="2", align="center",
                    ),
                    href="#setup", text_decoration="none",
                    padding_x="1.8em", padding_y="0.75em",
                    background="#00FFB2", border_radius="8px",
                    box_shadow="0 0 30px rgba(0,255,178,0.25), 0 4px 24px rgba(0,0,0,0.4)",
                    _hover={"background": "#00e6a0", "box_shadow": "0 0 40px rgba(0,255,178,0.4)", "transform": "translateY(-1px)"},
                    transition="all 0.2s ease",
                ),
                rx.link(
                    rx.hstack(
                        rx.icon("github", size=14, color="rgba(255,255,255,0.55)"),
                        rx.text("View Source", font_family="'DM Mono', monospace",
                            font_size="0.8rem", color="rgba(255,255,255,0.55)"),
                        spacing="2", align="center",
                    ),
                    href="https://github.com", text_decoration="none",
                    padding_x="1.8em", padding_y="0.75em",
                    border="1px solid rgba(255,255,255,0.1)", border_radius="8px",
                    _hover={"border_color": "rgba(0,255,178,0.3)", "background": "rgba(0,255,178,0.04)", "transform": "translateY(-1px)"},
                    transition="all 0.2s ease",
                ),
                spacing="4", flex_wrap="wrap", justify="center",
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.hstack(
                            rx.box(width="10px", height="10px", background="#FF5F57", border_radius="50%"),
                            rx.box(width="10px", height="10px", background="#FEBC2E", border_radius="50%"),
                            rx.box(width="10px", height="10px", background="#28C840", border_radius="50%"),
                            spacing="2",
                        ),
                        rx.text("post4u — curl", font_family="'DM Mono', monospace",
                            font_size="0.68rem", color="rgba(255,255,255,0.2)"),
                        justify="between", width="100%",
                    ),
                    rx.box(height="1px", width="100%", background="rgba(255,255,255,0.05)"),
                    rx.vstack(
                        rx.text('$ curl -X POST http://localhost:8000/posts/ \\',
                            font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="rgba(255,255,255,0.6)"),
                        rx.text('  -d \'{"content": "Shipped something new 🚀",',
                            font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="rgba(255,255,255,0.6)", padding_left="1em"),
                        rx.text('       "platforms": ["x","reddit","telegram","discord"]}\'',
                            font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="rgba(255,255,255,0.6)", padding_left="1em"),
                        rx.box(height="0.4em"),
                        rx.text('✓  x         tweet_id: 1234567890', font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="#00FFB2"),
                        rx.text('✓  reddit    post_id:  t3_abc123', font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="#00FFB2"),
                        rx.text('✓  telegram  msg_id:   987654', font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="#00FFB2"),
                        rx.text('✓  discord   status:   204', font_family="'DM Mono', monospace", font_size=rx.breakpoints(initial="0.68rem", md="0.76rem"), color="#00FFB2"),
                        align="start", spacing="1",
                    ),
                    spacing="3", width="100%",
                ),
                background="rgba(8,8,12,0.92)",
                border="1px solid rgba(0,255,178,0.1)",
                border_radius="12px",
                padding="1.8em",
                max_width="600px",
                width="100%",
                box_shadow="0 0 60px rgba(0,255,178,0.06), 0 40px 80px rgba(0,0,0,0.6)",
                margin_top="2em",
            ),
            spacing="6", align="center", width="100%",
            max_width="860px", margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5em", md="2.5em"),
            padding_top="10em", padding_bottom="8em",
            position="relative", z_index="1",
        ),
        position="relative", width="100%", overflow="hidden", background="#060608",
    )


# # # # # # #
# STATS BAR
# # # # # # #

def stat_item(number: str, label: str) -> rx.Component:
    return rx.vstack(
        rx.text(number, font_family="'Syne', sans-serif", font_size="1.9rem",
            font_weight="700", color="white", letter_spacing="-0.03em"),
        rx.text(label, font_family="'DM Mono', monospace", font_size="0.68rem",
            color="rgba(255,255,255,0.28)", letter_spacing="0.08em", text_transform="uppercase"),
        spacing="1", align="center",
    )


def stats_bar() -> rx.Component:
    return rx.box(
        rx.hstack(
            stat_item("4", "Platforms"),
            rx.box(width="1px", height="40px", background="rgba(255,255,255,0.07)"),
            stat_item("1", "API Call"),
            rx.box(width="1px", height="40px", background="rgba(255,255,255,0.07)"),
            stat_item("60s", "Deploy Time"),
            rx.box(width="1px", height="40px", background="rgba(255,255,255,0.07)"),
            stat_item("$0", "Monthly Cost"),
            spacing="8", justify="center", align="center", flex_wrap="wrap",
        ),
        width="100%", padding_y="3em",
        background="rgba(255,255,255,0.012)",
        border_top="1px solid rgba(255,255,255,0.05)",
        border_bottom="1px solid rgba(255,255,255,0.05)",
    )