# methodology.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name = TITLE )

# Tabs
tabs = html.Div(dbc.Tabs(
    [
        dbc.Tab(label="Costruzione dell'Indice", tab_id="construction"),
        dbc.Tab(label="Definizione degli Indicatori", tab_id="indicators"),
    ],
    id="metho_tabs",
    active_tab="construction",
    className= 'd-flex justify-content-around'
))

layout = html.Div([
        dbc.Row(dbc.Col(tabs)),
        dbc.Row(dbc.Col(id="metho_tab_content"), class_name='mt-4'),
    ])
