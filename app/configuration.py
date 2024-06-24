# configuration.py

# Title
TITLE = 'WeWorld Index 2024'

# Themes and colors
FIGURE_TEMPLATE = 'zephyr'
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
COLOR_SCALE = ["#D53A50", "#E97B4E", "#F0B060", "#DECE58", "#64A972", "#3E876B"]

# Tiers
TIER_LABELS = ['Very severe exclusion', 'Severe exclusion', 'Insufficient inclusion', 'Sufficient inclusion', 'Good inclusion', 'Very good inclusion']
TIER_BINS = [0, 45, 55, 65, 75, 85, 100] 

# Mapbox 
import os
MAP_TOKEN = os.getenv("MAP_TOKEN")
if MAP_TOKEN is not None: MAP_STYLE = "mapbox://styles/aripiz/clf1ay30l004n01lnzi17hjvj"
else: MAP_STYLE = "carto-positron"

# Files link
DATA_FILE = "../Data/index2024_data.csv"
META_FILE = "../Data/index2024_meta.csv"

#DATA_FILE = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/maipiuinvisibili2023_data.csv"
#META_FILE = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/maipiuinvisibili2023_metadata.csv"
GEO_FILE = "https://raw.githubusercontent.com/aripiz/weworld-maipiuinvisibili2023/master/data/italy_regions_low.json"
NOTES_FILE = "https://github.com/aripiz/weworld-maipiuinvisibili2023/raw/master/data/WeWorld-MaiPi%C3%B9Invisibili-2023_NoteTecniche.pdf"
REPORT_FILE = "https://github.com/aripiz/weworld-maipiuinvisibili2023/raw/master/data/WeWorld-MaiPi%C3%B9Invisibili-2023_Rapporto.pdf"