# render_data.py

import numpy as np
import plotly.express as px
import pandas as pd
import plotly.io as pio

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input, Output

from index import app
from index import metadata, data
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
    df = data[(data['area'].notna()) & (data['year']==year)].rename(columns={'year':'Year'})
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
    if metadata.loc[int(indicator)]['inverted']=='yes':
        colors = COLOR_SCALE[::-1]
        limits_scale = [metadata.loc[int(indicator)]['best_value'], metadata.loc[int(indicator)]['worst_value']]
    else:
        colors = COLOR_SCALE
        limits_scale = [metadata.loc[int(indicator)]['worst_value'], metadata.loc[int(indicator)]['best_value']]
    df = data.loc[data['year']==year].rename(columns={'year':'Year'})
    if kind=='Data':
        col = f'Indicator {int(indicator)} (data)'
        fig = px.choropleth_mapbox(df, geojson=GEO_FILE,
            locations='code', featureidkey="properties.ADM0_A3",
            color=col,
            range_color=limits_scale,
            color_continuous_scale=colors,
            hover_name='territory',
            hover_data={'code':False, 'Year': True, col: ':.3g'},
            zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=CENTER_COORDINATES[0])
        )
        fig.update_layout(coloraxis_colorbar=dict(title=metadata.loc[int(indicator)]['unit'], x=0.92, len=0.75))
    elif kind=='Scores':
        col = f'Indicator {int(indicator)}'
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
    Output("features_correlation", "figure"),
    Input('corr_x', 'value'),
    Input('corr_y', 'value'),
    Input('corr_pop', 'value'),
    Input('slider_year', 'value'))
def display_corr(x_data, y_data, population, year):
    df = data[(data['area'].notna()) & (data['year']==year)].rename(columns={'year':'Year', 'area':'Area'})
    x_data = x_data.split(":")[0] 
    y_data = y_data.split(":")[0]
    corr = df.corr('spearman', numeric_only=True)
    fig = px.scatter(df, x=x_data, y=y_data, size=population, color='Area', 
                     hover_name='territory', 
                     hover_data={'Area':False, 'Year': True, x_data: ':.3g', y_data:':.3g', population:':.3g'},
                     color_discrete_sequence=px.colors.qualitative.G10,
                     size_max = 50
    )
    #fig.update_traces(marker={'size': 15})
    fig.update_layout(title=f"Correlation coefficient: \u03c1\u209b = {corr.loc[x_data][y_data]:.3g}")
    #fig.update_xaxes(range=[-5, 105])
    #fig.update_yaxes(range=[-5, 105])    
    return fig

# Comparison
@app.callback(
    Output("comparison_chart", "figure"),
    Input('comp_x', 'value'),
    Input('comp_y', 'value'),
    Input('comp_pop', 'value'),
    Input('slider_year', 'value'))
def display_corr(x_data, y_data, population, year):
    df = data[(data['area'].notna()) & (data['year']==year)].rename(columns={'year':'Year', 'area':'Area'})
    #corr = df.corr('pearson', numeric_only=True)
    fig = px.scatter(df, x=x_data, y=y_data, size=population, color='Area', 
                     hover_name='territory', 
                     hover_data={'Area':False, 'Year': True, x_data: ':.3g', y_data:':.3g', population:':.3g'},
                     color_discrete_sequence=px.colors.qualitative.G10,
                     size_max = 50
    )

    if x_data == 'GDP per capita': fig.update_xaxes(type='log', ticksuffix=' $') #+  metadata.loc[101]['unit'])
    if y_data == 'GDP per capita': fig.update_yaxes(type='log', ticksuffix=' $') #+ metadata.loc[101]['unit'])
    return fig

# Ranking
@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("slider_year", "value"))
def display_ranking(feature, year):
    df = data[data['area'].notna()].set_index('code')
    years_list = data['year'].unique()
    final = df[df['year']==year][['territory', feature]]
    initial = df[df['year']==years_list[0]][['territory', feature]]

    initial['Rank'] = initial[feature].rank(ascending=False, method='min')
    final['Rank'] = final[feature].rank(ascending=False, method='min')
    
    final[f'Score change from {years_list[0]}'] = (final[feature] - initial[feature]).apply(sig_round)
    final[f'Rank change from {years_list[0]}'] = (initial['Rank'] - final['Rank'])

    final = final.reset_index().rename(columns={'territory':'Territory', feature:'Score'}).sort_values('Rank')
    rank_change_col = f'Rank change from {years_list[0]}'
    score_change_col = f'Score change from {years_list[0]}'
    final = final.set_index(['Rank', 'Territory'], drop=True)
    table = dbc.Table.from_dataframe(
                    final[['Score', score_change_col , rank_change_col]],
                    bordered=False,
                    hover=True,
                    responsive=True,
                    striped=True,
                    index = True
                )   
    return table

# Evolution
@app.callback(
    Output("evolution_plot", "figure"),
    Input("evolution_feature", "value"),
    Input("evolution_territory", "value"))
def display_evolution(component, territory):
    df = data.query("territory == @territory").rename(columns={'year':'Year', 'territory':'Territory'})
    if type(component) is list: component = [c.split(": ")[0] for c in component]
    else: component.split(": ")[0]
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=component, var_name='Component', value_name='Score')
    fig = px.line(df, x='Year', y='Score',
                hover_name='Territory',
                color='Territory',
                line_dash='Component',
                hover_data={'Territory':False},
                markers=True
        )
    fig.update_traces(marker={'size': 10})
    fig.update_layout(
        legend_title = 'Territory, Component',
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
    features = data.columns[8:23]
    df = data.query("territory == @territories and year==@year").rename(columns={'year':'Year', 'territory':'Territory'})
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
    features = data.columns[8:23].to_list()
    df = data.query("territory == @territories and year==@year").rename(columns={'year':'Year', 'territory':'Territory'})
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
    data = metadata.loc[int(indicator)]
    info = [indicator, 
            data['name'], 
            data['sub-index'],
            data['dimension'],
            data['definition'],
            data['unit'],
            data['last_update'],
            data['source'],
            data['source_link']
            ]
    return info
    
