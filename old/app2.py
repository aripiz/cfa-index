# app.py
# Dash webapp to present WeWorld "Mai più invisibili 2023" index and indicators
# available at http://aripiz.pythonanywhere.com/


#### Preamble ####
# Libraries and functions
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import pandas as pd
import plotly.io as pio
import numpy as np

def sig_round(x, precision=3):
    return np.float64(f'{x:.{precision}g}')

# Title
title = 'WeWorld Mai più invisibili 2023'

# Themes
figure_template = 'cosmo'
theme = dbc.themes.COSMO
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

load_figure_template(figure_template)
pio.templates.default = figure_template

#### External data ####
# Mapbox
map_token = "pk.eyJ1IjoiYXJpcGl6IiwiYSI6ImNsZjE5YzJrbjA2OWMzcHM0YzJyaXIydHAifQ.SWcexWOHS6ddnrGBx7idAw"
map_style = "mapbox://styles/aripiz/clf1ay30l004n01lnzi17hjvj" 

# Files link
data_file = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/maipiuinvisibili2023_data.csv"
indicators_meta_file = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/maipiuinvisibili2023_metadata.csv"
geo_data_file = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/italy_regions_low.json"

# Loading
data = pd.read_csv(data_file)
metadata = pd.read_csv(indicators_meta_file, index_col=0)
#geo_data = pd.read_json(geo_data_file,lines=True).to_dict('records')[0]

#### App ####
app = Dash(__name__, external_stylesheets=[theme, dbc_css], suppress_callback_exceptions=True, title=title)

# Main layout
app.layout = dbc.Container([
        dcc.Store(id="store"),
        dcc.Markdown("# WeWorld _Mai più invisibili 2023_"),
        #html.H1(children="WeWorld Mai più invisibili 2023", style={"text-align": "center", }),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Mappa", tab_id="map_features"),
                #dbc.Tab(label="Mappa dimensioni", tab_id="dimensions"),
                dbc.Tab(label="Mappa Indicatori", tab_id="map_indicators"),
                dbc.Tab(label="Correlazione", tab_id="correlations"),
                dbc.Tab(label="Classifica", tab_id="ranking"),
                dbc.Tab(label="Evoluzione", tab_id="evolution"),
            ],
            id="tabs",
            active_tab="map_features",
        ),
        html.Div(id="tab-content", className="p-4"),
    ],
    fluid=True,
    className="dbc"
)

# Tabs
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")])
def render_tab_content(active_tab, data):
    if active_tab is not None:
        if active_tab == "map_features":
            options_list = data.columns[4:23]
            years_list = data['anno'].unique()
            return html.Div([
                dbc.Row([
                dbc.Col([
                    html.P("Seleziona un Indice/Dimensione:"),
                    dcc.Dropdown(
                    id='feature',
                    options=options_list,
                    value=options_list[0],
                    style={"width": "60%"})
                ]),
                dbc.Col([
                    html.P("Seleziona un anno:"), 
                    dcc.Slider(
                        years_list[0],
                        years_list[-1],
                        step=None,
                        id='slider_year',
                        value=years_list[-1],
                        marks={str(year): str(year) for year in years_list})],
                    width=3)], 
                justify='evenly'),                
                dcc.Graph(
                    id="map",
                    #style={'width': '90vw', 'height': '70vh'}
                )
            ])
        elif active_tab == "map_indicators":
            #return "Sezione ancora da creare."
            options_list = [f"{num}: {metadata.loc[num]['nome']}" for num in metadata.index]
            years_list = data['anno'].unique()
            kind_list = ['Dati', 'Punteggi']
            return html.Div([
                dbc.Row([
                dbc.Col([
                    html.P("Seleziona un Indicatore:"),
                    dcc.Dropdown(
                    id='indicator',
                    options=options_list,
                    value=options_list[0],
                    style={"width": "100%"})]
                ),
                dbc.Col([
                    html.P("Scegli la tipologia:"),
                    dbc.RadioItems(
                    id='indicator_kind',
                    options=kind_list,
                    inline=True,
                    value= kind_list[1])],
                    width=2
                ),
                dbc.Col([
                    html.P("Seleziona un anno:"), 
                    dcc.Slider(
                        years_list[0],
                        years_list[-1],
                        step=None,
                        id='slider_year',
                        value=years_list[-1],
                        marks={str(year): str(year) for year in years_list})],
                    width=3
                )], justify='evenly'),                
                dcc.Graph(
                    id="indicators_map",
                    #style={'width': '90vw', 'height': '70vh'}
                )
            ])
        elif active_tab == "correlations":
            options_list = data.columns[4:23]
            years_list = data['anno'].unique()
            return html.Div([
                dbc.Row([
                dbc.Col([
                    html.P("Seleziona un Indice/Dimensione:"),
                    dcc.Dropdown(
                    id="dimension_x",
                    options = options_list,
                    value=options_list[0],
                    style={"width": "75%"}
                )]),
                dbc.Col([
                    html.P("Seleziona un altro Indice/Dimensione:"),
                    dcc.Dropdown(
                    id="dimension_y",
                    options = options_list,
                    value=options_list[1],
                    style={"width": "75%"}
                )]),
                dbc.Col([
                    html.P("Seleziona un anno:"), 
                    dcc.Slider(
                        years_list[0],
                        years_list[-1],
                        step=None,
                        id='slider_year',
                        value=years_list[-1],
                        marks={str(year): str(year) for year in years_list})],
                    width=3)], 
                justify='evenly'),
                dcc.Graph(
                    id="dimensions_correlation",
                    #style={'width': '90vw', 'height': '70vh'}
                    responsive=True
                )
            ])
        elif active_tab == 'ranking':
            options_list = options_list = data.columns[4:23]
            years_list = data['anno'].unique()
            return html.Div([
                dbc.Row([
                dbc.Col([
                html.P("Seleziona un Indice/Dimensione:"),
                dcc.Dropdown(
                    id="ranking_feature",
                    options = options_list,
                    value=options_list[0],
                    style={"width": "75%"}
                )]),
                dbc.Col([
                html.P("Seleziona un anno:"),
                dcc.Slider(
                        years_list[0],
                        years_list[-1],
                        step=None,
                        id='slider_year',
                        value=years_list[-1],
                        marks={str(year): str(year) for year in years_list})
                ],width=3)
                ]),
                html.Div(
                    id='ranking_table'
                )
            ])
        elif active_tab == 'evolution':
            territories_list = data['territorio'].unique()
            options_list = data.columns[4:23]
            return html.Div([
                dbc.Row([
                dbc.Col([
                html.P("Seleziona un Indice/Dimensione:"),
                dcc.Dropdown(
                    id="evolution_feature",
                    options = options_list,
                    value=options_list[0],
                    style={"width": "75%"},
                    multi=True
                )]),
                dbc.Col([
                html.P("Seleziona un territorio:"),
                dcc.Dropdown(
                    id='evolution_territory',
                    options = territories_list ,
                    value = 'Italia',
                    style={"width": "75%"},
                    multi=True
                )])]),
                dcc.Graph(
                    id="evolution",
                    style={'width': '90vw', 'height': '70vh'}
                    #responsive=True
                )
            ])
    return "Nessun elemento selezionato."

# Index map
@app.callback(
    Output("map", "figure"),
    Input("feature", "value"),
    Input('slider_year', 'value'))
def display_map_index(feature, year):
    df = data[data['area'].notna()]
    fig = px.choropleth(df.loc[df['anno']==year], geojson=geo_data_file,
        locations='codice_istat', featureidkey="properties.istat_code_num",
        projection='natural earth', 
        color=feature,
        range_color=[20,80],
        color_continuous_scale='RdYlGn',
        hover_name='territorio',
        hover_data={'codice_istat':False, 'anno': False,
                    'Generale': ':.3g', 'Contesto':':.3g', 'Bambini':':.3g', 'Donne':':.3g'},
    )
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Punteggio"),
    )
    return fig.update_geos(fitbounds="locations", visible=False)

# Indicators map
@app.callback(
    Output("indicators_map", "figure"),
    Input("indicator", "value"),
    Input('slider_year', 'value'),
    Input('indicator_kind', 'value'))
def display_map_indicators(indicator, year, kind):
    indicator = indicator.split(":")[0]
    if metadata.loc[int(indicator)]['inverted']=='yes':
        color_scale = 'RdYlGn_r'
        limits_scale = [metadata.loc[int(indicator)]['best_value'], metadata.loc[int(indicator)]['worst_value']]
    else:
        color_scale = 'RdYlGn'
        limits_scale = [metadata.loc[int(indicator)]['worst_value'], metadata.loc[int(indicator)]['best_value']]
    df = data.loc[data['anno']==year]
    if kind=='Dati':
        col = f'Indicatore {int(indicator)}'
        fig = px.choropleth(df, geojson=geo_data_file,
            locations='codice_istat', featureidkey="properties.istat_code_num",
            projection='natural earth', 
            color=col,
            range_color=limits_scale,
            color_continuous_scale=color_scale,
            hover_name='territorio',
            hover_data={'codice_istat':False, 'anno': False,
                    col: ':.3g'},
        )
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            coloraxis_colorbar=dict(title=metadata.loc[int(indicator)]['unità']),
        )
    else:
        col = f"{metadata.loc[int(indicator)]['sottoindice']}|{metadata.loc[int(indicator)]['dimensione']}|{indicator}"
        fig = px.choropleth(df.loc[df['anno']==year], geojson=geo_data_file,
            locations='codice_istat', featureidkey="properties.istat_code_num",
            projection='natural earth',
            color=col,
            range_color=[0,100],
            color_continuous_scale='RdYlGn',
            hover_name='territorio',
            hover_data={'codice_istat':False, 'anno': False,
                    col: ':.3g'},
        )
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            coloraxis_colorbar=dict(title="Punteggio"),
        )
    return fig.update_geos(fitbounds="locations", visible=False)

# Correlation
@app.callback(
    Output("dimensions_correlation", "figure"),
    Input('dimension_x', 'value'),
    Input('dimension_y', 'value'),
    Input('slider_year', 'value'))
def display_corr_dimensions(dimension_x, dimension_y,year):
    df = data[data['area'].notna()]
    fig = px.scatter(df.loc[df['anno']==year], x=dimension_x, y=dimension_y,
                 hover_name='territorio', color='area',
                 hover_data={'area':False, 'anno': False, dimension_x: ':.3g', dimension_y:':.3g'},  range_x=[20,90], range_y=[20,90])
    fig.update_traces(marker={'size': 15})
    fig.update_layout(legend_title = 'Area')
    return fig

# Ranking
@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("slider_year", "value"))
def display_ranking(feature, year):
    df = data[data['area'].notna()].set_index('territorio')
    final = df[df['anno']==year][[feature]]
    initial = df[df['anno']==2018][[feature]]
    final['Posizione'] = final[feature].rank(ascending=False, method='min')
    final['Variazione dal 2018'] = (final[feature]-initial[feature]).apply(sig_round)
    final = final.reset_index().rename(columns={'territorio':'Territorio', feature:'Punteggio'}).sort_values('Posizione')
    table = dbc.Table.from_dataframe(
                    final[['Posizione', 'Territorio', 'Punteggio', 'Variazione dal 2018']],
                    bordered=False,
                    hover=True,
                    responsive=True,
                    striped=True,
                )
    return table

# Evolution
@app.callback(
    Output("evolution", "figure"),
    Input("evolution_feature", "value"),
    Input("evolution_territory", "value"))
def display_evolution(features, territories):
    df = data.query("territorio == @territories").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
    df = pd.melt(df, id_vars=['Territorio', 'Anno'], value_vars=features, var_name='Indice/Dimensione', value_name='Punteggio')
    fig = px.line(df, x='Anno', y='Punteggio',
                hover_name='Territorio',
                color='Territorio',
                line_dash='Indice/Dimensione',
                hover_data={'Territorio':False}
        )
    #fig.update_traces(marker={'size': 15})
    fig.update_layout(
        legend_title = 'Legenda',
        xaxis = dict(tickvals = df['Anno'].unique()),
        yaxis = dict(title='Punteggio')
        )
    return fig

#### Degug ####
if __name__ == "__main__":
    app.run(debug=True)
