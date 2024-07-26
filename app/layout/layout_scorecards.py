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
        dbc.Col(html.H2(id='scorecard_header'), width=8),
        dbc.Col([
            dbc.Label("Territory"),
            dcc.Dropdown(
                id='scorecard_territory',
                options=territories_list,
                value='World',
            )], width=4, align='end')
    ], className='mt-2', justify='evenly' ),
    dbc.Row([
        dbc.Col(dcc.Graph(id="scorecard_map", style={'height': 200, "width": 200}), width=2, align='end'),
        dbc.Col(html.Div([
            html.H4("Area "),
            html.P(id="scorecard_area", style={'align':'right'}),
            html.H4("Population"),
            html.P(id="scorecard_pop", style={'align':'right'}),
            html.H4("GDP per capita"),
            html.P(id="scorecard_gdp", style={'align':'right'})
        ]), width=4, align='end'),
        dbc.Col(html.Div([
            html.H4("CFA Index Score "),
            html.P(id="scorecard_score"),
            html.H4("CFA Index Rank "),
            html.P(id="scorecard_rank", style={'align':'right'}),
            html.H4("Human Rights Implementaion "),
            html.P(id="scorecard_group")
        ]), width=5, align='end')
    ], className='mt-2', justify='evenly'),
   dbc.Row([
        dbc.Col(html.Div([
            html.H4("CFA Index progress"),
            dcc.Graph(id='scorecard_progress')
        ]), width=6),
        dbc.Col(html.Div([
            html.H4("Components profile"),
            dcc.Graph(id='scorecard_radar')
        ]), width=6)
    ], className='mt-2', justify='evenly'),
    # dbc.Row([
    #     dbc.Col(html.Div([
    #         html.H4("Components scores"),
    #         html.Div(id='table', children=[
    #             html.Table([
    #                 html.Thead(html.Tr([html.Th("Column 1"), html.Th("Column 2")])),
    #                 html.Tbody([
    #                     html.Tr([html.Td("Value 1"), html.Td("Value 2")]),
    #                     html.Tr([html.Td("Value 3"), html.Td("Value 4")])
    #                     # Add more rows as needed
    #                 ])
    #             ])
    #         ])
    #     ]))
    # ], className='mt-2', justify='evenly')
], fluid=True)

country_card = html.Div([
    dbc.Row([
        dbc.Col(html.H2(id='scorecard_header')),
        dbc.Col([
        dbc.Label("Territory"),
        dcc.Dropdown(
            id='scorecard_territory',
            options = territories_list ,
            value = 'World',
            style = {"width": "75%"}
        )]),
    ],  class_name = 'mt-2'),
    dbc.Row([
        dbc.Col(
        dcc.Graph(
            id="scorecard_map",
            style={'height': 200, "width":200}
        ), ),
        dbc.Col([html.H4('CFA Index')])
    ])
   
])

