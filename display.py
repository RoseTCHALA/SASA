#  Copyright (C) 2024, Rose TCHALA SARE (r.tchala-sare@etu.u-paris.fr)
#
# Ce programme a ete cree dans le cadre du module Programmation et projet tutoré 3
#Pour plus d'informations sur le programme et le contexte scientifique lire le fichier README disponible à la source du dossier


"""Voici le code qui permet d'afficher de manière dynamique les résultats de l'analyse d'accessibilité """

import os
import shutil

def clean_plots() :

    #Dossier qu'on doit vider avant de creer les nouveaux graphiques
    folder = './static/plots'

    #Iteration sur chaque fichier du dossier
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        try:
            #On regarde si c'est bien un fichier et on le supprime
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

            #Pareil pour les eventuels dossiers
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    

def write_template():
    # On récupère le nom des plots qui viennent d'être générés
    plot_names = os.listdir("./static/plots")

    print(f"{len(plot_names)} images générées ! ")   

    with open("./templates/display.html", "w") as file:
        if plot_names == []:
            # Retourne une page html blanche si il n'y a pas d'images dans le dossier plots
            return ""
        else:

            #On creer une page html simple qui affiche les résultats de notre analyse
            file.write(f"""<!doctype html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>SASA PLOTS</title> 
        <link rel="stylesheet" type="text/css" href="{{{{ url_for('static', filename='css/style.css') }}}}">
    </head>
    <body>
    <button onclick="window.location.href='/'"> Home</button>
""")
            
            for plot in plot_names:
                file.write(f"""<img src="{{{{ url_for('static', filename='plots/{plot}') }}}}" alt="#" class="image">\n""")
            
            file.write(f"""    </body>
</html>""")
            
            print("Les résultats sont prêts !")

