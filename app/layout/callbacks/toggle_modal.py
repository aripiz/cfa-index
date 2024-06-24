# toggle_modal.py

from fileinput import filename
from index import app
from index import df_data, df_meta

from dash import Input, Output, State, dcc, callback_context
import pandas as pd
import io

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
def download_excel(n_clicks, indicators, territories):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'download_button' in changed_id:
        colonne_metadati = ['sottoindice', 'dimensione', 'nome', 'unità', 'descrizione', 'aggiornamento', 'fonte', 'link']
        colonne_dati = [f'Indicatore {i}' for i in range(1,31)]

        meta = df_meta[colonne_metadati]  
        data = df_data.set_index(['territorio','anno'])[colonne_dati]
        file_name = "WeWorld-MaiPiùInvisibili-2023_Indicatori.xlsx"
        if indicators  is not None: 
            indicators = [int(indicator.split(":")[0]) for indicator in indicators]
            colonne_dati = [f'Indicatore {indicator}' for indicator in indicators]
            meta = meta.loc[indicators]
            data = data[colonne_dati]
            file_name = "WeWorld-MaiPiùInvisibili-2023_Indicatori-selezione.xlsx"
        if territories is not None:
            data = data.loc[territories]
            file_name = "WeWorld-MaiPiùInvisibili-2023_Indicatori-selezione.xlsx"
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            meta.to_excel(writer, sheet_name='metadati')
            data.to_excel(writer, sheet_name='dati')
        return dcc.send_bytes(buffer.getvalue(), filename=file_name)
    else: return None
