from graphics import *

chaine = "vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;\nvide,pas_joueur,pas_missile;\nvide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;vide,pas_joueur,pas_missile;"

def str_ver_dictionaire(chaine):
    grille = {}
    lignes = chaine.strip().split("\n")

    for y, ligne in enumerate(lignes):
        print(y)
        cellules = ligne.strip().split(";")
        for x, cellule in enumerate(cellules):
            if cellule:  # éviter les vides s’il y a un ";" en trop
                infos = cellule.split(",")
                grille[(x, y)] = {
                "type": infos[0],
                "joueur": infos[1],
                "missile": infos[2]
            }
    return(grille)




def init_terrain(fichier):
    terrain = {}
    with open(fichier, "r") as f:
        contenu = f.read()
        return(str_ver_dictionaire(contenu))

print(init_terrain("terain.txt"))
