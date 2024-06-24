# utilis.py

import numpy as np

# Significant figures rounding
def sig_round(x, precision=3):
    return np.float64(f'{x:.{precision}g}')