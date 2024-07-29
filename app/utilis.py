# utilis.py

import numpy as np
import pandas as pd
from dash import html

# Significant figures rounding
def sig_round(x, precision=3):
    return np.float64(f'{x:#.{precision}g}')

def sig_format(x, precision=3):
    if pd.isna(x): return "N/A"
    else: return f'{np.float64(x):#.{precision}g}'

def style_score_change_col(value, equal_buffer = 1.5):
    if -equal_buffer <= value <= equal_buffer:
        return {'backgroundColor': '#fff3cd', 'color': '#856404'}  # Giallo per valori tra -1 e 1
    elif value > equal_buffer:
        return {'backgroundColor': '#d4edda', 'color': '#155724'}  # Verde per valori positivi
    elif value < -equal_buffer:
        return {'backgroundColor': '#f8d7da', 'color': '#721c24'}  # Rosso per valori negativi

def style_rank_change_col(value):
    if value > 0:
        return {'backgroundColor': '#d4edda', 'color': '#155724'}  # Verde per miglioramenti di rank
    elif value < 0:
        return {'backgroundColor': '#f8d7da', 'color': '#721c24'}  # Rosso per peggioramenti di rank
    elif value == 0:
        return {'backgroundColor': '#fff3cd', 'color': '#856404'}  # Giallo per nessun cambiamento
    
# Funzione per determinare la freccia colorata
def get_score_change_arrow(value, equal_buffer = 1.5):
    if -equal_buffer <= value <= equal_buffer:
       return html.Span(className='arrow-right')
    elif value > equal_buffer:
        return html.Span(className='arrow-up')
    elif value < -equal_buffer:
        return html.Span(className='arrow-down')
    
def area_centroid(geodata, countries):
    selected_countries = geodata[geodata['ADM0_A3'].isin(countries)]
    combined_geometry = selected_countries.unary_union
    return {'lat': combined_geometry.centroid.y, 'lon': combined_geometry.centroid.x}


def get_value(dataframe, key, format_string, divide=1, default="N/A"):
    try:
        value = dataframe[key]
        if pd.isna(value):
            return default
        if divide != 1:
            value = value / divide
        return format_string.format(value)
    except (KeyError, TypeError, ValueError):
        return default