import dash_mantine_components as dmc
from dash import callback, Input, Output, State
import dash
import numpy as np
from utils.data import get_row, get_client_distribution
from utils.component import data_to_table, get_gauge_color
from dash_iconify import DashIconify
import requests
import os
from dotenv import load_dotenv

demo_icon = "teenyicons:adjust-horizontal-outline"
dash.register_page(__name__, image=DashIconify(icon=demo_icon, width=24, height=24))
dash.register_page(path="/", module=__name__, image=DashIconify(icon=demo_icon, width=24, height=24))

CHART_HEIGHT = 200
CHART_WIDTH = 300

days_birth_distribution, days_employed_distribution, days_registration_distribution, income_per_person_distribution = get_client_distribution(10)

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

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
                filledSegmentColor=get_gauge_color(0),
                size=600,
                thickness=50,
                value=0,
                label="",
                labelPosition="bottom",
            ),
            dmc.Title("Loan risk score", order=3)
        ],
        align="center", gap="md"
        ),
        withBorder=True,
        radius="md",
        p="md",
        shadow="xl"
    ),
    mt="xl"
)

graph_days_birth = dmc.Paper(
    [dmc.BarChart(
        id="score-distribution-chart",
        h=CHART_HEIGHT,
        w=CHART_WIDTH,
        dataKey="range",
        data=days_birth_distribution,
        series = [{"name": "count", "color": "violet"}],
        tickLine="xy",
        withXAxis=False,
    ),
    dmc.Space(h="md"),
    dmc.Text("Days birth distribution", ta="center")],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl"
)

graph_days_employed = dmc.Paper(
    [dmc.BarChart(
        id="score-distribution-chart",
        h=CHART_HEIGHT,
        w=CHART_WIDTH,
        dataKey="range",
        data=days_employed_distribution,
        series = [{"name": "count", "color": "violet"}],
        tickLine="xy",
        withXAxis=False,
    ),
    dmc.Space(h="md"),
    dmc.Text("Days employed distribution", ta="center")],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl"
)

graph_income_per_person = dmc.Paper(
    [dmc.BarChart(
        id="score-distribution-chart",
        h=CHART_HEIGHT,
        w=CHART_WIDTH,
        dataKey="range",
        data=income_per_person_distribution,
        series = [{"name": "count", "color": "violet"}],
        tickLine="xy",
        withXAxis=False,
    ),
    dmc.Space(h="md"),
    dmc.Text("Income per person distribution", ta="center")],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl"
)
graph_days_registration = dmc.Paper(
    [dmc.BarChart(
        id="score-distribution-chart",
        h=CHART_HEIGHT,
        w=CHART_WIDTH,
        dataKey="range",
        data=days_registration_distribution,
        series = [{"name": "count", "color": "violet"}],
        tickLine="xy",
        withXAxis=False,
    ),
    dmc.Space(h="md"),
    dmc.Text("Days registration distribution", ta="center")],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl"
)

layout = dmc.Grid(
    children=[
        dmc.GridCol(client_form, span={"base": 12, "md": 6}),
        dmc.GridCol(
            dmc.Grid(
                children=[
                    dmc.GridCol(semi_circle, span={"base": 12, "md": 12}),
                    dmc.GridCol(graph_days_birth, span={"base": 6, "md": 6}),
                    dmc.GridCol(graph_days_employed, span={"base": 6, "md": 6}),
                    dmc.GridCol(graph_days_registration, span={"base": 6, "md": 6}),
                    dmc.GridCol(graph_income_per_person, span={"base": 6, "md": 6})
                ]
            ), 
        span={"base": 12, "md": 6}
        )
    ]
)

@callback(
    Output(gauge_score, component_property="value"),
    Output(gauge_score, component_property="label"),
    Output(gauge_score, component_property="filledSegmentColor"),
    Output(client_informations, "children"),
    Input(button, "n_clicks"),
    State(client_id, component_property="value"),
)
def retrieve_client_info(n_clicks, input_value):
    if n_clicks:
        client_row = get_row(client_id=input_value)
        payload = client_row.to_json()

        response = requests.post(f"{API_BASE_URL}/predict", data=payload)

        score = 100 * response.json()["score"]

        client_inf = data_to_table(client_row)

        return int(np.round(score, 0)), f"{int(np.round(score, 0))}%", get_gauge_color(score), [client_inf]
    else:
        return 0, "", get_gauge_color(0), ["Search a Client..."]
