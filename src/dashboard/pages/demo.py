import dash_mantine_components as dmc
from dash import callback, Input, Output, State
import dash
import numpy as np
from utils.data import get_row
from utils.component import data_to_table
from fastapi.testclient import TestClient   # More efficient than querying the deployed API
from api.main import app as API
from dash_iconify import DashIconify

demo_icon = "teenyicons:adjust-horizontal-outline"
dash.register_page(__name__, image=DashIconify(icon=demo_icon, width=24, height=24))
dash.register_page(path="/", module=__name__, image=DashIconify(icon=demo_icon, width=24, height=24))

client = TestClient(API)

client_id = dmc.NumberInput(
    label="Client ID",
    description="Client ID from 100,001 to 456,255",
    placeholder="SK_ID_CURR", 
    min=100001, 
    max=456255,
    allowDecimal=False,
)

button = dmc.Button(
    id="search-button", 
    children=["Search"], 
    color="violet",
)
client_informations = dmc.Table(
    children=[],
)


client_form = dmc.Box(
    dmc.Grid(children=[
        dmc.GridCol(client_id, span=10),
        dmc.GridCol(button, span=2),
        dmc.GridCol(client_informations, span=12)
    ])
)
client_form = dmc.Box([
    dmc.Flex([
        dmc.Box(client_id, style={"flex": 1}),
        button
    ], align="flex-end", gap="md"),
    dmc.Space(h="md"),
    client_informations
])
semi_circle = dmc.Box(
    dmc.Paper(
        children=dmc.Stack([
            gauge_score := dmc.SemiCircleProgress(
                fillDirection="left-to-right",
                orientation="up",
                filledSegmentColor="violet",
                size=600,
                thickness=50,
                value=0,
                label="",
                labelPosition="bottom",
            ),
            dmc.Title("Loan risk score", order=3)
        ], align="center", gap="md"),
        withBorder=True,
        radius="md",
        p="md",
        shadow="xl"
    ),
    mt="xl"
    )

layout = dmc.Grid(
    children=[
        dmc.GridCol(client_form, span={"base": 12, "md": 6}),
        dmc.GridCol(semi_circle, span={"base": 12, "md": 6})
    ]
)

@callback(
    Output(gauge_score, component_property="value"),
    Output(gauge_score, component_property="label"),
    Output(client_informations, "children"),
    Input(button, "n_clicks"),
    State(client_id, component_property="value"),
)
def retrieve_client_info(n_clicks, input_value):
    if n_clicks:
        client_row = get_row(client_id=input_value)
        payload = client_row.to_json()

        response = client.post("/predict", content=payload)

        score = 100 * response.json()["score"]

        client_inf = data_to_table(client_row)

        return int(np.round(score, 0)), f"{int(np.round(score, 0))}%", [client_inf]
    else:
        return 0, "", ["Search a Client..."]

