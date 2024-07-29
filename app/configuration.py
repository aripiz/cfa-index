# configuration.py

# Title
TITLE = 'ChildFund Alliace Index 2024'

# Themes and colors
FIGURE_TEMPLATE = 'lux'
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
LAND_COLOR = "#3B3B3B"
OCEAN_COLOR = "hsl(0, 0, 88%)"
TIER_COLORS = ["#D53A50", "#E97B4E", "#F0B060", "#DECE58", "#64A972", "#3E876B"]

# Tiers
TIER_LABELS = ['Minimal', 'Limited', 'Basic', 'Moderate', 'Strong', 'Advanced']
#['Very severe exclusion', 'Severe exclusion', 'Insufficient inclusion', 'Sufficient inclusion', 'Good inclusion', 'Very good inclusion']
TIER_BINS = [0, 45, 55, 65, 75, 85, 100] 

# Mapbox 
import os
MAP_TOKEN = os.getenv("MAP_TOKEN")
if MAP_TOKEN is not None: MAP_STYLE = "mapbox://styles/aripiz/clf1ay30l004n01lnzi17hjvj"
else: MAP_STYLE = "carto-positron"
ZOOM_LEVEL = 0.9
CENTER_COORDINATES = (10 ,0)

# Files link
DATA_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/weworld-index2024_data.csv"
META_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/weworld-index2024_meta.csv"
GEO_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/ne_50m_admin_0_countries.geojson"
NOTES_FILE = ""
REPORT_FILE = ""