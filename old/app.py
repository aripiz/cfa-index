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
            options_list = df_data.columns[4:23]
            return html.Div([
                html.P("Seleziona un Indice/Dimensione:"),
                dcc.Dropdown(
                    id='feature',
                    options=options_list,
                    value=options_list[0],
                    style={"width": "60%"}
                ),
                dcc.Graph(
                    id="map",
                    style={'width': '90vw', 'height': '70vh'}
                )
            ])
        elif active_tab == "map_indicators":
            #return "Sezione ancora da creare."
            options_list = [f"{num}: {df_meta.loc[num]['nome']}" for num in df_meta.index]
            return html.Div([
                html.P("Seleziona un indicatore:"),
                dcc.Dropdown(
                    id='indicator',
                    options = options_list ,
                    value=options_list[0],
                    style={"width": "80%"}
                ),
                dcc.Graph(
                    id="indicators_map",
                    style={'width': '90vw', 'height': '70vh'}
                    #responsive=True
                )
            ])
        elif active_tab == "correlations":
            options_list = df_data.columns[4:23]
            return html.Div([
                html.P("Seleziona due Indici/Dimensioni da confrontare:"),
                dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id="dimension_x",
                    options = options_list,
                    value=options_list[0],
                    style={"width": "75%"}
                )),
                dbc.Col(dcc.Dropdown(
                    id='dimension_y',
                    options = options_list ,
                    value = options_list[1],
                    style={"width": "75%"}
                ))]),
                dcc.Graph(
                    id="dimensions_correlation",
                    style={'width': '90vw', 'height': '70vh'}
                    #responsive=True
                ),
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
                dcc.Dropdown(
                    id='ranking_year',
                    options = years_list ,
                    value = years_list[-1],
                    style={"width": "75%"}
                )])]),
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
                    id="evolution",
                    style={'width': '90vw', 'height': '70vh'}
                    #responsive=True
                )
            ])
    return "Nessun elemento selezionato."

# Index map
@app.callback(
    Output("map", "figure"),
    Input("feature", "value"))
def display_map_index(feature):
    df = df_data[df_data['area'].notna()]
    fig = px.choropleth(df, geojson=geo_data_file,
        locations='codice_istat', featureidkey="properties.istat_code_num",
        projection='natural earth', animation_frame='anno', animation_group='codice_istat',
        color=feature,
        range_color=[20,80],
        color_continuous_scale='RdYlGn',
        hover_name='territorio',
        hover_data={'codice_istat':False, 'anno': False,
                    'Generale': ':.3g', 'Contesto':':.3g', 'Bambini':':.3g', 'Donne':':.3g'},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Punteggio"),
        sliders = [dict(len=0.25, active= 4, x=0.5,xanchor='center', currentvalue= {"prefix": "Anno: "})],
    )
    fig["layout"].pop("updatemenus")
    return fig

# Indicators map
@app.callback(
    Output("indicators_map", "figure"),
    Input("indicator", "value"))
def display_map_indicators(indicator):
    indicator = indicator.split(":")[0]
    if df_meta.loc[int(indicator)]['inverted']=='yes':
        color_scale = 'RdYlGn_r'
        limits_scale = [df_meta.loc[int(indicator)]['best_value'], df_meta.loc[int(indicator)]['worst_value']]
    else:
        color_scale = 'RdYlGn'
        limits_scale = [df_meta.loc[int(indicator)]['worst_value'], df_meta.loc[int(indicator)]['best_value']]
    df = df_data
    fig = px.choropleth(df, geojson=geo_data_file,
        locations='codice_istat', featureidkey="properties.istat_code_num",
        projection='natural earth', animation_frame='anno', animation_group='codice_istat',
        color=indicator,
        labels={indicator: f'Indicatore {indicator}'},
        range_color=limits_scale,
        color_continuous_scale=color_scale,
        hover_name='territorio',
        hover_data={'codice_istat':False, 'anno': False,
                    indicator: ':.3g'},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title=df_meta.loc[int(indicator)]['unità']),
        sliders = [dict(len=0.25, active= 4, x=0.5,xanchor='center', currentvalue= {"prefix": "Anno: "})]
    )
    fig["layout"].pop("updatemenus")
    return fig

# Dimension map
@app.callback(
    Output("dimensions_map", "figure"),
    Input("dimension", "value"))
def display_map_dimensions(dimension):
    fig = px.choropleth(df_data, geojson=geo_data_file,
        locations='codice_istat', featureidkey="properties.istat_code_num",
        projection='natural earth', animation_frame='anno', animation_group='codice_istat',
        color=dimension,
        range_color=[0,100],
        color_continuous_scale='RdYlGn',
        hover_name='territorio',
        hover_data={'codice_istat':False, 'anno': False,
                    dimension: ':.3g'},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title='Punteggio'),
        sliders = [dict(len=0.25, active= 4, x=0.5,xanchor='center', currentvalue= {"prefix": "Anno: "})]
    )
    fig["layout"].pop("updatemenus")
    return fig

# Correlation
@app.callback(
    Output("dimensions_correlation", "figure"),
    Input('dimension_x', 'value'),
    Input('dimension_y', 'value'))
def display_corr_dimensions(dimension_x, dimension_y):
    df = df_data[df_data['area'].notna()]
    fig = px.scatter(df, x=dimension_x, y=dimension_y,
                 hover_name='territorio', color='area', animation_frame='anno', animation_group='territorio',
                 hover_data={'area':False, 'anno': False, dimension_x: ':.3g', dimension_y:':.3g'},  range_x=[10,90], range_y=[10,90])
    fig.update_traces(marker={'size': 15})
    fig.update_layout(
        legend_title = 'Area',
        sliders = [dict(len=0.25, active= 4, x=0.5,xanchor='center', currentvalue= {"prefix": "Anno: "})]
    )
    fig["layout"].pop("updatemenus")
    return fig

# Ranking
@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("ranking_year", "value"))
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
    Output("evolution", "figure"),
    Input("evolution_feature", "value"),
    Input("evolution_territory", "value"))
def display_evolution(features, territories):
    df = df_data.query("territorio == @territories").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
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
