# render_scorecards.py

import numpy as np
import plotly.express as px
import pandas as pd
import plotly.io as pio
import geopandas as gpd

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input, Output

from index import app
from index import data, geodata
from configuration import TIER_LABELS, TIER_BINS, GEO_FILE, FIGURE_TEMPLATE, COLOR_SCALE

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

def area_centroid(countries):
    selected_countries = geodata[geodata['ADM0_A3'].isin(countries)]
    combined_geometry = selected_countries.unary_union
    return {'lat': combined_geometry.centroid.y, 'lon': combined_geometry.centroid.x}

areas = {area: data[data['area'] == area]['code'].dropna().unique().tolist() for area in data['area'].dropna().unique()}
areas['World'] = data['code'].unique().tolist()

centroids = {row['ADM0_A3']: {'lat': row['geometry'].centroid.y, 'lon': row['geometry'].centroid.x} for _, row in geodata.iterrows()}
centroids.update({k: area_centroid(v) for k,v in areas.items()})

# Scorecard title
@app.callback(
    Output("scorecard_header", "children"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_title(territory):
    return territory

# Scorecard map
@app.callback(
    Output("scorecard_map", "figure"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_map(territory):
    if territory in areas:
        df = data[(data['area']==territory)].rename(columns={'year':'Year', 'area':'Area'})
        lat, lon = centroids[territory].values()
    else:
        df = data[(data['territory']==territory)].rename(columns={'year':'Year', 'area':'Area'})
        lat, lon = centroids[df['code'].values[0]].values()
    fig = px.choropleth(df,
                               geojson=GEO_FILE,
                               locations='code', 
                               featureidkey="properties.ADM0_A3",
                               color_discrete_sequence = ["#005D9E"],
                               hover_name='territory',
                               hover_data={'code':False, 'Year': False, 'Area': False}
        )
    fig.update_layout(
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo = dict(projection_type='orthographic', projection_scale = 1, showland=True, showocean=True, oceancolor="hsl(0, 0, 88%)")
    )
    if territory == 'World': 
        fig.update_layout(geo = dict(center=dict(lat=0, lon=0), projection_rotation=dict(lat=0, lon=0), landcolor="#005D9E"))
    else: 
        fig.update_layout(geo = dict(center=dict(lat=lat, lon=lon), projection_rotation=dict(lat=lat, lon=lon)))
    return fig

# Scorecard summary
@app.callback(
    Output("scorecard_area", "children"),
    Output("scorecard_pop", "children"),
    Output("scorecard_gdp", "children"),
    Output("scorecard_score", "children"),
    Output("scorecard_rank", "children"),
    Output("scorecard_group", "children"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_summary(territory):
    df_territory = data.set_index(['territory','year']).loc[territory, 2023]
    df_all = data[data['area'].notna()].set_index(['territory','year']) 
    df_all['rank'] = df_all.loc(axis=0)[:,2023]["CFA Index"].rank(ascending=False, method='min')
    df_all['tier'] = pd.cut(df_all.loc(axis=0)[:,2023]["CFA Index"], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()

    info = [
        f"{df_territory['area']}",
        f"{df_territory['Population, total']:.3g}",
        f"{df_territory['GDP per capita']:.3g} $",
        f"{df_territory['CFA Index']}/100",
        f"{df_all.loc[territory, 2023]['rank']:.0f}/157",
        f"{df_all.loc[territory, 2023]['tier']}",
    ]
    return info

# Scorecard progress
@app.callback(
    Output("scorecard_progress", "figure"),
    Input("scorecard_territory", "value"))
def display_evolution(territory):
    area = data.query("territory == @territory")['area'].to_list()[0]
    if territory != "World": territory = [territory, area, 'World']

    df = data.query("territory == @territory").rename(columns={'year':'Year', 'territory':'Territory'})
    fig = px.line(df, x='Year', y='CFA Index',
                hover_name='Territory',
                color='Territory',
                hover_data={'Territory':False},
                markers=True
        )
    fig.update_traces(marker={'size': 10})
    fig.update_layout(
        legend_title = 'Territory',
        xaxis = dict(tickvals = df['Year'].unique()),
        )
    return fig

# Scorecard radar
@app.callback(
    Output("scorecard_radar", "figure"),
    Input("scorecard_territory", "value"))
def display_radar(territory):
    features = data.columns[8:23]
    area = data.query("territory == @territory")['area'].to_list()[0]
    if territory != "World": territory = [territory, area, 'World']
    df = data.query("territory == @territory and year == 2023").rename(columns={'territory':'Territory'})
    df = pd.melt(df, id_vars=['Territory'], value_vars=features, var_name='Dimension', value_name='Score')
    label_map = {f: f.replace(' ', '<br>') for f in features}
    df['Dimension'] = df['Dimension'].map(label_map)
    fig = px.line_polar(df, theta='Dimension', r='Score',
                        line_close=True,
                        color='Territory', 
                        range_r=[0,100],
                        start_angle=90,
                        hover_name='Territory',
                        hover_data={'Territory':False, 'Dimension':True, 'Score':True}
        )
    fig.update_polars(radialaxis=dict(angle=90, tickangle=90))
    return fig
