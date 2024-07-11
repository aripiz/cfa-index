# layout_download.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
features_list = data.columns[4:]
years_list = data['year'].unique()
#indicators_list = [f"{num}: {metadata.loc[num]['name']}" for num in metadata.index]

#indicators_numbers = [f"{num}" for num in metadata.index]
territories_list = data['territory'].unique()

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
                        placeholder="All features",
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
                        placeholder="All territories",
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
                "Close", id="close_download", n_clicks=0, 
                )
        ),
    ],
    id="modal",
    centered=True,
    is_open=False,
)
