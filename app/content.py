# content.py

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks  import render_data
from layout.callbacks import render_tab
from layout.callbacks import render_scorecards

from layout.callbacks import toggle_modal
from layout.callbacks import toggle_collapse

from configuration import NOTES_FILE, REPORT_FILE

from layout.layout_download import modal_data_download

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", active='exact', href='/')),
        dbc.NavItem(dbc.NavLink("Data", active='exact', href="/data")),
        dbc.NavItem(dbc.NavLink("Scorecards", active='exact', href='/scorecards')),
        dbc.NavItem(dbc.NavLink("Methodology", active='exact', href="/methodology")),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Report", href=REPORT_FILE), 
                dbc.DropdownMenuItem("Techical Notes", href=NOTES_FILE), 
                dbc.DropdownMenuItem("Data", id='open_download', n_clicks=0),
                modal_data_download
            ],
            nav=True,
            label="Download",
            in_navbar=True,
        ),
    ],
    brand= [html.Img(src="assets/logo_weworld_neg.png", height='30px'), "  Index 2024"],
            #html.Img(src="assets/logo_maipiuinvisibili2023_neg.png", height="30px", alt='Index 2024')],
    brand_href="https://www.weworld.it",
    fixed='top',
    color='primary',
    dark=True
)

# Footer
footer = dbc.Navbar(
    dbc.Container([
        html.P("© 2024 WeWorld", style={'font-size':'xx-small'}, className='mb-0'), 
        html.P(["credits: ", html.A("aripiz", href="https://github.com/aripiz",className='link')], style={'font-size':'xx-small'}, className='mb-0')
    ]),
    style={"display": "flex", 'justify-content': 'space-between', 'flex':'1', 'height': '15px' },
    #color="primary",
    fixed='bottom',
)      
           
# Page
content = dbc.Container(page_container, class_name='mt-4', style={ 'padding-top': '80px', 'padding-bottom': '60px'}) 

# Main layout
app.layout = dbc.Container(
    [
        navbar,
        content,
        footer
    ],
    fluid=True,
    className="dbc",     
    style={"display": "flex", "flex-direction": "column"}
)
