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
df_data = pd.read_csv(data_file)
df_meta = pd.read_csv(indicators_meta_file, index_col=0)
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
                dbc.Tab(label="Mappa delle componenti", tab_id="map_features"),
                dbc.Tab(label="Classifica dei territori", tab_id="ranking"),
                dbc.Tab(label="Schede dei territori", tab_id="radar"),
                dbc.Tab(label="Mappa degli indicatori", tab_id="map_indicators"),
                dbc.Tab(label="Correlazioni delle componenti", tab_id="correlations"),
                dbc.Tab(label="Evoluzione delle componenti", tab_id="evolution"),
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
            options_list = df_data.columns[4:23]
            years_list = df_data['anno'].unique()
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
                    style={'height': '65vh'},
                    responsive=True
                )
            ])
        elif active_tab == "map_indicators":
            #return "Sezione ancora da creare."
            options_list = [f"{num}: {df_meta.loc[num]['nome']}" for num in df_meta.index]
            years_list = df_data['anno'].unique()
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
                    style={'height': '65vh'},
                    responsive=True
                )
            ])
        elif active_tab == "correlations":
            options_list = df_data.columns[4:23]
            years_list = df_data['anno'].unique()
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
                    style={'height': '65vh'},
                    responsive=True
                )
            ])
        elif active_tab == 'ranking':
            options_list = options_list = df_data.columns[4:23]
            years_list = df_data['anno'].unique()
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
            territories_list = df_data['territorio'].unique()
            options_list = df_data.columns[4:23]
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
                    id="evolution_plot",
                    style={'height': '65vh'},
                    responsive=True
                )
            ])
        elif active_tab == 'radar':
            territories_list = df_data['territorio'].unique()
            years_list = df_data['anno'].unique()
            return html.Div([
                dbc.Row([
                dbc.Col([
                html.P("Seleziona un territorio:"),
                dcc.Dropdown(
                    id='radar_territory',
                    options = territories_list ,
                    value = 'Italia',
                    style={"width": "75%"},
                    multi=True
                )]),
                dbc.Col([
                html.P("Seleziona un anno:"),
                dcc.Dropdown(
                    id='radar_year',
                    options = years_list ,
                    value = [years_list[0],years_list[-1]],
                    #style={"width": "75%"},
                    multi=True
                )],width=3)
                ]),
                dcc.Graph(
                    id="radar_chart",
                    style={'height': '65vh'},
                    responsive=True
                )
            ])
    return "Nessun elemento selezionato."

# Index map
@app.callback(
    Output("map", "figure"),
    Input("feature", "value"),
    Input('slider_year', 'value'))
def display_map_index(feature, year):
    df = df_data[df_data['area'].notna()]
    fig = px.choropleth_mapbox(df.loc[df['anno']==year], geojson=geo_data_file,
        locations='codice_istat', featureidkey="properties.istat_code_num",
        color=feature,
        range_color=[20,80],
        color_continuous_scale='RdYlGn',
        hover_name='territorio',
        hover_data={'codice_istat':False, 'anno': False,
                    'Generale': ':.3g', 'Contesto':':.3g', 'Bambini':':.3g', 'Donne':':.3g'},
        zoom=4.4, opacity=1, center=dict(lat=42, lon=12)
    )
    fig.update_layout(coloraxis_colorbar=dict(title="Punteggio", x=0.92))
    fig.update_layout(
        mapbox_style = map_style,
        mapbox_accesstoken = map_token,
        margin={"r":0,"t":30,"l":0,"b":0},
    )
    return fig
# Indicators map
@app.callback(
    Output("indicators_map", "figure"),
    Input("indicator", "value"),
    Input('slider_year', 'value'),
    Input('indicator_kind', 'value'))
def display_map_indicators(indicator, year, kind):
    indicator = indicator.split(":")[0]
    if df_meta.loc[int(indicator)]['inverted']=='yes':
        color_scale = 'RdYlGn_r'
        limits_scale = [df_meta.loc[int(indicator)]['best_value'], df_meta.loc[int(indicator)]['worst_value']]
    else:
        color_scale = 'RdYlGn'
        limits_scale = [df_meta.loc[int(indicator)]['worst_value'], df_meta.loc[int(indicator)]['best_value']]
    df = df_data.loc[df_data['anno']==year]
    if kind=='Dati':
        col = f'Indicatore {int(indicator)}'
        fig = px.choropleth_mapbox(df, geojson=geo_data_file,
            locations='codice_istat', featureidkey="properties.istat_code_num",
            color=col,
            range_color=limits_scale,
            color_continuous_scale=color_scale,
            hover_name='territorio',
            hover_data={'codice_istat':False, 'anno': False, col: ':.3g'},
            zoom=4.4, opacity=1, center=dict(lat=42, lon=12)
        )
        fig.update_layout(coloraxis_colorbar=dict(title=df_meta.loc[int(indicator)]['unità'], x=0.92))
    elif kind=='Punteggi':
        col = f"{df_meta.loc[int(indicator)]['sottoindice']}|{df_meta.loc[int(indicator)]['dimensione']}|{indicator}"
        fig = px.choropleth_mapbox(df.loc[df['anno']==year], geojson=geo_data_file,
            locations='codice_istat', featureidkey="properties.istat_code_num",
            color=col,
            range_color=[0,100],
            color_continuous_scale='RdYlGn',
            hover_name='territorio',
            hover_data={'codice_istat':False, 'anno': False, col: ':.3g'},
            zoom=4.4, opacity=1, center=dict(lat=42, lon=12)
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Punteggio", x=0.92))
    fig.update_layout(
        mapbox_style = map_style,
        mapbox_accesstoken = map_token,
        margin={"r":0,"t":30,"l":0,"b":0},
    )
    return fig

# Correlation
@app.callback(
    Output("dimensions_correlation", "figure"),
    Input('dimension_x', 'value'),
    Input('dimension_y', 'value'),
    Input('slider_year', 'value'))
def display_corr_dimensions(dimension_x, dimension_y,year):
    df = df_data[df_data['area'].notna()]
    fig = px.scatter(df.loc[df['anno']==year], x=dimension_x, y=dimension_y,
                 hover_name='territorio', color='area',
                 hover_data={'area':False, 'anno': False, dimension_x: ':.3g', dimension_y:':.3g'},
                 #range_x=[20,90], range_y=[20,90]
                 )
    fig.update_traces(marker={'size': 15})
    fig.update_layout(legend_title = 'Area')
    return fig

# Ranking
@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("slider_year", "value"))
def display_ranking(feature, year):
    df = df_data[df_data['area'].notna()].set_index('territorio')
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
    Output("evolution_plot", "figure"),
    Input("evolution_feature", "value"),
    Input("evolution_territory", "value"))
def display_evolution(features, territories):
    df = df_data.query("territorio == @territories").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
    df = pd.melt(df, id_vars=['Territorio', 'Anno'], value_vars=features, var_name='Indice/Dimensione', value_name='Punteggio')
    fig = px.line(df, x='Anno', y='Punteggio',
                hover_name='Territorio',
                color='Territorio',
                line_dash='Indice/Dimensione',
                hover_data={'Territorio':False},
                markers=True
        )
    #fig.update_traces(marker={'size': 8})
    fig.update_layout(
        legend_title = 'Territori, Componenti',
        xaxis = dict(tickvals = df['Anno'].unique()),
        yaxis = dict(title='Punteggio')
        )
    return fig

# Radar
@app.callback(
    Output("radar_chart", "figure"),
    Input("radar_territory", "value"),
    Input("radar_year", "value"))
def display_evolution(territories, year):
    features = df_data.columns[8:23]
    df = df_data.query("territorio == @territories and anno==@year").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
    df = pd.melt(df, id_vars=['Territorio', 'Anno'], value_vars=features, var_name='Indice/Dimensione', value_name='Punteggio')
    fig = px.line_polar(df, theta='Indice/Dimensione', r='Punteggio',
                        line_close=True, color='Territorio', line_dash='Anno',
                        range_r=[0,100],
                        start_angle=0,
                        hover_name='Territorio',
                        hover_data={'Territorio':False, 'Anno':True, 'Indice/Dimensione':True, 'Punteggio':True}
        )
    #fig.update_traces(fill='toself')

    return fig

#### Degug ####
if __name__ == "__main__":
    app.run(debug=True, port=8051)
