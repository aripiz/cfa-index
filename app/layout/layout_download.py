# layout_download.py

from index import df_data, df_meta
from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
features_list = df_data.columns[4:-1]
years_list = df_data['year'].unique()
#indicators_list = [f"{num}: {df_meta.loc[num]['name']}" for num in df_meta.index]

#indicators_numbers = [f"{num}" for num in df_meta.index]
territories_list = df_data['territory'].unique()

# Modal window
modal_data_download = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Data download"), close_button=False),
        dbc.ModalBody(
            html.Div([
                dbc.Label('Download all available data or select a subset'),
                dbc.Row(
                dbc.Col([
                    # dbc.DropdownMenu(
                    #     dbc.Checklist(
                    #         id="download_indicator",
                    #         options = features_list,
                    #         style={ "overflow-y":"scroll", "height": "200px", "padding-left":"10px", "padding-right":"10px"},
                    #     ),
                    #     label='Select features', 
                    # )
                    dcc.Dropdown(
                        id='download_indicator',
                        options=features_list,
                        multi=True,
                        placeholder="Select features",
                        style={"width": "100%",}
                    ),
                ], xs=12)),
                dbc.Row(
                dbc.Col([
                    html.Br(),
                    dcc.Dropdown(
                        id='download_territory',
                        options=territories_list,
                        multi=True,
                        placeholder="Select territories",
                        style={"width": "100%",}
                    ),
                    # dbc.DropdownMenu(
                    #     dbc.Checklist(
                    #         id='download_territory',
                    #         options = territories_list ,
                    #         style={ "overflow-y":"scroll", "height": "200px", "padding-left":"10px", "padding-right":"10px"},
                    #     ),
                    #     label='Select territories', 
                    # )
                ], xs=12)),
                html.Br(),
                dbc.Button('Download', id='download_button', n_clicks=0),
                dcc.Download(id='download_file')
            ],
            style={'text-align':'center'})
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Chiudi", id="close_download", n_clicks=0, 
                )
        ),
    ],
    id="modal",
    centered=True,
    is_open=False,
)
