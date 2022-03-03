import csv, os
path = "sauvegarde.csv"
separateur = ";"

dicA = {"S1":{},  #dictionnaire avec taille sous marin + etat case par case du sm
        "S2":{},
        "S3":{}}
dicB = {"S1":{},
        "S2":{},
        "S3":{}}

merA = []
merB = []

"""
Fonction utilisée en début de partie pour lire le fichier de sauvegarde
et si besoin mettre à jour les variables
"""
def readFile():    
    joueur = 0
    merA = [[[0 for i in range(10)]for j in range(5)]for k in range(3)]
    merB = [[[0 for i in range(10)]for j in range(5)]for k in range(3)]
    merUtilise = 0
    dicA = {"S1":{},
            "S2":{},
            "S3":{}}
    dicB = {"S1":{},
            "S2":{},
            "S3":{}}
    dicUtilise = 0
    
    global path,separateur
    file = open(path,"r")
    
    try:
        readingFile = csv.reader(file, delimiter=separateur)
        for colonne in readingFile:
            if colonne[0] == "joueur":
                joueur = int(colonne[1])
                
            if colonne[0] == "merA":                
                merTemp = list(colonne[1])
                while "[" in merTemp:
                    merTemp.remove("[")
                while "]" in merTemp:
                    merTemp.remove("]")
                while "," in merTemp:
                    merTemp.remove(",") 
                while " " in merTemp:
                    merTemp.remove(" ")
                while "\'" in merTemp:
                    merTemp.remove("\'")             
                
                incr = 0
                for k in range(3):
                    for j in range(5):
                        for i in range(10):
                            merA[k][j][i] = merTemp[incr]
                            incr = incr + 1
                            
            if colonne[0] == "merB":
                merTemp = list(colonne[1])
                while "[" in merTemp:
                    merTemp.remove("[")
                while "]" in merTemp:
                    merTemp.remove("]")
                while "," in merTemp:
                    merTemp.remove(",")
                while " " in merTemp:
                    merTemp.remove(" ")
                while "\'" in merTemp:
                    merTemp.remove("\'")
                
                incr = 0
                for k in range(3):
                    for j in range(5):
                        for i in range(10):
                            merB[k][j][i] = merTemp[incr]
                            incr = incr + 1
                            
            if colonne[0] == "merUtilise":
                if colonne[1] == "merA":
                    merUtilise = merA
                elif colonne[1] == "merB":
                    merUtilise = merB
                
            if colonne[0] == "dicA":
                dicSplit = colonne[1].replace("{","").replace(":","").replace("}","").replace("\"","").replace("\'","").replace(" ","")
                dicSplit = dicSplit.split(",")
                
                tabTypeSM = ["S1","S2","S2","S3","S3","S3"]    
                if len(dicSplit) == 6: #Si tous les SM sont posés (si pose incomplète avant shutdown il recommence)
                    for i in range(6):
                        element = dicSplit[i]
                        if element[0] == "S":
                            position = element[2] + element[3] + element[4]
                            etat = element[5]
                        else:
                            position = element[0] + element[1] + element[2]
                            etat = element[3]                           
                        dicA[ tabTypeSM[i] ][position] = etat
                        
            if colonne[0] == "dicB":
                dicSplit = colonne[1].replace("{","").replace(":","").replace("}","").replace("\"","").replace("\'","").replace(" ","")
                dicSplit = dicSplit.split(",")
                
                tabTypeSM = ["S1","S2","S2","S3","S3","S3"]    
                if len(dicSplit) == 6: #Si tous les SM sont posés (si pose incomplète avant shutdown il recommence)
                    for i in range(6):
                        element = dicSplit[i]
                        if element[0] == "S":
                            position = element[2] + element[3] + element[4]
                            etat = element[5]
                        else:
                            position = element[0] + element[1] + element[2]
                            etat = element[3]                           
                        dicB[ tabTypeSM[i] ][position] = etat
                

            if colonne[0] == "dicUtilise":
                if colonne[1] == "dicA":
                    dicUtilise = dicA
                elif colonne[1] == "dicB":
                    dicUtilise = dicB
                    
    except Exception as error:
        print("Erreur readFile() : ",error)
    
    finally:
        file.close()
        return joueur, merA, merB, merUtilise, dicA, dicB, dicUtilise

"""
Fonction utilisée pour mettre à jour le fichier de sauvegarde
arguments :
    objet : "joueur", "merA", "merB", "merUtilise", "dicA", "dicB", "dicUtilise"
    donnee : la donnée associée à l'objet (ex: si "joueur" -> 1 ou 2)
"""
def writeFile(objet,donnee):    
    global path,separateur

    try:
        # On ouvre le fichier en lecture
        file = open(path,"r")
        readingFile = csv.reader(file, delimiter=separateur)
        
        # On ouvre un fichier temporaire pour copier data sans ligne à modifier
        fileCopy = open("SauvegardeTemp.csv","a",newline="") # a = append : ajoute la ligne à la fin
        writingFileCopy = csv.writer(fileCopy, delimiter=separateur)
        for colonne in readingFile:
            if colonne[0] != objet:
                writingFileCopy.writerow([colonne[0],colonne[1]])
            else:
                writingFileCopy.writerow([objet,donnee])
        # On ferme le fichier en lecture
        file.close()
        # On ferme le fichier temporaire en écriture
        fileCopy.close()
        
        os.remove(path) # On supprime le fichier initial
        os.rename("SauvegardeTemp.csv",path) # On le "remplace" par le fichier temp, avec les données actualisées
        
    except Exception as error:
        print("Erreur writeFile() : ",error)
    finally:
        return 1

"""
Fonction utilisée pour initialiser un fichier de sauvegarde au format csv
"""
def initFile():
    global path,separateur
    
    try:
        file = open(path,"w")#on vide le fichier
        file.close()
        file = open(path,"a",newline="")#on y rentre les valeurs de variables par défaut
        writingFile = csv.writer(file, delimiter=separateur)
        writingFile.writerow(["joueur",1])
        writingFile.writerow(["merA",[[[0 for i in range(10)]for j in range(5)]for k in range(3)]])
        writingFile.writerow(["merB",[[[0 for i in range(10)]for j in range(5)]for k in range(3)]])
        writingFile.writerow(["merUtilise","merA"])
        writingFile.writerow(["dicA","{'S1':{},'S2':{},'S3':{}}"])
        writingFile.writerow(["dicB","{'S1':{},'S2':{},'S3':{}}"])
        writingFile.writerow(["dicUtilise","dicA"])
    except Exception as error:
        print("Erreur initFile() : ",error)
    finally:
        file.close()
        return 1

"""
Fonction utilisée pour créer une mer pour chaque joueur en début de partie
"""
def creationListe():
    mer= [[[0 for i in range(10)]for j in range(5)]for k in range(3)]
    return mer

"""
Fonction utilisée pour changer de joueur
et actualiser les mers et dictionnaires utilisés en fonction de action
Arguments :
    player : 1,2
    action : "pose", "tir"
"""
def changementJoueur(player, action):
    global merUtilise
    global dicUtilise
    if action == "pose":
        if player == 1: 
            player = 2 
            merUtilise=merB
            dicUtilise=dicB
        else: 
            player=1
            merUtilise=merA
            dicUtilise=dicA
    elif action == "tir":
        if player == 1: 
            player = 2 
            merUtilise=merA
            dicUtilise=dicA
        else: 
            player=1
            merUtilise=merB
            dicUtilise=dicB

    return player

"""
Fonction utilisée pour afficher côte à côte les mers des deux utilisateurs à chaque coup
Arguments :
    merA
    merB
"""        
def affichageMers(merA,merB):
    print("mer visée par J1\t\t\t\t\tmer visée par J2")
    for i in range(len(merB)):
        for j in range(len(merB[i])):
            for k in range(len(merB[i][j])):
                print(merB[i][j][k]," ", end="")
            print("\t\t",end="")
            for k in range(len(merA[i][j])):
                print(merA[i][j][k]," ", end="")
            print("")
        print("")
        
"""
Fonction utilisée pour mettre à jour la mer où un tir a été effectué
Arguments :
    profondeur : 0 à 2
    coordonneeX : 0 à 9
    coordonneeY : 0 à 4
    merUtilise : merA, merB
    visibilite : R(rien), V(vu)
"""
def updateMer(profondeur, coordonneeX, coordonneeY, merUtilise, visibilite):
    #Case visée
    if (caseExists(profondeur, coordonneeX, coordonneeY) and            #Si la case existe
        merUtilise[profondeur][coordonneeY][coordonneeX] != "V" and     #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX] != "T"and      #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX] != "C"):       #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur][coordonneeY][coordonneeX] = visibilite
    
    #Profondeur+1
    if (caseExists(profondeur+1, coordonneeX, coordonneeY) and          #Si la case existe
        merUtilise[profondeur+1][coordonneeY][coordonneeX] != "V" and   #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur+1][coordonneeY][coordonneeX] != "T"and    #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur+1][coordonneeY][coordonneeX] != "C"):     #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur+1][coordonneeY][coordonneeX] = visibilite
    
    #Profondeur-1    
    if (caseExists(profondeur-1, coordonneeX, coordonneeY) and          #Si la case existe
        merUtilise[profondeur-1][coordonneeY][coordonneeX] != "V" and   #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur-1][coordonneeY][coordonneeX] != "T"and    #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur-1][coordonneeY][coordonneeX] != "C"):     #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur-1][coordonneeY][coordonneeX] = visibilite

    #CoordonnéeX+1
    if (caseExists(profondeur, coordonneeX+1, coordonneeY) and          #Si la case existe
        merUtilise[profondeur][coordonneeY][coordonneeX+1] != "V" and   #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX+1] != "T"and    #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX+1] != "C"):     #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur][coordonneeY][coordonneeX+1] = visibilite

    #CoordonnéeX-1
    if (caseExists(profondeur, coordonneeX-1, coordonneeY) and            #Si la case existe
        merUtilise[profondeur][coordonneeY][coordonneeX-1] != "V" and     #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX-1] != "T"and      #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur][coordonneeY][coordonneeX-1] != "C"):       #Si pas C dedans (ne pas mettre R ou V si C dedans)
  
        merUtilise[profondeur][coordonneeY][coordonneeX-1] = visibilite

    #CoordonnéeY+1
    if (caseExists(profondeur, coordonneeX, coordonneeY+1) and            #Si la case existe
        merUtilise[profondeur][coordonneeY+1][coordonneeX] != "V" and     #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur][coordonneeY+1][coordonneeX] != "T"and      #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur][coordonneeY+1][coordonneeX] != "C"):       #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur][coordonneeY+1][coordonneeX] = visibilite

    #CoordonnéeY-1
    if (caseExists(profondeur, coordonneeX, coordonneeY-1) and            #Si la case existe
        merUtilise[profondeur][coordonneeY-1][coordonneeX] != "V" and     #Si pas V dedans (ne pas mettre R si V dedans)
        merUtilise[profondeur][coordonneeY-1][coordonneeX] != "T"and      #Si pas T dedans (ne pas mettre R ou V si T dedans)
        merUtilise[profondeur][coordonneeY-1][coordonneeX] != "C"):       #Si pas C dedans (ne pas mettre R ou V si C dedans)
        
        merUtilise[profondeur][coordonneeY-1][coordonneeX] = visibilite

"""
Fonction utilisée pour mettre à jour les dictionnaires avec la position des sous-marins
Arguments :
    typeSm : 1,2,3 (nombre de cases qu'il occupe)
"""
def poseSousMarin(typeSm): 
    global dicUtilise
    #typeSm = 1, 2 ou 3 selon le sous marin
    entry=[]
#verifier que coordonné sont pas pareil que celles d'avant
    if typeSm==1 or typeSm==2 or typeSm==3:
        valide=False
        while valide!=True:
            profondeur=int(input("profondeur :"))
            coordonne_x1=int(input("1ere Coordonnée x :"))
            coordonne_y1=int(input("1ere Coordonné y :"))
            if caseExists(profondeur, coordonne_x1, coordonne_y1 ) and caseFree(profondeur, coordonne_x1, coordonne_y1, dicUtilise) : 
                entry.append(str(profondeur)+str(coordonne_x1)+str(coordonne_y1)) #pose coordonné dans un tableau pour apres analyser si les coordoné d'un meme bateau ne sont pas les meme
                valide = True

    if typeSm==2 or typeSm==3:
        valide=False
        while valide!=True:
            coordonne_x2=int(input("2eme Coordonnée x :"))
            coordonne_y2=int(input("2eme Coordonné y :"))
            if caseExists(profondeur, coordonne_x2, coordonne_y2 ) and caseFree(profondeur, coordonne_x2, coordonne_y2, dicUtilise) and str(profondeur)+str(coordonne_x2)+str(coordonne_y2) not in entry:
                entry.append(str(profondeur)+str(coordonne_x2)+str(coordonne_y2))
                if coordonne_x1==coordonne_x2:  #test meme ligne
                    if coordonne_y2==coordonne_y1+1 or coordonne_y2==coordonne_y1-1:
                        valide=True
                if coordonne_y1==coordonne_y2:  #test meme colonne
                    if coordonne_x2==coordonne_x1+1 or coordonne_x2==coordonne_x1-1:
                        valide=True
            else:
                print("Impossible. Redonner des coordonnées...")

    if typeSm==3:
        valide = False
        while valide != True:
            coordonne_x3=int(input("3eme Coordonnée x :"))
            coordonne_y3=int(input("3eme Coordonné y :"))
            if caseExists(profondeur, coordonne_x3, coordonne_y3) and caseFree(profondeur, coordonne_x3, coordonne_y3, dicUtilise) and str(profondeur)+str(coordonne_x3)+str(coordonne_y3) not in entry:
                entry.append(str(profondeur)+str(coordonne_x2)+str(coordonne_y2))
                if coordonne_x1==coordonne_x3 and coordonne_x2==coordonne_x3:  #test meme ligne
                    if coordonne_y3==coordonne_y2+1 or coordonne_y3==coordonne_y1+1 or coordonne_y3==coordonne_y2-1 or coordonne_y3==coordonne_y1-1:
                        valide=True
                if coordonne_y1==coordonne_y3 and coordonne_y2==coordonne_y3:  #test meme colonne
                    if coordonne_x3==coordonne_x2+1 or coordonne_x3==coordonne_x1+1 or coordonne_x3==coordonne_x2-1 or coordonne_x3==coordonne_x1-1:
                        valide=True
                    else:
                        print("Impossible. Redonner des coordonnées...")

    if typeSm==1:
        dicUtilise["S1"][str(profondeur)+str(coordonne_x1)+str(coordonne_y1)]="S"
    if typeSm==2:
        dicUtilise["S2"][str(profondeur)+str(coordonne_x1)+str(coordonne_y1)]="S"
        dicUtilise["S2"][str(profondeur)+str(coordonne_x2)+str(coordonne_y2)]="S"
    if typeSm==3:
        dicUtilise["S3"][str(profondeur)+str(coordonne_x1)+str(coordonne_y1)]="S"
        dicUtilise["S3"][str(profondeur)+str(coordonne_x2)+str(coordonne_y2)]="S"
        dicUtilise["S3"][str(profondeur)+str(coordonne_x3)+str(coordonne_y3)]="S"
        
    return 1
    
"""
Fonction utilisée pour savoir si la case en question existe (pas de dépassement de tableau)
Arguments :
    profondeur : 0 à 2
    coordonneeX : 0 à 9
    coordonneeY : 0 à 4
"""
def caseExists(profondeur,coordonneeX,coordonneeY):
    profondeur = int(profondeur)
    coordonneeX = int(coordonneeX)
    coordonneeY = int(coordonneeY)
    if profondeur >= 0 and profondeur <= 2:
        if coordonneeX >= 0 and coordonneeX <= 9:
            if coordonneeY >= 0 and coordonneeY <= 4:
                return 1 #return 1 si case existante (valide)
    print("!erreur! Case non existante")
    return 0
    
"""
Fonction utilisée pour savoir si la case en question est libre ou non
Arguments :
    profondeur : 0 à 2
    x : 0 à 9
    y : 0 à 4
    dic : Dictionnaire utilisé (dicA,dicB)
"""
def caseFree(profondeur,x,y,dic):
    coordonnees = str(profondeur) + str(x) + str(y)
    if coordonnees not in dic["S1"] and coordonnees not in dic["S2"] and coordonnees not in dic["S3"]:
        return 1
    else:
        print("!erreur! Case occupée")
        return 0
   
"""
Fonction utilisée pour savoir si le tabeau visé est coulé ou juste touché
Arguments :
    profondeur : 0 à 2
    coordonneeX : 0 à 9
    coordonneeY : 0 à 4
    dicUtilise : dicA,dicB
"""
def tirCoule(profondeur, coordonneeX, coordonneeY, dicUtilise):
    tabTouche = []
    for value in dicUtilise.values():
        tabTouche.append(value)     # On stocke dans une liste toutes les valeurs dans le dictionnaire
    while tabTouche.count("T") != 0:
        tabTouche.remove("T")   # On supprime de la liste toutes les valeurs "T"
    if len(tabTouche) == 0:     # Si plus aucun élément après avoir supprimé tous les "T" : Toutes les parties du bateau étaient touchées
        for cle in dicUtilise.keys():
            dicUtilise[cle] = "C" # Donc le bateau est coulé
            merUtilise[int(cle[0])][int(cle[2])][int(cle[1])] = "C"
        return 1
    return 0

"""
Fonction utilisée pour viser un bateau. Met à jour la mer visée en fonction du résultat du tir
Arguments :
    dicUtilise : dicA,dicB
"""
def tir(dicUtilise):
    global merUtilise
    profondeur = int(input("Saisissez la profondeur où vous voulez tirer : "))
    coordonneeX = int(input("Saisissez la coordonnée X où vous voulez tirer : "))
    coordonneeY = int(input("Saisissez la coordonnée Y où vous voulez tirer : "))
    
    if caseExists(profondeur, coordonneeX, coordonneeY):
        if (caseFree(profondeur, coordonneeX, coordonneeY, dicUtilise) and     #
            caseFree(profondeur+1, coordonneeX, coordonneeY, dicUtilise) and   #
            caseFree(profondeur-1, coordonneeX, coordonneeY, dicUtilise) and   #
            caseFree(profondeur, coordonneeX+1, coordonneeY, dicUtilise) and   # Si cases adjacentes TOUTES libres
            caseFree(profondeur, coordonneeX-1, coordonneeY, dicUtilise) and   #
            caseFree(profondeur, coordonneeX, coordonneeY+1, dicUtilise) and   #
            caseFree(profondeur, coordonneeX, coordonneeY-1, dicUtilise)):     #
            
            updateMer(profondeur, coordonneeX, coordonneeY, merUtilise, "R")

        elif caseFree(profondeur, coordonneeX, coordonneeY, dicUtilise): #Si cases adj pas TOUTES libres MAIS case tirée est libre
        
            updateMer(profondeur, coordonneeX, coordonneeY, merUtilise, "V")
            
        else: #Si la case tirée n'est pas libre => Touché
            coordonnees = str(profondeur) + str(coordonneeX) + str(coordonneeY)
            if coordonnees in dicUtilise["S1"].keys():
                dicUtilise["S1"][coordonnees] = "T"
                if (tirCoule(profondeur, coordonneeX, coordonneeY, dicUtilise["S1"]) == 1): #On vérifie si bateau coulé
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'C'
                else:
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'T'
            elif coordonnees in dicUtilise["S2"].keys():
                dicUtilise["S2"][coordonnees] = "T"
                if (tirCoule(profondeur, coordonneeX, coordonneeY, dicUtilise["S2"]) == 1): #On vérifie si bateau coulé
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'C'
                else:
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'T'
            elif coordonnees in dicUtilise["S3"].keys():
                dicUtilise["S3"][coordonnees] = "T"
                if (tirCoule(profondeur, coordonneeX, coordonneeY, dicUtilise["S3"]) == 1): #On vérifie si bateau coulé
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'C'
                else:
                    merUtilise[profondeur][coordonneeY][coordonneeX] = 'T'
            else:
                print("Erreur tir(): coordonnees not in dicUtilise['Sx'].keys()")

#################
#     _Main_    #
#################
def main():
    global path
    global joueur 
    global merA
    global merB
    global merUtilise
    global dicA
    global dicB
    global dicUtilise

    merA=creationListe()
    merB=creationListe()
    
    joueur = 1
    dicUtilise=dicA
    merUtilise=merA

    if not os.path.isfile(path):
        initFile()# S'il n'y a pas de fichier de sauvegarde on en crée un
    joueur, merA, merB, merUtilise, dicA, dicB, dicUtilise = readFile()# On récupère toutes les valeurs du fichier

    if len(dicB["S3"]) == 0:#Si tous les SM n'étaient pas posés dans fichier sauvegarde
        #Partie pose des bateaux
        for i in range(2): #Pour chaque joueur
            for i in range(1,4):
                print("Joueur",joueur,": Vous posez votre sous-marin à ",i," cases.")
                poseSousMarin(i)
            joueur = changementJoueur(joueur, "pose")
    
        joueur = changementJoueur(joueur, "tir") #Pour que le 1er tireur soit J1 (Un changement de trop dans boucle for au dessus)


    while ("S" in dicUtilise["S1"].values() or
           "S" in dicUtilise["S2"].values() or
           "S" in dicUtilise["S3"].values()): #Tant que TOUS les sous-marins ne sont pas entièrement découverts
    
        joueur = changementJoueur(joueur, "tir")
        print("\n---------------------------------\n")
        affichageMers(merA, merB)
        print("Joueur",joueur)
        tir(dicUtilise)
        
        # Actualise fichier de sauvegarde après chaque tir
        writeFile("joueur", joueur)
        writeFile("dicA", dicA)
        writeFile("dicB", dicB)
        writeFile("merA", merA)
        writeFile("merB", merB)
        if joueur == 1:
            writeFile("dicUtilise", "dicB")
            writeFile("merUtilise", "merB")
        else:
            writeFile("dicUtilise", "dicA")
            writeFile("merUtilise", "merA")
            
    #Sortie while => Tous les sous-marins sont découverts
    print("Joueur",joueur,"a gagné !!!")
    os.remove(path)# Jeu terminé, on supprime le fichier de sauvegarde

main()#Exécution méthode _Main_







