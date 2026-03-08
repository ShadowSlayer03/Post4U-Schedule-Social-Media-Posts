import reflex as rx
from post4u_frontend.components.navbar import navbar
from post4u_frontend.components.footer import footer
from post4u_frontend.components.hero import hero_section, stats_bar
from post4u_frontend.components.landing_sections import features_section, platforms_section, setup_section
from post4u_frontend.dashboard import dashboard


def index() -> rx.Component:
    return rx.box(
        rx.html("""<style>
            @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap');
            *{box-sizing:border-box} html{scroll-behavior:smooth}
            body{margin:0;padding:0;background:#060608}
            ::-webkit-scrollbar{width:4px}
            ::-webkit-scrollbar-track{background:#060608}
            ::-webkit-scrollbar-thumb{background:rgba(0,255,178,0.2);border-radius:2px}
            ::-webkit-scrollbar-thumb:hover{background:rgba(0,255,178,0.38)}
        </style>"""),
        navbar(),
        rx.vstack(
            hero_section(),
            stats_bar(),
            features_section(),
            platforms_section(),
            setup_section(),
            footer(),
            spacing="0",
            width="100%",
        ),
        background="#060608",
        min_height="100vh",
        width="100%",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=False,
        radius="medium",
        accent_color="green",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500;600&family=DM+Sans:wght@400;500&display=swap",
        "/date-picker.css",
    ],
    style={
        "background": "#060608",
        "color": "white",
        "font_family": "'DM Sans', sans-serif",
    }
)

app.add_page(index, route="/")
app.add_page(dashboard, route="/dashboard")