import pygame
import random

# Initialisation de pygame
pygame.init()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (213, 50, 80)
vert = (0, 255, 0)
bleu = (50, 153, 213)

# Dimensions de l'écran
largeur_ecran = 900
hauteur_ecran = 700

# Taille du serpent
taille_serpent = 10

# Vitesse par défaut et difficulté
vitesse_serpent = 10
difficulte = 0

# Police
police_score = pygame.font.SysFont("arial", 25)
police_menu = pygame.font.SysFont("arial", 40)

# Initialisation de l'écran
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption('Snake Game')

horloge = pygame.time.Clock()

# Fonction pour afficher le score
def afficher_score(score):
    valeur = police_score.render("Score: " + str(score), True, blanc)
    ecran.blit(valeur, [0, 0])

# Fonction pour le menu de difficulté
def menu_difficulte():
    global vitesse_serpent, difficulte
    en_menu = True

    while en_menu:
        ecran.fill(bleu)
        titre = police_menu.render("Choisissez la difficulté", True, blanc)
        facile = police_menu.render("1: Facile (Vitesse: 10)", True, blanc)
        normal = police_menu.render("2: Normal (Vitesse: 15)", True, blanc)
        difficile_option = police_menu.render("3: Difficile (Vitesse: 20)", True, blanc)

        ecran.blit(titre, [largeur_ecran / 6, hauteur_ecran / 3])
        ecran.blit(facile, [largeur_ecran / 6, hauteur_ecran / 2])
        ecran.blit(normal, [largeur_ecran / 6, hauteur_ecran / 2 + 50])
        ecran.blit(difficile_option, [largeur_ecran / 6, hauteur_ecran / 2 + 100])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    vitesse_serpent = 10
                    difficulte = 0
                    en_menu = False
                elif event.key == pygame.K_2:
                    vitesse_serpent = 15
                    difficulte = 5
                    en_menu = False
                elif event.key == pygame.K_3:
                    vitesse_serpent = 20
                    difficulte = 10
                    en_menu = False

# Fonction principale du jeu
def jeu_snake():
    global vitesse_serpent, difficulte
    game_over = False
    game_close = False

    x = largeur_ecran / 2
    y = hauteur_ecran / 2

    x_change = 0
    y_change = 0

    serpent = []
    longueur_serpent = 1

    nourriture_x = round(random.randrange(0, largeur_ecran - taille_serpent) / 10.0) * 10.0
    nourriture_y = round(random.randrange(0, hauteur_ecran - taille_serpent) / 10.0) * 10.0

    while not game_over:

        while game_close:
            ecran.fill(bleu)
            message = police_score.render("Game Over! Appuie sur C pour rejouer ou Q pour quitter", True, rouge)
            ecran.blit(message, [largeur_ecran / 6, hauteur_ecran / 3])
            afficher_score(longueur_serpent - 1)
            pygame.display.update()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jeu_snake()  

        # Gestion des touches de direction (Flèches et ZQSD)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    x_change = -taille_serpent
                    y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = taille_serpent
                    y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_z:
                    y_change = -taille_serpent
                    x_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = taille_serpent
                    x_change = 0
                elif event.key == pygame.K_SPACE:
                    vitesse_serpent *= 2   
                elif event.key == pygame.K_LSHIFT:
                    vitesse_serpent = 5  

            # Rétablir la vitesse par défaut
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    vitesse_serpent = 10 + difficulte
                if event.key == pygame.K_LSHIFT:
                    vitesse_serpent = 10 + difficulte

        # Vérification des limites de l'écran
        if x >= largeur_ecran or x < 0 or y >= hauteur_ecran or y < 0:
            game_close = True

        x += x_change
        y += y_change
        ecran.fill(noir)

        # Dessiner la nourriture
        pygame.draw.rect(ecran, vert, [nourriture_x, nourriture_y, taille_serpent, taille_serpent])

        # Mouvement du serpent
        tete_serpent = []
        tete_serpent.append(x)
        tete_serpent.append(y)
        serpent.append(tete_serpent)

        if len(serpent) > longueur_serpent:
            del serpent[0]

        # Si le serpent se mord lui-même
        for segment in serpent[:-1]:
            if segment == tete_serpent:
                game_close = True

        # Dessiner le serpent
        for i, segment in enumerate(serpent):
            if i == len(serpent) - 1:  # La tête du serpent
                pygame.draw.rect(ecran, rouge, [segment[0], segment[1], taille_serpent, taille_serpent])
            else:  # Le corps du serpent
                pygame.draw.rect(ecran, blanc, [segment[0], segment[1], taille_serpent, taille_serpent])

        # Si le serpent mange la nourriture
        if x == nourriture_x and y == nourriture_y:
            nourriture_x = round(random.randrange(0, largeur_ecran - taille_serpent) / 10.0) * 10.0
            nourriture_y = round(random.randrange(0, hauteur_ecran - taille_serpent) / 10.0) * 10.0
            longueur_serpent += 1

        afficher_score(longueur_serpent - 1)

        pygame.display.update()

        horloge.tick(vitesse_serpent)

    pygame.quit()
    quit()

# Lancer le menu de difficulté puis le jeu
menu_difficulte()
jeu_snake()
