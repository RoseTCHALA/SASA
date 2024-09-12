#  Copyright (C) 2024, Rose TCHALA SARE (r.tchala-sare@etu.u-paris.fr)
#
# Ce programme a ete cree dans le cadre du module Programmation et projet tutoré 3
#Pour plus d'informations sur le programme et le contexte scientifique lire le fichier README disponible à la source du dossier


"""Voici le code qui permet de générer et gérer l'interface web-based du calcul de SASA"""

from flask import Flask, render_template, request
import molecule
import display

#On crée une instance de Flask
app = Flask(__name__, static_folder='static')

@app.route('/')
def welcome ():
    print("Arrivée sur la page d'acceuil")
    return render_template("home.html")


#Action après l'envoi du formulaire
@app.route('/predict', methods=['POST'])
def predict():

    #On récupere le fichier du formulaire
    uploaded_file = request.files.get('file')

    if uploaded_file:

        print("File :", uploaded_file.filename)

        #Donc la on transforme l'objet donné par le formuaire en str 
        file_content_bytes = uploaded_file.read()
        file_content_str = file_content_bytes.decode('utf-8')
        file_lines = file_content_str.splitlines()

        #On récupere l'objet molécule
        la_molecule = molecule.Molecule.read_PDB(file_lines, uploaded_file.filename)


        #On retire chaque contenu du fichier plot, il faut qu'il soit vide
        display.clean_plots()

        #On calcule le SASA de chaque molécule et on génere les plots
        molecule.Molecule.calcul_SASA(la_molecule)

        #On rédige un nouveau fichier HTML qui affiche chaque plot
        display.write_template()
        
        #On affiche le fichier HTML qui affiche les résultats
        return render_template("display.html")

    else:
        print("No file uploaded")
        return render_template("home.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


