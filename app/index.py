# index.py

from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd

from configuration import DATA_FILE, META_FILE, TITLE, DBC_CSS

# Loading data
df_data = pd.read_csv(DATA_FILE)
df_meta = pd.read_csv(META_FILE, index_col=0)

# App 
app = Dash(
    __name__, 
    title=TITLE,
    external_stylesheets=[DBC_CSS], 
    suppress_callback_exceptions=True, 
    use_pages=True,
    )

# Google Analytics 
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-1348DFKDC1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-1348DFKDC1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""