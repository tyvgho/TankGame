from graphics import *

# Initialisation de la fenêtre
init_fenetre(500, 400, "Affichage du mur")

# Chargement de l'image du mur
charge_image("mur.png")

# Boucle principale
while pas_echap():
    # Affichage de l'image du mur au point (100, 100)
    affiche_image("mur.png", (100, 100))
    
    # Mise à jour de l'affichage
    affiche_tout()