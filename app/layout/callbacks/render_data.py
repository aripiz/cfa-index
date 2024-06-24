# render_data.py

import plotly.express as px
import pandas as pd
import plotly.io as pio

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input, Output

from index import app
from index import df_meta, df_data
from configuration import MAP_STYLE, MAP_TOKEN, GEO_FILE, FIGURE_TEMPLATE, COLOR_SCALE, TIER_BINS, TIER_LABELS
from utilis import sig_round

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

ZOOM_LEVEL = 4.3

# Features map
@app.callback(
    Output("map", "figure"),
    Input("feature", "value"),
    Input('slider_year', 'value'))
def display_map_index(feature, year):
    df = df_data[(df_data['area'].notna()) & (df_data['year']==year)].copy()
    df['Tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()

    fig = px.choropleth(df, #geojson=GEO_FILE,
        locations='code', #featureidkey="properties.istat_code_num",
        #color=feature,
        #range_color=[0,100],
        #color_continuous_scale=COLOR_SCALE,
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS,COLOR_SCALE)),
        category_orders={'Tier': TIER_LABELS},
        hover_name='name',
        hover_data={'code':False, 'year': False,
                    feature: ':.3g'},
        #zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=42, lon=12)
    )
    fig.update_layout(legend=dict(title_text="Livelli d'inclusione/esclusione",xanchor='right', yanchor='top', x=0.95, y=0.92))
    #fig.update_layout(coloraxis_colorbar=dict(title="Punteggio", x=0.92))
    fig.update_layout(
        #mapbox_style = MAP_STYLE,
        #mapbox_accesstoken = MAP_TOKEN,
        margin={"r":0,"t":0,"l":0,"b":0},
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
        colors = COLOR_SCALE[::-1]
        limits_scale = [df_meta.loc[int(indicator)]['best_value'], df_meta.loc[int(indicator)]['worst_value']]
    else:
        colors = COLOR_SCALE
        limits_scale = [df_meta.loc[int(indicator)]['worst_value'], df_meta.loc[int(indicator)]['best_value']]
    df = df_data.loc[df_data['year']==year].copy()
    if kind=='Dati':
        col = f'Indicator {int(indicator)}'
        # fig = px.choropleth(df, #geojson=GEO_FILE,
        #     locations='code', #featureidkey="properties.istat_code_num",
        #     color=col,
        #     range_color=limits_scale,
        #     color_continuous_scale=colors,
        #     hover_name='name',
        #     hover_data={'code':False, 'year': False, col: ':.3g'},
        #     #zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=42, lon=12)
        # )
        # fig.update_layout(coloraxis_colorbar=dict(title=df_meta.loc[int(indicator)]['unit'], x=0.92, len=0.75))
    elif kind=='Punteggi':
        col = f"{df_meta.loc[int(indicator)]['subindex']}|{df_meta.loc[int(indicator)]['dimension']}|{indicator}"
        fig = px.choropleth(df, #geojson=GEO_FILE,
            locations='code', #featureidkey="properties.istat_code_num",
            color=col,
            range_color=[0,100],
            color_continuous_scale=COLOR_SCALE,
            hover_name='name',
            hover_data={'code':False, 'year': False, col: ':.3g'},
            #zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=42, lon=12)
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Score", x=0.92,  len=0.75))
    fig.update_layout(
        #mapbox_style = MAP_STYLE,
        #mapbox_accesstoken = MAP_TOKEN,
        margin={"r":0,"t":0,"l":0,"b":0},
    )
    return fig

# Correlation
@app.callback(
    Output("dimensions_correlation", "figure"),
    Input('dimension_x', 'value'),
    Input('dimension_y', 'value'),
    Input('slider_year', 'value'))
def display_corr_dimensions(dimension_x, dimension_y,year):
    df = df_data[(df_data['area'].notna()) & (df_data['anno']==year)].copy()
    fig = px.scatter(df, x=dimension_x, y=dimension_y,
                 hover_name='territorio', color='area',
                 hover_data={'area':False, 'anno': False, dimension_x: ':.3g', dimension_y:':.3g'},
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
    fig.update_traces(marker={'size': 10})
    fig.update_layout(
        legend_title = 'Territori, Componenti',
        xaxis = dict(tickvals = df['Anno'].unique()),
        yaxis = dict(title='Punteggio')
        )
    return fig

# Radar chart
@app.callback(
    Output("radar_chart", "figure"),
    Input("radar_territory", "value"),
    Input("radar_year", "value"))
def display_radar(territories, year):
    features = df_data.columns[8:23]
    df = df_data.query("territorio == @territories and anno==@year").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
    df = pd.melt(df, id_vars=['Territorio', 'Anno'], value_vars=features, var_name='Dimensione', value_name='Punteggio')
    fig = px.line_polar(df, theta='Dimensione', r='Punteggio',
                        line_close=True, color='Territorio', line_dash='Anno',
                        range_r=[0,100],
                        start_angle=90,
                        hover_name='Territorio',
                        hover_data={'Territorio':False, 'Anno':True, 'Dimensione':True, 'Punteggio':True}
        )
    fig.update_polars(radialaxis=dict(angle=90, tickangle=90))
    return fig

# Radar table
@app.callback(
    Output("radar_table", "children"),
    Input("radar_territory", "value"),
    Input("radar_year", "value"))
def display_radar_table(territories, year):
    features = df_data.columns[8:23].to_list()
    df = df_data.query("territorio == @territories and anno==@year").rename(columns={'anno':'Anno', 'territorio':'Territorio'})
    df = pd.melt(df, id_vars=['Territorio', 'Anno'], value_vars=features, var_name='Dimensione', value_name='Punteggio').set_index(['Dimensione', 'Territorio', 'Anno']).unstack(['Territorio','Anno']).loc[features]
    table = dbc.Table.from_dataframe(
                    df,
                    bordered=False,
                    hover=True,
                    index=True,
                    responsive=True,
                    striped=True,
                )
    return table

# Indicators description
@app.callback(
    [Output("indicator_num", "children"),
     Output("indicator_name", "children"),
     Output("indicator_sub", "children"),
     Output("indicator_dim", "children"),
     Output("indicator_des", "children"),
     Output("indicator_unit", "children"),
     Output("indicator_update", "children"),
     Output("indicator_source", "children"),
     Output("indicator_source", "href"),
    ],
    Input("indicator", "value"))
def update_indicator_description(indicator):
    indicator = indicator.split(":")[0]
    data = df_meta.loc[int(indicator)]
    info = [indicator, 
            data['nome'], 
            data['sottoindice'],
            data['dimensione'],
            data['descrizione'],
            data['unità'],
            data['aggiornamento'],
            data['fonte'],
            data['link']
            ]
    return info
    
