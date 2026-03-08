from post4u_frontend.components.datetime_picker import date_picker
import reflex as rx
from post4u_frontend.states.dashboard_state import DashboardState
from .helpers import (
    slabel,
    flabel,
    input_style,
    ptoggle,
    prow,
    content_area,
)
from .buttons import post_btn, unschedule_btn, refresh_posts_btn
from .custom_select import custom_select

# # # # # # # # # #
# DASHBOARD TABS
# # # # # # # # # #


def schedule_tab() -> rx.Component:
    return rx.vstack(
        slabel("// schedule post"),
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=11,
                            color="rgba(255,255,255,0.5)"),
                    rx.text("Home", font_family="'DM Mono', monospace",
                            font_size="0.9rem", color="rgba(255,255,255,0.5)"),
                    spacing="2", align="center",
                ),
                href="/", text_decoration="none",
                _hover={"opacity": "0.7"}, transition="opacity 0.15s",
            ),
            height="100%", spacing="1", align="start", width="100%",
        ),
        rx.html(
            '<h2 style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;color:white;margin:0 0 0.1em 0;letter-spacing:-0.02em">Schedule a Post</h2>'
        ),
        rx.text(
            "Set platforms, write content, pick a time. Leave time blank to post immediately.",
            font_family="'DM Sans', sans-serif",
            font_size="0.82rem",
            color="rgba(255,255,255,0.27)",
            margin_bottom="1em",
        ),
        rx.vstack(
            flabel("Content"), content_area(), spacing="2", width="100%", align="start"
        ),
        rx.vstack(
            flabel("Platforms"), prow(), spacing="2", width="100%", align="start"
        ),
        rx.vstack(
            flabel("Scheduled Time (ISO 8601 — optional)"),
            date_picker(
                selected=DashboardState.scheduled_time,
                on_change=DashboardState.set_scheduled_time,
                **input_style()
            ),
            spacing="2",
            width="100%",
            align="start",
        ),
        rx.vstack(
            flabel("Media (Optional)"),
            rx.upload(
                rx.vstack(
                    rx.icon("upload", size=20, color="rgba(255,255,255,0.15)"),
                    rx.text(
                        "Drop file here or click to browse",
                        font_family="'DM Mono', monospace",
                        font_size="0.72rem",
                        color="rgba(255,255,255,0.3)",
                    ),
                    rx.cond(
                        DashboardState.media_file,
                        rx.box(
                            rx.hstack(
                                rx.icon("file-check", size=14,
                                        color="#00FFB2"),
                                rx.text(
                                    DashboardState.media_file[0],
                                    font_family="'DM Mono', monospace",
                                    font_size="0.65rem",
                                    color="#00FFB2",
                                ),
                                rx.icon(
                                    "x",
                                    size=12,
                                    color="rgba(255,255,255,0.4)",
                                    cursor="pointer",
                                    on_click=DashboardState.set_media_file(
                                        None),
                                    stop_propagation=True,
                                    _hover={"color": "#FF4B4B"},
                                ),
                                spacing="2",
                            ),
                            padding="0.4em 0.8em",
                            background="rgba(0,255,178,0.05)",
                            border="1px solid rgba(0,255,178,0.2)",
                            border_radius="6px",
                            margin_top="0.5em",
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),
                id="media_upload",
                border="1px dashed rgba(255,255,255,0.1)",
                padding="2em",
                border_radius="12px",
                background="rgba(255,255,255,0.01)",
                _hover={
                    "border_color": "rgba(255,255,255,0.2)", "background": "rgba(255,255,255,0.02)"},
                width="100%",
                on_drop=DashboardState.handle_upload(
                    rx.upload_files(upload_id="media_upload")),
            ),
            on_mouse_up=DashboardState.handle_upload(
                rx.upload_files(upload_id="media_upload")),
            spacing="2",
            width="100%",
            align="start",
        ),
        post_btn("Schedule Post →"),

        spacing="5",
        align="start",
        width="55%",
    )


def post_now_tab() -> rx.Component:
    return rx.vstack(
        slabel("// post now"),
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=11,
                            color="rgba(255,255,255,0.5)"),
                    rx.text("Home", font_family="'DM Mono', monospace",
                            font_size="0.9rem", color="rgba(255,255,255,0.5)"),
                    spacing="2", align="center",
                ),
                href="/", text_decoration="none",
                _hover={"opacity": "0.7"}, transition="opacity 0.15s",
            ),
            height="100%", spacing="1", align="start", width="100%",
        ),
        rx.html(
            '<h2 style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;color:white;margin:0 0 0.1em 0;letter-spacing:-0.02em">Post Immediately</h2>'
        ),
        rx.text(
            "No scheduling. Fires the moment you hit post.",
            font_family="'DM Sans', sans-serif",
            font_size="0.82rem",
            color="rgba(255,255,255,0.27)",
            margin_bottom="1.5em",
        ),
        rx.vstack(
            flabel("Content"), content_area(), spacing="2", width="100%", align="start"
        ),
        rx.vstack(
            flabel("Platforms"), prow(), spacing="2", width="100%", align="start"
        ),
        post_btn("Post Now →"),
        spacing="5",
        align="start",
        width="55%",
    )


def history_tab() -> rx.Component:
    return rx.vstack(
        slabel("// history"),
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=11,
                            color="rgba(255,255,255,0.5)"),
                    rx.text("Home", font_family="'DM Mono', monospace",
                            font_size="0.9rem", color="rgba(255,255,255,0.5)"),
                    spacing="2", align="center",
                ),
                href="/", text_decoration="none",
                _hover={"opacity": "0.7"}, transition="opacity 0.15s",
            ),
            height="100%", spacing="1", align="start", width="100%",
        ),
        rx.html(
            '<h2 style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;color:white;margin:0 0 0.1em 0;letter-spacing:-0.02em">Post History</h2>'
        ),
        rx.vstack(
            rx.text(
                "All the posts that are posted/scheduled to be posted.",
                font_family="'DM Sans', sans-serif",
                font_size="0.82rem",
                color="rgba(255,255,255,0.27)",
            ),
            rx.text(
                "Platforms in green represent successful posts, while orange indicates failures.",
                font_family="'DM Sans', sans-serif",
                font_size="0.82rem",
                color="rgba(255,255,255,0.27)",
            ),
            gap="0.5em",
            margin_bottom="1em",
        ),
        refresh_posts_btn(),
        rx.cond(
            DashboardState.posts.length() == 0,
            rx.box(
                rx.vstack(
                    rx.icon("inbox", size=26, color="rgba(255,255,255,0.08)"),
                    rx.text(
                        "No posts yet — click Refresh",
                        font_family="'DM Mono', monospace",
                        font_size="0.73rem",
                        color="rgba(255,255,255,0.18)",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding_y="4em",
                background="rgba(255,255,255,0.01)",
                border="1px solid rgba(255,255,255,0.05)",
                border_radius="12px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.grid(
                rx.foreach(
                    DashboardState.posts,
                    lambda post: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.hstack(
                                    rx.foreach(
                                        ["x", "reddit", "telegram", "discord"],
                                        lambda plat: rx.cond(
                                            post["status"].get(plat),
                                            rx.box(
                                                rx.text(
                                                    plat.upper(),
                                                    font_family="'DM Mono', monospace",
                                                    font_size="0.55rem",
                                                    font_weight="700",
                                                    color=rx.cond(
                                                        post["status"].get(plat, {}).get(
                                                            "status") == "success",
                                                        "#00FFB2",
                                                        "rgba(255,180,0,0.85)",
                                                    ),
                                                ),
                                                padding_x="0.6em",
                                                padding_y="0.2em",
                                                background=rx.cond(
                                                    post["status"].get(plat, {}).get(
                                                        "status") == "success",
                                                    "rgba(0,255,178,0.05)",
                                                    "rgba(255,180,0,0.05)",
                                                ),
                                                border=rx.cond(
                                                    post["status"].get(plat, {}).get(
                                                        "status") == "success",
                                                    "1px solid rgba(0,255,178,0.15)",
                                                    "1px solid rgba(255,180,0,0.15)",
                                                ),
                                                border_radius="4px",
                                            ),
                                        )
                                    ),
                                    spacing="2",
                                ),
                                rx.spacer(),
                                rx.vstack(
                                    rx.text(
                                        "ID: " + post.id,
                                        font_family="'DM Mono', monospace",
                                        font_size="0.55rem",
                                        color="rgba(255,255,255,0.1)",
                                    ),
                                    rx.text(
                                        rx.cond(post.scheduled_time, "Scheduled: " + post.scheduled_time, "Posted immediately"),
                                        font_family="'DM Mono', monospace",
                                        font_size="0.6rem",
                                        color="rgba(255,255,255,0.3)",
                                    ),
                                    align="end",
                                    spacing="0",
                                ),
                                width="100%",
                                align="center",
                            ),
                            # Middle: Content
                            rx.box(
                                rx.text(
                                    post["content"],
                                    font_family="'DM Sans', sans-serif",
                                    font_size="0.88rem",
                                    color="rgba(255,255,255,0.7)",
                                    line_height="1.6",
                                ),
                                width="100%",
                                padding_y="0.5em",
                            ),
                            # Bottom: Metadata
                            rx.divider(border_color="rgba(255,255,255,0.03)"),
                            rx.hstack(
                                rx.icon("clock", size=10,
                                        color="rgba(255,255,255,0.2)"),
                                rx.text(
                                    "Created: " + post.get("created_at", ""),
                                    font_family="'DM Mono', monospace",
                                    font_size="0.55rem",
                                    color="rgba(255,255,255,0.2)",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            spacing="3",
                            align="start",
                        ),
                        padding="1.5em",
                        background="rgba(255,255,255,0.01)",
                        border="1px solid rgba(255,255,255,0.04)",
                        border_radius="12px",
                        width="100%",
                        _hover={
                            "border_color": "rgba(255,255,255,0.08)", "background": "rgba(255,255,255,0.015)"},
                        transition="all 0.2s ease",
                    ),
                ),
                spacing="4",
                columns="2",
                width="100%",
            ),
        ),
        spacing="5",
        align="start",
        width="100%",
        on_mount=DashboardState.load_posts,
    )


def unschedule_tab() -> rx.Component:
    return rx.vstack(
        slabel("// unschedule post"),
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=11,
                            color="rgba(255,255,255,0.5)"),
                    rx.text("Home", font_family="'DM Mono', monospace",
                            font_size="0.9rem", color="rgba(255,255,255,0.5)"),
                    spacing="2", align="center",
                ),
                href="/", text_decoration="none",
                _hover={"opacity": "0.7"}, transition="opacity 0.15s",
            ),
            height="100%", spacing="1", align="start", width="100%",
        ),
        rx.html(
            '<h2 style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;color:white;margin:0 0 0.1em 0;letter-spacing:-0.02em">Unschedule a Post</h2>'
        ),
        rx.text(
            "Unschedule posts that are no longer required to be posted.",
            font_family="'DM Sans', sans-serif",
            font_size="0.82rem",
            color="rgba(255,255,255,0.27)",
            margin_bottom="1em",
        ),
        rx.box(
            rx.hstack(
                rx.icon("alert-triangle", size=14,
                        color="rgba(255,180,0,0.6)"),
                rx.text(
                    "This does not delete the post from the platform if it was already posted.",
                    font_family="'DM Mono', monospace",
                    font_size="0.7rem",
                    color="rgba(255,180,0,0.55)",
                ),
                spacing="3",
                align="center",
            ),
            background="rgba(255,180,0,0.04)",
            border="1px solid rgba(255,180,0,0.1)",
            border_radius="8px",
            padding="0.82em 1em",
            width="100%",
        ),
        rx.vstack(
            flabel("Select Post"),
            custom_select(
                options=DashboardState.post_select_options,
                value=DashboardState.delete_post_id,
                on_change=DashboardState.set_delete_post_from_option,
                placeholder="Pick a post to unschedule...",
                width="100%",
            ),
            rx.cond(
                DashboardState.delete_post_id != "",
                rx.hstack(
                    rx.icon("check", size=11, color="#00FFB2"),
                    rx.text(
                        "Selected: " + DashboardState.delete_post_id,
                        font_family="'DM Mono', monospace",
                        font_size="0.62rem",
                        color="rgba(0,255,178,0.6)",
                    ),
                    spacing="1",
                    align="center",
                ),
            ),
            spacing="2",
            width="100%",
            align="start",
        ),
        unschedule_btn("Unschedule →"),
        spacing="5",
        align="start",
        width="55%",
        on_mount=DashboardState.load_posts,
    )
