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