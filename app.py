#####################################################################
# IMPORTS :

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from dash.dependencies import Input, Output, State

import LANG
lang = LANG.fr
DECIMAL_SEPARATOR = ','


#####################################################################
# IMPORT DES COMPOSANTS (SOUS-PARTIES) DE L'APPLICATION :

from shared import app
from cotes import get_cote_layout
from pipotron import get_pipotron_layout


#####################################################################
# PARAMETRES GENERAUX :

server = app.server
app.title = lang['title']


#####################################################################
# CHOIX DU CONTENU A AFFICHER EN FONCTION DE L'URL :

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Pour intercepter l’URL et ses changements
    html.Div(id="content")
])

@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname.startswith("/cotes"):
        return get_cote_layout()
    elif pathname.startswith("/pipotron"):
        return get_pipotron_layout()
    else:
        # Propose un choix à l'utilisateur :
        return [
            html.H1(children=lang['title']),
            html.H3(children=lang['choose_app']),
            html.H4(children=html.A(href="/cotes", children=lang['title_cotes'])),
            html.H4(html.A(href="/pipotron", children=lang['title_pipotron']))
        ]


#####################################################################
# LANCEMENT DU SERVEUR :

if __name__ == '__main__':   # Indispensable pour Heroku
    app.run_server(debug=True)
