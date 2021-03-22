#####################################################################
# IMPORTS :

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import re
import sys

import LANG
lang = LANG.fr

from shared import app


#####################################################################
# PREPARATION DES DONNEES (indépendante des actions du client) :

S_pipotron_reviews = pd.read_csv("data/pipotron_reviews.txt", header=None).iloc[:, 0]
S_pipotron_generated = pd.read_csv("data/pipotron_generated.txt", header=None).iloc[:, 0]

# On peut s'arrêter là si besoin pour débugguer :
""" sys.exit() """



#####################################################################
# FONCTIONS DE GENERATION DE CONTENU (hors callbacks) :

def get_pipotron_layout():
  return html.Div(className='main', children=[
    html.P(children=html.A(href="/", children=lang['back_to_main'])),
    html.H1(children=lang['title_pipotron']),
    html.Div(children=[
      html.H2(children=lang['real_review']),
      html.Div(id="real-review", className="review", children=S_pipotron_reviews.sample(1)),
      html.Button(lang['change_real_review'], id='change-real-review', n_clicks=0)
    ]),
    html.Div(children=[
      html.H2(children=lang['fake_review']),
      html.Div(id="fake-review", className="review", children=S_pipotron_generated.sample(1)),  
      html.Button(lang['change_fake_review'], id='change-fake-review', n_clicks=0)
    ]),
    html.Div(children=[
      html.H2(children=lang['wanna_know_more']),
      html.Button("", id='change-info', n_clicks=0),
      html.Div(id='div-info-pipotron', children="")
    ])
  ])




#####################################################################
# CALLBACKS :

@app.callback(
  Output('real-review', 'children'), 
  [Input('change-real-review', 'n_clicks')]
)
def update_real_review(n_clicks):
    return S_pipotron_reviews.sample(1)

@app.callback(
  Output('fake-review', 'children'), 
  [Input('change-fake-review', 'n_clicks')]
)
def update_fake_review(n_clicks):
    return S_pipotron_generated.sample(1)

@app.callback(
  [Output('div-info-pipotron', 'children'),
   Output('change-info', 'children')],
  [Input('change-info', 'n_clicks')], 
  [State('change-info', 'children')]
)
def update_info(n_clicks, button_text):
    if button_text==lang['change_info_display']:
        return html.Div(className="infos", children=dcc.Markdown(lang['info_pipotron'])), lang['change_info_hide']
    else:
        return "", lang['change_info_display']




