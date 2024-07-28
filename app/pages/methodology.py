# methodology.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name = TITLE )

# Tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(label="Index Construction", tab_id="construction"),
        dbc.Tab(label="Indicators List", tab_id="indicators"),
    ],
    id="metho_tabs",
    active_tab="construction",
    className= 'd-flex justify-content-around'
)

layout = dbc.Container([
        dbc.Row(dbc.Col(tabs)),
        dbc.Row(dbc.Col(id="metho_tab_content"),className='mt-2'),
    ], class_name='mt-4')
