# data.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name = TITLE )

# Tabs
tabs = html.Div(dbc.Tabs(
    [
        dbc.Tab(label="Mappa componenti", tab_id="map_features"),
        dbc.Tab(label="Classifica territori", tab_id="ranking"),
        dbc.Tab(label="Profili territori", tab_id="radar"),
        dbc.Tab(label="Mappa indicatori", tab_id="map_indicators"),
        dbc.Tab(label="Correlazioni componenti", tab_id="correlations"),
        dbc.Tab(label="Evoluzione componenti", tab_id="evolution"),
    ],
    id="data_tabs",
    active_tab="map_features",
    className= 'd-flex justify-content-around'
))

layout = html.Div(
    [
        dbc.Row(dbc.Col(tabs)),
        dbc.Row(dbc.Col(id="data_tab_content"), class_name='mt-4')
    ],
)