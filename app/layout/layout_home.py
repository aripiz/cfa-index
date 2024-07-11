# layout_home.py

import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from index import data
from configuration import MAP_STYLE, MAP_TOKEN, GEO_FILE, FIGURE_TEMPLATE, COLOR_SCALE, TIER_BINS, TIER_LABELS
load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Home map
def display_map_home():
    df = data[data['area'].notna()].copy()
    df['Tier'] = pd.cut(df['General'], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()
    fig = px.choropleth(df.loc[df['year']==2023], #geojson=GEO_FILE,
        locations='code', #featureidkey="properties.istat_code_num",
        color='Tier',
        #range_color=[20,80],
        color_discrete_map=dict(zip(TIER_LABELS,COLOR_SCALE)),
        category_orders={'Tier': TIER_LABELS},
        hover_name='territory',
        hover_data={'code':False, 'year': False,
                    'General': ':.3g', 'Context':':.3g', 'Children':':.3g', 'Women':':.3g'},
        #zoom=4.5, opacity=1, center=dict(lat=42, lon=12)
    )
    fig.update_layout(legend=dict(title_text="Livelli d'inclusione/esclusione",xanchor='right', yanchor='top', x=0.95, y=0.92))
    fig.update_layout(
        #mapbox_style = MAP_STYLE,
        #mapbox_accesstoken = MAP_TOKEN,
        margin={"r":0,"t":0,"l":0,"b":0},
    )
    return fig