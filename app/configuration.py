# configuration.py

# Main properties
TITLE = 'ChildFund Alliace Index 2024'
BRAND_LINK = "https://childfundalliance.org/"
CREDITS_LINK = "https://github.com/aripiz"

TEMPLATE = 'lux'

# Themes and colors
TEMPLATE_CSS = f"https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/{TEMPLATE}/bootstrap.min.css"
FIGURE_TEMPLATE = TEMPLATE.lower()
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

LAND_COLOR = "#3B3B3B"
OCEAN_COLOR = "hsl(0, 0, 88%)"
TIER_COLORS = ["#D53A50", "#E97B4E", "#F0B060", "#DECE58", "#64A972", "#3E876B"]
SEQUENCE_COLOR = [
    "#3c3c3c",  # Grigio scuro
    "#d55350",  # Rosso corallo
    "#41c072",  # Verde smeraldo
    "#ffc15f",  # Giallo chiaro
    "#439acf",  # Blu cielo
    "#7b4c39",  # Marrone caldo
    "#a64d79",  # Rosa scuro
    "#2e8b57",  # Verde bosco
    "#ff6f00",  # Arancione vivace
    "#1e90ff"   # Blu dodger
]

# Tiers
TIER_LABELS = ['Minimal', 'Limited', 'Basic', 'Moderate', 'Strong', 'Advanced']
TIER_BINS = [0, 45, 55, 65, 75, 85, 100] 

# Mapbox 
import os
MAP_TOKEN = os.getenv("MAP_TOKEN")
if MAP_TOKEN is not None: MAP_STYLE = "mapbox://styles/aripiz/clf1ay30l004n01lnzi17hjvj"
else: MAP_STYLE = "carto-positron"
ZOOM_LEVEL = 0.9
CENTER_COORDINATES = (13 ,5)

# Files link
DATA_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/weworld-index2024_data.csv"
META_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/weworld-index2024_meta.csv"
GEO_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/ne_50m_admin_0_countries.geojson"
NOTES_FILE = "https://raw.githubusercontent.com/aripiz/weworld-index2024/main/data/ChildFundAlliance-Index-2024_TechnicalNotes.pdf"
REPORT_FILE = ""