# Calculer la Surface Accessible au Solvant (SASA)

##### Vous cherchez à calculer la surface accessible au solvant de votre molécule ? Vous êtes au bon endroit !

##### Cette application permet de calculer la Surface Accesible à une moléclule d'eau en Å² d'une structure issue de votre fichier PDB. Elle a été conçue en suivant le la méthode de Shake et Rupley (1973) et offre une interface Web qui permet de déposer facilement votre fichier de visualiser l'accessibilité individuelle atomique des résidus de la molécule.

##### L'algorithme utilise python comme interpéteur. L'interface est compatible avec tous les navigateurs.

##### L'algorithme à nécessité dans sa construction différentes stratégies pour optimiser le temps de calcul.

## Prise en main

### 1 : Téléchargement du repository

Note : il est essentiel d'avoir Conda sur votre machine pour utiliser le programme. Vous pouvez installer anaconda ici : 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

##### Dans votre terminal, lancez les commandes : 
git clone https://github.com/RoseTCHALA/SASA.gitcd SASAconda env create -f env.ymlconda activate envpython app.py ou python3 app.py
### 2 : Execuction du script app.py (de préférence via un terminal ou VS Code)

Votre terminal affichera une adresse https de développement local (par exemple http://127.0.0.1:5000). Ouvrez le lien dans le navigateur de votre choix et gardez le terminal ouvert pour suivre l'avancement des calculs.

### 3 : Comment calculer la SASA de ma molécule ? 

Pour l'instant, il n'est pas encore possible de préciser la surface en Å² du solvant. On suppose donc que la molécule en question est la molécule d'eau. L'utilisateur n'a pas à définir le nombre de points qui approxime la sphère délimitant chaque résidu.

##### Et donc ? 

Et donc une fois arrivé(e) sur l'interface web sain(e) et sauf(ve), il suffit de cliquer sur le bouton calculer et chosir le fichier PDB de votre choix. Une fois le fichier choisi le programme se lance automatiquement.

### 4 : Suivre l'avancée du programme

Malheureusement, pour les molécules les plus coriaces l'algorithme peut prendre un certain temps... Cependant, dans votre terminal, vous pouvez suivre l'avancée des étapes avec des messages sont affichés au fur et à mesure de la progession.

### 5 : Comment visualiser les résultats ? 

Une fois les calculs terminés, un message s'affiche dans le terminal pour dire que les résultats sont prêts. La page se met à jour automatiquement dans le navigateur web.

## Comprendre les résultats

### Dans le terminal

Dans le terminal, on voit affiché tous les atomes de la molécule avec leurs accessibilités individuelles respectives, leur classe (polaire ou non polaire) et leur numéro de résidu. Dans les trois dernières lignes, on peut également lire :

-La surface accessible totale de la molécule.

-La surface accessible des atomes polaires uniquement.

-La surface accessible des atomes polaires uniquement.

Il est important de noter que, pour la surface accessible des atomes polaires, les atomes non polaires sont également pris en compte et peuvent occulter la surface de chaque résidu, et inversement.

### Dans le navigateur

Dans le navigateur, un seul graphique est affiché.

En abcisse, on trouve le numéro de résidu de l'atome et en ordonné, c'est sa surface accessible en Å². Dans la légende on retrouve la surface totale accessible ainsi que la surface accessible des atomes polaires et non polaires et l'emplacement des chaines (si la structure en a).

##### Quelle est l'utilité du terminal si on y trouve les mêmes informations que sur les graphiques ? 

Dans le terminal on peut observer l'accesibilité individuelle des atomes.

## Limites et disscussion

Contrairement à la publication de Shake et Rupley en 1973, qui s'appuie sur les rayons atomiques des résidus basés sur les travaux de Pauling (1960), j'ai choisi d'utiliser les rayons atomiques déterminés par Bondi (1964). Ces rayons sont désormais considérés comme la référence en chimie et ont été validés par divers chimistes ayant reproduit les mêmes expériences. De plus, comme eux, les résidus d'hydrogènes ne sont pas pris en compte dans les calculs.

Un des axes d'amélioration de ce programme serait de permettre le multiprocessing dans le cas ou on doit tester de très grosses molécules.

## Validité des résultats

Lors du dévelopement du logiciel, j'ai comparé mes résultats avec ceux issus du logiciel n access. Les résultats diffèrent de quelque dizaines d'Å pour les grosses molécules mais en général, les valeurs sont similaires.
