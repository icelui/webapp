#####################################################################
# IMPORTS :

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
import sys

import LANG
lang = LANG.fr
DECIMAL_SEPARATOR = ','


#####################################################################
# PREPARATION DES DONNEES (indépendante des actions du client) :

DF_ideal = pd.read_csv("data/idealwine.csv")
DF_ideal_pred_xg_2015 = pd.read_csv("data/idealwine_pred_2015_2020.csv")
DF_ideal_pred_tf_2015 = pd.read_csv("data/idealwine_pred_tf_2015_2020.csv")
DF_ideal_pred_xg_2020 = pd.read_csv("data/idealwine_pred_2020_2025.csv")
DF_ideal_pred_tf_2020 = pd.read_csv("data/idealwine_pred_tf_2020_2025.csv")

DF_viz1_data = DF_ideal[DF_ideal.millesime>=1982].copy()
DF_viz1_choice = DF_viz1_data.groupby(['pays_region', 'domaine', 'appellation', 'nom_du_vin', 'couleur'], as_index=False)['cote_2020'].count()
DF_viz1_choice = DF_viz1_choice[DF_viz1_choice['cote_2020']>=8].drop(columns='cote_2020').reset_index(drop=True)

DF_viz2_data = DF_ideal[(DF_ideal.millesime>=2004) & (DF_ideal.millesime<=2016)].copy()
DF_temp = DF_viz2_data.groupby(['pays_region', 'domaine', 'appellation', 'nom_du_vin', 'couleur'], as_index=False)['cote_2020'].count()
DF_temp = DF_temp[DF_temp.cote_2020>=13].drop(columns='cote_2020')
print("Nombre de vins retenus pour la visualisation no 2 :", len(DF_temp))
DF_viz2_data = DF_viz2_data.merge(DF_temp)
DF_temp = DF_temp.groupby(['appellation'], as_index=False)['nom_du_vin'].count()
DF_viz2_choice = DF_temp[DF_temp.nom_du_vin >= 5].drop(columns='nom_du_vin').sort_values(by='appellation').reset_index(drop=True)
print("Nombre d'appellations retenues pour la visualisation no 2 :", len(DF_viz2_choice))
DF_viz2_data = DF_viz2_data.merge(DF_viz2_choice).groupby(['appellation', 'millesime'], as_index=False)['cote_2020'].mean()

L_col_cote = [col for col in DF_ideal.columns if ((re.search(r'^cote_', col)!=None) and (int(re.sub(r'^cote_', "", col))>=2005))]
L_col_id = ['appellation', 'domaine', 'nom_du_vin', 'couleur', 'millesime']
DF_viz3_data = DF_ideal[DF_ideal.millesime>=1990][L_col_id + L_col_cote].dropna()
DF_temp = DF_viz3_data.groupby(["appellation", "nom_du_vin"], as_index=False).first()[["appellation", "nom_du_vin"]].groupby("appellation", as_index=False).count()
DF_viz3_choice = DF_temp[DF_temp["nom_du_vin"]>4][["appellation"]].sort_values(by='appellation')

DF_viz3a_data = DF_ideal[DF_ideal.millesime>=1996][L_col_id + L_col_cote].dropna(subset=['cote_2015', 'cote_2020'])
DF_viz3a_data['infl_2015_2020'] = DF_viz3a_data['cote_2020'] / DF_viz3a_data['cote_2015'] - 1
DF_viz3a_data = DF_viz3a_data[DF_viz3a_data['infl_2015_2020']<=10]  # Suppression des valeurs aberrantes
DF_viz3a_data = DF_viz3a_data.sort_values(by=['infl_2015_2020'], ascending=False).head(30).reset_index(drop=True).reset_index()
DF_viz3a_choice = DF_viz3a_data[['index'] + L_col_id + ['infl_2015_2020']]
DF_viz3a_data = DF_viz3a_data.melt(id_vars=['index']+L_col_id, value_vars=L_col_cote, var_name='annee_cote', value_name='cote')
DF_viz3a_data['annee_cote'] = DF_viz3a_data['annee_cote'].apply(lambda s: int(re.sub(r"^cote_", "", s)))
DF_viz3a_data = DF_viz3a_data.sort_values(by=['index', 'annee_cote']).dropna()
#print("DF_viz3a_data.columns = ", DF_viz3a_data.columns.tolist())
#DF_viz3a_data.to_csv("test001.csv", index=False)

# On peut s'arrêter là si besoin pour débugguer :
""" sys.exit() """



#####################################################################
# FONCTIONS DE GENERATION INITIALE DE CONTENU (hors callbacks) :

def get_prediction_tab(vizname, with_tf=True):
    options = [{'label': lang['xgboost'], 'value': 'xg'}]
    if with_tf:
        options = options + [{'label': lang['tensorflow'], 'value': 'tf'}]

    return dcc.Tab(              
        id='tab-'+vizname,
        value='tab-'+vizname,
        label=lang[vizname],
        className='tab',
        selected_className='selected-tab',
        children=[html.Div(
            id='div_tab_'+vizname,
            className='div-tab',
            children=[
                html.H3(lang['title_'+vizname]),
                html.P(lang[vizname+'_desc']),
                html.Table(className='table-center', children=[html.Tbody([
                    html.Tr(children=[
                        html.Td(children=html.H6(lang['choose_model'])),
                        html.Td(children=[dcc.Dropdown(
                            id=vizname+'_choice_model',
                            className='viz-dropdown-large',
                            multi=False,
                            options=options,
                            value='xg'
                        )])
                    ]),
                    html.Tr(children=[
                        html.Td(children=html.H6(lang['choose_action'])),
                        html.Td(children=[dcc.Dropdown(
                            id=vizname+'_choice_action',
                            className='viz-dropdown-large',
                            multi=False,
                            options=[
                                {'label': lang['see_pred'], 'value': 'viz'},
                                {'label': lang['get_reco_test'], 'value': 'reco'}
                            ],
                            value='reco'
                        )])
                    ]), 
                    html.Tr(id=vizname+'_tr_choose_number', children=[
                        html.Td(children=html.H6(lang['choose_number'])),
                        html.Td(children=[dcc.Dropdown(
                            id=vizname+'_choice_nbwines',
                            className='viz-dropdown-small',
                            multi=False,
                            options=[{'label': n, 'value': n} for n in np.arange(5, 55, 5)],
                            value=20
                        )])
                    ]),
                    html.Tr(id=vizname+'_tr_choose_wine', children=[
                        html.Td(children=html.H6(lang['choose_wine_alea'])),
                        html.Td(children=[dcc.Dropdown(
                            id=vizname+'_choice_wine',
                            className='viz-dropdown-large',
                            multi=False
                        )])
                    ]) 
                ])]),
                html.Div(id=vizname+'_result', className='viz-result')
            ]
        )]
    )

#####################################################################
# DEFINITION GENERALE DU CONTENU DE L'APPLICATION WEB :

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = lang['title']
server = app.server
app.layout = html.Div(className='main', children=[
    dcc.Location(id='url', refresh=False),  # Pour intercepter un appel à la page
    html.H1(children=lang['title']),
    dcc.Tabs(
        id='main-tabs',
        value='tab-viz6',
        className='main-tabs',
        parent_className='parent-main-tabs',
        colors={
            'border': 'brown',  # Couleur des bordures des onglets
            'primary': 'brown',  # Couleur de ligne au-dessus de l'onglet sélectionné
            'background': '#EFE0E0'  # Couleur de fond des onglets non sélectionnés
        },
        children = [
            dcc.Tab(
                id='tab-viz0',
                value='tab-viz0',
                label=lang['viz0'],
                className='tab',
                selected_className='selected-tab',
                children=[html.Div(
                    id='div_tab_viz0',
                    className='div-tab',
                    children=[dcc.Markdown(lang['info'])]
                )]
            ),
            dcc.Tab(
                id='tab-viz4',
                value='tab-viz4',
                label=lang['viz4'],
                className='tab',
                selected_className='selected-tab',
                children=[html.Div(
                    id='div_tab_viz4',
                    className='div-tab',
                    children=[
                        html.H3(lang['title_viz4']),
                        html.Table(className='table-center', children=[html.Tbody([
                            html.Tr(children=[
                                html.Td(children=html.H6(lang['choose_action'])),
                                html.Td(children=[dcc.Dropdown(
                                    id='viz4_choice_action',
                                    className='viz-dropdown-large',
                                    multi=False,
                                    options=[
                                        {'label': lang['title_viz1'], 'value': 'viz1'},
                                        {'label': lang['title_viz2'], 'value': 'viz2'},
                                        {'label': lang['title_viz3'], 'value': 'viz3'},
                                        {'label': lang['title_viz3a'], 'value': 'viz3a'}
                                    ],
                                    value='viz1'
                                )])
                            ]),
                            html.Tr(id='tr_viz1', children=[
                                html.Td(children=html.H6(lang['choose_wine_alea'])),
                                html.Td(children=[dcc.Dropdown(
                                    id='viz1_choice',
                                    className='viz-dropdown-large',
                                    multi=False,
                                )])
                            ]),
                            html.Tr(id='tr_viz2', children=[
                                html.Td(children=html.H6(lang['choose_appellation'])),
                                html.Td(children=[dcc.Dropdown(
                                    id='viz2_choice',
                                    className='viz-dropdown-large',
                                    multi=False,
                                    options=(options := [{'label': app, 'value': app} for app in DF_viz2_choice['appellation'].tolist()]),
                                    value=options[0]['value']
                                )])
                            ]),
                            html.Tr(id='tr_viz3', children=[
                                html.Td(children=html.H6(lang['choose_appellation'])),
                                html.Td(children=[dcc.Dropdown(
                                    id='viz3_choice',
                                    className='viz-dropdown-large',
                                    multi=False,
                                    options=(options := [{'label': app, 'value': app} for app in DF_viz3_choice['appellation'].tolist()]),
                                    value=options[0]['value']
                                )])
                            ]),
                            html.Tr(id='tr_viz3a', children=[
                                html.Td(children=html.H6(lang['choose_wine'])),
                                html.Td(children=[dcc.Dropdown(
                                    id='viz3a_choice',
                                    className='viz-dropdown-large',
                                    multi=False,
                                    options = (options := [{'label': label, 'value': value} for (value, label) in zip(
                                        DF_viz3a_choice['index'],    
                                        DF_viz3a_choice.apply(lambda S: 
                                            S['domaine'] + " : " + S['nom_du_vin'] + " " + str(int(S['millesime'])) + " (" \
                                                + S['appellation'] + ", " + S['couleur'] + ")",
                                            axis=1
                                        )
                                    )]),
                                    value = options[0]['value']
                                )])
                            ])
                        ])]),
                        html.Div(id='viz4_result', className='viz-result')
                    ]
                )]
            ), 
            get_prediction_tab('viz5'),
            get_prediction_tab('viz6', with_tf=True)
        ]
    )
])


#####################################################################
# INITIALISATIONS AU CHARGEMENT DE L'APPLICATION :

# Initialiser le choix aléatoire de vins pour l'onglet 1 :
@app.callback(
    [Output('viz1_choice', 'options'),
     Output('viz1_choice', 'value')],
    [Input('url', 'pathname')]
)
def set_random_wine_choice_viz1(pathname):
    DF_choice = DF_viz1_choice.sample(24)
    options = [{'label': label, 'value': value} for (value, label) in zip(
        DF_choice.index,    
        DF_choice.apply(lambda S: S['domaine'] + " : " + S['nom_du_vin'] + " (" + S['appellation'] + ", " + S['couleur'] + ")", axis=1)
    )]
    value = options[0]['value']
    return options, value



#####################################################################
# MISES A JOUR EN FONCTION DES ACTIONS DE L'UTILISATEUR :

# Pour l'onglet de visualisation, actualiser les choix proposés à l'utilisateur en fonction de l'action qu'il a choisie :
@app.callback(
    [Output('tr_viz1', 'style'),
     Output('tr_viz2', 'style'),
     Output('tr_viz3', 'style'),
     Output('tr_viz3a', 'style')],
    [Input('viz4_choice_action', 'value')]
)    
def set_tr_viz4(value):
    if value=='viz1':
        return {}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif value=='viz2':
        return {'display': 'none'}, {}, {'display': 'none'}, {'display': 'none'}
    elif value=='viz3':
        return {'display': 'none'}, {'display': 'none'}, {}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {}


# Définir le graphique de la 1e viz en fonction du choix de vin fait par l'utilisateur :
def set_viz1_result(value):
    DF_data = DF_viz1_data.merge(DF_viz1_choice.loc[[value]])
    DF_data = DF_data[['millesime', 'cote_2020']].sort_values(by=['millesime'])
    fig = px.scatter(DF_data, x='millesime', y='cote_2020', trendline='ols', trendline_color_override='lightgrey')
    fig.update_traces(selector=dict(mode="markers"), mode="lines+markers", marker = go.scatter.Marker(symbol='hexagon-dot', size=8))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text=lang['vintage'])
    fig.update_yaxes(title_text=lang['price'])
    children = [
        html.H4([lang['viz1_desc'], html.A('idealwine.com', href='https://www.idealwine.com'), " :"]),
        dcc.Graph(id='viz1-graph', figure=fig)
    ]
    return children

# Définir le graphique de la 2e viz en fonction du choix d'appellation fait par l'utilisateur :
def set_viz2_result(value):
    DF_data = DF_viz2_data[DF_viz2_data.appellation==value].sort_values(by=['millesime'])
    fig = px.scatter(DF_data, x='millesime', y='cote_2020')
    fig.update_traces(mode="lines+markers", line=dict(color="#d41010"), marker=go.scatter.Marker(symbol='triangle-up', size=10))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text=lang['vintage'])
    fig.update_yaxes(title_text=lang['avg_price'])
    children = [
        html.H4([lang['viz2_desc']]),
        dcc.Graph(id='viz2-graph', figure=fig)
    ]    
    return children

# Définir le graphique de la 3e viz en fonction du choix d'appellation fait par l'utilisateur :
def set_viz3_result(value):
    DF_data = DF_viz3_data[DF_viz3_data.appellation==value].melt(id_vars=L_col_id, value_vars=L_col_cote, var_name='annee_cote', value_name='cote').reset_index()
    DF_data['annee_cote'] = DF_data['annee_cote'].apply(lambda s: re.sub(r"^cote_", "", s))
    DF_data = DF_data.groupby(['appellation', 'domaine', 'nom_du_vin', 'annee_cote']) \
        .apply(lambda G: pd.Series({'cote_moy': G['cote'].mean(), 'cote_max': G['cote'].max()})).reset_index()
    DF_data['vin'] = DF_data.apply(lambda S: S['domaine'] + " : " + S['nom_du_vin'], axis=1)
    DF_data = DF_data.sort_values(by=['annee_cote']).rename({    
        'nom_du_vin': lang['wine_name'],
        'annee_cote': lang['estimation_year']
    }, axis=1)
    
    fig = px.scatter(DF_data, x='cote_moy', y='cote_max', animation_frame=lang['estimation_year'], animation_group="vin", \
        color=lang['wine_name'], hover_name="vin", labels=lang['wine_name'])
    fig.update_traces(marker=go.scatter.Marker(size=10))
    fig.update_layout(showlegend=True)
    fig.update_xaxes(title_text=lang['avg_price_allvint'])
    fig.update_yaxes(title_text=lang['max_price_allvint'])
    fig.update_xaxes(range=[DF_data.cote_moy.min()-0.05*(DF_data.cote_moy.max()-DF_data.cote_moy.min()), DF_data.cote_moy.max()+0.05*(DF_data.cote_moy.max()-DF_data.cote_moy.min())])
    fig.update_yaxes(range=[DF_data.cote_max.min()-0.05*(DF_data.cote_max.max()-DF_data.cote_max.min()), 1.05*DF_data.cote_max.max()+0.05*(DF_data.cote_max.max()-DF_data.cote_max.min())])
    children = [
        html.H4([lang['viz3_desc']]),
        dcc.Graph(id='viz3-graph', figure=fig)
    ]
    return children

# Définir le graphique de la 4e viz en fonction du choix d'appellation fait par l'utilisateur :
def set_viz3a_result(value):
    DF_data = DF_viz3a_data[DF_viz3a_data['index']==value]
    fig = go.Figure(
        data = go.Scatter(
            x=DF_data.annee_cote,
            y=DF_data.cote,
            mode='lines+markers',
            line=dict(color="#000060")
        ),
        layout = go.Layout(showlegend=False)
    )
    fig.update_traces(marker=go.scatter.Marker(size=10))
    fig.update_xaxes(title_text=lang['estimation_year'])
    fig.update_yaxes(title_text=lang['price'])
    children = dcc.Graph(figure=fig)
    return children

# Actualiser le contenu de l'onglet de visualisation :
@app.callback(
    Output('viz4_result', 'children'),
    [Input('viz4_choice_action', 'value'),
     Input('viz1_choice', 'value'),
     Input('viz2_choice', 'value'),
     Input('viz3_choice', 'value'),
     Input('viz3a_choice', 'value')]
)
def set_viz4_result(value_choice_action, value_viz1, value_viz2, value_viz3, value_viz3a):
    if value_choice_action=='viz1':
        return set_viz1_result(value_viz1)
    elif value_choice_action=='viz2':
        return set_viz2_result(value_viz2)
    elif value_choice_action=='viz3':
        return set_viz3_result(value_viz3)
    else:
        return set_viz3a_result(value_viz3a)

# Actualiser la sélection aléatoire de vins proposés en fonction du modèle choisi dans les onglets de prédiction :
def set_random_wine_choice(DF_ideal_pred):
    DF_choice = DF_ideal_pred[['pays_region', 'domaine', 'appellation', 'nom_du_vin', 'couleur', 'millesime']].sample(24)
    options = [{'label': label, 'value': value} for (value, label) in zip(
        DF_choice.index,    
        DF_choice.apply(lambda S: S['domaine'] + " : " + S['nom_du_vin'] + " " + str(S['millesime']) + " (" + S['appellation'] + ")", axis=1)
    )]
    value = options[0]['value']
    return options, value

@app.callback(
    [Output('viz5_choice_wine', 'options'),
     Output('viz5_choice_wine', 'value')],
    [Input('viz5_choice_model', 'value')]
)
def set_random_wine_choice_viz5(value):
    if value=='tf':
        DF_ideal_pred = DF_ideal_pred_tf_2015
    else:
        DF_ideal_pred = DF_ideal_pred_xg_2015
    return set_random_wine_choice(DF_ideal_pred)

@app.callback(
    [Output('viz6_choice_wine', 'options'),
     Output('viz6_choice_wine', 'value')],
    [Input('viz6_choice_model', 'value')]
)
def set_random_wine_choice_viz6(value):
    if value=='tf':
        DF_ideal_pred = DF_ideal_pred_tf_2020
    else:
        DF_ideal_pred = DF_ideal_pred_xg_2020
    return set_random_wine_choice(DF_ideal_pred)

# Pour les onglets de prédiction, actualiser les choix proposés à l'utilisateur en fonction de l'action qu'il a choisie :
def set_tr(value):
    if value=='reco':
        choose_number_style = {}
        choose_wine_style = {'display': 'none'}
    else:
        choose_number_style = {'display': 'none'}
        choose_wine_style = {}  
    return choose_number_style, choose_wine_style

@app.callback(
    [Output('viz5_tr_choose_number', 'style'),
     Output('viz5_tr_choose_wine', 'style')],
    [Input('viz5_choice_action', 'value')]
)
def set_viz5_tr(value):
    return set_tr(value)

@app.callback(
    [Output('viz6_tr_choose_number', 'style'),
     Output('viz6_tr_choose_wine', 'style')],
    [Input('viz6_choice_action', 'value')]
)
def set_viz6_tr(value):
    return set_tr(value)

# Fonction de construction de la visualisation, commune aux onglets de prédiction :
def set_pred_viz(value, DF_data, year, delta=5):
    DF_data0 = DF_data.loc[[value]]
    DF_data0 = DF_data0.melt(id_vars=L_col_id+['pred_cote'], value_vars=L_col_cote, var_name='annee_cote', value_name='cote').reset_index()
    DF_data0['annee_cote'] = DF_data0['annee_cote'].apply(lambda s: int(re.sub(r"^cote_", "", s)))
    DF_data0 = DF_data0.sort_values(by='annee_cote').dropna()
    DF_data1 = DF_data0[DF_data0.annee_cote<=year]
    DF_data2 = DF_data0[DF_data0.annee_cote==year]
    DF_data2 = DF_data2[['annee_cote', 'cote']].append(pd.Series({'annee_cote': (year+delta), 'cote': DF_data2.iloc[0,:]['pred_cote']}), ignore_index=True)

    trace1 = go.Scatter(
        x=DF_data2.annee_cote, 
        y=DF_data2.cote,
        mode="lines+markers",
        name=lang['prediction'],
        line=dict(color='brown', dash='dot')
    )
    if year<2020:
        DF_data3 = DF_data0[DF_data0.annee_cote>=year]  # Les cotes non fournies au modèle
        fig = go.Figure(
            data = go.Scatter(
                x=DF_data3.annee_cote,
                y=DF_data3.cote,
                mode='lines+markers',
                name=lang['unknown_in'] + ' ' + str(year),
                line=dict(color="#C0BCFF")
            ), 
            layout = go.Layout(showlegend=True)
        )
        fig.add_trace(trace1)
    else:
        fig = go.Figure(
            data = trace1, 
            layout = go.Layout(showlegend=True)
        ) 
    fig.add_trace(go.Scatter(
        x=DF_data1.annee_cote,
        y=DF_data1.cote,
        mode='lines+markers',
        name=lang['known_in'] + ' ' +str(year),
        line=dict(color="#000060")
    ))
    fig.update_traces(marker=go.scatter.Marker(size=10))
    fig.update_xaxes(title_text=lang['estimation_year'])
    fig.update_yaxes(title_text=lang['price'])
    if year<2020:
        fig.update_yaxes(range=[0, 1.05*max(DF_data1.cote.max(), DF_data2.cote.max(), DF_data3.cote.max())])
    else:
        fig.update_yaxes(range=[0, 1.05*max(DF_data1.cote.max(), DF_data2.cote.max())]) 
    children = dcc.Graph(figure=fig)
    return children

# Fonction de construction de la recommandation d'investissement, commune aux onglets de prédiction :
def set_reco_result(value, DF_data, year=2015, delta=5, with_target=False):
    nb_domaines = value
    DF_invest = DF_data.sort_values(by=['pred_infl'], ascending=False)
    DF_invest = DF_invest.reset_index().groupby(['pays_region', 'domaine']).first().reset_index().set_index('index')
    DF_invest = DF_invest.sort_values(by=['pred_infl'], ascending=False).head(nb_domaines)
    DF_invest = DF_invest.sort_values(by=['pays_region', 'domaine'])
    if year<2020:
        infl_avg = DF_data.cible.mean()
        invest_avg = DF_invest.cible.mean()
        ratio_avg = invest_avg / infl_avg

    if with_target:
        DF_invest = DF_invest[['pays_region', 'domaine', 'nom_du_vin', 'appellation', 'couleur', 'millesime', 'cible']]
        DF_invest[lang['inflation']+' '+str(year)+'-'+str(year+delta)] = DF_invest['cible'].apply(lambda v: "{:.0%}".format(v))
        DF_invest = DF_invest.drop(columns=['cible'])
    else:
        DF_invest = DF_invest[['pays_region', 'domaine', 'nom_du_vin', 'appellation', 'couleur', 'millesime']]
 
    # Pour optimiser l'affichage :
    DF_invest = DF_invest.rename(
        {
            'pays_region': lang['region'],
            'domaine': lang['domain'],
            'nom_du_vin': lang['wine_name'],
            'appellation': lang['appellation'],
            'couleur': lang['color'],            
            'millesime': lang['vintage']
        },
        axis=1
    )
    if year<2020:
        children = [
            html.P(lang['infl_avg_01'] + str(year) + lang['infl_avg_02'] + str(year+delta) + lang['infl_avg_03'] + " : "),
            html.H5('{:.1%}'.format(infl_avg).replace('.', DECIMAL_SEPARATOR)),
            html.P(lang['invest_avg_2015'] + " : "),
            html.H5('{:.1%}'.format(invest_avg).replace('.', DECIMAL_SEPARATOR))
        ]
    else:
        children = [
            html.P(lang['invest_avg_2020']),
        ]
    children = children + [
        DataTable(
            id='viz5_table',
            style_cell={
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'fontSize': 12,
                'font-family': 'sans-serif',
                'height': 'auto'
            },
            style_header={
                'backgroundColor': 'rgb(241, 226, 226)', # #EFE0E0
                'fontWeight': 'bold'
            },
            columns=[{"name": col, "id": col} for col in DF_invest.columns],
            data=DF_invest.to_dict('records')
        )
    ]
    return children

# Actualiser la restitution affichée pour le modèle 2015 en fonction des différents choix de l'utilisateur :
@app.callback(
    Output('viz5_result', 'children'),
    [Input('viz5_choice_model', 'value'),
     Input('viz5_choice_action', 'value'),
     Input('viz5_choice_nbwines', 'value'),
     Input('viz5_choice_wine', 'value')]
)
def set_viz5_result(value_model, value_action, value_nbwines, value_wine):
    if value_model=='tf':
        DF_data = DF_ideal_pred_tf_2015
    else:
        DF_data = DF_ideal_pred_xg_2015

    if value_action=='reco':
        children = set_reco_result(value_nbwines, DF_data=DF_data, year=2015, delta=5, with_target=True)
    else:
        children = set_pred_viz(value_wine, DF_data=DF_data, year=2015, delta=5)
    return children

# Actualiser la restitution affichée pour le modèle 2020 en fonction des différents choix de l'utilisateur :
@app.callback(
    Output('viz6_result', 'children'),
    [Input('viz6_choice_model', 'value'),
     Input('viz6_choice_action', 'value'),
     Input('viz6_choice_nbwines', 'value'),
     Input('viz6_choice_wine', 'value')]
)
def set_viz6_result(value_model, value_action, value_nbwines, value_wine):
    if value_model=='tf':
        DF_data = DF_ideal_pred_tf_2020
    else:
        DF_data = DF_ideal_pred_xg_2020

    if value_action=='reco':
        children = set_reco_result(value_nbwines, DF_data=DF_data, year=2020, delta=5, with_target=False)
    else:
        children = set_pred_viz(value_wine, DF_data=DF_data, year=2020, delta=5)
    return children



#####################################################################
# LANCEMENT DU SERVEUR :

if __name__ == '__main__':
    app.run_server(debug=True)
