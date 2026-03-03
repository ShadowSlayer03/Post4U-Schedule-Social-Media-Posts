import reflex as rx

config = rx.Config(
    app_name="post4u_frontend",
    app_module_import="post4u_frontend.index", 
    backend_port=8001,
    env=rx.Env.DEV,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)