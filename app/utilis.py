# utilis.py

import numpy as np

# Significant figures rounding
def sig_round(x, precision=3):
    return np.float64(f'{x:.{precision}g}')

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