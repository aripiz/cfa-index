# data.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name = TITLE )

# Tabs
tabs = html.Div(dbc.Tabs(
    [
        dbc.Tab(label="Map", tab_id="map_features"),
        dbc.Tab(label="Ranking", tab_id="ranking"),
        dbc.Tab(label="Progress", tab_id="evolution"),
        dbc.Tab(label="Profiles", tab_id="radar"),
        dbc.Tab(label="Indicators", tab_id="map_indicators"),
        dbc.Tab(label="Correlations", tab_id="correlations"),
        dbc.Tab(label="Comparison", tab_id="comparison"),
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