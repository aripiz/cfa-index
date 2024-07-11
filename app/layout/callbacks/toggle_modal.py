# toggle_modal.py

from fileinput import filename
from index import app
from index import data, metadata

from dash import Input, Output, State, dcc, callback_context
import pandas as pd
import io

metadata.index.name = 'indicator'
@app.callback(
    Output("modal", "is_open"),
    [Input("open_download", "n_clicks"), Input("close_download", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("download_file", "data"),
    [Input("download_button", "n_clicks"),
    Input('download_indicator','value'),
    Input('download_territory', 'value')],
    prevent_initial_call=True,
)
def download_excel(n_clicks, features, territories):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'download_button' in changed_id:
        meta_columns = ['subindex', 'dimension', 'name', 'unit', 'definition', 'last_update', 'source', 'source_link']
        meta = metadata[meta_columns]  
        data = data.set_index(['territory','year'])
        file_name = "WeWorld-Index-2024_Data.xlsx"
        if features  is not None: 
            data = data[features]
        if territories is not None:
            data = data.loc[territories]
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            meta.to_excel(writer, sheet_name='indicators_metadata')
            data.to_excel(writer, sheet_name='data')
        return dcc.send_bytes(buffer.getvalue(), filename=file_name)
    else: return None
