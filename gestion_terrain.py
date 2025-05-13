from graphics import *
import utilitaire
taille_cases = 50
hauteur_fenetre = 600
largeur_fenetre = 1000
nb_ligne = largeur_fenetre//taille_cases
nb_colone = hauteur_fenetre//taille_cases
misiles = []
joueur_a = {"nom":"joueur_a","vie":10,"position":(0,0)}
joueur_b = {"nom":"joueur_b","vie":10,"position":(nb_ligne-1,nb_colone-1)}#-1 car on conte appartire de la ligne et colone 0

# Chargement de la texture de mur


def importer_image(image_path):
    return Image.open(image_path)

def dans_terain(coordoner):
    x,y = coordoner
    return (x < nb_ligne and y < nb_colone and x > -1 and y > -1)


def aditione_tuple(t1,t2):
    return utilitaire.addition_tuple(t1,t2)


def str_ver_dictionaire(chaine):
    grille = {}
    lignes = chaine.strip().split("\n")

    for y, ligne in enumerate(lignes):
        cellules = ligne.strip().split(";")
        for x, cellule in enumerate(cellules):
            if cellule:  # éviter les vides s’il y a un ";" en trop
                infos = cellule.split(",")
                grille[(y,x)] = {
                "objet": infos[0],
                "joueur": infos[1],
                "missile": infos[2]
            }
    return(grille)

def init_terrain(fichier):
    terrain = {}
    with open(fichier, "r") as f:
        contenu = f.read()
        terrain = str_ver_dictionaire(contenu)
        joueur_a["position"] = trouve_cordonet_joueur("joueur_a",terrain)
        joueur_b["position"] = trouve_cordonet_joueur("joueur_b",terrain)
        return terrain

def trouve_cordonet_joueur(nom_joueur,terrain):
    for cle, valeur in terrain.items():
       for cle2, valeur2 in valeur.items():
            if valeur2 == nom_joueur:
                return cle



def affiche_terrain(terrain):
    # Affiche tout le terrain à l'écran
    for i in range(nb_ligne):
        for j in range(nb_colone):
            if terrain[i,j]["objet"] == "sol":
                modifie_taille_image("herbe.png", taille_cases, taille_cases)
                affiche_image("herbe.png", casse_vers_coordonee((i,j)))
            elif terrain[i,j]["objet"] == "mur":
                # Utiliser la texture de mur au lieu d'un carré noir
                # Redimensionner l'image en conservant les proportions et en utilisant smoothscale
                modifie_taille_image("mur.png", taille_cases, taille_cases)
                affiche_image("mur.png", casse_vers_coordonee((i,j)))
            if terrain[i,j]["joueur"] == "joueur_a":
                affiche_rectangle_plein(casse_vers_coordonee((i,j)),casse_vers_coordonee((i+1,j+1)),bleu)
            elif terrain[i,j]["joueur"] == "joueur_b":
                affiche_rectangle_plein(casse_vers_coordonee((i,j)),casse_vers_coordonee((i+1,j+1)),rouge)
            if terrain[i,j]["missile"] == "missile_a":
                affiche_rectangle_plein(casse_vers_coordonee((i,j)),casse_vers_coordonee((i+1,j+1)),vert)
            elif terrain[i,j]["missile"] == "missile_b":
                affiche_rectangle_plein(casse_vers_coordonee((i,j)),casse_vers_coordonee((i+1,j+1)),violet)


def coordonnee_vers_casse(co):
    x,y = co
    case_i = int(x // taille_cases)
    case_j = int(y // taille_cases)
    return (case_i, case_j)

def casse_vers_coordonee(co):
    i,j =co
    case_x = i * taille_cases
    case_y = j * taille_cases

    return (case_x, case_y)


def main_a():
    init_fenetre(largeur_fenetre, hauteur_fenetre, "Tank La Revanche")
    affiche_auto_off
    terrain = init_terrain("terain.txt")  # Il faut stocker le terrain retourné
    while pas_echap():
        affiche_terrain(terrain)
        affiche_tout
        attendre(10)



def edyte_terain():
    init_fenetre(largeur_fenetre, hauteur_fenetre, "Tank La Revanche")
    remplir_fenetre(blanc)
    affiche_auto_off()
    fichier = open("terain.txt","w")
    for i in range(nb_ligne):
        for j in range(nb_colone):
            fichier.write("sol,pas_joueur,pas_missile;")
        fichier.write("\n")
    fichier.close()
    terrain = init_terrain("terain.txt")
    affiche_terrain(terrain)
    affiche_tout()
    while pas_echap():
        clic = wait_clic()
        x,y = clic
        clic_i ,clic_j = coordonnee_vers_casse((x,y))
        if touche_enfoncee('K_s'):
            fichier = open("terain.txt","w")
            for i in range(nb_ligne):
                for j in range(nb_colone):
                    objet = terrain[i,j]["objet"]
                    joueur = terrain[i,j]["joueur"]
                    missile = terrain[i,j]["missile"]
                    fichier.write(f"{objet},{joueur},{missile};")
                fichier.write("\n")
            print("sauvgarde_efectuer")
            fichier.close()
        if clic_j > nb_colone-1 or clic_i >nb_ligne-1:
            pass
        else:
            if terrain[clic_i,clic_j]["objet"] == "sol"and not touche_enfoncee('K_a') and not touche_enfoncee('K_b'):
                terrain[clic_i,clic_j]["objet"] = "mur"
            else :
                terrain[clic_i,clic_j]["objet"] = "sol"
            get_fleches()  # Obligatoire pour que les événements clavier soient mis à jour
            if touche_enfoncee('K_a'):
                terrain[clic_i,clic_j]["joueur"] = "joueur_a"
            if touche_enfoncee('K_b'):
                terrain[clic_i,clic_j]["joueur"] = "joueur_b"

            affiche_terrain(terrain)
            affiche_tout()

if __name__ == "__main__":
    edyte_terain()