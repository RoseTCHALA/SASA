#  Copyright (C) 2024, Rose TCHALA SARE (r.tchala-sare@etu.u-paris.fr)
#
# Ce programme a ete cree dans le cadre du module Programmation et projet tutoré 3
#Pour plus d'informations sur le programme et le contexte scientifique lire le fichier README disponible à la source du dossier


import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


#Rayon atomique (spheres Wan Der Waals)
#Valeurs précisées par Bondi (1964) par propriété physique des gaz (https://fr.wikipedia.org/wiki/Rayon_de_van_der_Waals)
#Pour chaque atome ne figurant pas sur notre liste on l'approxime avec le rayon de la molécule solvant

radii_dict = {
        "H": 1.200,
        "HE": 1.400,
        "C": 1.700,
        "N": 1.550,
        "O": 1.520,
        "F": 1.470,
        "NA": 2.270,
        "MG": 1.730,
        "P": 1.800,
        "S": 1.800,
        "CL": 1.750,
        "K": 2.750,
        "CA": 2.310,
        "NI": 1.630,
        "CU": 1.400,
        "ZN": 1.390,
        "SE": 1.900,
        "BR": 1.850,
        "CD": 1.580,
        "I": 1.980,
        "HG": 1.550,
    }

#creation de la classe Atome
class Atom:
	def __init__(self,x,y,z, numres = "", name = "", type = "", accessibility = None, radii = None, Wan_der_Waals = None, classe = None, chain = None) :
		self.name = name


		#Chaine de l'atome si il y a 
		self.chain = None 

		#Type de residu
		self.type = type

		#Numero de residu
		self.numres = numres

		#Chaque objet atome comprend un attribut donnant son accessibilité (si disponible)
		self.accessibility = None

		#coordonnees dans le plan cartesien
		self.x = x
		self.y = y
		self.z = z

		#radii Wan der Walls de l'atome + la sonde
		self.radii = None

		#Cordonnees de la sphere d'aproximation wan der waals de l'atome
		self.Wan_der_Waals = None

		#Si on veut savoir si l'atome est polaire ou non 
		self.classe =  None


	#On définit la manière dont l'atome s'affiche
	def __str__(self):

		if self.classe :
			polarity = "POLAR"
		else :
			polarity = "NON-POLAR"

		if self.accessibility is None: 
			d = (
				f"Atom : x = {round(self.x, 3):<8} ; "
				f"y = {round(self.y, 3):<8} ; "
				f"z = {round(self.z, 3):<8} ; "
				f"numres = {str(self.numres):<6} ; "
				f"type = {self.type:<6}"
				f"{polarity:<7}"
			)

		else:

			#calcul du pourcentage de sphere acessible
			V =  4 * math.pi * (self.radii**2)
			pourcentage =  self.accessibility / V * 100 

			d = (
				f"Atom : x = {round(self.x, 3):<8} ; "
				f"y = {round(self.y, 3):<8} ; "
				f"z = {round(self.z, 3):<8} ; "
				f"numres = {str(self.numres):<6} ; "
				f"type = {self.type:<6} ; "
				f"accessibility(A°^2) = {round(self.accessibility,3):<10} ({round(pourcentage, 2):<5})%  ; "
				f"{polarity:<7}"
			)
		return d
			
			
	#essentiel : calcule la distance entre deux atomes
	def calc_distance(self, atom) :
		d = (( self.x - atom.x )**2 + ( self.y - atom.y )**2 + ( self.z - atom.z )**2 )**0.5
		#print(d)
		return d 
	
		
	def mute_atom(self,name1) :
			self.name = name1

	def chain_atom(self,chaine) :
			self.chain = chaine
	
	def num_atom(self,numero) :
			self.numres = numero
			
	def type_atom(self,name1) :
			self.type = name1

	def acess_atom(self,value) :
			self.accessibility = value

	def radii_atom(self,value) :
			self.radii = value

	def sphere_wdw_atom(self, sphere) :
		self.Wan_der_Waals = sphere

	def __class_atom__(self, value) :
		if value == True :
			self.classe = True #POLAR ATOM
		elif value == False :
			self.classe = False #NON POLAR ATOM
		else :
			print("Please enter a correct value to check the class (True/False)")

		


#On crée une classe sphère qui va computer une sphère de n points
#On peut aussi faire une translation 

class Sphere(Atom):

	#CREATION DE LA SPHERE
	def compute_sphere_golden_spiral(n):

		# Initialisation des paramètres
		dl = np.pi * (3 - np.sqrt(5))
		dz = 2.0 / n 

		#Creation d'une matrice pour contenir les coordonnées
		coords = np.zeros((n, 3), dtype=np.float32)

		z = 1 - dz / 2  
		for k in range(n):
			
			r = np.sqrt(1 - z**2)

			#Calcul des coordonnées sphériques
			longitude = k * dl
			x = np.cos(longitude) * r
			y = np.sin(longitude) * r
			coords[k] = [x, y, z]

			
			z -= dz

		print(f"Sphère de {n} points bien crée !")
		return coords
	
	def translation(self, atom):

		#Le radius de l'atome DOIT etre un float et non un str ou autre
		if atom.radii is not None and isinstance(atom.radii, float) : 

			sphere_atome = []
			
			# Translation des points par apport au rayon de l'atome
			for point in self:
				translated_point = [
					point[0] * atom.radii,
					point[1] * atom.radii,
					point[2] * atom.radii
				]
				
				#On déplace les points de la sphère jusqu'au centre de l'atome
				sphere_atome.append([
					translated_point[0] + atom.x,
					translated_point[1] + atom.y,
					translated_point[2] + atom.z
				])
			
			#On ajoute à l'atome les coordonnées de sa sphère personalisée ! 
			atom.Wan_der_Waals = np.array(sphere_atome)

		else:
			print("Attention ; l'atome n'a pas d'attiribut radii correct")



#Classe Molecule qui permet de lire un fichier PDB et extraire les informations necessaires au calcul de la SASA 
#d'un groupe d'atomes

class Molecule(Atom) :

	def __init__(self,name, accessibility = None, polar_accessibility = None, non_polar_accessibility = None, nbchains = None) :
		
		self.name = name	
		self.atoms = []
		self.accessibility = None
		self.polar_accessibility = None
		self.non_polar_accessibility = None

		#On compute le nombre de chaines de la molécule
		self.nbchains = None


	#Permet d'avoir le nombre de chaines de la molécule
	#Si il y a plusieurs chaines alors le plot sera adapté
	def __molecule_chains__(self,nb) :
			self.nbchains = nb

		
	def __molecule_SASA__(self,valeur) :
			self.accessibility = valeur

	def __molecule_SASA_POLAR__(self,valeur) :
			self.polar_accessibility = valeur

	def __molecule_SASA_NON_POLAR__(self,valeur) :
			self.non_polar_accessibility = valeur
		
	def __str__(self):
		for atom in self.atoms :
			f = ""
			for atom in self.atoms :
				f = f + f"\n{atom}"

			if self.accessibility is not None :
				d = (
					f"Liste des atomes : {f}\n"
					f"Nom protéine : {self.name}\n"
					f"Accessibilité Totale (A°^2) : {round(self.accessibility,3)}\n"
					f"Accessibilité Atomes non polaires (A°^2) : {round(self.non_polar_accessibility,3)}\n"
					f"Accessibilité Atomes polaires (A°^2) : {round(self.polar_accessibility,3)}\n "
					)
				return d
			else :
				d = (
					f"Liste des atomes : {f}\n"
					f"Nom protéine : {self.name}\n" 
					)
				
				return d
		
	def add_atom(self, atom) :
		if isinstance(atom, Atom) :
			self.atoms.append(atom)


	#Cette fonction permet de retrouver un atome dans une protéine avec son numero de résidu
	def __find_atom__(self, numres):
		#Il faut etre sur que le numero de résidu soit un nombre entier
		if not isinstance(numres, int):
			raise TypeError(f"Attention, le numero de résidu doit etre un entier et non : {type(numres).__name__}.")
		
		#On récupere l'atome si le numero de résidu est le bon
		for atom in self.atoms:
			if atom.numres == numres:
				return atom
			
	#Modifie un atome de la proteine
	def __change_atom__(self, atom, new_atom) :
		i= self.atoms.index(atom)
		self.atoms[i] = new_atom

	
	#Prend en argument le dictionnaire des connectivité (que les carbonnes connectés à d'autres atomes)
	#Si le carbonne en question est connecté à plus de deux hetero atomes
	#Alors le carbonne devient polaire
	def __change_polarity__(self, atom_connections) :

		#La on va récuperer le numero de résidu des atomes qui deviennent polaire
		#La stratégie est de les modifier tous a la fin pour eviter qu'ils deviennent des atomes polaires en cours
		#du calcul et ne faussent les resultats pour les eventuels autres atomes auxquels ils sont connectes
		atoms_to_change = []
		for carbonne in atom_connections :
			polar = 0
			liste = atom_connections.get(carbonne)
			#On rapelle que le carbonne doit avoir AU MOINS deux connections avec un hetero atome
			if len(liste) > 1 :
				for atome in liste :
					if atome.classe == True :
						print(atome)
						polar += 1 
						if polar == 2 :
							atoms_to_change.append(carbonne)
							break

		#Maintenant on va convertir chaque carbonne lié a >= 2 hetero atome en atome non polaire
		for numero in atoms_to_change : 
			accurate_atom = self.__find_atom__(numero)
			accurate_atom.__class_atom__(True)
			old_atom = self.__find_atom__(numero)

			self.__change_atom__(old_atom, accurate_atom)


	#Cette fonction permet de creer un objet molécule a partir d'un texte
	#Pas de spécification de la chaine 
	def create_molecule(f,name) :

		L = []
		conect_lines = []

		for i in range(0,len(f)) : 
			ligne = f[i]
			if ligne.startswith("ATOM") and ligne[76:78].strip() != "H" : 
				a = Atom(float(ligne[30:38]), float(ligne[38:46]), float(ligne[46:54]))
				a.type_atom(ligne[76:78].strip())
				a.num_atom(int(ligne[7:11]))

				#"Normal atom are considered not polar"
				a.__class_atom__(False)
				L.append(a)

			elif ligne.startswith("HETATM") and ligne[76:78].strip() != "H" : 
				a = Atom(float(ligne[30:38]), float(ligne[38:46]), float(ligne[46:54]))
				a.type_atom(ligne[76:78].strip())
				a.num_atom(int(ligne[7:11]))

				#Hetero atoms are  polar
				a.__class_atom__(True)
				L.append(a)

				#Partie importante

				#Si le fichier comporte des informations entre la connectivité des atomes
				#Par exemple si on résidu de carbonne est connecté à > 2 heteroatomes
				#Alors il est considéré comme non polaire.
			
			elif ligne.startswith("CONECT") : 
				conect_lines.append(ligne.split())

		#creation d'un objet molécule
		molecule = Molecule(name)
		for atom in L :
			molecule.add_atom(atom)

		#Si il y a des atomes connectés :
		if len(conect_lines) > 0 :

				atom_connections = {}


				
				for line in conect_lines:
					atom_serial = int(line[1])  # Atom serial number
					atom = molecule.__find_atom__(atom_serial)

					#On ne recherche que les connections des carbonnes non polaires
					if atom.type == "C" and atom.classe == False : 
						connected_atoms = [molecule.__find_atom__(int(indice)) for indice in line[2:]]  # Ajoute les atomes à la liste du dictionnaire
						# Add the connections for this atom
						if atom_serial not in atom_connections:
							atom_connections[atom_serial] = []

						#On ajoute les atomes connectés à la liste
						atom_connections[atom_serial].extend(connected_atoms)

				molecule.__change_polarity__(atom_connections)

			

			
		return(molecule)
	

	#Fonction qui crée un objet molécule en prenant en compte l'identité de la chaine
	def strip_chain(f,name) :
			L = []
			conect_lines = []

			for i in range(0,len(f)) : 
				ligne = f[i]
				if ligne.startswith("ATOM") and ligne[76:78].strip() != "H" : 
					a = Atom(float(ligne[30:38]), float(ligne[38:46]), float(ligne[46:54]))
					a.type_atom(ligne[76:78].strip())
					a.num_atom(int(ligne[7:11]))
					a.chain_atom(ligne[21:22])

					#"Normal atom are considered not polar"
					a.__class_atom__(False)
					L.append(a)

				elif ligne.startswith("HETATM") and ligne[76:78].strip() != "H" : 
					a = Atom(float(ligne[30:38]), float(ligne[38:46]), float(ligne[46:54]))
					a.type_atom(ligne[76:78].strip())
					a.num_atom(int(ligne[7:11]))
					a.chain_atom(ligne[21:22])


					#Hetero atoms are  polar
					a.__class_atom__(True)
					L.append(a)

					#Partie importante

					#Si le fichier comporte des informations entre la connectivité des atomes
					#Par exemple si on résidu de carbonne est connecté à > 2 heteroatomes
					#Alors il est considéré comme non polaire.
				
				elif ligne.startswith("CONECT") : 
					conect_lines.append(ligne.split())

			#creation d'un objet molécule
			molecule = Molecule(name)
			for atom in L :
				molecule.add_atom(atom)

			#Si il y a des atomes connectés :
			if len(conect_lines) > 0 :

					atom_connections = {}


					
					for line in conect_lines:
						atom_serial = int(line[1])  # Atom serial number
						atom = molecule.__find_atom__(atom_serial)

						#On ne recherche que les connections des carbonnes non polaires
						if atom.type == "C" and atom.classe == False : 
							connected_atoms = [molecule.__find_atom__(int(indice)) for indice in line[2:]]  # Ajoute les atomes à la liste du dictionnaire
							# Add the connections for this atom
							if atom_serial not in atom_connections:
								atom_connections[atom_serial] = []

							#On ajoute les atomes connectés à la liste
							atom_connections[atom_serial].extend(connected_atoms)

					molecule.__change_polarity__(atom_connections)

				

				
			return(molecule)
		
	
	#Fonction qui permet de lire un fichier PDB
	# Retourne une seule molécule ou une liste de molécule	
	def read_PDB(file, filename) :

		filename = filename.removesuffix(".pdb")

		#On part du principe qu'il n'y a pas de chaine spécifiée pour la molécule
		nb_chains = 0

		for ligne in file :
				if ligne.startswith("COMPND") and "CHAIN" in ligne :
					g = ligne.split() ; index = (g.index("CHAIN:"))
					#On regarde si la molécule comporte plusieurs chaines 
					nb_chains = (len(g[index + 1 :]))

		if nb_chains == 1 : 
			print(f"Il y a une seule chaine dans la molecule")

			molecule = Molecule.create_molecule(file, filename)
			return molecule	

		if nb_chains > 1 :
			print(f"Il y a {nb_chains} chaines dans la molecule")
			#Création d'une liste qui comprend plusieurs chaines de la molécule
			liste_molecule = []
			molecule = Molecule.strip_chain(file,filename)
			#On ajoute le nombre de chaines en tant que attribut dans la molécule
			molecule.__molecule_chains__(nb_chains)
			return molecule
							

		#Pas d'information sur la chaine dans le fichier PDB alors on lit la molécule normalement
		if nb_chains == 0 :
			molecule = Molecule.create_molecule(file, filename)
			print("One molecule created (No chain informations)")
			return molecule
	
		
		
	#Calcul d'une matrice de distances d'une molécule (triangulaire pour reduire l'espace de stockage)

	def matrice_distance(self) :
		#On recupere les atomes (et leurs coordonnees!) de l'objet molecule
		liste_atomes = self.atoms	
		n = len(liste_atomes)

		#initialisation d'une matrice vide
		coords = np.zeros((n, 3))

		#Computation des coordonnées pour chaque atome
		for i, atom in enumerate(liste_atomes):
			coords[i] = [atom.x, atom.y, atom.z]

		#Calcul de la distance
		dist_array = pdist(coords, metric='euclidean')

		#Conversion en matrice
		matrice = squareform(dist_array)

		#L'objet retourne est une matrice triangulaire (0 sous la diagonale) pour optimiser l'espace
		print("La matrice de distances à bien été calculée")
		return(matrice)

	def cartes_contact(matrice, seuil=5):

		contact_mask = (matrice < seuil) & (matrice != 0)  # On ne fait pas attention à la diagonale

		#On met 1 si il y au contact, 0 si il n'y en a pas
		carte_contact = contact_mask.astype(float)

		#Tous les éléments de la diagonales sont égaux à 0 
		np.fill_diagonal(carte_contact, 0)

		return carte_contact
	
	def translation(self, sphere, radii_solvant = 1.52) :
		for atom in self.atoms :
			radii = radii_dict.get(atom.type)

			if radii is None :
				radii = radii_solvant

			atom.radii_atom(value = radii + radii_solvant)
			Sphere.translation(sphere, atom)

	#Calcul de l'accessibilité individuelle pour chaque atome
	def atomic_accessibility(self, n = 92, radii_solvant = 1.52) :

		print(f"On arrive au serieux du sujet : calcul du SASA pour chaque atome de {self.name}")

		TOTAL_SASA, POLAR_SASA, NON_POLAR_SASA = 0,0,0



		#Calcul de la matrice de distance
		matrice = Molecule.matrice_distance(self)

		#Carte de contact pour eviter de calculer l'accessibilité des atomes trop eloignés
		carte = Molecule.cartes_contact(matrice)

		sphere = Sphere.compute_sphere_golden_spiral(n = 92)


		#La partie "rolling ball"
		Molecule.translation(self, sphere, radii_solvant)

		#iteration sur chaque atome
		for i in range(0, len(self.atoms)) :
			atom = self.atoms[i]

			#On récupere la liste d'indices de voisins "proches" via la matrice carte contact: proche == 1
			voisins = indices_1 = np.where(carte[i] == 1)[0]

			#On part du principe que aucun point de la sphere est n'est accessible
			n_accessible = len(sphere)

			#Maintenant on va iterer sur chaque point de la sphère 
			for point in atom.Wan_der_Waals : 
				overlapping = False
				#On récupere l'indice de chaque voisin proche
				for indice in voisins :

					#On calcule la distance entre le point et le centre de la sphere de l'atome voisin
					#essentiel voir si il n'y a pas de superposition entre deux sphere
					#evite les calculs inutiles

					voisin = self.atoms[indice]	

					d =  Atom.calc_distance(Atom(x=point[0], y = point[1], z = point[2]), voisin)

					#calcul du ratio
					ratio = d / voisin.radii

					if ratio < 1  : 
						overlapping = True
						n_accessible -= 1
						#On arrete tous les calculs pour ce point
						break

				

			
			#On a le nombre d'atome accessibles
			#print(n_accessible)
			#Maintenant on va transformer ce nombre en une surface en A°^2

			#Surface de la sphere recouverte par un seul point
			rayon_sphere =  4 * math.pi * atom.radii ** 2 / len(sphere)


			surface_accessible = rayon_sphere * n_accessible

			TOTAL_SASA += surface_accessible

			if atom.classe :
				POLAR_SASA += surface_accessible
			else :
				NON_POLAR_SASA += surface_accessible




			#On modifie l'objet atom auquel on ajoute l'acessibilité
			atom.acess_atom(surface_accessible)
			#print(surface_accessible)
		
		print("TOTAL_SASA:", TOTAL_SASA)  # Check initial value

		#On remplit l'accessibilité totale en surface de la molecule en attribut
		self.__molecule_SASA__(TOTAL_SASA)
		self.__molecule_SASA_POLAR__(POLAR_SASA)
		self.__molecule_SASA_NON_POLAR__(NON_POLAR_SASA)



	def plot_acess(self):
		#Creation d'une liste vide pour les ordonnées
		y, x = [],[]

		#On compute l'accessibilité de chaque atome dans la liste vide
		for atom in self.atoms :
			y.append(atom.accessibility)
			x.append(atom.numres)

		#plt.plot(x, y, linestyle='-', color='navy') 
		plt.bar(x, y, color='navy') 

		plt.title(f'{self.name}')
		plt.xlabel('Numero de résidu')
		plt.ylabel('Surface exposée (Å²)')

		#plt.grid(True)

		legende = f""" Surface d'Accessibilité totale (Å²) : {round(self.accessibility,2)} \n Atomes Polaires : {round(self.polar_accessibility,2)} \n Atomes Non Polaires : {round(self.non_polar_accessibility,2)}"""
		plt.text(-0.1, -0.3, legende, transform=plt.gca().transAxes, fontsize=9)
		plt.tight_layout()
		plt.savefig(f"./static/plots/{self.name.replace(' ','_')}.png", dpi=2400)

		plt.close()



	def plot_acess_chains(self):
		color_map = {
        'A': 'navy',
        'B': 'black',
        'C': 'blue',
		"A'": 'red',
        "B'": 'pink',
        "C'": 'orange',

    }
		if self.nbchains is not None:
			x, y, colors, chain_labels = [], [], [], []
			for atom in self.atoms:
				y.append(atom.accessibility)
				x.append(atom.numres)

				chain_id = atom.chain
				colors.append(color_map.get(chain_id, 'gray'))


				#On ajoute la chaine à la liste des chaines disponibles pour la légence
				if atom.chain not in chain_labels:
					chain_labels.append(atom.chain)
			



			plt.bar(x, y, color=colors)

			plt.title(f'{self.name}')
			plt.xlabel('Numero de résidu')
			plt.ylabel('Surface exposée (Å²)')

			legend_elements = [plt.Line2D([0], [0], color=color_map[chain], lw=4, label=f'Chaine {chain}')
                           for chain in chain_labels]
			
			plt.legend(handles=legend_elements, title="Chaines")

			legende = f""" Surface d'Accessibilité totale (Å²) : {round(self.accessibility, 2)} \n Atomes Polaires : {round(self.polar_accessibility, 2)} \n Atomes Non Polaires : {round(self.non_polar_accessibility, 2)}"""
			plt.text(-0.1, -0.3, legende, transform=plt.gca().transAxes, fontsize=9)

			plt.tight_layout()
			plt.savefig(f"./static/plots/{self.name.replace(' ', '_')}.png", dpi=2400)

			plt.close()






			


	#Generation de l'accessibilité atomique, de graphique en une seule fonction
	def calcul_SASA(molecule, radii_solvant = 1.52, n = 92) :

		#Une seule chaine ou pas de chaine spécifiée
		if isinstance(molecule, Molecule) :

			molecule.atomic_accessibility(n, radii_solvant)

			if molecule.nbchains is None : 
				molecule.plot_acess()

			else :
				molecule.plot_acess_chains()
		print(molecule)

	





		

    
