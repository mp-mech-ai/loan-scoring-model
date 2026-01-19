import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from utils.data import get_api_usage, get_evidently_analysis, get_score_distribution
from datetime import datetime
import pandas as pd

analytics_icon = "teenyicons:area-chart-outline"
dash.register_page(__name__, image=DashIconify(icon=analytics_icon, width=24, height=24))

CHART_HEIGHT = 250

usage = get_api_usage()
score = get_score_distribution()
report = get_evidently_analysis()

report_paper = dmc.Paper(
    id="report-paper",
    children=[
        dmc.Stack(
            children=[dmc.LoadingOverlay(
                    visible=False,
                    id="loading-overlay",
                    loaderProps={"type": "bars", "color": "black", "size": "lg"},
                    overlayProps={"radius": "sm", "blur": 2},
                    zIndex=10,
                ),
            html.Iframe(
                id="report-iframe", 
                srcDoc=report,
                style={
                    "width": "100%",
                    "height": "900px",
                    "border": "none"
                }
            ),
            dmc.Button(
                children="Generate Report", 
                id="generate-report", 
                variant="gradient",
                gradient={"from": "red", "to": "violet"},
                loaderProps={"type": "bars", "color": "black", "size": "xs"}
                )
            ],
            align="center",
            gap="md"
        )
    ],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl",
    style={"width": "100%"},
    pos="relative"
)

initial_data = [{"time": f'{(datetime.now() - pd.Timedelta(5*i, "s")).strftime("%H:%M:%S")}', "latency": 0} for i in range(9, -1, -1)]

api_latency_chart = dmc.Paper(
    children=[
        dmc.Stack(
            children=[
                dcc.Store(id='latency-store', data=initial_data),
                dmc.AreaChart(
                    id="latency-chart",
                    h=CHART_HEIGHT,
                    dataKey="time",
                    data=initial_data,
                    series=[{"name": "latency", "color": "red.6"}],
                    curveType="monotone",
                    tickLine="xy",
                    withGradient=True,
                    withDots=True,
                    unit=" ms",
                ),
                dmc.Group(
                    children=[
                        dmc.Indicator(
                            children=[dmc.Text("")],
                            processing=True,
                            color="red",
                            position="middle-center"
                        ),
                        dmc.Text("Live API latency"),
                    ]
                    ),
                dcc.Interval(
                    id='latency-interval',
                    interval=5000,
                    n_intervals=0
                )
            ],
            align="center",
            gap="md"
        ),
    ],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl",
    style={"width": "100%"} 
)

refresh_usage_chart_button = dmc.Button(
    children=DashIconify(icon="mdi:refresh"),
    id="refresh-usage-chart",
    color="black",
    variant="outline",
    style={"width": "36px", "height": "36px", "padding": 0}
)

usage_chart = dmc.Paper(
    children=[
        dmc.Stack(
            children=[
                dmc.AreaChart(
                    id="usage-chart",
                    h=CHART_HEIGHT,
                    dataKey="dt",
                    data=usage,
                    series = [{"name": "usage", "color": "red.6"}],
                    curveType="monotone",
                    tickLine="xy",
                    withGradient=False,
                    withXAxis=False,
                    withDots=False,
                ),
                dmc.Grid(
                    children=[
                        dmc.GridCol(span=4),
                        dmc.GridCol(span=4, children=dmc.Text("Last day API Usage", ta="center")),
                        dmc.GridCol(span=4, children=dmc.Box(refresh_usage_chart_button, style={"textAlign": "right"}))
                    ],
                    style={"width": "100%"}
                )
            ],
            align="center",
            gap="md"
        )
    ],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl",
    style={"width": "100%"} 
)

score_distribution_chart_button = dmc.Button(
    children=DashIconify(icon="mdi:refresh"),
    id="refresh-score-distribution",
    color="black",
    variant="outline",
    style={"width": "36px", "height": "36px", "padding": 0}
)

score_distribution_chart = dmc.Paper(
    children=[
        dmc.Stack(
            children=[
                dmc.BarChart(
                    id="score-distribution-chart",
                    h=CHART_HEIGHT,
                    dataKey="range",
                    data=score,
                    series = [{"name": "count", "color": "red.6"}],
                    tickLine="xy",
                    withXAxis=False,
                ),
                dmc.Grid(
                    children=[
                        dmc.GridCol(span=4),
                        dmc.GridCol(span=4, children=dmc.Text("Score Distribution", ta="center")),
                        dmc.GridCol(span=4, children=dmc.Box(score_distribution_chart_button, style={"textAlign": "right"}))
                    ],
                    style={"width": "100%"}
                )
            ],
            align="center",
            gap="md"
        )
    ],
    withBorder=True,
    radius="md",
    p="md",
    shadow="xl",
    style={"width": "100%"} 
)


layout = dmc.Grid(
    children=[
        dmc.GridCol(
            id="evidently-report",
            children=[report_paper],
            span={"base": 12, "md": 8}
        ),
        dmc.GridCol(
            children=dmc.Stack(
                children=[
                    usage_chart,
                    score_distribution_chart,
                    api_latency_chart
                ],
                align="center",
                gap="md"
            ), 
            span={"base": 12, "md": 4}),
    ]
)


@callback(
    Output('latency-store', 'data'),
    Output('latency-chart', 'data'),
    Input('latency-interval', 'n_intervals'),
    State('latency-store', 'data'),
    prevent_initial_call=True
)
def update_latency_chart(n, stored_data):
    from utils.data import get_api_latency
    
    current_latency = get_api_latency()
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Rolling window: remove first, append last
    new_data = stored_data[1:] + [{
        "time": current_time,
        "latency": current_latency
    }]
    
    return new_data, new_data

@callback(
    Output('report-iframe', 'srcDoc'),
    Input('generate-report', 'n_clicks'),
    running=[(Output("generate-report", "loading"), True, False), (Output("loading-overlay", "visible"), True, False)],
    prevent_initial_call=True
)
def generate_report(n_clicks):
    new_report = get_evidently_analysis()
    return new_report

@callback(
    Output('usage-chart', 'data'),
    Input('refresh-usage-chart', 'n_clicks'),
    running=[(Output("refresh-usage-chart", "loading"), True, False)],
    prevent_initial_call=True
)
def refresh_usage_chart(n_clicks):
    new_usage = get_api_usage()
    return new_usage


@callback(
    Output('score-distribution-chart', 'data'),
    Input('refresh-score-distribution', 'n_clicks'),
    running=[(Output("refresh-score-distribution", "loading"), True, False)],
    prevent_initial_call=True
)
def refresh_score_distribution_chart(n_clicks):
    new_score = get_score_distribution()
    return new_score