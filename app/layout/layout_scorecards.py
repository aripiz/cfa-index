from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
subindexes_list = [data.columns[4]]
features_list = data.columns[4:23].to_list()
years_list = data['year'].unique()
components_list = [f"Indicator {num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]
indicators_list = [f"{num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]
kind_list = ['Data', 'Scores']
territories_list = data['territory'].unique()
auxiliary_list = metadata.loc[101:102]['name'].to_list()
population_list = data.columns[83:86].to_list()


card = dbc.Container([
    dbc.Row([
        dbc.Col(html.P("Select a territory (Country/Area/World) from the list and explore the scorecard proving an insight on the CFA Index performance."), lg = 8, xs =12),
        dbc.Col([
            dbc.Label("Territory"),
            dcc.Dropdown(
                id='scorecard_territory',
                options=territories_list,
                value='World',
            )], lg=4, xs=12,align='end'),
    ], className='mt-4', justify='evenly' ),
    dbc.Row([
        dbc.Col(html.H2(id='scorecard_header'), lg=12, xs=12),
    ], className='mt-4', justify='evenly' ),
    dbc.Row([
        dbc.Col(dcc.Graph(id="scorecard_map", 
                          style={'height': 200, "width": 200},
                          config={'displayModeBar': False, 'editable':False}), lg=2, xs = 12, align='center'),
        dbc.Col(html.Div([
            html.H4("Area "),
            html.P(id="scorecard_area", style={'align':'right'}),
            html.H4("Population"),
            html.P(id="scorecard_pop", style={'align':'right'}),
            html.H4("GDP per capita"),
            html.P(id="scorecard_gdp", style={'align':'right'})
        ]), lg=4, xs=12, align='end'),
        dbc.Col(html.Div([
            html.H4("CFA Index Score "),
            html.P(id="scorecard_score"),
            html.H4("CFA Index Rank "),
            html.P(id="scorecard_rank", style={'align':'right'}),
            html.H4("Human Rights Implementaion "),
            html.P(id="scorecard_group")
        ]), lg=5, xs=12, align='end')
    ], className='mt-4', justify='evenly'),
   dbc.Row([
        dbc.Col(html.Div([
            html.H4("Progress"),
            dcc.Graph(id='scorecard_progress', config={'displaylogo':False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d', 'resetScale2d']})
        ]), lg=6, xs= 12),
        dbc.Col(html.Div([
            html.H4("Profile"),
            dcc.Graph(id='scorecard_radar', config={'displaylogo':False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d', 'resetScale2d']})
        ]), lg=6, xs= 12)
    ], className='mt-2', justify='evenly'),
    dbc.Row([dbc.Col([
            html.H4("Components"),
            html.Div(id='scorecard_table', 
                     className='table-container'
)
        ])
    ], className='mt-4', justify='evenly')
])

