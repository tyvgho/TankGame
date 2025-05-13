from main import *
from graphics import *
import csv
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename

TYPE_CASES_MAX = 5  #TYPE_SOL + TYPE_MUR + TYPE_PORTE = (0,1,2)

# Alexandre
def init_cases() -> List[List[int]]:
    """Retourne une matrice de taille TAILLE_TERRAIN remplie de TYPE_SOL"""
    return [[TYPE_SOL for _ in range(TAILLE_TERRAIN[0])] for _ in range(TAILLE_TERRAIN[1])]

def affiche_terrain_editeur(cases : Cases):
    """Affiche le terrain dans l'editeur"""
    for cy, ligne in enumerate(cases):
        for cx, _case in enumerate(ligne):
            affiche_case((cx,cy),obtenir_couleur_case(cases,(cx,cy),COULEUR_CASES[cases[cy][cx]]))

def exporter_terrain_csv(cases, fichier = "level.csv"):
    print(f"Exportation du terrain dans le fichier '{fichier}'")
    with open(fichier, "w") as f:
        w = csv.writer(f)
        w.writerows(cases)
    print("Exporter avec succès.")

PRESET_CASE = {
    0 : {}
}

def importer_terrain_csv(fichier = "level.csv") -> Cases:
    with open(fichier) as f:
        r = csv.reader(f)
        cases = []
        for line in r:
            if len(line) == 0:
                continue
            ligne = []
            for element in line:
                ligne.append(PRESET_CASE[int(element)])
            cases.append(ligne)
    return cases


def obtenir_couleur_case_editeur(cases : Cases, coord : Coord, couleur_forcee : Couleur = None) -> Couleur:
    """
    La couleur est modifiée pour que les cases pair ont une couleur plus claire que les cases impairs.
    La fonction renvoie une couleur de type `Couleur`.
    """
    if couleur_forcee is None:
        _case = obtenir_case(cases, coord)
        couleur = noir
        if _case in COULEUR_CASES:
            couleur = COULEUR_CASES[_case]
        if (coord[0]+coord[1])%2==0:
            couleur = addition_tuple(couleur,(COULEUR_ALTERNATIVE,COULEUR_ALTERNATIVE,COULEUR_ALTERNATIVE,0))
            couleur = clamp_tuple(couleur,0,255)
        return couleur
    #Si couleur_forcee est une couleur
    couleur = couleur_forcee
    if (coord[0]+coord[1])%2==0:
            couleur = addition_tuple(couleur_forcee,(COULEUR_ALTERNATIVE,COULEUR_ALTERNATIVE,COULEUR_ALTERNATIVE,0)) # Augmente la couleur de 20 pour avoir une couleur plus claire (RGB)
            couleur = clamp_tuple(couleur,0,255) # Evite les erreur de couleur min (0,0,0) max (255,255,255)
    return couleur
def comportement_editeur(cases : Cases, clic : Coord, ennemies : List[Coord], joueur : Coord):
    i, j = fenetre_vers_grille(*clic)

    decalage_case = (TAILLE_FENETRE[0] % TAILLE_CASE, TAILLE_FENETRE[1] % TAILLE_CASE)

    if (i < TAILLE_TERRAIN[0]) and (j < TAILLE_TERRAIN[1]):
        cases[j][i] = (obtenir_case(cases,(i,j)) + 1) % TYPE_CASES_MAX
        #couleur = clamp_tuple(couleur, 0, 255)  # Évite les erreurs de dépassement de couleur
        affiche_case((i,j),obtenir_couleur_case_editeur(cases,(i,j),COULEUR_CASES[cases[j][i]]))
        print("Case modifiée : (",i,",",j,") ->",NOM_CASES[obtenir_case(cases,(i,j))])
    else:
        print("Hors terrain : (",i,",",j,")")
        if i > 0 and i < 4: # Sauvegarder
            exporter_terrain_csv(
                cases,
                fichier=asksaveasfilename(
                    filetypes = [("Fichiers CSV","*.csv")],
                    title= "Exporter un terrain d'un fichier *.csv",
                    initialdir = "./",
                    defaultextension=".csv"
                )
            )
        if i > 4 and i < (4+3): # Charger
            ennemies.clear()
            joueur = (0,0)
            cases, joueur, ennemies = init_terrain(
                askopenfilename(
                    filetypes = [("Fichiers CSV","*.csv")],
                    title= "Importer un terrain d'un fichier *.csv",
                    initialdir = "./",
                    defaultextension=".csv"
                )
            )
            affiche_jeu(cases, joueur, ennemies, 0, 0)

def main_editeur():
    init_fenetre(*TAILLE_FENETRE,"Hello guys ! [EDITEUR]")
    cases = init_cases()
    position_joueur = (0,0)
    positions_ennemies = []
    fermer_jeu = False
    affiche_terrain_editeur(cases)
    
    if (TAILLE_FENETRE[1] % TAILLE_CASE) > 0:
        y = TAILLE_FENETRE[1]
        bordure_y = TAILLE_FENETRE[1] % TAILLE_CASE
        taille_bouton_sauvegarder = TAILLE_CASE * 4
        taille_bouton_charger = taille_bouton_sauvegarder + TAILLE_CASE * 3
        centre_bouton_sauvegarder = taille_bouton_sauvegarder // 2
        centre_bouton_charger =  taille_bouton_sauvegarder + (TAILLE_CASE * 3)//2
        affiche_rectangle_plein((0,y),(taille_bouton_sauvegarder,y-bordure_y),rouge)
        affiche_rectangle_plein((taille_bouton_sauvegarder,y),(taille_bouton_charger,y-bordure_y),bleu)
        affiche_rectangle_plein((taille_bouton_charger,y),(TAILLE_FENETRE[0],y-bordure_y),blanc)
        affiche_texte_centre("Sauvegarder",(centre_bouton_sauvegarder,y-(bordure_y)//2),blanc,taille_police = bordure_y,police = "mono")
        affiche_texte_centre("Charger",(centre_bouton_charger,y-(bordure_y)//2),blanc,taille_police = bordure_y,police = "mono")

    while pas_echap():
        clic = wait_clic()
        comportement_editeur(cases,clic, positions_ennemies, position_joueur)
    exit(0)

print("editeur.py name -> ",__name__)
if __name__ == "__main__":
    main_editeur()