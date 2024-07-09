# render_data.py

import numpy as np
import plotly.express as px
import pandas as pd
import plotly.io as pio

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input, Output

from index import app
from index import df_meta, df_data
from configuration import CENTER_COORDINATES, MAP_STYLE, MAP_TOKEN, GEO_FILE, FIGURE_TEMPLATE, COLOR_SCALE, TIER_BINS, TIER_LABELS, ZOOM_LEVEL
from utilis import sig_round

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Features map
@app.callback(
    Output("map", "figure"),
    Input("feature", "value"),
    Input('slider_year', 'value'))
def display_map_index(feature, year):
    df = df_data[(df_data['area'].notna()) & (df_data['year']==year)].rename(columns={'year':'Year'})
    df['Tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()
    fig = px.choropleth_mapbox(df, geojson=GEO_FILE,
        locations='code', featureidkey="properties.ADM0_A3",
        #color=feature,
        #range_color=[0,100],
        #color_continuous_scale=COLOR_SCALE,
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS,COLOR_SCALE)),
        category_orders={'Tier': TIER_LABELS},
        hover_name='territory',
        hover_data={'code':False, 'Year': True,
                    feature: ':.3g'},
        zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=CENTER_COORDINATES[0])
    )
    fig.update_layout(legend=dict(title_text="Human Rights Implementation",xanchor='right', yanchor='top', x=0.95, y=0.92))
    fig.update_layout(coloraxis_colorbar=dict(title="Score", x=0.92))
    fig.update_layout(
        mapbox_style = MAP_STYLE,
        mapbox_accesstoken = MAP_TOKEN,
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
    df = df_data.loc[df_data['year']==year].rename(columns={'year':'Year'})
    if kind=='Data':
        col = f'Indicator {int(indicator)}'
        fig = px.choropleth_mapbox(df, geojson=GEO_FILE,
            locations='code', featureidkey="properties.ADM0_A3",
            color=col,
            range_color=limits_scale,
            color_continuous_scale=colors,
            hover_name='territory',
            hover_data={'code':False, 'Year': True, col: ':.3g'},
            zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=CENTER_COORDINATES[0])
        )
        fig.update_layout(coloraxis_colorbar=dict(title=df_meta.loc[int(indicator)]['unit'], x=0.92, len=0.75))
    elif kind=='Scores':
        col = f"Component {indicator}"
        fig = px.choropleth_mapbox(df, geojson=GEO_FILE,
            locations='code', featureidkey="properties.ADM0_A3",
            color=col,
            range_color=[0,100],
            color_continuous_scale=COLOR_SCALE,
            hover_name='territory',
            hover_data={'code':False, 'Year': True, col: ':.3g'},
            zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=CENTER_COORDINATES[0])
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Score", x=0.92,  len=0.75))
    fig.update_layout(
        mapbox_style = MAP_STYLE,
        mapbox_accesstoken = MAP_TOKEN,
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
    df = df_data[(df_data['area'].notna()) & (df_data['year']==year)].rename(columns={'year':'Year'})
    fig = px.scatter(df, x=dimension_x, y=dimension_y,
                 hover_name='territory', color='area',
                 hover_data={'area':False, 'Year': True, dimension_x: ':.3g', dimension_y:':.3g'},
                 color_discrete_sequence=px.colors.qualitative.G10
                 )
    fig.update_traces(marker={'size': 15})
    fig.update_layout(legend_title = 'Area')
    fig.update_xaxes(range=[0, 105])
    fig.update_yaxes(range=[0, 105])
    
    return fig

# Ranking
@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("slider_year", "value"))
def display_ranking(feature, year):
    df = df_data[df_data['area'].notna()].set_index('code')
    years_list = df_data['year'].unique()
    final = df[df['year']==year][['territory', feature]]
    initial = df[df['year']==years_list[0]][['territory', feature]]
    final['Rank'] = final[feature].rank(ascending=False, method='min')
    final[f'Change since {years_list[0]}'] = (final[feature]-initial[feature]).apply(sig_round)
    final = final.reset_index().rename(columns={'territory':'Territory', feature:'Score'}).sort_values('Rank')
    table = dbc.Table.from_dataframe(
                    final[['Rank', 'Territory', 'Score', f'Change since {years_list[0]}']],
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
    df = df_data.query("territory == @territories").rename(columns={'year':'Year', 'territory':'Territory'})
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=features, var_name='Sub-index/Dimension', value_name='Score')
    fig = px.line(df, x='Year', y='Score',
                hover_name='Territory',
                color='Territory',
                line_dash='Sub-index/Dimension',
                hover_data={'Territory':False},
                markers=True
        )
    fig.update_traces(marker={'size': 10})
    fig.update_layout(
        legend_title = 'Territories, Components',
        xaxis = dict(tickvals = df['Year'].unique()),
        yaxis = dict(title='Score')
        )
    return fig

# Radar chart
@app.callback(
    Output("radar_chart", "figure"),
    Input("radar_territory", "value"),
    Input("radar_year", "value"))
def display_radar(territories, year):
    features = df_data.columns[8:23]
    df = df_data.query("territory == @territories and year==@year").rename(columns={'year':'Year', 'territory':'Territory'})
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=features, var_name='Dimension', value_name='Score')
    fig = px.line_polar(df, theta='Dimension', r='Score',
                        line_close=True,
                        color='Territory', 
                        line_dash='Year',
                        range_r=[0,100],
                        start_angle=90,
                        hover_name='Territory',
                        hover_data={'Territory':False, 'Dimension':True, 'Score':True}
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
    df = df_data.query("territory == @territories and year==@year").rename(columns={'year':'Year', 'territory':'Territory'})
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=features, var_name='Dimension', value_name='Score').set_index(['Dimension', 'Territory', 'Year']).unstack(['Territory','Year']).loc[features]
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
            data['name'], 
            data['subindex'],
            data['dimension'],
            data['definition'],
            data['unit'],
            data['last_update'],
            data['source'],
            data['source_link']
            ]
    return info
    
