from graphics import *
from gestion_terrain import *
import time
import pygame
from math import cos, sin, pi
from typing import List, Tuple, Dict
from utilitaire import *

FPS = 60
DPF = 1/FPS
TAILLE_ECRAN = (1280,720)
TIME_UNTIL_FPS_AVERAGE = 1.0
TANK_MAX_SPEED = 5
TANK_ACCELERATION = 20.0
TANK_FRICTION = 10.0
TANK_SIZE = 50
TANK_VITESSE_ROTATION = 135 # en degrée par seconde
TAILLE_PETIT_CANON = pi/8
TAILLE_GRAND_CANON = pi/6
TANK_RECULE = 10


COSMETIC_TANK = {
    "TAILLE_TANK" : 50,
    "RAYON_PETIT_CANON" : pi/12, # en radian
    "RAYON_GRAND_CANON" : pi/24, # en radian
    "TAILLE_PETIT_CANON" : 0.38,
    "TAILLE_GRAND_CANON" : 1.0,
    "TAILLE_CERCLE" : 0.3 # en pourcentage
}



chrono_loop = "chrono_loop"

Coord = List[float]
Tank = Dict
    
# Mathis (5)
def draw_tank(tank_q : Tank):
    tank = tank_q["coord"]
    rotation = tank_q["rotation"]
    couleur = tank_q["couleur"]

    mid_x, mid_y = (tank[0] + TANK_SIZE/2, tank[1] + TANK_SIZE/2)
    points = [
        (tank[0], tank[1]), # top left
        (tank[0] + TANK_SIZE, tank[1]), # top right
        (tank[0] + TANK_SIZE, tank[1] + TANK_SIZE), # bottom right
        (tank[0], tank[1] + TANK_SIZE) # bottom left
    ]
    rotated_points = []
    for point in points:

        x, y = point
        rotated_x = mid_x + (x - mid_x) * math.cos(rotation) - (y - mid_y) * math.sin(rotation)
        rotated_y = mid_y + (x - mid_x) * math.sin(rotation) + (y - mid_y) * math.cos(rotation)
        rotated_points.append((rotated_x, rotated_y))

    # Draw an arrow at the front of the tank from the middle of the tank to the middle front of the tank (middle right at 0 degree)
    affiche_triangle_plein(rotated_points[0], rotated_points[1], rotated_points[2], couleur)
    affiche_triangle_plein(rotated_points[0], rotated_points[2], rotated_points[3], couleur)
    milieu_du_tank = mid_x, mid_y
    affiche_cercle(milieu_du_tank, int(TANK_SIZE*0.4), noir, 3)

    # Canon
    affiche_triangle_plein(
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.cos(rotation + COSMETIC_TANK["RAYON_PETIT_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.sin(rotation + COSMETIC_TANK["RAYON_PETIT_CANON"])
        ),
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.cos(rotation + COSMETIC_TANK["RAYON_GRAND_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.sin(rotation + COSMETIC_TANK["RAYON_GRAND_CANON"])
        ),
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.cos(rotation - COSMETIC_TANK["RAYON_GRAND_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.sin(rotation - COSMETIC_TANK["RAYON_GRAND_CANON"])
        ),
        noir
    )
    # for the other side
    affiche_triangle_plein(
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.cos(rotation - COSMETIC_TANK["RAYON_PETIT_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.sin(rotation - COSMETIC_TANK["RAYON_PETIT_CANON"])
        ),
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.cos(rotation - COSMETIC_TANK["RAYON_GRAND_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_GRAND_CANON"])*math.sin(rotation - COSMETIC_TANK["RAYON_GRAND_CANON"])
        ),
        (
            mid_x + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.cos(rotation + COSMETIC_TANK["RAYON_PETIT_CANON"]),
            mid_y + (TANK_SIZE*COSMETIC_TANK["TAILLE_PETIT_CANON"])*math.sin(rotation + COSMETIC_TANK["RAYON_PETIT_CANON"])
        ),
        noir
    )
    # and now 4 lines around the tank
    affiche_ligne(rotated_points[0],rotated_points[1],noir)
    affiche_ligne(rotated_points[1],rotated_points[2],noir)
    affiche_ligne(rotated_points[2],rotated_points[3],noir)
    affiche_ligne(rotated_points[3],rotated_points[0],noir)

# Alexandre (4)
def obtenir_centre_tank(tank : Tank):
    return addition_tuple(tank["coord"],(TANK_SIZE/2,TANK_SIZE/2))

# Quentin (2)
def detection_collision(next_x, next_y, terrain):
    """
    Détecte si un tank à la position (next_x, next_y) entre en collision avec un obstacle.

    Args:
        next_x (float): Position X prévue du tank
        next_y (float): Position Y prévue du tank
        terrain (dict): Dictionnaire représentant le terrain

    Returns:
        bool: True s'il y a collision, False sinon
    """
    # 4 coins autour de (next_x, next_y)
    corners = [
        (next_x, next_y),
        (next_x + TANK_SIZE, next_y),
        (next_x, next_y + TANK_SIZE),
        (next_x + TANK_SIZE, next_y + TANK_SIZE)
    ]

    for (cx, cy) in corners:
        i, j = coordonnee_vers_casse((cx, cy))
        if not dans_terain((i, j)) or terrain[i, j]["objet"] != "sol":
            #print("Collision")
            return True

    return False

# Mathis (1)
def step(tank1 : Tank, delta_time, terrain):
    # if cercle[0] > 480:
    #     cercle[0] = cercle[0] % 480
    # else:
    #     cercle[0] += delta_time * 300

    fleche = get_fleches()

    touches = {
        "gauche" : touche_enfoncee(tank1["touche"]["gauche"]),
        "droite" : touche_enfoncee(tank1["touche"]["droite"]),
        "haut" : touche_enfoncee(tank1["touche"]["haut"]),
        "bas" : touche_enfoncee(tank1["touche"]["bas"]),
        #"rotation_gauche" : touche_enfoncee(tank1["touche"]["rotation_gauche"]),
        #"rotation_droite" : touche_enfoncee(tank1["touche"]["rotation_droite"])
    }


    tank1["vitesse"] = clamp(tank1["vitesse"] + (int(touches["haut"]) - int(touches["bas"])) * delta_time * tank1["acceleration"], -TANK_MAX_SPEED, TANK_MAX_SPEED)
    tank1["vitesse"] -= sign(tank1["vitesse"]) * delta_time * TANK_FRICTION
    if abs(tank1["vitesse"]) < 0.1:
        tank1["vitesse"] = 0

    next_x : float = (tank1["coord"][0] + cos(tank1["rotation"]) * tank1["vitesse"])
    next_y : float = (tank1["coord"][1] + sin(tank1["rotation"]) * tank1["vitesse"])

    # Utiliser la nouvelle fonction de détection de collision
    collision = detection_collision(next_x, next_y, terrain)


    if not collision:
        tank1["coord"] = [next_x,next_y]
    else:
        # Parti du code pour slide
        
        if not detection_collision(next_x, tank1["coord"][1], terrain):
            tank1["coord"][0] = next_x
        elif not detection_collision(tank1["coord"][0], next_y, terrain):
            tank1["coord"][1] = next_y
            

    tank1["rotation"] += (int(touches["gauche"]) - int(touches["droite"])) * (delta_time * (2*pi/360*TANK_VITESSE_ROTATION))

# Mathis (6)
def tire_misile(joueur_a,joueur_b,misiles,terain): 

    distance_spawn_balle = TANK_SIZE + 10

    delta_a = (distance_spawn_balle*cos(joueur_a["rotation"]),distance_spawn_balle*sin(joueur_a["rotation"]))
    delta_b = (distance_spawn_balle*cos(joueur_b["rotation"]),distance_spawn_balle*sin(joueur_b["rotation"]))

    point_a = addition_tuple(obtenir_centre_tank(joueur_a),delta_a)
    point_b = addition_tuple(obtenir_centre_tank(joueur_b),delta_b)

    joueur_a["bout_du_canon"] = point_a
    joueur_b["bout_du_canon"] = point_b

    for joueur in [joueur_a,joueur_b]:
        if touche_enfoncee(joueur["touche"]["tirer"]) and joueur["can_fier"]:
            misiles.append({"direction": joueur["rotation"], "joueur": "A", "coord": joueur["bout_du_canon"]})
            joueur["vitesse"] -= TANK_RECULE
            joueur["can_fier"] = False
        elif not touche_enfoncee(joueur["touche"]["tirer"]):
            joueur["can_fier"] = True

# Quentin (8)
def deplace_misile(misiles,delta_time,terain,TANK_1 ,TANK_2):
    vitesse_missile = 400  # pixels/sec, choisis ce que tu veux

    missiles_a_supprimer = []  # liste pour stocker les missiles détruits

    for missile in misiles:
        direction = missile["direction"]
        x, y = missile["coord"]
        collision_missile_tank(missile,TANK_1 ,TANK_2,missiles_a_supprimer)

        # Avancer le missile
        next_x = x + cos(direction) * vitesse_missile * delta_time
        next_y = y + sin(direction) * vitesse_missile * delta_time

        # Vérification collision
        i, j = coordonnee_vers_casse((next_x, next_y))
        if not dans_terain((i, j)) or terain[i, j]["objet"] != "sol":
            missiles_a_supprimer.append(missile)
            continue


        # Pas de collision alors on peut déplacer
        missile["coord"] = (next_x, next_y)
        draw_misiles(missile)

    # Supprimer les missiles qui ont touché un mur ou sont sortis | Pour éviter les probleme
    for missile in missiles_a_supprimer:
        misiles.remove(missile)

# Quentin (7)
def draw_misiles(misiles):
    taille_missile = 20
    x,y = addition_tuple(misiles["coord"],(-taille_missile/2,-taille_missile/2))
    # Redimensionner l'image du missile en conservant les proportions
    # Taille appropriée pour un missile (ajustez selon vos besoins)
    
    modifie_taille_image("missile.png", taille_missile, taille_missile, conserver_proportions=True, smooth=True)
    modifie_transparence("missile.png",(0,255,0),alpha=100)
    
    #affiche_cercle_plein((x,y),taille_missile,rouge)
    affiche_image("missile.png",(x,y))

# Quentin (9)
def collision_missile_tank(missile,TANK_1 ,TANK_2,missiles_a_supprimer):
    x_missile, y_missile = missile["coord"]

    # Zone du tank 1
    x1, y1 = TANK_1["coord"]
    if x1 <= x_missile and x_missile <= x1 + TANK_SIZE and y1 <= y_missile and y_missile <= (y1 + TANK_SIZE):
        missiles_a_supprimer.append(missile)
        TANK_1["vie"] -= 1

    # Zone du tank 2
    x2, y2 = TANK_2["coord"]
    if x2 <= x_missile and x_missile <= x2 + TANK_SIZE and y2 <= y_missile and y_missile <= y2 + TANK_SIZE:
        missiles_a_supprimer.append(missile)
        TANK_2["vie"] -= 1

# Alexandre (10)
def jeu_fini(TANK_1 ,TANK_2):
    if TANK_1["vie"] == 0:
        remplir_fenetre(blanc)
        affiche_texte(f"Le joueur 2 a gagné",(200,300),rouge,50)
        affiche_tout()
        return True
    if TANK_2["vie"] == 0:
        remplir_fenetre(blanc)
        affiche_texte(f"Le joueur 1 a gagné",(200,300),rouge,50)
        affiche_tout()
        return True

# Alexandre (0)
def main():
    init_fenetre(*TAILLE_ECRAN,"Tank la revanche.")
    terrain = init_terrain("terain.txt")
    misiles = []
    Jeu_fini = False
    TANK_1 : Tank = {
        "coord" : [casse_vers_coordonee(trouve_cordonet_joueur("joueur_b",terrain))[0],casse_vers_coordonee(trouve_cordonet_joueur("joueur_b",terrain))[1]],
        "rotation" : 0.0,
        "couleur" : rouge,
        "vie" : 3,
        "vitesse" : 0,
        "acceleration" : TANK_ACCELERATION,
        "touche" : {
            "gauche" : "K_a",
            "droite" : "K_d",
            "haut" : "K_w",
            "bas" : "K_s",
            "rotation_gauche" : "K_q",
            "rotation_droite" : "K_e",
            "tirer" : "K_SPACE"
        }
    }

    TANK_2 : Tank = {
        "coord" : [casse_vers_coordonee(trouve_cordonet_joueur("joueur_a",terrain))[0],casse_vers_coordonee(trouve_cordonet_joueur("joueur_a",terrain))[1]],
        "rotation" : 0.0,
        "couleur" : bleu,
        "vie" : 3,
        "vitesse" : 0,
        "acceleration" : TANK_ACCELERATION,
        "touche" : {
            "gauche" : "K_LEFT",
            "droite" : "K_RIGHT",
            "haut" : "K_UP",
            "bas" : "K_DOWN",
            "rotation_gauche" : "K_KP7",
            "rotation_droite" : "K_KP9",
            "tirer" : "K_l"
        }
    }

    init_chrono(chrono_loop)
    lance_chrono(chrono_loop)

    delta_time : float = 0.01
    last_chronos_time = 0
    frames : int = 0
    act_time = 0
    frame_array = [0]
    displayed_frame_array = [0]
    TUFA_last_refresh = 0
    affiche_auto_off()

    while pas_echap():
        if not jeu_fini(TANK_1 ,TANK_2):
            Jeu_fini = jeu_fini(TANK_1 ,TANK_2)

            affiche_terrain(terrain)
            # Code Ici
            #remplir_fenetre(blanc)
            step(TANK_1,delta_time,terrain)
            step(TANK_2,delta_time,terrain)
            draw_tank(TANK_1)
            draw_tank(TANK_2)

            #for tank in [TANK_1,TANK_2]:
                #affiche_cercle_plein(tank.get("bout_du_canon",(0,0)),30,vert)
            #tire des misile
            tire_misile(TANK_1,TANK_2,misiles,terrain)
            deplace_misile(misiles,delta_time,terrain,TANK_1 ,TANK_2)
            #collision_missile_tank(misiles, TANK_1, TANK_2)
            #fait_chier = fait_chier + (delta_time * ((2*pi/360)*45))
            affiche_texte(f"FPS : {round(1/delta_time)}/{FPS}",(0,22),noir,20)
            affiche_texte(f"FPS Avg: {round(moyenne_array(displayed_frame_array),1)} - 0.1% Low : {min_array(displayed_frame_array)} - Frames : {frames}",(0,0),noir,20)
            affiche_texte(f"Vie Tank 1 : {TANK_1['vie']}",(1,580),rouge,20)
            affiche_texte(f"Vie Tank 2 : {TANK_2['vie']}",(830,580),bleu,20)
            # Gestion de la framerate


            (act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array) = frame_handling(act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array)
            #clock.tick(FPS)
        else :# Si le jeu est fini, attendre un clic avant de recommencer
            wait_clic()
            terrain = init_terrain("terain.txt")
            misiles = []
            TANK_1 : Tank = {
                "coord" : [casse_vers_coordonee(trouve_cordonet_joueur("joueur_b",terrain))[0],casse_vers_coordonee(trouve_cordonet_joueur("joueur_b",terrain))[1]],
                "rotation" : 0.0,
                "couleur" : rouge,
                "vie" : 3,
                "vitesse" : 0,
                "acceleration" : TANK_ACCELERATION,
                "touche" : {
                    "gauche" : "K_a",
                    "droite" : "K_d",
                    "haut" : "K_w",
                    "bas" : "K_s",
                    "rotation_gauche" : "K_q",
                    "rotation_droite" : "K_e",
                    "tirer" : "K_SPACE"
                }
            }

            TANK_2 : Tank = {
                "coord" : [casse_vers_coordonee(trouve_cordonet_joueur("joueur_a",terrain))[0],casse_vers_coordonee(trouve_cordonet_joueur("joueur_a",terrain))[1]],
                "rotation" : 0.0,
                "couleur" : bleu,
                "vie" : 3,
                "vitesse" : 0,
                "acceleration" : TANK_ACCELERATION,
                "touche" : {
                    "gauche" : "K_LEFT",
                    "droite" : "K_RIGHT",
                    "haut" : "K_UP",
                    "bas" : "K_DOWN",
                    "rotation_gauche" : "K_KP7",
                    "rotation_droite" : "K_KP9",
                    "tirer" : "K_RSHIFT"
                }
            }


if __name__ == "__main__":
    main()

