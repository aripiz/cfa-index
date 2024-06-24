# home.py

from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, path='/', name=TITLE)

from layout.layout_home import display_map_home

layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Markdown(
                "In un mondo in cui le diseguaglianze permangono e la povertà è ancora un problema globale, donne, bambini, bambine e adolescenti sono ovunque le categorie di persone più a rischio di esclusione sociale. Per questo, il primo obiettivo di WeWorld è la **promozione del diritto all’inclusione di donne, bambini e giovani in Italia e nel mondo.**"),
                dcc.Markdown(
                "Condizione imprescindibile per realizzare azioni di inclusione e proporre politiche sociali è conoscere il più possibile le loro condizioni di vita e i rischi di emarginazione sociale a cui vanno incontro. L’Indice biennale **_Mai più invisibili_ sulla condizione di donne, bambini e adolescenti in Italia**, pubblicato per la prima volta nel 2020, **nasce dall’esigenza di valutare in quali ambiti vi sono forme di inclusione/esclusione a livello regionale.**"),
                dcc.Markdown(
                "L’Italia viene monitorata nella sua capacità di garantire e promuovere i diritti di queste categorie sociali attraverso una serie di **30 Indicatori**, raggruppati in **15 Dimensioni**, a loro volta divise in **3 Sottoindici**: Contesto, Bambini e Donne che aggregati forniscono un **Indice generale.**"), 
                dbc.Card(dcc.Markdown(
                """
                **L’Indice _Mai più invisibili_** è uno strumento che:
                - **Valuta il progresso dei territori** alla luce delle condizioni di inclusione che riescono a garantire alle categorie più vulnerabili: donne, bambini e adolescenti.
                - **Tiene conto delle condizioni di donne e minori in maniera congiunta**, interdipendente e simultanea, riconoscendo un nesso tra l’implementazione dei diritti di una categoria sul benessere dell’altra e viceversa.
                - **Considera il concetto di inclusione al di là di un’accezione dello sviluppo puramente economicistica,** aprendo a una visione ampia, multidimensionale, dinamica e positiva, personale, sociale e intersezionale, universale.
                """), body=True)
            ], lg = 6, xs = 12),
            dbc.Col(dcc.Graph(figure=display_map_home(), responsive=True, style ={"height":"80vh"}), lg = 6, xs = 12, align='top')        
        ],
        justify='evenly'),
    ])


        #    dbc.ListGroup([
        #             dbc.ListGroupItem(dcc.Markdown("**Valuta il progresso dei territori** alla luce delle condizioni di inclusione che riescono a garantire alle categorie più vulnerabili: donne, bambini e adolescenti.")),
        #             dbc.ListGroupItem(dcc.Markdown("**Tiene conto delle condizioni di donne e minori in maniera congiunta**, interdipendente e simultanea, riconoscendo un nesso tra l’implementazione dei diritti di una categoria sul benessere dell’altra e viceversa.")), 
        #             dbc.ListGroupItem(dcc.Markdown("**Considera il concetto di inclusione al di là di un’accezione dello sviluppo puramente economicistica,** aprendo a una visione ampia, multidimensionale, dinamica e positiva, personale, sociale e intersezionale, universale."))
        #         ], flush=False,)