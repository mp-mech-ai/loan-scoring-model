import pandas as pd
import dash_mantine_components as dmc

def data_to_table(data: pd.Series) -> dmc.Table:
    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(k),
                dmc.TableTd(v)
            ]
        )
        for k, v in data.to_dict().items()
    ]
    body = dmc.TableTbody(rows)

    return dmc.Table([body])


def get_gauge_color(value):
    """Return modern color based on value thresholds"""
    if value < 33:
        return "#10b981"  # Modern emerald green
    elif value < 66:
        return "#f59e0b"  # Modern amber/orange
    else:
        return "#ef4444"  # Modern coral red