from dash import Dash, callback, Input, Output, State
import dash
import dash_mantine_components as dmc

app = Dash(
    __name__, 
    use_pages=True,
    suppress_callback_exceptions=True
)

server = app.server

# AppShell children
navbar = dmc.AppShellNavbar(
    children=[
        dmc.Group(
            children=[
                dmc.Title(id="menu-title", children="Menu", order=2, style={"display": "none"}),
                dmc.Burger(id="mobile-burger", size="sm", hiddenFrom="sm", opened=False),
                dmc.Burger(id="desktop-burger", size="sm", visibleFrom="sm", opened=True)
            ],
            style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}
        ),
        dmc.Space(h="md"),
        *[dmc.NavLink(
            id=page["relative_path"], 
            label=page["name"], 
            href=page["relative_path"], 
            leftSection=page["image"],
            active="exact",
            color="violet",
            ) for page in dash.page_registry.values()]],
    p="md",
)
main = dmc.AppShellMain(
    dash.page_container
)

def get_layout():
    return dmc.AppShell(
        id="appshell",
        children=[
            navbar,
            main,
        ],
        navbar={
            "width": 300,
            "breakpoint": "sm"
        },
        padding="md",
    )

# AppShell holder
appshell = get_layout()


app.layout = dmc.MantineProvider(
    children=appshell, 
    forceColorScheme="light"
)

@callback(
    Output("appshell", "navbar"),
    Output("menu-title", "style"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, navbar):
    if desktop_opened:
        navbar["width"] = 300 
        s = {"display": "block"}
        return navbar, s
    elif mobile_opened:
        navbar["width"] = 300
        s = {"display": "block"}
        return navbar, s
    else:
        navbar["width"] = 80
        s = {"display": "none"}
        return navbar, s
