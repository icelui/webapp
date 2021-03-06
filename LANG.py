fr = {
    'title': "Quelques exemples de réalisations autour du vin",
    'choose_app': "Choisissez SVP l'une des réalisations suivantes :",
    'back_to_main': "(Retour au choix de l'une des réalisations)",
    'in_progress': "En construction",
    

    ############################################################################
    # Chaînes de caractères pour la cote des grands vins de France :

    'title_cotes': "La cote des grands vins de France : recommandations d'investissement",

    'viz0': "Informations",
    'viz4': "Visualisations",
    'viz5': "Prédiction 2015 (test)",
    'viz6': "Prédiction 2020",
    'choose_wine_alea': "Choisissez un vin parmi cette sélection aléatoire :",
    'choose_wine': "Choisissez un vin :",
    'choose_appellation': "Choisissez une appellation :",
    'vintage': "Millésime",
    'price': "Cote en euros (bouteille de 75 cL)",
    'avg_price': "Cote moyenne des vins de l'appellation en euros",
    'avg_price_allvint': "Cote moyenne du vin en euros (tous millésimes)",
    'max_price_allvint': "Cote maximale du vin en euros (tous millésimes)",
    'wine_name': "Nom du vin",
    'estimation_year': "Année de cotation",
    'prediction': "Prédiction",
    'known_in': "Cotes utilisées par le modèle prédictif, car connues en",
    'unknown_in': "Cotes non utilisées par le modèle prédictif, car inconnues en",
    'choose_number': "Choisissez le nombre de vins (de domaines différents) de votre portefeuille d'investissement :",
    'choose_model': "Choisissez un modèle prédictif :",
    'choose_action': "Que voulez-vous faire ?",
    'infl_avg_01': "L'inflation moyenne des vins, entre ",
    'infl_avg_02': " et ",
    'infl_avg_03': ", sur l'ensemble des vins faisant l'objet d'une prédiction, est de",
    'invest_avg_2015': """Le modèle prédictif (qui ne dispose d'aucune information ultérieure à 2015) propose d'investir en 2015 sur
                          les vins ci-dessous. La rentabilité moyenne de ce portefeuille à 5 ans est de""",
    'invest_avg_2020': "Le modèle prédictif propose d'investir en 2020 sur les vins ci-dessous :",
    'region': "Région",
    'appellation': "Appellation",
    'domain': "Domaine", 
    'color': "Couleur",
    'xgboost': "Forêts aléatoires (random forests) boostées par la technologie XGBoost",
    'tensorflow': "Réseau de neurones denses et récurrents (LSTM) entraîné avec Tensorflow",
    'see_pred': "Visualiser la prédiction de cote dans 5 ans pour quelques vins de la base",
    'get_reco_test': "Obtenir une recommandation d'investissement",
    'inflation': "Inflation",

    'title_viz1': "Voir la variation de cote (actuelle) de quelques vins en fonction du millésime",
    'title_viz2': "Voir la variation de cote moyenne d'une appellation en fonction du millésime",
    'title_viz3': "Voir l'évolution temporelle de la cote des grands vins d'une appellation",
    'title_viz3a': "Voir l'évolution temporelle de la cote des vins de plus forte inflation entre 2015 et 2020",
    'title_viz4': "Je propose ici quelques exemples de visualisation sur les données collectées...",
    'title_viz5': "Modèles prédictifs '2015' (pour tester la validité des prédictions)",
    'title_viz6': "Modèles prédictifs '2020' (pour vous aider à investir aujourd'hui)",

    'viz1_desc': "Voici la cote actuelle des millésimes de ce vin (1982 et postérieurs) selon ",
    'viz2_desc': "La cote moyenne des vins de l'appellation dans chaque millésime permet de repérer les meilleurs millésimes :",
    'viz3_desc': "Lancez l'animation pour voir l'évolution de la cote moyenne de chaque vin au fil des années :",
    'viz5_desc': """Imaginez... Nous sommes en 2015. Le modèle prédit la cote de chaque vin dans 
                    5 ans, soit en 2020. Il a été entraîné comme il aurait pu l'être en 2015 : en variable cible, 
                    les cotes de la dernière année disponible, soit 2015 ; en variables explicatives, les données disponibles
                    5 ans avant, soit en 2010. Le modèle entraîné est ensuite utilisé pour prédire les cotes dans 5 ans, soit
                    en 2020, à partir des données disponibles en 2015. De ces prédictions est déduite une recommandation
                    d'investissement, dont la performance est évaluée a posteriori, en 2020.""",
    'viz6_desc': """Nous sommes en 2020. Le modèle prédit la cote de chaque vin dans 
                    5 ans, soit en 2025. Il a été entraîné avec en variable cible, 
                    les cotes de la dernière année disponible, soit 2020 ; en variables explicatives, les données disponibles
                    5 ans avant, soit en 2015. Le modèle entraîné est ensuite utilisé pour prédire les cotes 
                    en 2025, à partir des données disponibles en 2020. De ces prédictions est déduite une recommandation
                    d'investissement.""",

    'info': '''
               #### Origine des données :
               Toute les données utilisées ici ont été collectées sur le site [Idealwine](https://www.idealwine.com), qui est une
               référence en matière d'estimation de prix ("cote") des grands vins français.

               #### Choix d'implémentation :
               Les modèles prédictifs, pour prédire la cote future d'un millésime donné d'un vin donné, s'appuient uniquement sur des données disponibles 5 ans plus tôt.
               Il s'agit non seulement de données connues pour ce vin millésimé, mais également de données (moyennes ou maximales) connues pour l'ensemble des millésimes du
               même vin, pour l'ensemble des vins du même domaine, et enfin pour l'ensemble des vins de la même appellation.

               Pour les modèles prédictifs ne recourant pas aux réseaux de neurones (_deep learning_), plusieurs techniques de régression ont été testées et optimisées :
               régression linéaire, machines à vecteurs de support (SVM), forêt aléatoire (random forest) "classiques", forêt aléatoire "boostée" par XGBoost. Après
               recherche des paramètres optimaux pour chacune de ces solutions, c'est la dernière qui s'est avérée la plus performante en termes de recommandations 
               d'investissement, et qui a donc été publiée sur ce site. 

               Pour les modèles de _deep learning_, un réseau non séquentiel permet d'utiliser des couches de neurones récurrents (LSTM) pour traiter les séries temporelles,
               et de combiner les sorties de ces couches avec celles de couches "denses" utilisées pour les variables explicatives non séquentielles.

               #### Technologies utilisées pour réaliser ce site :
               Pour la partie web : Python, [Anaconda](https://www.anaconda.com/), [Dash](https://plotly.com/dash/),
               [Plotly Graphing Libraries](https://plotly.com/graphing-libraries/), [Heroku](https://heroku.com/) et
               [Git](https://git-scm.com/) pour la publication.

               Pour la collecte et la préparation des données : Python, Anaconda, [Scrapy](https://scrapy.org/) et [Pandas](https://pandas.pydata.org/).

               Pour le _machine learning_ et le _deep learning_ : [Numpy](https://numpy.org/), [Scikit-Learn](https://scikit-learn.org/), 
               [XGBoost](https://xgboost.readthedocs.io/), [Tensorflow](https://www.tensorflow.org/) et [Keras](https://keras.io/).

               Pour ouvrir les bouteilles : un tire-bouchon à [double levier](https://images-na.ssl-images-amazon.com/images/I/417Oc0h5b9L._AC_.jpg), toujours ! 

            ''',


    ############################################################################
    # Chaînes de caractères pour le pipotron :

    'title_pipotron': "Un pipotron qui génère des commentaires professionnels de dégustation de vin",

    'real_review': "Voici un commentaire de vin réel, issu de la Revue du Vin de France :",
    'fake_review': "... et voici un commentaire imaginaire (fictif) généré par le pipotron :",
    'change_real_review': "Choisir un autre",
    'change_fake_review': "Choisir un autre",
    'wanna_know_more': "Vous voulez en savoir plus ?",
    'change_info_display': "Afficher les informations",
    'change_info_hide': "Masquer les informations",
    'choose_wine_color': "Couleur du vin (à choisir) :",
    'blanc': "Blanc",
    'rouge': "Rouge",

    'info_pipotron':
            '''
               #### Origine des données :
               Les données utilisées ici ont été collectées sur le site de la [Revue du vin de France](https://www.larvf.com), et ne sont
               accessibles que par abonnement.

               #### Choix d'implémentation :
               Le pipotron s'appuie sur un générateur de type GPT2, préentraîné sur la langue française par 
               [Antoine Louis](https://github.com/antoiloui/belgpt2). J'ai fait subir à ce réseau de neurones un entraînement
               spécifique (_fine tuning_) pour qu'il apprenne à imiter les commentaires de la Revue du vin de France. Cf.
               [GitHub](https://github.com/icelui/pipotron).
               Le modèle étant très gros (500 Mo), il n'est pas directement utilisé par ce site web : celui-ci s'appuie sur un
               "cache" de quelques centaines de commentaires fictifs générés par le modèle.
               
               #### Technologies utilisées :
               Pour la partie web : Python, [Anaconda](https://www.anaconda.com/), [Dash](https://plotly.com/dash/), [Heroku](https://heroku.com/) et
               [Git](https://git-scm.com/) pour la publication.

               Pour la collecte et la préparation des données : Python, Anaconda, [Scrapy](https://scrapy.org/) et [Pandas](https://pandas.pydata.org/).

               Pour le _deep learning_ : [Tensorflow](https://www.tensorflow.org/) et [Keras](https://keras.io/), et la 
               bibliothèque [Transformers](https://huggingface.co/transformers/) de la société [HuggingFace](https://huggingface.co).

            ''',



}

