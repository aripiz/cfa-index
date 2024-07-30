# layout_home.py

import imp
import dash_bootstrap_components as dbc
from dash import dcc, html

import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from index import data
from configuration import GEO_FILE, FIGURE_TEMPLATE, TIER_COLORS, TIER_BINS, TIER_LABELS, OCEAN_COLOR, BRAND_LINK
load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Home map
def display_map():
    year = 2023
    feature = 'CFA Index' 
    df = data[(data['area'].notna()) & (data['year']==year)].rename(columns={'year':'Year', 'area':'Area'})
    df['Tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()
    fig = px.choropleth(df, geojson=GEO_FILE,
        locations='code', featureidkey="properties.ADM0_A3",
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS,TIER_COLORS)),
        category_orders={'Tier': TIER_LABELS},
        custom_data = ['territory', 'Area', feature, 'Tier', 'Year']
    )
    fig.update_layout(legend=dict(title_text="Human Rights Implementation", xanchor='right', yanchor='top', x=0.95, y=0.92))
    fig.update_layout(coloraxis_colorbar=dict(title="Score", x=0.92))
    template = "<b>%{customdata[0]}</b><br>" + "<i>%{customdata[1]}</i><br><br>" + f"{feature}: "+ "%{customdata[2]:#.3g}/100<br>" + f"Human Rights Implementation: " + "%{customdata[3]}<br><br>" + f"Year: "+ "%{customdata[4]}" + "<extra></extra>"
    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo = dict(projection_type='natural earth', showland=True, showocean=True, oceancolor=OCEAN_COLOR,  showframe=False,  projection_scale=1.0, scope='world'),
    )
    return fig

# Text
opening_text = f'''
The **ChildFund Alliance Index** is a flagship report by [ChildFund Alliance]({BRAND_LINK}). It is a tool designed to **measure the living conditions of women and children worldwide** by assessing the promotion, exercise, and violation of their rights. CFA Index is formerly known as the WeWorld Index and published annually since 2015 by WeWorld, the Italian member of ChildFund Alliance.
'''
description_text = '''
CFA Index ranks **157 countries** from 2015 to 2023 combining **30 different indicators.** The Index consists of an absolute 0-100 score aiming at inquiring the implementation of human rights for children and women at the country, regional area and world level.

Explore the dashboard for more details:

- **[Data](/data):** Access detailed data that make up the Index, with the ability to view interactive maps and charts.
- **[Scorecards](/scorecards):** Country scorecards showing scores and rankings based on various indicators.
- **[Methodology](/methodology):** Description of the methodology used to collect and analyze data.

Navigate through these sections to better understand the impact of the ChildFund Alliance Index and discover how the rights of women and children are promoted, exercised, and violated in different countries. All resources, including full reports and datasets, are available to download.
'''

about_text = '''
Eleven child-focused development and humanitarian agencies are part of the global ChildFund Alliance network, which helps children and their families overcome poverty and the underlying conditions that prevent children from reaching their full potential. Together we reach nearly 36 million children and family members in 70 countries. Members work to end violence and exploitation against children; provide expertise in emergencies and disasters to ease the harmful impact on children and their communities; and engage children, families and communities to create lasting change.
'''

# Structure
home = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.H1("ChildFund Alliance Index"),
            dcc.Markdown(opening_text, className='my-4'),
            dcc.Graph(figure=display_map(), config={'displayModeBar': False, 'editable': False}, className='my-4', id='map_home'),
            dcc.Markdown(description_text, className='my-4'),
        ], lg=12, xs=12),
        className='mt-2', justify='around'
    ),
    dbc.Row(
        dbc.Col([
            html.H4("About ChildFund Alliance"),
            dcc.Markdown(about_text)
        ], lg = 12, xs = 12),
        className='mt-4', justify='around'
    ),
])