# layout_home.py

import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from dash import dcc, html

from index import data
from configuration import BRAND_LINK, MAP_STYLE, MAP_TOKEN, GEO_FILE, FIGURE_TEMPLATE, TIER_COLORS, TIER_BINS, TIER_LABELS, ZOOM_LEVEL, CENTER_COORDINATES, OCEAN_COLOR
load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Home map
def display_map():
    year = 2023.
    feature = 'CFA Index' 
    df = data[(data['area'].notna()) & (data['year']==year)].rename(columns={'year':'Year', 'area':'Area'})
    df['Tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()


    # fig = px.choropleth_mapbox(df, geojson=GEO_FILE,
    #     locations='code', featureidkey="properties.ADM0_A3",
    #     #color=feature,
    #     #range_color=[0,100],
    #     #color_continuous_scale=TIER_COLORS,
    #     color='Tier',
    #     color_discrete_map=dict(zip(TIER_LABELS,TIER_COLORS)),
    #     category_orders={'Tier': TIER_LABELS},
    #     #hover_name='territory',
    #     #hover_data={'code':False, 'Year': True,          feature: ':.3g'},
    #     zoom=ZOOM_LEVEL, opacity=1, center=dict(lat=CENTER_COORDINATES[0]),
    #     custom_data = ['territory', 'Area', feature, 'Tier', 'Year']

    # )
    
    fig = px.choropleth(df, geojson=GEO_FILE,
        locations='code', featureidkey="properties.ADM0_A3",
        #color=feature,
        #range_color=[0,100],
        #color_continuous_scale=TIER_COLORS,
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS,TIER_COLORS)),
        category_orders={'Tier': TIER_LABELS},
        #hover_name='territory',
        #hover_data={'code':False, 'Year': True,          feature: ':.3g'},
        custom_data = ['territory', 'Area', feature, 'Tier', 'Year']

    )
    fig.update_layout(legend=dict(title_text="Human Rights Implementation", xanchor='right', yanchor='top', x=0.95, y=0.92))
    fig.update_layout(coloraxis_colorbar=dict(title="Score", x=0.92))
    template = "<b>%{customdata[0]}</b><br>" + "<i>%{customdata[1]}</i><br><br>" + f"{feature}: "+ "%{customdata[2]:#.3g}<br>" + f"Human Rights Implementation: " + "%{customdata[3]}<br><br>" + f"Year: "+ "%{customdata[4]}" + "<extra></extra>"
    fig.update_traces(hovertemplate=template)
    
    # fig.update_layout(
    #         mapbox_style = MAP_STYLE,
    #         mapbox_accesstoken = MAP_TOKEN,
    #         margin={"r":0,"t":0,"l":0,"b":0},
    #         mapbox_bounds=dict(west=-180, east=180, south=-85, north=85)
    #     )
    fig.update_layout(
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo = dict(projection_type='natural earth', showland=True, showocean=True, oceancolor=OCEAN_COLOR,  showframe=False,  projection_scale=1.0, scope='world'),
    )
    return fig

home = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.H1("ChildFund Alliance Index"),
            html.Div(["The ChildFund Alliance Index is a flagship report by ", html.A("ChildFund Alliance", href=BRAND_LINK), ". Formerly known as the WeWorld Index and published annually since 2015 by WeWorld - the Italian member of ChildFund Alliance - CFA Index is a tool to measure the living conditions of women and children worldwide by assessing the promotion, exercise, and violation of their rights."])
        ],  lg = 12, xs = 12 ),
        className='mt-2', justify='around' ),
    dbc.Row(
        dbc.Col(
        dcc.Graph(figure=display_map(), config = {'displayModeBar': False, 'editable':False}), lg = 12, xs = 12),
        className='mt-2', justify='around'),
    dbc.Row(
        dbc.Col([
            html.H4("About ChildFund Alliance"),
            html.P("Eleven child-focused development and humanitarian agencies are part of the global ChildFund Alliance network, which helps children and their families overcome poverty and the underlying conditions that prevent children from reaching their full potential. Together we reach nearly 36 million children and family members in 70 countries. Members work to end violence and exploitation against children; provide expertise in emergencies and disasters to ease the harmful impact on children and their communities; and engage children, families and communities to create lasting change.")
        ], lg = 12, xs = 12),
        className='mt-4', justify='around' ),

])