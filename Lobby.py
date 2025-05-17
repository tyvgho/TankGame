from graphics import *
from typing import Dict, Tuple, List
import gestion_terrain
from utilitaire import *
import main as main_tank

Coordonnee = Tuple[int, int]
Couleur = Tuple[int, int, int, int]
Bouton = Dict

bouton_par_defaut : Bouton = {
    "position" : (0,0),
    "taille" : (0,0),
    "texte" : "Jouer",
    "couleur" : (0,0,0),
    "couleur_selectionnee" : (0,0,0),
    "texte_selectionne" : "Jouer",
    "survolee" : False,
    "fonction" : None
}

def afficher_bouton(bouton : Bouton):
    couleur = bouton["couleur"]
    texte = bouton["texte"]
    if bouton["survolee"]:
        couleur = bouton["couleur_selectionnee"]
        texte = bouton["texte_selectionne"]
        
    affiche_rectangle(bouton["position"], addition_tuple(bouton["position"], bouton["taille"]), couleur)
    affiche_texte_centre(texte, addition_tuple(bouton["position"],multiplication_tuple(bouton["taille"],0.5)), couleur, bouton["taille"][1]-10)

def comportement_bouton(clic : Coordonnee, clique : bool, boutons : List[Bouton]):
    cx, cy = clic
    for bouton in boutons:
        bx, by = bouton["position"]
        tx, ty = addition_tuple(bouton["position"], bouton["taille"])
        if cx >= bx and cx <= tx and cy >= by and cy <= ty:
            if clique:
                bouton["fonction"]()
            else:
                bouton["survolee"] = True
        else:
            bouton["survolee"] = False
        afficher_bouton(bouton)

def main():
    affiche_auto_off()
    init_fenetre(500, 400, "Affichage du mur")

    bouton = bouton_par_defaut.copy()
    bouton["position"] = (100,100)
    bouton["taille"] = (200,50)
    bouton["texte"] = "Jouer"
    bouton["couleur"] = (255,0,0)
    bouton["couleur_selectionnee"] = (0,255,0)
    bouton["texte_selectionne"] = "Jouer !"
    bouton["fonction"] = main_tank.main
    
    bouton2 = bouton_par_defaut.copy()
    bouton2["position"] = (100,300)
    bouton2["taille"] = (200,50)
    bouton2["texte"] = "Quitter"
    bouton2["couleur"] = (255,0,0)
    bouton2["couleur_selectionnee"] = (0,255,0)
    bouton2["texte_selectionne"] = "Quitter"
    
    bouton2["fonction"] = lambda: exit()

    bouton3 = bouton_par_defaut.copy()
    bouton3["position"] = (100,200)
    bouton3["taille"] = (200,50)
    bouton3["texte"] = "Modifier"
    bouton3["couleur"] = (255,0,0)
    bouton3["couleur_selectionnee"] = (0,255,0)
    bouton3["texte_selectionne"] = "Editeur"
    
    bouton3["fonction"] = gestion_terrain.edyte_terain
    print(bouton["fonction"])


    delta_time : float = 0.01
    last_chronos_time = 0
    frames : int = 0
    act_time = 0
    frame_array = [0]
    displayed_frame_array = [0]
    TUFA_last_refresh = 0
    clic = (0,0)

    while pas_echap():

        remplir_fenetre(blanc)
        act_time = time.time()
        clic = obtenir_position_curseur()
        comportement_bouton(clic, souris_cliquee(), [bouton,bouton2,bouton3])

        (act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array) = frame_handling(act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array)


main()