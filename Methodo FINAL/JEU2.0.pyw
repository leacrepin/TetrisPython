import pygame
from pygame.locals import *
import sys
import random
import time
import os.path

pygame.init()

##Variables globales des JEUX

manqué=0 #nombre de manqué dans TAUPE
tab_grille = [] #Grille matrice de TETRIS
tab_grilleequivposition = []   #Grille matrice d'equivalence en position par rapport à la grille TETRIS
tab_pieces = [] #Liste des pieces dans TETRIS
tab_piececourantepos = [] #Liste des positions courante de la piece TETRIS
points = 0 #nombre de points (TETRIS et TAUPE)
typepiececourante =0 #Type de la piece courante TETRIS
pivcourant=0 #Pivotement de la piece courante TETRIS
tab_reserve=[] #Liste de la reserve [Type de la piece dans la reserve,Pivotement de la piece dans la reserve] TETRIS
tentativereserve=0 #Tentative d'utilisation de la reserve (on ne peut pas reutiliser la reserve tant qu'une piece n'est pas posée) TETRIS
piecesuiv=[] #Liste de la piece suivante construite comme la reserve [Type de la piece suivante,Pivotement de la piece suivante] TETRIS
level=0 #Niveau TETRIS
lignes=0 #Nombres de lignes supprimées dans TETRIS

    ##  TAUPE   ##

def taupejeu():
    global points# On remet à 0 les points au cas où on a déjà joué et les manqués
    global manqué
    points=0
    manqué=0
    
    fond = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/background.jpg").convert()
    
    #Chargement du personnage
    marteau = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/Marteau_ALBW.png").convert_alpha()
    dimension_marteaux = marteau.get_width()/2 # x centre
    dimension_marteauy = marteau.get_height()/2 # y centre
    perso_x = random.randint(100, 400)
    perso_y = random.randint(30, 300)
    marteau_x=2000
    marteau_y=2000
    
    #Chargement du texte
    pygame.font.init()
    myfont2 = pygame.font.SysFont('Comic Sans MS', 50)
    tapetaupe1 = myfont2.render(str(points), False, (0, 0, 0))
    manquétexte = myfont2.render(str(manqué), False, (0, 0, 0))
    
    #Debut du temps
    
    debut = time.time()
    debutmarteau=1000000000000000000000
    emarteau=0

    #BOUCLE INFINIE2
    continuer = 1
    while continuer:
        if time.time()-debutmarteau>0.25 and emarteau==1:
            debutmarteau=1000000000000000000000
            emarteau=0
            marteau_x=2000
            marteau_y=2000
            perso_x = random.randint(100, 400)
            perso_y = random.randint(30, 300)
            debut = time.time()
        if time.time()-debut>0.75 and points!=0 and emarteau==0:#Temps pour cliquer sur le perso (au premier bon point on commence le chrono)
            manqué=manqué+1
            perso_x = random.randint(100, 400)
            perso_y = random.randint(30, 300)
            debut = time.time()
        if manqué ==3 :
            print("3 manqués") 
            print("points = "+str(points)+"")
            continuer=0
        for event in pygame.event.get():	#Attente des événements
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:	#Si clic gauche
                    son.play()
                    marteau_x = event.pos[0]-dimension_marteaux
                    marteau_y = event.pos[1]-dimension_marteauy
                    fenetre.blit(marteau, (marteau_x, marteau_y))
                    debutmarteau= time.time()
                    emarteau=1
                    if event.pos[0]>perso_x and event.pos[0]<(perso_x+perso.get_width()) and event.pos[1]>perso_y and event.pos[1]<(perso_y+perso.get_height()): #on observe la position du clic
                        print("bien joué !")
                        points=points+1 #Si c'est bon on donne un point
                    else :
                        manqué=manqué+1
            if event.type == KEYDOWN:
                if event.key==K_ESCAPE: #on arrete de jouer donc on donne le nombre de points
                    print("points = "+str(points)+"")
                    continuer=1
        pygame.display.update()
        
        #Re-collage
        tapetaupe1 = myfont2.render(str(points), False, (0, 0, 0))
        manquétexte = myfont2.render(str(manqué), False, (0, 0, 0))
        fenetre.blit(fond, (0,0))	
        fenetre.blit(perso, (perso_x, perso_y))
        fenetre.blit(marteau, (marteau_x, marteau_y))
        fenetre.blit(tapetaupe1, (10, 0))
        fenetre.blit(manquétexte, (600, 0))
        
        #Rafraichissement
        pygame.display.flip()
    
    
    ##  TETRIS   ##

    
def Tetris():
    global points# On remet à 0 les points au cas où on a déjà joué
    points=0
    fenetre = pygame.display.set_mode((24*11*3, 24*21))#Creation d'une fenetre pygame + sa taille
    
    #Chargement du texte et de sa police d'ecriture+taille
    pygame.font.init()
    myfont2 = pygame.font.SysFont('Times Roman', 50)

    #Chargement et collage du fond
    fond = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/black-screen.png").convert()
    fenetre.blit(fond, (0,0))


    #Chargement des couleurs des pieces
    block = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/basic_block1.gif").convert_alpha()
    block4 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/basic_block1.gif").convert_alpha()
    block7 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/L.png").convert_alpha()
    block6 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/Linverse.png").convert_alpha()
    block5 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/pyramide.png").convert_alpha()
    block3 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/barre.png").convert_alpha()
    block2 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/carre.png").convert_alpha()
    block1 = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/basic_block4.gif").convert_alpha()
    neige = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/basic_block5.gif").convert_alpha()
    dimension_persox = block.get_width()/2 # x du point centre d'une piece
    dimension_persoy = block.get_height()/2 # y du point centre d'une piece
    
    #Chargement des sons
    pygame.mixer.pre_init()
    bouger=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/bouger.wav".encode())
    pivoter=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/pivoter.wav".encode())
    levelup=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/levelup.wav".encode())
    lignepleineson=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/lignepleine.wav".encode())
    ausol=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/ausol.wav".encode())
    tetris=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/Original Tetris Theme - Extended 10min (Nintendo).wav".encode())

    #Rafraîchissement de l'écran
    pygame.display.flip()
    
    #Fonctions TETRIS

    def initialisation():
        #Creation de la grille ect
        
        global tab_grille,tab_grilleequivposition,tab_pieces,tab_piececourantepos,points,typepiececourante,pivcourant,tab_reserve,tentativereserve,piecesuiv,level,lignes
        
        tab_grille = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0]] 
        tab_grilleequivposition = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0]]  
        tab_pieces = []
        tab_piececourantepos = []
        points = 0
        typepiececourante =0
        pivcourant=0
        tab_reserve=[]
        tentativereserve=0
        piecesuiv=[]
        level=0
        lignes=0
    
        for j in range(0,12):
            tab_grille[20][j]=1
        for j in range(0,20):
            tab_grille[j][0]=1
            tab_grille[j][11]=1
    
        for j in range(0,21):
            for i in range(0,12):
                a = j*dimension_persoy*2
                b = i*dimension_persox*2
                tab_grilleequivposition[j][i]=[b,a]
                                        
        piece1 =[[(0,1,0,0),(0,1,1,0),(0,0,1,0),(0,0,0,0)],#<-1ere position->0 1 0 0
                    [(0,0,0,0),(0,0,1,1),(0,1,1,0),(0,0,0,0)],#<-2eme     0 1 1 0 
                    [(0,1,0,0),(0,1,1,0),(0,0,1,0),(0,0,0,0)],#<-3eme     0 0 1 0 
                    [(0,0,0,0),(0,0,1,1),(0,1,1,0),(0,0,0,0)]]#<-4eme     0 0 0 0

        piece2 = [[(0,2,2,0),(0,2,2,0),(0,0,0,0),(0,0,0,0)],         # 0 1 1 0
                    [(0,2,2,0),(0,2,2,0),(0,0,0,0),(0,0,0,0)],      # 0 1 1 0
                    [(0,2,2,0),(0,2,2,0),(0,0,0,0),(0,0,0,0)],      # 0 0 0 0
                    [(0,2,2,0),(0,2,2,0),(0,0,0,0),(0,0,0,0)]]      # 0 0 0 0

        piece3 = [[(0,3,0,0),(0,3,0,0),(0,3,0,0),(0,3,0,0)],        # 0 3 0 0
                    [(3,3,3,3),(0,0,0,0),(0,0,0,0),(0,0,0,0)],      # 0 3 0 0
                    [(0,3,0,0),(0,3,0,0),(0,3,0,0),(0,3,0,0)],      # 0 3 0 0
                    [(3,3,3,3),(0,0,0,0),(0,0,0,0),(0,0,0,0)]]      # 0 3 0 0

        piece4 = [[(0,0,4,0),(0,4,4,0),(0,4,0,0),(0,0,0,0)],       # 0 0 4 0
                    [(0,0,0,0),(0,4,4,0),(0,0,4,4),(0,0,0,0)],     # 0 4 4 0
                    [(0,0,4,0),(0,4,4,0),(0,4,0,0),(0,0,0,0)],     # 0 4 0 0
                    [(0,0,0,0),(0,4,4,0),(0,0,4,4),(0,0,0,0)]]     # 0 0 0 0

        piece5 = [[(0,5,0,0),(0,5,5,0),(0,5,0,0),(0,0,0,0)],       # 0 5 0 0
                    [(0,0,0,0),(0,0,5,0),(0,5,5,5),(0,0,0,0)],     # 0 5 5 0
                    [(0,0,0,5),(0,0,5,5),(0,0,0,5),(0,0,0,0)],     # 0 5 0 0
                    [(0,5,5,5),(0,0,5,0),(0,0,0,0),(0,0,0,0)]]     # 0 0 0 0

        piece6 = [[(0,0,6,0),(0,0,6,0),(0,6,6,0),(0,0,0,0)],    # 0 0 6 0
                 [(0,0,0,0),(0,6,6,6),(0,0,0,6),(0,0,0,0)],     # 0 0 6 0
                 [(0,6,6,0),(0,6,0,0),(0,6,0,0),(0,0,0,0)],     # 0 6 6 0
                 [(0,0,0,0),(0,6,0,0),(0,6,6,6),(0,0,0,0)]]     # 0 0 0 0

        piece7 = [[(0,7,0,0),(0,7,0,0),(0,7,7,0),(0,0,0,0)],    # 0 7 0 0
                 [(0,0,0,0),(0,0,0,7),(0,7,7,7),(0,0,0,0)],     # 0 7 0 0
                 [(0,7,7,0),(0,0,7,0),(0,0,7,0),(0,0,0,0)],     # 0 7 7 0
                 [(0,0,0,0),(0,7,7,7),(0,7,0,0),(0,0,0,0)]]     # 0 0 0 0

        tab_pieces =(piece1,piece2,piece3,piece4,piece5,piece6,piece7)

    def newpiece():#Nouvelle piece random avec un pivotement random
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        global tentativereserve
        tentativereserve=0
        tab_piececourantepos = []
        pivcourant = random.randint(0,3)
        typepiececourante = random.randint(0,len(tab_pieces)-1)
        if typepiececourante==2 and (pivcourant==0 or pivcourant==2):
            for i in range(0,len(tab_pieces[typepiececourante][pivcourant])-1):
                for j in range(0,len(tab_pieces[typepiececourante][pivcourant][i])):
                    tab_grille[i+2][j+3]=tab_pieces[typepiececourante][pivcourant][i][j]
                    if(tab_pieces[typepiececourante][pivcourant][i][j] != 0):
                        tab_piececourantepos=tab_piececourantepos+[[i+2,j+3]]
            a=0
            while a!=2:
                pivotement()
                a=a+1
        else:
            for i in range(0,len(tab_pieces[typepiececourante][pivcourant])-1):
                for j in range(0,len(tab_pieces[typepiececourante][pivcourant][i])):
                    tab_grille[i+1][j+3]=tab_pieces[typepiececourante][pivcourant][i][j]
                    if(tab_pieces[typepiececourante][pivcourant][i][j] != 0):
                        tab_piececourantepos=tab_piececourantepos+[[i+1,j+3]]
    
    def newpiecespecial(type,piv):#Nouvelle piece definie
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        tab_piececourantepos = []
        pivcourant = piv
        typepiececourante = type
        if typepiececourante==2 and (pivcourant==0 or pivcourant==2):
            for i in range(0,len(tab_pieces[typepiececourante][pivcourant])-1):
                for j in range(0,len(tab_pieces[typepiececourante][pivcourant][i])):
                    tab_grille[i+2][j+3]=tab_pieces[typepiececourante][pivcourant][i][j]
                    if(tab_pieces[typepiececourante][pivcourant][i][j] != 0):
                        tab_piececourantepos=tab_piececourantepos+[[i+2,j+3]]
            a=0
            while a!=2:
                pivotement()
                a=a+1
        else:
            for i in range(0,len(tab_pieces[typepiececourante][pivcourant])-1):
                for j in range(0,len(tab_pieces[typepiececourante][pivcourant][i])):
                    tab_grille[i+1][j+3]=tab_pieces[typepiececourante][pivcourant][i][j]
                    if(tab_pieces[typepiececourante][pivcourant][i][j] != 0):
                        tab_piececourantepos=tab_piececourantepos+[[i+1,j+3]]
    
    def maxgauche(i):#Renvoie la colonne la plus à gauche pour la ligne i de la piece courante
        global tab_piececourantepos
        global tab_grille
        debut=0
        max=0
        for j in tab_piececourantepos:
            if debut==0 :
                if j[0]==i:
                    debut=1
                    max=j[1]
            else :
                if max > j[1] and j[0]==i:
                    max=j[1]
        return max
    
    def maxdroite(i):#Renvoie la colonne la plus à droite pour la ligne i de la piece courante
        global tab_piececourantepos
        global tab_grille
        debut=0
        max=0
        for j in tab_piececourantepos:
            if debut==0 :
                if j[0]==i:
                    debut=1
                    max=j[1]
            else :
                if max < j[1] and j[0]==i:
                    max=j[1]
        return max
    
    def maxbas(j):#Renvoie la ligne la plus basse pour la colonne j de la piece courante
        global tab_piececourantepos
        global tab_grille
        debut=0
        max=0
        for i in tab_piececourantepos:
            if debut==0 :
                if i[1]==j:
                    debut=1
                    max=i[0]
            else :
                if max < i[0] and i[1]==j:
                    max=i[0]
        return max
    
    def deplacementgauchepossible():#Renvoie True si le deplacement vers la gauche est possible
        global tab_piececourantepos
        global tab_grille
        lignes=[]
        maxlignes=[]
        for j in tab_piececourantepos:
            if j[0] in lignes :
                a=0
            else :
                lignes=lignes+[j[0]]
        for i in lignes :
            maxlignes=maxlignes+[maxgauche(i)]
        for k in range(0,len(maxlignes)):
            if tab_grille[lignes[k]][maxlignes[k]-1]!=0:
                return False
        return True
    
    def deplacementdroitepossible():#Renvoie True si le deplacement vers la droite est possible
        global tab_piececourantepos
        global tab_grille
        lignes=[]
        maxlignes=[]
        for j in tab_piececourantepos:
            if j[0] in lignes :
                a=0
            else :
                lignes=lignes+[j[0]]
        for i in lignes :
            maxlignes=maxlignes+[maxdroite(i)]
        for k in range(0,len(maxlignes)):
            if tab_grille[lignes[k]][maxlignes[k]+1]!=0:
                return False
        return True
    
    def deplacementbaspossible():#Renvoie True si le deplacement vers le bas est possible
        global tab_piececourantepos
        global tab_grille
        lignes=[]
        maxlignes=[]
        for j in tab_piececourantepos:
            if j[1] in lignes :
                a=0
            else :
                lignes=lignes+[j[1]]
        for i in lignes :
            maxlignes=maxlignes+[maxbas(i)]
        for k in range(0,len(maxlignes)):
            if tab_grille[maxlignes[k]+1][lignes[k]]!=0:
                return False
        return True
    
    def deplacementbas():#Deplace la piece courante vers le bas
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        if deplacementbaspossible():
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=0
            for i in range(0,len(tab_piececourantepos)):
                tab_piececourantepos[i][0]=tab_piececourantepos[i][0]+1
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=typepiececourante+1
    
    def deplacementgauche():#Deplace la piece courante à gauche
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        if deplacementgauchepossible():
            bouger.play()
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=0
            for i in range(0,len(tab_piececourantepos)):
                tab_piececourantepos[i][1]=tab_piececourantepos[i][1]-1
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=typepiececourante+1
            
    def deplacementdroite():#Deplace la piece courante à droite
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        if deplacementdroitepossible():
            bouger.play()
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=0
            for i in range(0,len(tab_piececourantepos)):
                tab_piececourantepos[i][1]=tab_piececourantepos[i][1]+1
            for j in tab_piececourantepos:
                tab_grille[j[0]][j[1]]=typepiececourante+1
            
    def lignepleine():#Retourne Vrai ou Faux s'il y a effectivement une ligne pleine dans la grille
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        for i in range(0,len(tab_grille)-1):
            a=0
            for j in range(0,len(tab_grille[i])):
                if tab_grille[i][j]!=0:
                    a=a+1
            if a==12 :
                return True
        return False
    
    def lignepleinesupp():#Regarde s'il y a une ligne pleine puis la supprime et met à jour les points 
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        b=0
        while lignepleine():
            i=0
            while i !=len(tab_grille):
                a=0
                if lignepleine()==False:
                    i=len(tab_grille)
                else:
                    for j in range(0,len(tab_grille[i])):
                        if tab_grille[i][j]!=0:
                            a=a+1
                    if a==12:
                        miseajourbas(i)
                        b=b+1
                    i=i+1
        miseajourpoints(b)
    
    def miseajourpoints(b):#Mise à jour des points en fonction du nombre de ligne supprimée en même temps
        global points
        global level
        global lignes
        lignepleineson.play()
        lignes=lignes+b
        if b==1 :
            points=points+40*(level+1)
        if b==2 :
            points=points+100*(level+1)
        if b==3 :
            points=points+300*(level+1)
        if b==4 :
            points=points+1200*(level+1)
        miseajourlevel()
            
    def miseajourlevel():
        global lignes
        global level
        if lignes>9:
            a=lignes//10
            if a>level:
                levelup.play()
            level=a

    def miseajourbas(n):#On decale les lignes
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        L=[]
        for i in range(1,n+1):
            L=L+[i]
        L.reverse()
        for i in L:
            for j in range(0,len(tab_grille[i])):
                tab_grille[i][j]=tab_grille[i-1][j]
        for j in range(0,12):
            tab_grille[20][j]=1
        for j in range(0,len(tab_grille[i])):
            tab_grille[0][j]=0
        for j in range(0,20):
            tab_grille[j][0]=1
            tab_grille[j][11]=1
    
    def deplacementfinal():#La piece est au plus bas possible on passe à la nouvelle
        if deplacementbaspossible()==False:
            lignepleinesupp()
            suivant()

    def directbas():#Met la piece le plus en bas
        while deplacementbaspossible()==True:
            deplacementbas()
        
    def maxdroitepiece():#Sers à trouver le point le plus à droite de la piece courante
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        debut=0
        for i in tab_piececourantepos :
            if debut==0:
                max=i[1]
                debut=1
            else:
                if max < i[1]:
                    max = i[1]
        return max
                
    def maxbaspiece():#Sers à trouver le point le plus en bas de la piece courante
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        debut=0
        for i in tab_piececourantepos :
            if debut==0:
                debut=1
                max=i[0]
            else:
                if max < i[0]:
                    max = i[0]
        return max

    def maxbaspieceliste():#Fais exactement comme maxbaspiece mais pour la piece equivalente dans tab_pieces
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        debut=0
        A=tab_pieces[typepiececourante][pivcourant]
        for i in range(0,len(A)):
            for j in range(0,len(A[i])):
                if debut==0 and A[i][j]!=0:
                    debut=1
                    max=i
                elif A[i][j]!=0 and max<i:
                    max=i
        return max

    def maxdroitepieceliste():#Fais exactement comme maxdroitepiece mais pour la piece equivalente dans tab_pieces
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        debut=0
        A=tab_pieces[typepiececourante][pivcourant]
        for i in range(0,len(A)):
            for j in range(0,len(A[i])):
                if debut==0 and A[i][j]!=0:
                    debut=1
                    max=j
                elif A[i][j]!=0 and max<j:
                    max=j
        return max
                
    def pivotement():#Pivote la piece
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        global tab_grille
        tabgrillereserve=tab_grille
        pivreserve=pivcourant
        tabpositionreserve=tab_piececourantepos
        a=maxdroitepiece()-maxdroitepieceliste()
        b=maxbaspiece()-maxbaspieceliste()
        mur=0
        pivcourant=(pivcourant+1)%len(tab_pieces[typepiececourante])
        for A in tab_piececourantepos:
            tab_grille[A[0]][A[1]]=0
        tab_piececourantepos=[]
        B=tab_pieces[typepiececourante][pivcourant]
        for i in range(0,len(B)):
            for j in range(0,len(B[i])):
                if B[i][j]!=0:
                    tab_piececourantepos=tab_piececourantepos+[[i+b,j+a]]
        for A in tab_piececourantepos:
            if A[1]>=len(tab_grille[0])-1 or A[1]<=0 or mur==1 :#si quand on pivote on est dans le mur donc on peut pas et on reprend les valeurs de base
                tab_grille=tabgrillereserve
                pivcourant=pivreserve
                tab_piececourantepos=tabpositionreserve
                mur=1
            if tabgrillereserve[A[0]][A[1]]!=0:#si quand on pivote on est dans les pieces deja posée alors on reprend les valeurs de base
                tab_grille=tabgrillereserve
                pivcourant=pivreserve
                tab_piececourantepos=tabpositionreserve
                mur=1
        if mur==0:
            pivoter.play()
        for A in tab_piececourantepos:
            tab_grille[A[0]][A[1]]=typepiececourante+1
            
    def miseajourHScore():#Met à jour HS
        global points
        fichier = open("C:/Users/leacr/Downloads/Methodo FINAL/HS.txt", "r")
        if points > int(fichier.read()):
            fichier.close()
            f = open('C:/Users/leacr/Downloads/Methodo FINAL/HS.txt','w')
            f.write(str(points))
            f.close()
        else :
            fichier.close()
            
    def HScore():#Retourne l'HS ex: "340"
        fichier = open("C:/Users/leacr/Downloads/Methodo FINAL/HS.txt", "r")
        return fichier.read()
        fichier.close()
        
    def reserve():#Reserve
        global typepiececourante
        global pivcourant
        global tab_reserve
        global tentativereserve
        for A in tab_piececourantepos:
            tab_grille[A[0]][A[1]]=0
        if tab_reserve==[]:
            tab_reserve=tab_reserve+[typepiececourante,pivcourant]
            newpiece()
        elif tentativereserve==0:
            tentativereserve=1
            L=tab_reserve
            tab_reserve=[]
            tab_reserve=tab_reserve+[typepiececourante,pivcourant]
            newpiecespecial(L[0],L[1])
            
    def suivant():#Piece suivante
        global tentativereserve
        global piecesuiv
        global tab_pieces
        global typepiececourante
        global pivcourant
        global tab_piececourantepos
        tentativereserve=0
        if piecesuiv==[]:
            pivcourantsuivant = random.randint(0,3)
            typepiecesuivant = random.randint(0,len(tab_pieces)-1)
            piecesuiv=piecesuiv+[typepiecesuivant,pivcourantsuivant]
            newpiece()
        else:
            A=piecesuiv
            piecesuiv=[]
            pivcourantsuivant = random.randint(0,3)
            typepiecesuivant = random.randint(0,len(tab_pieces)-1)
            piecesuiv=piecesuiv+[typepiecesuivant,pivcourantsuivant]
            newpiecespecial(A[0],A[1])

    #BOUCLE INFINIE
    global level
    tetris.play()
    premiereutilisation=0
    debut = time.time()
    tempsdelatenceausol =-1000000000 #Variable qui va nous donner le temps de bouger lorsque qu'on est contre le sol
    initialisation()
    tempspiece=1
    continuer = 1
    while continuer:
        pygame.display.flip()
        if tempspiece!=0 :
            tempspiece=1-0.1*level
        if deplacementbaspossible()==False and time.time()-tempsdelatenceausol >1:#On laisse 1 seconde pour bouger contre le sol
            ausol.play()
            for A in tab_piececourantepos:
                if A[0]==1:#Si le deplacement bas n'est pas possible et que l'on est en haut alors perdu
                    continuer=0
                    print("Perdu !")
                    print("Nombre de points = "+str(points))
                    miseajourHScore()
                    tetris.stop()#On arrete le son
            lignepleinesupp()#On est au fond donc on regarde s'il est possible de supprimer une ou des lignes
            deplacementfinal()
            debut = time.time()
        if (time.time()-debut)>tempspiece and deplacementbaspossible()==True:#La piece descend quand elle n'est pas au contact du sol
            deplacementbas()
            debut = time.time()
            tempsdelatenceausol = time.time()
        for event in pygame.event.get():	#Attente des événements
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:	#Si clic gauche on commence la partie
                    suivant() #On commence le jeu
                    premiereutilisation=1
            if event.type == KEYDOWN and premiereutilisation!=0:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key==K_DOWN:
                    bouger.play()
                    deplacementbas()
                    deplacementfinal()
                if event.key==K_RIGHT:
                    deplacementdroite()
                if event.key==K_LEFT:
                    deplacementgauche()
                if event.key==K_SPACE:
                    directbas()
                    deplacementfinal()
                if event.key==K_UP:
                    pivotement()
                if event.key==K_c:
                    reserve()
            
        pygame.display.update()
	
        #Collage
        
        #Texte 
        tetris1 = myfont2.render(("Score : "+str(points)+""), False, (255, 255, 255))#texte Score
        tetris2 = myfont2.render(("HS : "+HScore()+""), False, (255, 255, 255))#texte HS
        tetris3 = myfont2.render(("Reserve : "), False, (255, 255, 255))#texte Reserve
        tetris4 = myfont2.render(("Piece suivante : "), False, (255, 255, 255))#texte Piece suivante
        tetris5 = myfont2.render(("Niveau : "+str(level)+" Lignes : "+str(lignes)), False, (255, 255, 255))#texte Niveau
        
        #Fond et sa position
        fenetre.blit(fond, (0,0))	
        
        #Affichage des Pieces et leurs positions
        for j in range(0,21):#On affiche notre tab_grille 1=piece0 0=neige/gris 2=piece1 etc
            for i in range(0,12):
                if tab_grille[j][i]==1:
                    fenetre.blit(block1, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==0:
                    fenetre.blit(neige, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==2:
                    fenetre.blit(block2, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==3:
                    fenetre.blit(block3, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==4:
                    fenetre.blit(block4, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==5:
                    fenetre.blit(block5, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==6:
                    fenetre.blit(block6, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
                if tab_grille[j][i]==7:
                    fenetre.blit(block7, (tab_grilleequivposition[j][i][0], tab_grilleequivposition[j][i][1]))
        if tab_reserve!=[]:
            A=tab_pieces[tab_reserve[0]][tab_reserve[1]]
            for j in range(0,len(A)):#On affiche notre reserve
                for i in range(0,len(A[j])):
                    if A[j][i]==1:
                        fenetre.blit(block1, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==2:
                        fenetre.blit(block2, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==3:
                        fenetre.blit(block3, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==4:
                        fenetre.blit(block4, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==5:
                        fenetre.blit(block5, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==6:
                        fenetre.blit(block6, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
                    if A[j][i]==7:
                        fenetre.blit(block7, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+15][i][1]))
        if piecesuiv!=[]:
            A=tab_pieces[piecesuiv[0]][piecesuiv[1]]
            for j in range(0,len(A)):#On affiche notre piece suivante
                for i in range(0,len(A[j])):
                    if A[j][i]==1:
                        fenetre.blit(block1, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==2:
                        fenetre.blit(block2, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==3:
                        fenetre.blit(block3, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==4:
                        fenetre.blit(block4, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==5:
                        fenetre.blit(block5, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==6:
                        fenetre.blit(block6, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
                    if A[j][i]==7:
                        fenetre.blit(block7, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0]+tab_grilleequivposition[j][i][0], tab_grilleequivposition[j+9][i][1]))
        #Position du TEXTE
        fenetre.blit(tetris1, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0], tab_grilleequivposition[0][1][1]))
        fenetre.blit(tetris2, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0], tab_grilleequivposition[3][1][1]))
        fenetre.blit(tetris4, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0], tab_grilleequivposition[6][1][1]))
        fenetre.blit(tetris3, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][5][0], tab_grilleequivposition[12][1][1]))
        fenetre.blit(tetris5, (tab_grilleequivposition[0][10][0]+tab_grilleequivposition[0][2][0], tab_grilleequivposition[18][1][1]))
	
        #Rafraichissement
        pygame.display.flip()








    ##  JEU   ##



fenetre = pygame.display.set_mode((640, 480))

#Chargement du son
pygame.mixer.pre_init()
son=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/boing.wav".encode())
sonmenu=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/Pookatori and Friends (online-audio-converter.com).wav".encode())
sonmenu.play()

#Chargement et collage du fond
fond = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/a39d6ed5e4cbd7f205095e1d62d238eb.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement du texte
pygame.font.init()
myfont = pygame.font.SysFont('Wolf in the City', 120)
myfont2 = pygame.font.SysFont('Wolf in the City', 50)
text = myfont.render('Menu', False, (0, 0, 0))
tapetaupe1 = myfont2.render('Jouer au Tape Taupe : 1', False, (184, 32, 16))
tetris = myfont2.render('Jouer à Tetris : 2', False, (184, 32, 16))

#Chargement et collage du personnage
perso = pygame.image.load("C:/Users/leacr/Downloads/Methodo FINAL/perso.png").convert_alpha()
perso_x = 263
perso_y = 177
fenetre.blit(perso, (perso_x, perso_y))
dimension_persox = perso.get_width()/2 # x centre
dimension_persoy = perso.get_height()/2 # y centre


#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    points=0
    manqué=0
	for event in pygame.event.get():	#Attente des événements
		if event.type == QUIT:
            pygame.quit()
            sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:	#Si clic gauche
				#On change les coordonnées du perso
				perso_x = event.pos[0]-dimension_persox
				perso_y = event.pos[1]-dimension_persoy
				son.play()
        if event.type == KEYDOWN:
            if event.key==K_ESCAPE:
                 pygame.quit()
                 sys.exit()
            if event.key==K_1:
                print("jeu taupe")
                taupejeu() #on joue au jeu taupe si on fait la touche 1
            if event.key==K_2:
                print("jeu tetris")
                sonmenu.stop()
                Tetris()
                fenetre = pygame.display.set_mode((640, 480))
                pygame.mixer.pre_init()
                son=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/boing.wav".encode())
                sonmenu=pygame.mixer.Sound("C:/Users/leacr/Downloads/Methodo FINAL/Pookatori and Friends (online-audio-converter.com).wav".encode())
                sonmenu.play()
	pygame.display.update()
	
	#Re-collage
	fenetre.blit(fond, (0,0))	
	fenetre.blit(perso, (perso_x, perso_y))
	fenetre.blit(text, (209, 50))
	fenetre.blit(tapetaupe1, (130, 244))
	fenetre.blit(tetris, (130, 300))
	
	#Rafraichissement
	pygame.display.flip()

