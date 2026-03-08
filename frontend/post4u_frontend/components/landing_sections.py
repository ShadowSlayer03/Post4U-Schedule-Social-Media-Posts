import reflex as rx


# # # # # # # # # #
# FEATURES SECTION
# # # # # # # # # #

def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(icon, size=20, color="#00FFB2"),
                width="44px", height="44px",
                background="rgba(0,255,178,0.06)",
                border="1px solid rgba(0,255,178,0.12)",
                border_radius="10px",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.text(title,
                    font_family="'Syne', sans-serif", font_size="0.98rem",
                    font_weight="700", color="white", margin_top="0.8em", letter_spacing="-0.01em"),
            rx.text(description,
                    font_family="'DM Sans', sans-serif", font_size="0.83rem",
                    color="rgba(255,255,255,0.32)", line_height="1.65"),
            align="start", spacing="2",
        ),
        padding="1.8em",
        background="rgba(255,255,255,0.016)",
        border="1px solid rgba(255,255,255,0.055)",
        border_radius="16px",
        _hover={
            "border_color": "rgba(0,255,178,0.2)",
            "background": "rgba(0,255,178,0.022)",
            "transform": "translateY(-4px)",
            "box_shadow": "0 20px 60px rgba(0,0,0,0.4)",
        },
        transition="all 0.3s ease",
        cursor="default",
    )


def features_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("// FEATURES",
                    font_family="'DM Mono', monospace", font_size="0.7rem",
                    color="rgba(0,255,178,0.55)", letter_spacing="0.15em"),
            rx.html("""<h2 style="
                font-family: 'Syne', sans-serif;
                font-size: clamp(3.5rem, 3.5vw, 2.7rem);
                font-weight: 700; color: white; text-align: center;
                letter-spacing: -0.03em; margin: 0.3em 0 0 0; line-height: 1.15;">
                Everything you need.<br/>
                <span style="color: rgba(255,255,255,0.2);">Nothing you don't.</span>
            </h2>"""),
            rx.grid(
                feature_card("zap", "Instant Cross-posting",
                             "One POST request publishes to all platforms simultaneously with per-platform success tracking."),
                feature_card("clock", "Reliable Scheduling",
                             "APScheduler-powered jobs stored in MongoDB. No Redis overhead. Survives restarts."),
                feature_card("lock", "Your Data, Your Server",
                             "Self-hosted means zero third-party access. Your API keys never leave your machine."),
                feature_card("code-2", "FastAPI Backend",
                             "Async Python with FastAPI + Beanie ODM. Typed, documented, and fast by default."),
                feature_card("refresh-cw", "Smart Retry Logic",
                             "Failed platforms don't block the rest. Partial success is tracked per post."),
                feature_card("terminal", "Docker One-liner",
                             "Full stack spins up with docker-compose up. MongoDB included. Zero config needed."),
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                spacing="4", width="100%", margin_top="3em",
            ),
            spacing="4", align="center", width="100%",
            max_width="1100px", margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5em", md="2.5em"),
            padding_y="6em",
            id="features",
        ),
        width="100%", background="#060608",
    )


# # # # # # # # # #
# PLATFORMS SECTION
# # # # # # # # # #

def platform_card(icon: str, name: str, lib: str, description: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=22, color=color),
                    width="46px", height="46px",
                    background="rgba(255,255,255,0.03)",
                    border="1px solid rgba(255,255,255,0.07)",
                    border_radius="12px",
                    display="flex", align_items="center", justify_content="center",
                ),
                rx.vstack(
                    rx.text(name, font_family="'Syne', sans-serif",
                            font_size="0.93rem", font_weight="700", color="white"),
                    rx.text(lib, font_family="'DM Mono', monospace",
                            font_size="0.66rem", color=color, letter_spacing="0.04em"),
                    spacing="0", align="start",
                ),
                spacing="3", align="center",
            ),
            rx.text(description,
                    font_family="'DM Sans', sans-serif", font_size="0.82rem",
                    color="rgba(255,255,255,0.28)", line_height="1.6"),
            align="start", spacing="3",
        ),
        padding="1.8em",
        background="rgba(255,255,255,0.016)",
        border="1px solid rgba(255,255,255,0.055)",
        border_radius="16px",
        _hover={"border_color": f"{color}44", "transform": "translateY(-3px)"},
        transition="all 0.25s ease",
    )


def platforms_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("// INTEGRATIONS",
                    font_family="'DM Mono', monospace", font_size="0.7rem",
                    color="rgba(0,255,178,0.55)", letter_spacing="0.15em"),
            rx.html("""<h2 style="
                font-family: 'Syne', sans-serif;
                font-size: clamp(3.5rem, 3.5vw, 2.7rem);
                font-weight: 700; color: white; text-align: center;
                letter-spacing: -0.03em; margin: 0.3em 0 0 0;">
                Four platforms. One call.</h2>"""),
            rx.grid(
                platform_card("twitter", "X (Twitter)", "tweepy v4",
                              "Post tweets with full OAuth 1.0a. Read/write access, thread support coming soon.", "#1DA1F2"),
                platform_card("message-circle", "Reddit", "praw 7.x",
                              "Submit text or link posts to any subreddit your account has posting access to.", "#FF4500"),
                platform_card("send", "Telegram", "python-telegram-bot",
                              "Post to any channel where your bot has admin rights. Markdown and HTML supported.", "#229ED9"),
                platform_card("hash", "Discord", "webhooks",
                              "Zero-auth posting via webhooks. Create one in server settings, paste the URL. Done.", "#5865F2"),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="4", width="100%", margin_top="3em",
            ),
            spacing="4", align="center", width="100%",
            max_width="900px", margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5em", md="2.5em"),
            padding_y="6em",
            id="platforms",
        ),
        width="100%",
        background="rgba(255,255,255,0.007)",
        border_top="1px solid rgba(255,255,255,0.04)",
        border_bottom="1px solid rgba(255,255,255,0.04)",
    )


# # # # # # # #
# SETUP SECTION
# # # # # # # #

def step_block(num: str, title: str, lines: list) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.text(num, font_family="'DM Mono', monospace", font_size="0.63rem",
                            color="#060608", font_weight="700"),
                    background="#00FFB2", border_radius="50%",
                    width="22px", height="22px",
                    display="flex", align_items="center", justify_content="center",
                ),
                rx.text(title, font_family="'Syne', sans-serif", font_size="0.9rem",
                        font_weight="700", color="white"),
                spacing="3", align="center",
            ),
            rx.box(
                rx.vstack(
                    *[rx.text(line,
                              font_family="'DM Mono', monospace",
                              font_size=rx.breakpoints(
                                  initial="0.7rem", md="0.77rem"),
                              color="#00FFB2" if line.startswith("✓") else (
                                  "rgba(255,255,255,0.25)" if line.startswith(
                                      "#") else "rgba(255,255,255,0.7)"
                              ),
                              white_space="pre",
                              ) for line in lines],
                    spacing="1", align="start",
                ),
                background="rgba(0,0,0,0.45)",
                border="1px solid rgba(255,255,255,0.06)",
                border_radius="10px",
                padding="1.2em",
                width="100%",
                overflow_x="auto",
            ),
            spacing="4", align="start",
        ),
        flex="1",
        min_width="200px",
    )


def setup_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("// QUICK START",
                    font_family="'DM Mono', monospace", font_size="0.7rem",
                    color="rgba(0,255,178,0.55)", letter_spacing="0.15em"),
            rx.html("""<h2 style="
                font-family: 'Syne', sans-serif;
                font-size: clamp(3.5rem, 3.5vw, 2.7rem);
                font-weight: 700; color: white; text-align: center;
                letter-spacing: -0.03em; margin: 0.3em 0 0 0;">
                Up in 60 seconds.</h2>"""),
            rx.hstack(
                step_block("01", "Clone & Configure", [
                    "git clone github.com/you/post4u",
                    "cd post4u",
                    "cp .env.example .env",
                    "# fill in your API keys",
                ]),
                step_block("02", "Launch", [
                    "docker-compose up -d",
                    "",
                    "✓ mongo   started",
                    "✓ api     started  :8000",
                ]),
                step_block("03", "Post", [
                    'curl -X POST /posts/ \\',
                    '  -d \'{"content":"gm",',
                    '  "platforms":["x","reddit"]}\'',
                ]),
                spacing="6", width="100%",
                flex_wrap=rx.breakpoints(initial="wrap", lg="nowrap"),
                align="start", margin_top="3em",
            ),
            rx.link(
                rx.hstack(
                    rx.icon("book-open", size=15, color="#060608"),
                    rx.text("Full docs in README",
                            font_family="'DM Mono', monospace", font_size="0.78rem",
                            color="#060608", font_weight="700"),
                    spacing="2", align="center",
                ),
                href="https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts", text_decoration="none",
                padding_x="2em", padding_y="0.85em",
                background="#00FFB2", border_radius="8px",
                margin_top="2em",
                box_shadow="0 0 30px rgba(0,255,178,0.2)",
                _hover={
                    "box_shadow": "0 0 40px rgba(0,255,178,0.35)", "transform": "translateY(-1px)"},
                transition="all 0.2s ease",
            ),
            spacing="4", align="center", width="100%",
            max_width="1100px", margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5em", md="2.5em"),
            padding_y="6em",
            id="setup",
        ),
        width="100%", background="#060608",
    )
