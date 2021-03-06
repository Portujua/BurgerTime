# Imports
import sys
import math
import time
import pygame
import random
from pygame.locals import *

import PIL.Image
from pyglet.input.evdev_constants import KEY_T

# ============================== Variables ==============================

# Constantes Juego
TOTALLEVELS = 8

# Constantes MENU
MENU_PLAY = 5
MENU_SELECTUSER = 4
MENU_HIGHSCORES = 3
MENU_HOWTOPLAY = 2
MENU_EXIT = 1
MAX_OPTIONS = 5
MENU_TITLE = None # Esto tendra la imagen del menu
MENU_TITLE_TWO = None # Tambien

# Propiedades del menu
# Para crear una opcion nueva es igual que los monstruos, se anade 1 item a cada arreglo de opciones
# se modifica arriba MAX_OPTIONS, y se anade la opcion nueva

selectedOption = 5              # Opcion seleccionada por defecto
selectedOptionY = 200           # Coordenada Y del cursor en el menu
selectedOptionX  = 260          # Coordenada X del cursor del menu
selectedOptionWidth = 50        # Ancho del cursor del menu
selectedOptionHeight = 50       # Alto del cursor del menu
distanceBetweenOptions = 100    # Distancia entre cada opcion del menu (para mover el triangulo)

optionNames = ["Salir", "Instrucciones", "Altos Puntajes", "Seleccionar Usuario", "Jugar"]
optionXCoords = [17, 13, 12.5, 10, 17]
optionYCoords = [22.5, 19.5, 16.5, 13.5, 10.5]


# Estados del juego
isInMenu = True
isInUserMenu = False
isPlaying = False
isPaused = False
isRunning = True
isSelectingLevel = False
isSwitchingLevel = False
isInHighscores = False
isInHowToPlay = False
actualHighscore = "1"
levelSelected = 1
actualLevel = 1


# "Constantes" Teclado
KEY_UP = 273 #38
KEY_LEFT = 276 #37
KEY_DOWN = 274 #40
KEY_RIGHT = 275 #39
KEY_a = 97
KEY_s = 115
KEY_d = 100
KEY_w = 119
KEY_p = 112
KEY_f = 102

KEY_A = 65
KEY_S = 83
KEY_D = 68
KEY_W = 87
KEY_P = 80
KEY_T = 116
KEY_ENTER = 13
KEY_NUMPADENTER = 271
KEY_SPACE = 32
KEY_BACKSPACE = 8
KEY_ESC = 27

KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_5 = 53
KEY_6 = 54
KEY_7 = 55
KEY_8 = 56
KEY_9 = 57

KEY_NUMPAD1 = 257
KEY_NUMPAD2 = 258
KEY_NUMPAD3 = 259
KEY_NUMPAD4 = 260
KEY_NUMPAD5 = 261
KEY_NUMPAD6 = 262
KEY_NUMPAD7 = 263
KEY_NUMPAD8 = 264
KEY_NUMPAD9 = 265

# Colores constantes
COLOR_FLOOR = 0xFF00FF
COLOR_STAIRS = 0x00FF00

COLOR_MEAT = 0x975016
COLOR_TOPBREAD = 0xFF9D00
COLOR_BOTTOMBREAD = 0xCE7B00
COLOR_LETTUCE = 0x62D551
COLOR_TOMATO = 0xFF2833
COLOR_CHEESE = 0xFFE23F

COLOR_EGG = 0xFFEB89
COLOR_SAUSAGE = 0xFF3B14
COLOR_GHERKIN = 0x1F6821



# Estaticas
global mainComponent
global window
global pygameClock



# Propiedades de la ventana
playerName = "Chefsito"
windowTitle = "BurgerTime"
windowWidth = 800
windowHeight = 600
frameCap = 100.0
SECOND = float(1)




# Otras variables auxiliares
charLastKey = None
enterPressed = False

lastTimeKeyPressed = 0



### ---------- Propiedades del mapa ----------

map = []
global mapWidth
global mapHeight
blockSize = 20 # Tamano de cada imagen

# Imagenes
MAP_FILES_PATH = "../res/textures/map/"
global mapFloorImage
global mapStairsImage

# Constantes mapa
TILE_SIZE = 1 # Tamano de las texturas

TILE_NULL = -1
TILE_NONE = 0
TILE_FLOOR = 1
TILE_STAIRS = 2
TILE_PLAYER = 3
TILE_MONSTER = 4
TILE_BOTTOMSTAIRS = 5
TILE_BREAD = 6
TILE_MEAT = 7
TILE_LETTUCE = 8
TILE_TOMATO = 9
TILE_CHEESE = 10
WALKABLE_TILES = [1,2,6,7,8,9,10]


# Propiedades de la pimienta
pepperImg = pygame.image.load("../res/textures/game/items/pepper.png")
pepperPos = [0, 0]
pepperMapX = []
pepperMapY = []
pepperMapTime = []
PEPPER_MAX_SPAWN_TIME = 5.000000000
MAXPEPPERS = 6
pepperTime = 0
pepperSize = 1
pepperLastDir = 0
PEPPER_SPEED = 0.20


### ---------- Propiedades de la/s hamburguesas ------------
# Imagenes
BREADTOP_PATH = "../res/textures/game/hamburguer/breadTop/"
BREADBOTTOM_PATH = "../res/textures/game/hamburguer/breadBottom/"
LETTUCE_PATH = "../res/textures/game/hamburguer/lettuce/"
MEAT_PATH = "../res/textures/game/hamburguer/meat/"
TOMATO_PATH = "../res/textures/game/hamburguer/tomato/"
CHEESE_PATH = "../res/textures/game/hamburguer/cheese/"

breadTopImages = []
lettuceImages = []
meatImages = []
tomatoImages = []
cheeseImages = []
breadBottomImages = []

ingredientsImages = [breadTopImages, lettuceImages, meatImages, tomatoImages, cheeseImages, breadBottomImages]

# Posiciones
breadTopPositions = []
lettucePositions = []
meatPositions = []
tomatoPositions = []
cheesePositions = []
breadBottomPositions = []

ingredientsPositions = [breadTopPositions, lettucePositions, meatPositions, tomatoPositions, cheesePositions, breadBottomPositions]

# Temporizadores para controlar el pisado
breadTopTimers = []
lettuceTimers = []
meatTimers = []
tomatoTimers = []
cheeseTimers = []
breadBottomTimers = []

ingredientsTimers = [breadTopTimers, lettuceTimers, meatTimers, tomatoTimers, cheeseTimers, breadBottomTimers]

# Destinos (para ver si un ingrediente esta bajando..)
breadTopDestination = []
lettuceDestination = []
meatDestination = []
tomatoDestination = []
cheeseDestination = []
breadBottomDestination = []

ingredientsDestinations = [breadTopDestination, lettuceDestination, meatDestination, tomatoDestination, cheeseDestination, breadBottomDestination]

breadTopFloors = []
lettuceFloors = []
meatFloors = []
tomatoFloors = []
cheeseFloors = []
breadBottomFloors = []

ingredientsFloors = [breadTopFloors, lettuceFloors, meatFloors, tomatoFloors, cheeseFloors, breadBottomFloors]

# Otros
TIMETORESET = 2.000000000
offsetWhenWalked = 0.2
fallSpeed = 0.1
INGREDIENTS_FLOOR = 29


### ---------- Propiedades del Jugador ----------

SCORE = 0
PEPPER_IN_STOCK = 3

# Constantes de las imagenes
PIMAGE_STAND = 0
PIMAGE_WRIGHT = 1
PIMAGE_WLEFT = 2
PIMAGE_CLIMBING = 3

# Imagen que estamos pintando actualmente
actualImageToDraw = (PIMAGE_STAND, 0) # (id, nroImagen)

# Array de direcciones de imagenes
allPlayerImagesPath = [ "../res/textures/game/player/stand/", # PIMAGE_STAND
                        "../res/textures/game/player/walking/right/", # PIMAGE_WRIGHT  Solamente la direccion, usaremos FOR
                        "../res/textures/game/player/walking/left/", # PIMAGE_WLEFT    para sacar el nombre de las imagenes
                        "../res/textures/game/player/climbing/" # PIMAGE_CLIMBING
                        ]


# Imagenes del jugador, crearemos solamente los array en blanco con el numero de imagenes que son
pImages = [[0], # PIMAGE_STAND
           [0,0], # PIMAGE_WRIGHT   Como tenemos 3 imagenes para caminar a la derecha, inicializamos con 3 ceros
           [0,0], # PIMAGE_WLEFT
           [0,0] # PIMAGE_CLIMBING
           ]

# Info del jugador
playerLifes = 3
lifeMapX = []
lifeMapY = []
lifeMapTime = []
LIFE_SPAWN_TIME = 5.00000
lifeSize = 1
lifeImg = pygame.image.load("../res/textures/game/items/life.png")


# Restricciones
canClimb = False
canWalk = True
canJump = True
canShoot = True


# Estados
isAlive = True
isClimbing = False
isWalking = False
isJumping = False
isShooting = False


# Posicion
playerPosition = []



# Tamano
playerHeight = 2
playerWidth = 1



# Movimiento
speedX = 0.11
speedY = 0.08
movementVector = [0,0] # [x,y] --> x {-1,0,1} ... y {-1,0,1}
lastXMove = 0

# Salto
jumpHeight = 2
jumpTimer = 0
jumpOffset = 0
jumpSpeed = 3.5




### ---------- Propiedades los Monstruos ----------
# Para anadir un monstruo simplemente se anade un valor extra a cada arreglo a gusto de consumidor XD

RESPAWNTIME = 4.000000
respawnArray = []


# Array de direcciones de imagenes
allMonstersImagesPath = [ "../res/textures/game/monsters/walking/right/", # MIMAGE_WRIGHT  Solamente la direccion, usaremos FOR
                        "../res/textures/game/monsters/walking/left/", # MIMAGE_WLEFT    para sacar el nombre de las imagenes
                        #"../res/textures/game/monsters/climbing/" # MIMAGE_CLIMBING
                        ]

# Todas las imagenes del huevo
eggImages = [[0,0,0], # WALKING LEFT
             [0,0,0]  # WALKING RIGHT
             ]

# Todas las imagenes de la salchicha
sausageImages = [[0,0,0,0], # WALKING LEFT
                 [0,0,0,0]  # WALKING RIGHT
                 ]

# Todas las imagenes del pepinillo
gherkinImages = [[0,0,0,0], # WALKING LEFT
                 [0,0,0,0]  # WALKING RIGHT
                 ]

# Todos los monstruos con todas sus imagenes
allMonstersImages = [eggImages, sausageImages, gherkinImages]


# Nombres (sera usado para saber la cantidad de monstruos y seran anadidos mediante el archivo del mapa)
mNames = []

# Caminos desde los monstruos al jugador
monstersPaths = []

# ID de todos los monstruos presentes en el nivel (usado para cargar los monstruos)
monstersInLevel = []

# Colores (Provisional)
mColors = ["red", "blue"]

# Posicion
mX = [] # Posicion X
mY = [] # Posuicion Y


# Tamano
mHeight = []
mWidth = []


# Movimiento
mSpeedX = []
mSpeedY = []


# Monster ID
MONSTER_EGG = 0
MONSTER_SAUSAGE = 1
MONSTER_GHERKIN = 2

# Velocidades de cada monstruo
MONSTER_EGG_SPEED = [0.05, 0.05]
MONSTER_SAUSAGE_SPEED = [0.05, 0.05]
MONSTER_GHERKIN_SPEED = [0.05, 0.05]

# Tamanos de cada monstruo
MONSTER_EGG_SIZE = [1, 1]
MONSTER_SAUSAGE_SIZE = [1, 1]
MONSTER_GHERKIN_SIZE = [1, 1]

# Nro de imagenes
MONSTER_EGG_NUMBEROFIMAGES_WALKING = 3
MONSTER_EGG_NUMBEROFIMAGES_CLIMBING = 2
MONSTER_SAUSAGE_NUMBEROFIMAGES_WALKING = 4
MONSTER_SAUSAGE_NUMBEROFIMAGES_CLIMBING = 2
MONSTER_GHERKIN_NUMBEROFIMAGES_WALKING = 4
MONSTER_GHERKIN_NUMBEROFIMAGES_CLIMBING = 2

## --------- Imagenes de cada monstruo
# Arreglo de las direcciones de cada imagen de cada monstruo en orden d elos monster ID
allMonstersFolderPath = [ # Huevo
                         ["../res/textures/game/monsters/egg/walking/left/",
                            "../res/textures/game/monsters/egg/walking/right/"],
                         # Salchicha
                         ["../res/textures/game/monsters/sausage/walking/left/",
                            "../res/textures/game/monsters/sausage/walking/right/"],
                         # Pepinillo
                         ["../res/textures/game/monsters/gherkin/walking/left/",
                            "../res/textures/game/monsters/gherkin/walking/right/"]
                        ]                         

# Constantes de las imagenes
MIMAGE_WRIGHT = 0
MIMAGE_WLEFT = 1
MIMAGE_CLIMBING = 2


# Imagen que estamos pintando actualmente
monstersActualImageToDraw = [] #(MIMAGE_WRIGHT, 0) # (id, nroImagen)

# Todos los estados de los monstruos
allMonstersStates = ["walking"]



### ----------------- Usuarios -----------------
# Variable para mantener un arreglo de usuarios
# Contendra un arreglo por cada usuario, donde cada campo sera:
# [Nick, Clave, Nombre, Apellido, Email, Telefono]; respectivamente... y un arreglo de puntuaciones
users = []

# Estados
isCreatingNewProfile = False
isSelectingProfile = False
creatingNewProfileStates = [False, False, False, False, False, False]
selectingProfileStates = [False, False]

# Constantes
USER_NICK = 0
USER_PASSWORD = 1
USER_NAME = 2
USER_LASTNAME = 3
USER_EMAIL = 4
USER_PHONE = 5

USERMENU_CREATE = 1
USERMENU_SELECT = 2
USERMENU_BACK = 3
USERMENU_MAXOPTIONS = 3

# Usuario seleccionado para jugar
userSelected = [["No Seleccionado", "No Seleccionado", "No Seleccionado", "No Seleccionado", "No Seleccionado", "No Seleccionado"], []]
userSelectedId = 0

# Cosas para el menu
userMenuOptions = ["Crear Usuario", "Seleccionar Usuario", "Volver atras"]
userMenuSelectedOption = 1
userMenuY = [10.5, 15.5, 20.5]
userMenuX = [12,9,13]
strWritten = ""
userWritten = ["", ""]
newUserWritten = [["", "", "", "", "", ""], [[], [], [], [], [], [], [], []]]

infoMessage = ""
infoMessageTimer = 0
TIMER_INFOMESSAGE = 3



# ============================== Funciones y procedimientos ==============================       

# Metodo para cargar todos los objetos y texturas del juego
def loadGameObjects():
    # Cargamos las imagenes del jugador
    global pImages    
    # Creamos un nuevo array de imagenes auxiliar
    auxpImages = []
    
    # Hacemos un for que recorra todas las direcciones de imagenes
    for i in range(0, len(allPlayerImagesPath)):
        # Anadimos un nuevo set de imagenes
        auxpImages.append([])
        # Ahora hacemos un for que recorra cuantas imagenes hay en este directorio
        for k in range(0, len(pImages[i])):
            # Ahora cargamos cada una de ellas
            path = allPlayerImagesPath[i] + str(k) + ".png"
            newImage = pygame.image.load(path);
            auxpImages[i].append(newImage)
    
    pImages = auxpImages;
    
    # Imagenes de los monstruos
    global eggImages, sausageImages, gherkinImages, allMonstersImages
    # Creamos un nuevo array de imagenes auxiliar
    auxmImages = []
    
    # Hacemos un for que recorra todos los monstruos disponibles
    for m in range(0, len(allMonstersFolderPath)):
        # Anadimos un nuevo monstruo
        auxmImages.append([])
        # Hacemos un for que recorra todas las carpetas de imagenes de cada monstruo
        for c in range(0, len(allMonstersFolderPath[m])):
            # Anadimos un nuevo set de imagenes para el monstruo actual
            auxmImages[m].append([])
            # Recorremos todas las imagenes en el directorio actual
            for i in range(len(allMonstersImages[m][c])):
                # Cargamos cada una de ellas
                path = allMonstersFolderPath[m][c] + str(i) + ".png"
                newImage = pygame.image.load(path)
                auxmImages[m][c].append(newImage)
    
    allMonstersImages = auxmImages    
    
        
    # Hamburguesa
    global breadTopImages, lettuceImages, meatImages, tomatoImages, cheeseImages, breadBottomImages
    # Pan Tope
    breadTopImages.append(pygame.image.load(BREADTOP_PATH + "left.png"))
    breadTopImages.append(pygame.image.load(BREADTOP_PATH + "center.png"))
    breadTopImages.append(pygame.image.load(BREADTOP_PATH + "right.png"))
    
    # Lechuga
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "left.png"))
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "center.png"))
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "right.png"))
    
    # Carne
    meatImages.append(pygame.image.load(MEAT_PATH + "left.png"))
    meatImages.append(pygame.image.load(MEAT_PATH + "center.png"))
    meatImages.append(pygame.image.load(MEAT_PATH + "right.png"))
    
    # Tomate
    tomatoImages.append(pygame.image.load(TOMATO_PATH + "left.png"))
    tomatoImages.append(pygame.image.load(TOMATO_PATH + "center.png"))
    tomatoImages.append(pygame.image.load(TOMATO_PATH + "right.png"))
    
    # Queso
    cheeseImages.append(pygame.image.load(CHEESE_PATH + "left.png"))
    cheeseImages.append(pygame.image.load(CHEESE_PATH + "center.png"))
    cheeseImages.append(pygame.image.load(CHEESE_PATH + "right.png"))
    
    # Pan Abajo
    breadBottomImages.append(pygame.image.load(BREADBOTTOM_PATH + "left.png"))
    breadBottomImages.append(pygame.image.load(BREADBOTTOM_PATH + "center.png"))
    breadBottomImages.append(pygame.image.load(BREADBOTTOM_PATH + "right.png"))
    
    # Mapa
    global mapFloorImage, mapStairsImage
    mapFloorImage = pygame.image.load(MAP_FILES_PATH + "floor.png")
    mapStairsImage = pygame.image.load(MAP_FILES_PATH + "stairs.png")
    
    
    
# Metodo para "soltar" las teclas del teclado
def releaseKeys():
    global movementVector, isWalking
    
    movementVector = [0,0]
    isWalking = False
    
    
# Metodo para anadir puntuacion
def addScore(amount):
    global SCORE
    
    SCORE += amount
    
# Metodo para resetear el mensaje de informacion
def resetInfoMessage():
    global infoMessage
    if time.time() - infoMessageTimer > TIMER_INFOMESSAGE:
        infoMessage = ""
    

# Metodo para anadir el score al usuario (final del nivel)
def addFinalScore(username, lvl):
    global SCORE
    for user in users:
        if user[0][0] == username:
            user[1][lvl-1].append(str(SCORE))
            print("Terminaste el nivel " + str(lvl) +  " con un puntaje de " + str(SCORE))
            SCORE = 0
            
# Aparecer una pimienta en el mapa
def spawnPepper():
    global pepperMapX, pepperMapY, pepperMapTime
    
    r = getRandomMapPosition()
    pepperMapX.append(convertToMapX(r))
    pepperMapY.append(convertToMapY(r))
    pepperMapTime.append(time.time())
    
# Aparecwer una vida en el mapa
def spawnLife():
    global lifeMapX, lifeMapY, lifeMapTime
    
    r = getRandomMapPosition()
    lifeMapX.append(convertToMapX(r))
    lifeMapY.append(convertToMapY(r))
    lifeMapTime.append(time.time())
    
    
def tickLifeItem():
    #### Para las que esten por el mapa            
    global lifeMapTime, lifeMapX, lifeMapY, playerLifes
    
    if isAlive:
        for i in range(0, len(lifeMapTime)):
            # Para reiniciarlas
            if time.time() - lifeMapTime[i] > LIFE_SPAWN_TIME:
                lifeMapTime[i] = 0
                lifeMapX[i] = 0
                lifeMapY[i] = 0
            # Para ver si la agarramos
            print(lifeMapX)
            print(lifeMapY)
            print(i)
            if math.floor(playerPosition[0]) == lifeMapX[i] and math.floor(playerPosition[1]) == lifeMapY[i]:
                playerLifes += 1
                lifeMapX[i] = 0
                lifeMapY[i] = 0

    


# =====================================================================================
# =====================================================================================
# ============================== Archivos de Texto ====================================
# =====================================================================================
# =====================================================================================

# Carga de usuarios a la memoria
def loadUsers():
    global users
    # Abrimos el archivo
    file = open("../res/data/db.txt", "r")
    
    # Leemos todas las lineas
    lines = file.readlines()
    
    i = -1
    k = 0 # 0 = info, 1 = scores
    lvl = 0 # Si es 0 no es un nivel
    
    # Recorremos cada una de las lineas
    for line in lines:
        # Recortamos el enter del final..
        if line[len(line)-1:] == "\n":
            line = line[:len(line)-1]
        
        if line == "<newuser>":
            users.append([])
            i += 1
            lvl = 0
            # Este es el arreglo de la informacion
            users[i].append([])
            k = 0
        elif line == "<scores>":
            # Arreglo de las puntuaciones
            users[i].append([])
            k = 1
            # Anado todos los niveles
            for h in range(0,8):
                users[i][k].append([])
            
            lvl = 0
        elif line == "<1>":
            lvl = 1
        elif line == "<2>":
            lvl = 2
        elif line == "<3>":
            lvl = 3
        elif line == "<4>":
            lvl = 4
        elif line == "<5>":
            lvl = 5
        elif line == "<6>":
            lvl = 6
        elif line == "<7>":
            lvl = 7
        elif line == "<8>":
            lvl = 8
        else:
            if lvl == 0:
                users[i][k].append(line)
            else:
                users[i][k][lvl-1].append(line)    
            
    
    print(users)
    # Cerramos el archivo
    file.close()
    

# Chequear si existe un usuario
def userExists(nick):
    for user in users:
        if user[0][USER_NICK] == nick:
            return True
    return False

# Metodo para devolver un usuario
def doLogin(user, password):
    global userSelectedId
    userSelectedId = -1
    for u in users:
        userSelectedId += 1
        if u[0][0] == user and u[0][1] == password:
            return u
    
    return [["Login Failed", "Login Failed", "Login Failed", "Login Failed", "Login Failed", "Login Failed"], []]


# Metodo para reescribir el archivo
def rewriteUsersFile():
    # Abrimos el archivo
    file = open("../res/data/db.txt", "w")
    
    for user in users:
        file.write("<newuser>\n")        
        for info in user[0]:
            file.write(info + "\n")
            
        file.write("<scores>\n")
        for lvl in range(0,8):
            for score in user[1][lvl]:
                file.write("<" + str(lvl+1) + ">\n")
                file.write(str(score) + "\n")
        


# =====================================================================================
# =====================================================================================
# ================================== Funcionales ======================================
# =====================================================================================
# =====================================================================================

# Metodo para convertir a RGB
def convertToRGB(red, blue, green):
    return ((red << 16) | (blue << 8) | green)


# Metodo para convertir el string de un color a un vector RGB
def getColor(name):
    if name == "red":
        return (255, 0, 0)
    elif name == "green":
        return (0, 255, 0)
    elif name == "blue":
        return (0, 0, 255)
    elif name == "white":
        return (255, 255, 255)
    elif name == "black":
        return (0,0,0)
    elif name == "pink":
        return (255,0,255)
    elif name == "orange":
        return (255, 128, 0)
    elif name == "bread":
        return (255, 157, 0)
    elif name == "meat":
        return (151, 80, 22)
    elif name == "lettuce":
        return (98, 213, 81)
    elif name == "cyan":
        return (0, 255, 255)
    
def getRandomColor():
    r = random.randint(0, 9)
    if r == 1:
        return getColor("red")
    elif r == 2:
        return getColor("green")
    elif r == 3:
        return getColor("blue")
    elif r == 4:
        return getColor("white")
    elif r == 5:
        return getColor("pink")
    elif r == 6:
        return getColor("orange")
    elif r == 7:
        return getColor("bread")
    elif r == 8:
        return getColor("meat")
    elif r == 9:
        return getColor("lettuce")
    elif r == 0:
        return getColor("cyan")
    
    

# Metodo para cargar una imagen
def loadImage(filePath):
    return pygame.image.load(filePath)


# Metodo para reiniciar todos los obj hamburguesas
def resetHamburguerObjects():
    global breadBottomPositions, breadBottomTimers, breadBottomDestination, breadBottomFloors, cheesePositions, cheeseTimers, cheeseDestination, cheeseFloors, tomatoPositions, tomatoTimers, tomatoDestination, tomatoFloors, breadTopPositions, lettucePositions, meatPositions, breadTopTimers, lettuceTimers, meatTimers, breadTopDestination, lettuceDestination, meatDestination, breadTopFloors, lettuceFloors, meatFloors
    
    # Posiciones
    breadTopPositions = []
    lettucePositions = []
    meatPositions = []
    tomatoPositions = []
    cheesePositions = []
    breadBottomPositions = []
    
    # Temporizadores para controlar el pisado
    breadTopTimers = []
    lettuceTimers = []
    meatTimers = []
    tomatoTimers = []
    cheeseTimers = []
    breadBottomTimers = []
    
    # Destinos (para ver si un ingrediente esta bajando..)
    breadTopDestination = []
    lettuceDestination = []
    meatDestination = []
    tomatoDestination = []
    cheeseDestination = []
    breadBottomDestination = []
    
    # Pisos
    breadTopFloors = []
    lettuceFloors = []
    meatFloors = []
    tomatoFloors = []
    cheeseFloors = []
    breadBottomFloors = []


# Metodo para cargar el mapa de una imagen (pixel a pixel)
def loadMap(filePath):
    global breadTopPositions, meatPositions, lettucePositions, tomatoPositions, cheesePositions, breadBottomPositions, monstersInLevel
    
    # Reinicializamos todos los objetos de hamburguesas
    resetHamburguerObjects()
    
    # Renombramos la ruta a la carpeta de mapas
    filePath = "../res/maps/" + filePath
    
    # Cargamos la imagen
    image = PIL.Image.open(filePath)
    
    # Obtenemos sus pixels
    pixels = image.load()
    
    # Inicializamos el mapa
    mapReaded = []
    
    # Obtenemos las dimensiones de la imagen
    ix, iy = image.size
    
    # Guardamos el Ancho/Alto en las variables globales
    global mapWidth
    mapWidth = ix
    global mapHeight
    mapHeight = iy
    
    # Contadores para ir anadiendo objetos leidos
    cTBread = -1 
    cLettuce = -1
    cMeat = -1
    cTomato = -1
    cCheese = -1
    cBBread = -1
    
    sameObject = False

    # Recorremos todos los pixels de la imagen
    for y in range(0, iy):
        for x in range(0, ix):
            # Obtenemos las componentes del vector RGB
            r, g, b = pixels[x, y]

            # Creamos el color RGB
            rgb = (r << 16) | (g << 8) | b

            # Chequeamos si es el color
            if (rgb & 0xFFFFFF) == 0: # Negro (Nada)
                sameObject = False
                mapReaded.append(TILE_NONE)
            elif rgb == COLOR_FLOOR:
                sameObject = False
                mapReaded.append(TILE_FLOOR)
            elif rgb == COLOR_STAIRS:
                sameObject = False
                mapReaded.append(TILE_STAIRS)
            # ========== PAN ARRIBA ==========
            elif rgb == COLOR_TOPBREAD:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual un pan
                # Entonces va a pegar el pan en la posicion actual en vez de "crear" un 
                # nuevo objeto de pan
                if not sameObject: 
                    sameObject = True
                    cTBread += 1
                    breadTopPositions.append([])
                    breadTopTimers.append([])
                    breadTopDestination.append(0)
                    breadTopFloors.append(0)

                breadTopPositions[cTBread].append((x, y))
                breadTopTimers[cTBread].append(0)
            # ========== PAN ==========
            elif rgb == COLOR_BOTTOMBREAD:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual un pan
                # Entonces va a pegar el pan en la posicion actual en vez de "crear" un 
                # nuevo objeto de pan
                if not sameObject: 
                    sameObject = True
                    cBBread += 1
                    breadBottomPositions.append([])
                    breadBottomTimers.append([])
                    breadBottomDestination.append(0)
                    breadBottomFloors.append(0)

                breadBottomPositions[cBBread].append((x, y))
                breadBottomTimers[cBBread].append(0)
            # ========== CARNE ==========
            elif rgb == COLOR_MEAT:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual una carne
                # Entonces va a pegar la carne en la posicion actual en vez de "crear" un 
                # nuevo objeto de carne
                if not sameObject: 
                    sameObject = True
                    cMeat += 1
                    meatPositions.append([])
                    meatTimers.append([])
                    meatDestination.append(0)
                    meatFloors.append(0)

                meatPositions[cMeat].append((x, y)) 
                meatTimers[cMeat].append(0)
            # ========== LECHUGA ==========
            elif rgb == COLOR_LETTUCE:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual una lechuga
                # Entonces va a pegar la lechuga en la posicion actual en vez de "crear" un 
                # nuevo objeto de lechuga
                if not sameObject: 
                    sameObject = True
                    cLettuce += 1
                    lettucePositions.append([])
                    lettuceTimers.append([])
                    lettuceDestination.append(0)
                    lettuceFloors.append(0)

                lettucePositions[cLettuce].append((x, y))
                lettuceTimers[cLettuce].append(0) 
            # ========== TOMATE ==========
            elif rgb == COLOR_TOMATO:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual un tomate
                # Entonces va a pegar el tomate en la posicion actual en vez de "crear" un 
                # nuevo objeto de tomate
                if not sameObject:
                    sameObject = True
                    cTomato += 1
                    tomatoPositions.append([])
                    tomatoTimers.append([])
                    tomatoDestination.append(0)
                    tomatoFloors.append(0)
                
                tomatoPositions[cTomato].append((x, y))
                tomatoTimers[cTomato].append(0)
            # ========== QUESO ==========
            elif rgb == COLOR_CHEESE:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual un queso
                # Entonces va a pegar el queso en la posicion actual en vez de "crear" un 
                # nuevo objeto de queso
                if not sameObject:
                    sameObject = True
                    cCheese += 1
                    cheesePositions.append([])
                    cheeseTimers.append([])
                    cheeseDestination.append(0)
                    cheeseFloors.append(0)
                
                cheesePositions[cCheese].append((x, y))
                cheeseTimers[cCheese].append(0)
            else:
                if rgb == COLOR_EGG:
                    monstersInLevel.append(MONSTER_EGG)
                    monstersPaths.append(None)
                elif rgb == COLOR_SAUSAGE:
                    monstersInLevel.append(MONSTER_SAUSAGE)
                    monstersPaths.append(None)
                elif rgb == COLOR_GHERKIN:
                    monstersInLevel.append(MONSTER_GHERKIN)
                    monstersPaths.append(None)
                sameObject = False
                mapReaded.append(TILE_NULL)
            
    # Actualizamos en memoria xd
    global ingredientsImages, ingredientsPositions, ingredientsTimers, ingredientsDestinations, ingredientsFloors
    
    ingredientsImages = [breadTopImages, lettuceImages, meatImages, tomatoImages, cheeseImages, breadBottomImages]
    ingredientsPositions = [breadTopPositions, lettucePositions, meatPositions, tomatoPositions, cheesePositions, breadBottomPositions]
    ingredientsTimers = [breadTopTimers, lettuceTimers, meatTimers, tomatoTimers, cheeseTimers, breadBottomTimers]
    ingredientsDestinations = [breadTopDestination, lettuceDestination, meatDestination, tomatoDestination, cheeseDestination, breadBottomDestination]
    ingredientsFloors = [breadTopFloors, lettuceFloors, meatFloors, tomatoFloors, cheeseFloors, breadBottomFloors]        
            
    
    # Retornamos el mapa leido
    return mapReaded


# Metodo para obtener el valor del mapa en la posicion x,y
def getMapValue(x, y):
    x = math.floor(x)
    y = math.floor(y)
    # Chequeamos que no nos salgamos de la matriz
    if x + y * mapWidth >= 0 and x < mapWidth:
        return map[x + y * mapWidth]
    return 0


# Metodo para obtener la coordenada X de el punto generado random
def convertToMapX(pos):
    return pos % mapWidth

# Metodo para obtener la coordenada Y de el punto generado random
def convertToMapY(pos):
    return math.floor(pos / mapWidth)


# Metodo para obtener una posicion aleatoria en el mapa
def getRandomMapPosition():
    while True:
        r = random.randint(0, mapWidth*mapHeight - 1)
        if map[r] == TILE_FLOOR:
            return r
        


# Metodo para evitar que se meta por el piso al bajar
def fixStairsBug(ex, ey, eWidth, eHeight):
    # Si en la entidad hay piso, y abajo tambien, entonces le resto el offset que baja a la pos actual
    # Se puede ver cual es el bug desactivandola, posicionandose en una escalera y en vez de subir
    # bajen... Van a ver que se mete por el piso 1 cuadro hacia abajo y luego vuelve a aparecer arriba
    if (getMapValue(ex+(eWidth/2), ey+eHeight+blockSize) == TILE_FLOOR) and (getMapValue(ex+(eWidth/2), ey+eHeight) == TILE_FLOOR):
        return -(ey - ey*blockSize)
    return 0

# Metodo para saber si podemos movernos a un recuadro x,y
def canMoveTo(x, y, movementVector, sx, sy): # sx = speedX
    # Obtenemos las coordenadas del vector movimiento
    vx = movementVector[0]
    vy = movementVector[1]
    
    if getMapValue(math.floor(x + sx + vx), math.floor(y + sy + vy)) in WALKABLE_TILES:
        return True
    elif isClimbing:
        return True
    else:
        return False
    

# Metodo para obtener los "hijos" de una coordenada dentro de la matriz
# Los hijos de una coordenada son aquellos valores que son caminables dentro de la matriz (piso, escaleras)
def getChilds(x, y, visited, allPaths):
    # Como solamente nos podemos mover en 4 direcciones solo debemos ver esas direcciones
    # Creamos la matriz de hijos que vamos a devolver
    allChilds = []
    
    # Obtenemos todos los valores de las direcciones (para no escribir tanto en los if)
    up = getMapValue(x, y-1)
    down = getMapValue(x, y+1)
    left = getMapValue(x-1, y)
    right = getMapValue(x+1, y)            
            
        
    # Si a la izquierda hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (left in WALKABLE_TILES) and (not((x-1, y) in visited) or ((x, y-1) in allPaths)):
        allChilds.append((x-1, y))
        
    # Si a la derecha hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (right in WALKABLE_TILES) and (not((x+1, y) in visited) or ((x, y-1) in allPaths)):
        allChilds.append((x+1, y))
        
    # Si arriba hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (up in WALKABLE_TILES) and (not((x, y-1) in visited) or ((x, y-1) in allPaths)):
        allChilds.append((x, y-1))
        
    # Si abajo hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (down in WALKABLE_TILES) and (not((x, y+1) in visited) or ((x, y-1) in allPaths)):
        allChilds.append((x, y+1))
        
    return allChilds
    

# Metodo para ir de una coordenada A a una coordenada B dentro de la matriz
# de manera recursiva
# a,b son vectores (x,y), path es la matriz de matrices de todos los caminos posibles (la que vamos a devolver)
# visited son los nodos que ya visitamos, al llamar la funcion por primera vez se envia Vacio
# Le enviamos dos puntos A,B en coordenadas del mapa
def getPathTo(a, b, path, visited, allPaths, iteration):     
    # Marcamos como visitado el nodo actual
    visited.append(a)
    # Obtenemos las componentes de A
    ax, ay = a

    # Buscamos los hijos
    aChilds = getChilds(ax, ay, visited, allPaths)

    # Si A no tiene hijos, llegamos a una calle ciega
    if len(aChilds) == 0: 
        return False
    
    
    # Recorremos todos los hijos de A
    for child in aChilds:
        # Anadimos el nodo actual al camino
        path.append(child)
        # Chequeamos si es nuestro destino
        if child == b:
            return True
        # Sino llamamos recursivamente a la funcion con el nuevo hijo para que busque hijos en el
        else:
            arrived = getPathTo(child, b, path, visited, allPaths, iteration+1)
            # Chequeamos si llegamos por alguno de los hijos
            # Si no llegamos, sacamos al nodo actual del camino
            if not arrived:
                path.remove(child)
            # Si en efecto llegamos, devolvemos TRUE para finalizar todo
            else:
                # Chequeamos, si iteration = 0 es que estamos en el primer loop
                # Y debemos devolver el camino en vez de True
                if iteration == 0:
                    #print("Camino: ", path)
                    #return path
                    allPaths.append(path)
                    path = []
                else:
                    return True
    # Si terminamos de recorrer todos los hijos y no llegamos, devolvemos FALSE
    # Chequeamos si estamos en el loop principal, si es asi entonces devolvemos el mismo punto donde estabamos
    if iteration == 0:
        if len(allPaths) > 0:
            # Creamos una variable para guardar el camino mas corto
            shortestPath = allPaths[0]
            shortestLength = len(shortestPath)
            
            # Vemos cual de todos es el mas corto
            for p in allPaths:
                if len(p) < shortestLength:
                    shortestPath = p
                    shortestLength = len(p)
                #print("Un camino de ", len(p), " es: ", p)
            
            #print("")
            #print("El mas corto fue de ", shortestLength, " y es: ", shortestPath)
            return shortestPath
        else:
            return None
    else: # Sino, devolvemos falso para notificar que termino el loop y no encontro camino con ese hijo
        return False
    
# Este metodo es para calcular el vector movimiento dado un punto hacia donde ir
# Es usado para ir a los distintos puntos que nos genera la busqueda de camino
# Le enviamos el array de puntos para llegar al destino, a pesar que solo usaremos el primero
# La posicion X,Y del objeto a mover, la velocidad X,Y para ese objeto
# Devuelve un vector movimiento
def getMovementVector(p, ex, ey):
    global lastXMove
    # Obtenemos las coordenadas del punto p
    px, py = p[0]

    # Creamos el vector movimiento (sin movimiento, por ahora)
    mVector = [0,0]
    
    if ey < py:
        mVector[1] = 1
    elif ey > py:
        mVector[1] = -1
    elif ex < px:
        mVector[0] = 1
    elif ex > px:
        mVector[0] = -1
    
    return mVector        


# Metodo para agregar un monstruo
def addMonster(id):
    global mNames, mX, mY, mHeight, mWidth, mSpeedX, mSpeedY, monstersActualImageToDraw, mImages, respawnArray
    if id == MONSTER_EGG:
        mNames.append("Huevo")
        mSpeedX.append(MONSTER_EGG_SPEED[0])
        mSpeedY.append(MONSTER_EGG_SPEED[1])
        mWidth.append(MONSTER_EGG_SIZE[0])
        mHeight.append(MONSTER_EGG_SIZE[1])
    elif id == MONSTER_SAUSAGE:
        mNames.append("Salchicha")
        mSpeedX.append(MONSTER_SAUSAGE_SPEED[0])
        mSpeedY.append(MONSTER_SAUSAGE_SPEED[1])
        mWidth.append(MONSTER_SAUSAGE_SIZE[0])
        mHeight.append(MONSTER_SAUSAGE_SIZE[1])
    elif id == MONSTER_GHERKIN:
        mNames.append("Pepinillo")
        mSpeedX.append(MONSTER_GHERKIN_SPEED[0])
        mSpeedY.append(MONSTER_GHERKIN_SPEED[1])
        mWidth.append(MONSTER_GHERKIN_SIZE[0])
        mHeight.append(MONSTER_GHERKIN_SIZE[1])
        
        
    r = getRandomMapPosition()
    mX.append(convertToMapX(r))
    mY.append(convertToMapY(r))
    respawnArray.append(0)
    maitd = (MIMAGE_WRIGHT, 0)
    monstersActualImageToDraw.append(maitd) 
    

# Metodo para obtener posiciones random en todos las entidades del juego
def initActors():
    global mX, mY, playerPosition, canClimb, canWalk, canJump, canShoot, isClimbing, isWalking, isJumping, isShooting
    
    # Reiniciamos los estados por si morimos subiendo una escalera
    canClimb = False
    canWalk = True
    canJump = True
    canShoot = True
    isClimbing = False
    isWalking = False
    isJumping = False
    isShooting = False
    
    # Inicializamos todos los arreglos de los monstruos
    global mNames, mX, mY, mHeight, mWidth, mSpeedX, mSpeedY, monstersActualImageToDraw, respawnArray, pepperMapX, pepperMapY, pepperMapTime, lifeMapX, lifeMapY, lifeMapTime
    mNames = []
    mX = []
    mY = []
    mHeight = []
    mWidth = []
    mSpeedX = []
    mSpeedY = []
    monstersActualImageToDraw = []
    respawnArray = []
    pepperMapX = []
    pepperMapY = []
    pepperMapTime = []
    lifeMapX = []
    lifeMapY = []
    lifeMapTime = []
    
    # Le asignamos una posicion random al jugador
    r = getRandomMapPosition()
    playerPosition = [convertToMapX(r), convertToMapY(r)]    
    
    # Cargamos los monstruos
    for n in range(0, len(monstersInLevel)):
        mid = monstersInLevel[n]
        addMonster(mid)        


# =====================================================================================
# =====================================================================================
# ============================= Metodos para Pintar ===================================
# =====================================================================================
# =====================================================================================

# Pintar rectangulos (por tenerlo.)
def drawRect(x, y, width, height, rgbColor):
    pygame.draw.rect(window, rgbColor, (x*blockSize, y*blockSize, width*blockSize, height*blockSize))
    
    

# Pintar lineas (Por tenerlo..)
def drawLines(px, py, qx, qy, rgbColor, weight):
    pygame.draw.line(window, rgbColor, (px*blockSize, py*blockSize), (qx*blockSize, qy*blockSize), weight)
    

# Metodo para pintar string, el string sera pintado centrado en el punto x,y dado.. Ejemplo:
# Si se da como punto window.width/2, window.height/2 entonces saldra centrado en la pantalla
def drawString(x, y, string, font, rgbColor, size):
    str = pygame.font.SysFont(font, size)
    lbl = str.render(string, 1, rgbColor)
    window.blit(lbl, (x*blockSize, y*blockSize))


# Metodo para pintar imagenes sin redimensionar
def drawImage(image, x, y):
    window.blit(image, (x*blockSize,y*blockSize))
    
# Metodo para pintar imagenes redimensionadas
def drawImageR(image, x, y, width, height): 
    window.blit(pygame.transform.scale(image, (width*blockSize, height*blockSize)), (x*blockSize, y*blockSize))
    
    
# Metodo para pintar poligonos
def drawPolygon(points, rgbColor):
    pygame.draw.polygon(window, rgbColor, points)    
    

# Metodo que pinta el mapa basandose en la matriz del mapa y el tamano de cada bloque
# Aqui hay un problema, le toma 0.5 seg renderizar esto
def drawMap():    
    # Creamos dos variables para ir llevando el offset
    # Cada bloque se pintara en una coordenada X mas el OFFSET total
    xOffset = 0
    yOffset = 0
    
    # Recorremos todo el mapa
    for y in range(0, mapHeight):
        for x in range(0, mapWidth):
            # Chequeamos para no pintar cosas innecesarias
            if (xOffset > windowWidth) or (yOffset > windowHeight): continue
            
            # Wtf
            if (x + y*mapWidth) < 0 or (x + y*mapWidth) >= len(map):
                continue
            
            # Obtenemos la coordenada actual
            actCoord = map[x + y*mapWidth]
            
            if actCoord == TILE_NONE or actCoord == TILE_NULL:
                xOffset += 1
                continue
            
            # Variable para la textura actual
            actImage = None
            
            # Como se pinta desde la esquina superior izq, las escaleras van a aparecer pintadas
            # Un cuadro mas arriba, por lo que debemos bajarlas si es que vamos a pintar una
            stairsOffset = 0 
            
            # Setteamos el color segun el numero en la matriz
            if actCoord == TILE_FLOOR:
                actImage = mapFloorImage
            elif actCoord == TILE_STAIRS:
                actImage = mapStairsImage
                stairsOffset = TILE_SIZE
            
            # Pintamos el bloque
            drawImageR(actImage, xOffset, yOffset + stairsOffset, TILE_SIZE, TILE_SIZE)
            
            # Actualizamos los offset
            xOffset += TILE_SIZE # Podriamos tener 1 solo offset ya que son iguales
            
        xOffset = 0 # Reiniciamos el offset del eje X para comenzar a pintar desde 0
        yOffset += TILE_SIZE # Sumamos blockSize al offset del eje Y para pintar abajo

        

# =====================================================================================
# =====================================================================================
# =============================== Metodos Hamburguesa =================================
# =====================================================================================
# =====================================================================================

# Metodo para ver si los ingredientes caen encima de algun monstruo
def checkCollisionWithMonsters(x, y):
    global respawnArray, monstersPaths, mX, mY
    
    for m in range(0, len(mNames)):
        monsterX = math.floor(mX[m])
        # Si le pegamos a algun monstruo
        if (x == monsterX or x+1 == monsterX or x+2 == monsterX or x+3 == monsterX) and y == math.floor(mY[m]):
            # Creamos un item de vida en el mapa
            spawnLife()
            # Borramos ese monstruo
            addScore(1050)
            respawnArray[m] = time.time()
            monstersPaths[m] = None
            r = getRandomMapPosition()
            mX[m] = convertToMapX(r)
            mY[m] = convertToMapY(r)   
            
                

# Metodo para obtener el numero de entidades que estan encima de los ingredientes
def getNumberOfEntitiesOn(ingredient):
    total = 0
    # Recorremos cada coordenada del ingrediente a ver si hay alguien encima
    for i in range(0, len(ingredient)):
        # Obtenemos las coordenadas x,y de ese punto
        ix, iy = ingredient[i]
        
        # Revisamos el jugador
        if ix == math.floor(playerPosition[0]) and iy == math.floor(playerPosition[1]):
            total += 1
        
        # Revisamos cada monstruo
        for m in range(0, len(mNames)):
            if ix == math.floor(mX[m]) and iy == math.floor(mY[m]):
                total += 1
        
    print("Va a bajar ", total)
    return total
    
    

# Metodo para bajar un ingrediente al siguiente nivel
# Le pasamos como parametro la matriz de posiciones del ingrediente
def moveDown(ingredient, numberOfFloors):
    if numberOfFloors == 0:
        return
    # Primero tomo el valor Y
    x, y = ingredient[0]
    
    # Coincidencias de piso (Para bajar n pisos)
    coincidences = 0

    # Arreglamos los pisos a bajar si estan malos
    if str(numberOfFloors) == "[0]" or str(numberOfFloors) == "[0, 0]" or str(numberOfFloors) == "[0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0, 0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0, 0, 0, 0, 0]" or str(numberOfFloors) == "[0, 0, 0, 0, 0, 0, 0, 0, 0]":
        numberOfFloors = 1
    
    # Busco donde esta la siguiente plataforma desde esa Y hacia abajo
    nextY = 1
    while True:
        if getMapValue(x, y + nextY) == TILE_FLOOR:
            coincidences += 1
            if coincidences == numberOfFloors:
                break
        nextY += 1
        # Chequeo que no haya llegado abajo en todo
        # Porque de ser asi, estoy bajando de la ultima plataforma hacia abajo
        if y + nextY > mapHeight-12:
            break
        
    return y+nextY

# Metodo para resetear el timer de un ingrediente
# Le pasamos como parametro la matriz de timer del ingrediente
def resetTimer(ingredient):
    for i in range(0, len(ingredient)):
        ingredient[i] = 0
    return ingredient
              
                
# Metodo para ver si el ingrediente enviado como parametro colisiona con algun otro ingrediente                
def checkCollision(ingredient, numberOfFloors):
    global ingredientsPositions, ingredientsDestinations
    
    # Obtenemos las coordenadas del parametro
    ix, iy = ingredient[0]
    
    # Chequeamos la colision en cada uno de los ingredientes
    for type in range(0, len(ingredientsPositions)):
        # Recorremos cada ingrediente actual 
        for ing in range(0, len(ingredientsPositions[type])):
            if ingredient == ingredientsPositions[type][ing]:
                continue
            ax, ay = ingredientsPositions[type][ing][0]
            if ix == ax and math.floor(iy+1) == ay:
                ingredientsDestinations[type][ing] = moveDown(ingredientsPositions[type][ing], numberOfFloors)
                addScore(500 + int(ingredientsDestinations[type][ing] / 10) * 200)        
        
    

# Metodo para actualizar las posiciones de los ingredientes que estan cayendo
def tickIngredients():
    global ingredientsPositions, ingredientsDestinations
    
    # Recorremos todos los tipos de ingredientes
    for type in range(0, len(ingredientsPositions)):
        # Recorremos cada ingrediente de ese tipo
        for ing in range(0, len(ingredientsPositions[type])):
            if ingredientsDestinations[type][ing] == 0:
                continue
            # Recorremos todas las posiciones para ir bajandolas
            for pos in range(0, len(ingredientsPositions[type][ing])):
                x, y = ingredientsPositions[type][ing][pos]
                y += fallSpeed
                if y > ingredientsDestinations[type][ing]:
                    y = ingredientsDestinations[type][ing]
                # Asignamos el nuevo valor
                ingredientsPositions[type][ing][pos] = (x, y)
            # Chequeamos la colision
            checkCollision(ingredientsPositions[type][ing], ingredientsFloors[type])
            # Vemos si llegamos al destino para quitar el "destino"
            x, y = ingredientsPositions[type][ing][0]
            if y == ingredientsDestinations[type][ing]:
                ingredientsDestinations[type][ing] = 0
                checkCollisionWithMonsters(x, y)  
        
    

# Metodo para poder llevar a cabo el "bajar" las partes
def tickHamburguers():
    global ingredientsFloors, ingredientsDestinations, ingredientsTimers
    # Revisamos si pisamos alguno de los cuadros de los objetos primero.. 
    # De ser asi, iniciamos un temporizador para mantener ese cuadro pisado por X tiempo
    # Y ver si el ingrediente cae    
    # Primero setteamos el timer de lo que estemos pisando y reiniciamos los que no
    
    # Recorremos todos los tipos de ingredientes
    for type in range(0, len(ingredientsPositions)):
        # Recorremos todos los ingredientes de este tipo
        for ing in range(0, len(ingredientsPositions[type])):            
            # Recorremos todas las posiciones del ingrediente actual
            for pos in range(0, len(ingredientsPositions[type][ing])):
                # Vemos si estamos pisando el actual para settearle el tiempo
                x, y = ingredientsPositions[type][ing][pos]
                if math.floor(playerPosition[0]) == x and math.floor(playerPosition[1]) == y:
                    ingredientsTimers[type][ing][pos] = time.time()
                
                # Vemos si se cumplio el tiempo para resetearselo
                if time.time() - ingredientsTimers[type][ing][pos] > TIMETORESET:
                    ingredientsTimers[type][ing][pos] = 0
            
            # Ahora vemos si algun ingrediente ya fue todo pisado para bajarlo       
            # Creamos una variable para ver cuantos items del objeto actual
            # Estan pisados
            checkedItems = 0
            
            # Recorremos todos los cuadros del ingrediente actual
            for sqm in range(0, len(ingredientsTimers[type][ing])):
                # Si es distinto de cero, esta piso y sumo 1 al contador
                if ingredientsTimers[type][ing][sqm] != 0:
                    checkedItems += 1
            # Luego, verifico si el numero de pisados es igual a la longitud del ingrediente
            if checkedItems == len(ingredientsTimers[type][ing]):
                ingredientsFloors[type] = getNumberOfEntitiesOn(ingredientsPositions[type][ing])
                ingredientsDestinations[type][ing] = moveDown(ingredientsPositions[type][ing], ingredientsFloors[type])
                ingredientsTimers[type][ing] = resetTimer(ingredientsTimers[type][ing])
                addScore(ingredientsFloors[type] * 200 + int(ingredientsDestinations[type][ing] / 10) * 300)
                spawnPepper()
                
    
    tickIngredients()
    

# Metodo para pintar las hamburguesas
def renderHamburguers():
    # Recorremos todos los tipos de ingredientes
    for type in range(0, len(ingredientsPositions)):
        # Recorremos todos los ingredientes de ese tipo
        for ing in range(0, len(ingredientsPositions[type])):
            # Recorremos todas las posiciones del ingrediente actual
            for pos in range(0, len(ingredientsPositions[type][ing])):
                x, y = ingredientsPositions[type][ing][pos]
                # Si el ingrediente esta pisado lo pintaremos 10px mas abajo
                offset = 0
                if ingredientsTimers[type][ing][pos] != 0:
                    offset = offsetWhenWalked
                
                # Pintamos la textura izquierda si i = 0
                # Si i = len-1 pintamos la textura derecha
                # Sino la textura central
                textureToUse = 0
                if pos == 0:
                    textureToUse = 0
                elif pos == len(ingredientsPositions[type][ing]) - 1:
                    textureToUse = 2
                else:
                    textureToUse = 1
                drawImageR(ingredientsImages[type][textureToUse], x, y + offset, TILE_SIZE, TILE_SIZE)
    
    

# =====================================================================================
# =====================================================================================
# ================================= Metodos Jugador ===================================
# =====================================================================================
# =====================================================================================

# Metodo para activar el disparo
def shootPepper():
    global canShoot, isShooting, pepperTime, PEPPER_IN_STOCK
    if canShoot and not isShooting and PEPPER_IN_STOCK > 0:
        canShoot = False
        isShooting = True
        PEPPER_IN_STOCK -= 1
        pepperTime = time.time()
        

# Metodo para pintar la pimienta
def renderPepper():
    # Primero pintamos las pimientas que hayan por el mapa
    for i in range(0, len(pepperMapX)):
        if pepperMapX[i] != 0 and pepperMapY[i] != 0:
            drawImageR(pepperImg, pepperMapX[i], pepperMapY[i], pepperSize, pepperSize)
    
    
    # Luego, si estamos disparando, la pimienta que disparamos
    global isShooting, canShoot
    
    if not isShooting:
        return
    
    # Si estamos disparando, entonces pintamos la pimienta en la posicion X
    # Y vamos a ir sumando el  inverso del primer cuadrante del coseno
    cos = (1 - math.cos((time.time() - pepperTime) * 2))
    
    # Si ya se cumplio el primer cuadrante, no pintamos y le activamos que pueda disparar de nuevo
    if cos >= 1:
        isShooting = False
        canShoot = True
        return
    
    # Pintamos la pimienta
    #drawRect(pepperPos[0], pepperPos[1] + cos, pepperSize, pepperSize, getColor("cyan"))
    drawImageR(pepperImg, pepperPos[0], pepperPos[1] + cos, int(pepperSize), int(pepperSize))
    
    

# Metodo para mover la pimienta
def tickPepper():
    #### Para las que esten por el mapa            
    global pepperMapTime, pepperMapX, pepperMapY, PEPPER_IN_STOCK

    for i in range(0, len(pepperMapTime)):
        # Para reiniciarlas
        if time.time() - pepperMapTime[i] > PEPPER_MAX_SPAWN_TIME:
            pepperMapTime[i] = 0
            pepperMapX[i] = 0
            pepperMapY[i] = 0
        # Para ver si la agarramos
        if math.floor(playerPosition[0]) == pepperMapX[i] and math.floor(playerPosition[1]) == pepperMapY[i] and PEPPER_IN_STOCK < MAXPEPPERS:
            PEPPER_IN_STOCK += 1
            pepperMapX[i] = 0
            pepperMapY[i] = 0
    
    #### Para la que estamos disparando
    global pepperPos, pepperLastDir
    
    # Si no estamos disparando, actualizamos la posicion de la pimienta
    if not isShooting:
        pepperPos[0] = playerPosition[0]
        pepperPos[1] = playerPosition[1]
        pepperLastDir = lastXMove
        return
    
    # Si estamos disparando aumentamos la X
    pepperPos[0] += pepperLastDir * PEPPER_SPEED         


# Metodo para actualizar el jugador
def tickPlayer():
    global canClimb, isClimbing, isAlive, isInMenu, isPlaying, playerLifes
    
    tickPepper()
    tickLifeItem()
    
    # Revisamos primero que nada si no estamos vivos para reiniciar todo
    if not isAlive:
        isAlive = True
        playerLifes -= 1
        if playerLifes < 0:
            users[userSelectedId][1].append(SCORE)
            rewriteUsersFile()
            print(users)
            isInMenu = True
            isPlaying = False
            playerLifes = 3
        else:
            initActors()
    
    if canMoveTo(math.floor(playerPosition[0]), math.floor(playerPosition[1]), movementVector, speedX, speedY):
        # Movemos al jugador segun el vector movimiento
        playerPosition[0] += movementVector[0] * speedX
        playerPosition[1] += movementVector[1] * speedY
    
    # Chequeo si no me sali de la ventana
    if playerPosition[0] > mapWidth:
        playerPosition[0] = mapWidth-playerWidth
    elif playerPosition[0] < 0:
        playerPosition[0] = 0
    
    # Como todo aqui tiene que ver con escalar, si isJumping entonces saltamos todo este codigo
    if isJumping:
        return
    
    # Revisamos si esta parado sobre una escalera para permitirle subir
    if (getMapValue(playerPosition[0], playerPosition[1]) == TILE_STAIRS) or (getMapValue(playerPosition[0], playerPosition[1]-1.0) == TILE_STAIRS):
        canClimb = True
    else:
        canClimb = False
    
    # Si estamos subiendo, chequeamos si llegamos arriba en todo o abajo en todo
    if isClimbing:
        # Si estamos en BLANCO y abajo hay ESCALERAS significa que estabamos subiendo, llegamos arriba
        # y nos pasamos.. por lo que debemos mover abajo 1 cuadro al jugador y poner que ya no estamos escalando
        if (getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])) == TILE_NONE and
            getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])+1.0) == TILE_STAIRS):
            playerPosition[1] = math.floor(playerPosition[1])+1.0
            isClimbing = False
        # Si Estamos en PISO y arriba nuestro hay ESCALERAS quiere decir que estabamos bajando y llegamos
        # abajo en todo, por lo que tenemos que decir que ya no estamos escalando y centrarnos en el piso que estamos
        elif (getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])) == TILE_FLOOR and
              getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])-1.0) == TILE_STAIRS):
            isClimbing = False
            playerPosition[1] = math.floor(playerPosition[1])
        # Si por alguna razon lo de arriba falla, esto lo arregla
        elif (getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])) == TILE_FLOOR and
              getMapValue(math.floor(playerPosition[0]), math.floor(playerPosition[1])+1.0) == TILE_FLOOR):
            playerPosition[1] = math.floor(playerPosition[1])-1.0
            isClimbing = False
        

# Metodo para pintar el HUD del jugador
def renderHUD():
    # Pintamos las vidas
    for i in range(0, playerLifes):
        drawImageR(lifeImg, 1 + i, 1, lifeSize, lifeSize)        
    
    #drawString(1, 1, "Vidas: " + str(playerLifes), "Consolas", getColor("white"), 32)  
    drawString(30, 1, "Score: " + str(SCORE), "Consolas", getColor("white"), 28)
    drawString(mapWidth/2.0 - 1.0, 0.5, "Nivel " + str(actualLevel), "Tahoma", getColor("white"), 20)
    
    # Pintamos la pimienta restante 
    for i in range(0, PEPPER_IN_STOCK):        
        drawImageR(pepperImg, 1 + i, 2, pepperSize, pepperSize)    
    

# Metodo para pintar los items de vida por el mapa
def renderLifeItems():
    for i in range(0, len(lifeMapX)):
        if lifeMapX[i] != 0 and lifeMapY[i] != 0:
            drawImageR(lifeImg, lifeMapX[i], lifeMapY[i], lifeSize, lifeSize)


    
# Metodo para obtener la textura que vamos a usar para pintar
def setPlayerActualTexture():
    global actualImageToDraw
    
    # Actualizamos que textura se debe pintar mediante el vector movimiento
    if isClimbing:
        # Necesitamos ver el status actual, y si es el mismo sumamos uno para pintar la sig imagen
        actualStatus, actualImgId = actualImageToDraw
        
        # Si el status es el mismo que el anterior, sumamos uno al id de imagen
        if actualStatus == PIMAGE_CLIMBING:                
            actualImgId += 1
            # Chequeamos no pasarnos del limite de spritesheets
            if actualImgId >= len(pImages[actualStatus]):
                actualImgId = 0                
        # Sino, setteamos el nuevo spritesheet y comenzamos de 0
        else:
            actualImgId = 0
            actualStatus = PIMAGE_CLIMBING
            
        actualImageToDraw = (actualStatus, actualImgId)          
    elif not isWalking:
        actualImageToDraw = (PIMAGE_STAND, 0)
    elif isWalking:
        # Si esta caminando, vemos hacia donde esta caminando con el vector de movimiento
        dir, nvm = movementVector # Dir va a tener nuestra coord X, nvm no nos sirve de nada pero es necesario
        if dir == 1:               
            # Necesitamos ver el status actual, y si es el mismo sumamos uno para pintar la sig imagen
            actualStatus, actualImgId = actualImageToDraw
            
            # Si el status es el mismo que el anterior, sumamos uno al id de imagen
            if actualStatus == PIMAGE_WRIGHT:                
                actualImgId += 1
                # Chequeamos no pasarnos del limite de spritesheets
                if actualImgId >= len(pImages[actualStatus]):
                    actualImgId = 0                
            # Sino, setteamos el nuevo spritesheet y comenzamos de 0w
            else:
                actualImgId = 0
                actualStatus = PIMAGE_WRIGHT
                
            actualImageToDraw = (actualStatus, actualImgId)
        else:
            # Necesitamos ver el status actual, y si es el mismo sumamos uno para pintar la sig imagen
            actualStatus, actualImgId = actualImageToDraw
            
            # Si el status es el mismo que el anterior, sumamos uno al id de imagen
            if actualStatus == PIMAGE_WLEFT:                
                actualImgId += 1
                # Chequeamos no pasarnos del limite de spritesheets
                if actualImgId >= len(pImages[actualStatus]):
                    actualImgId = 0                
            # Sino, setteamos el nuevo spritesheet y comenzamos de 0
            else:
                actualImgId = 0
                actualStatus = PIMAGE_WLEFT
                
            actualImageToDraw = (actualStatus, actualImgId)
    return actualImageToDraw
    



# Metodo para pintar el jugador
def renderPlayer():    
    global jumpOffset, canJump, isJumping, canClimb, actualImageToDraw
    
    # Si estoy saltando, entonces obtengo el offset de salto y le cambio el signo
    if isJumping:
        jumpOffset = -math.sin((time.time() - jumpTimer)* jumpSpeed) * jumpHeight
    
    # Si el offset de salto es positivo, quiere decir que termino el salto (grafica del seno entre 0 y pi)
    # entonces, reseteo todos los valores para poder escalar y saltar de nuevo..
    if jumpOffset > 0:
        jumpOffset = 0
        canJump = True
        canClimb = True
        isJumping = False
        
    # Setteamos la textura actual
    setPlayerActualTexture()
    
    # Pintamos el rectangulo de area del jugador
    #drawRect(playerPosition[0], playerPosition[1] + jumpOffset, playerWidth, playerHeight, ((193 << 16) | (193 << 8) | 193))
    
    # Finalmente, pintamos
    status, imgId = actualImageToDraw
    drawImageR(pImages[status][imgId], playerPosition[0] - playerWidth/2, playerPosition[1] + jumpOffset - 1, playerWidth, playerHeight)
    
    # Centro del jugador (Provisional)
    #drawRect(playerPosition[0], playerPosition[1], 0.3, 0.3, getColor("green"))
        
    # Pintamos el HUD del jugador
    renderHUD()
    
    # Pintamos la pimienta que lanzamos (si es que la lanzamos)
    renderPepper()
    
    # Pintamos los items de vida por el mapa
    renderLifeItems()
    
    

# Metodo para activar el teclado en modo jugador
def inputPlayer(e):
    global playerX, playerY, enterPressed, isClimbing, canJump, isJumping, jumpTimer, canClimb, isPaused, movementVector, lastXMove, isWalking
    
    # Primero chequeamos si se pauso el juego, para asi saltar todo este codigo
    if e == KEY_P or e == KEY_p:
        # Invertimos el valor de isPaused
        isPaused = not(isPaused)
        
    # Si al invertirlo es TRUE, quiere decir que el juego esta pausado, saltamos todo este codigo
    if isPaused:
        return
    
    if (e == KEY_D or e == KEY_RIGHT or e == KEY_d) and not (isClimbing):
        movementVector = [1,0]
        lastXMove = 1
        isWalking = True
    elif (e == KEY_A or e == KEY_LEFT or e == KEY_a) and not (isClimbing):
        movementVector = [-1,0]
        lastXMove = -1
        isWalking = True
    elif (e == KEY_S or e == KEY_DOWN or e == KEY_s) and (canClimb or isClimbing):
        movementVector = [0,1]
        isWalking = False
        isClimbing = True
        canJump = False
    elif (e == KEY_W or e == KEY_UP or e == KEY_w) and (canClimb or isClimbing):        
        movementVector = [0,-1]
        isWalking = False
        isClimbing = True
        canJump = False
    elif not isClimbing:
        isWalking = False
        canJump = True

    # Si va a saltar, le prohibo que escale y salte nuevamente hasta que vuelva a caer
    # Ademas, obtengo el tiempo actual (ms) para usarlo al calcular el offset de salto
    # mediante la funcion seno, que entre [0,pi] es positiva, entonces, este tiempo
    # que se guarde aqui menos el tiempo actual van a dar numeros que comenzaran en 0
    # e iran subiendo, para asi obtener la curva del seno como salto
    if e == KEY_SPACE and canJump and not isJumping:
        canJump = False
        isJumping = True
        canClimb = False
        jumpTimer = time.time() # Parametro para el seno
    
    # Pimienta
    if e == KEY_f:
        shootPepper()
        
    if e == KEY_ENTER:
        enterPressed = True
    else:
        enterPressed = False
        
        

# =====================================================================================
# =====================================================================================
# ============================ Inteligencia Articial ==================================
# =====================================================================================
# =====================================================================================

# Metodo para ver si los monstruos colisionan con la pimienta disparada
def monstersCheckCollision():
    global respawnArray, mX, mY, monstersPaths
    
    if isShooting:
        for m in range(0, len(mNames)):
            # Colision con la pimienta lanzada
            if ((pepperPos[0] + pepperSize/2.0 >= mX[m]) 
                and (pepperPos[0] + pepperSize/2.0 <= mX[m] + mWidth[m])
                and (pepperPos[1] + pepperSize/2.0 >= mY[m])
                and (pepperPos[1] + pepperSize/2.0 <= mY[m] + mHeight[m])):
                # Si entra aqui, la pimienta le pego
                addScore(350)
                respawnArray[m] = time.time()
                monstersPaths[m] = None
                r = getRandomMapPosition()
                mX[m] = convertToMapX(r)
                mY[m] = convertToMapY(r)                
                


# Metodo para hacer que reaparezcan los monstruos
def respawnMonsters():
    global respawnArray
    
    for m in range(0, len(mNames)):
        if respawnArray[m] != 0:
            if time.time() - respawnArray[m] > RESPAWNTIME:
                respawnArray[m] = 0


# Metodo para arreglar la posicion del monstruo al subir
def getYFixed(mx, my, mHeight):
    mx = math.floor(mx)
    my = math.floor(my)
    
    if getMapValue(mx, my) == TILE_NONE:
        return mHeight
    return 0

# Setteamos la textura actual a pintar
def setMonsterActualTexture(mDir, mAct):
    global monstersActualImageToDraw
    
    # Obtenemos el status actual y el img id actual
    actualStatus, actualImgId = monstersActualImageToDraw[mAct]
    
    if mDir == 1:
        # Si el status es el mismo que el anterior, sumamos uno a la imagen
        if actualStatus == MIMAGE_WLEFT:
            actualImgId += 1
            # Chequeamos no habernos pasado del limite de imgs
            if actualImgId >= len(allMonstersImages[monstersInLevel[mAct]][actualStatus]):
                actualImgId = 0
        # Sino, setteamos el nuevo spritesheet desde 0
        else:
            actualImgId = 0
            actualStatus = MIMAGE_WLEFT
    else:
        # Si el status es el mismo, sumamos
        if actualStatus == MIMAGE_WRIGHT:
            actualImgId += 1
            # Chequeamos no pasarnos...
            if actualImgId >= len(allMonstersImages[monstersInLevel[mAct]][actualStatus]):
                actualImgId = 0
        # Sino, setteamos desde 0
        else:
            actualImgId = 0
            actualStatus = MIMAGE_WRIGHT
            
    monstersActualImageToDraw[mAct] = (actualStatus, actualImgId)
    
            
    
    
    
    

# Metodo para que se muevan los monstruos
def tickMonsters():
    global isAlive, monstersActualImageToDraw, monstersPaths
    
    respawnMonsters()
    
    # Recorremos todos los monstruos
    for i in range(0, len(monstersInLevel)):
        # Si el monstruo no esta visible no queremos hacer nada.. asi que chequeamos
        if respawnArray[i] != 0:
            continue
        
        # Obtenemos la posicion del jugador respecto al mapa
        playerPos = (math.floor(playerPosition[0]), math.floor(playerPosition[1]))

        # Arreglamos la Y del monstruo por si esta bugeada
        mY[i] += getYFixed(mX[i], mY[i], mHeight[i])
        
        # Obtenemos la posicion del monstruo respecto al mapa
        monsterPos = (math.floor(mX[i]), math.floor(mY[i]))

        # Calculamos el camino
        # Si no esta setteado el camino, lo setteamos
        if monstersPaths[i] == None:
            monstersPaths[i] = getPathTo(monsterPos, playerPos, [], [], [], 0)
        else:    
            # Si ya existe el camino, chequeamos si el ultimo nodo es distinto a la posicion del jugador
            # De ser asi, la unica opcion posible es que se halla movido 1 cuadro hacia N,S,E,O
            # En dado caso de ser asi, se debe pegar la nueva posicion del jugador al camino si es que
            # esta posicion no existe en el camino.. De ya existir, se debe restar la ultima al camino       
            if monstersPaths[i][len(monstersPaths[i]) - 1] != playerPos:
                #print("Hubo un cambio!")
                if playerPos in monstersPaths[i]:
                    #print("Quitando el ultimo: " + str(monstersPaths[i][len(monstersPaths[i]) - 1]))
                    monstersPaths[i].remove(monstersPaths[i][len(monstersPaths[i]) - 1])                    
                else:
                    #print("Anadiendo playerPos: " + str(playerPos))
                    monstersPaths[i].append(playerPos)
        
            # Chequeo si ya esta en el primer nodo de su camino para quitar ese nodo
            if monstersPaths[i][0] == monsterPos:
                monstersPaths[i].remove(monstersPaths[i][0])
                    
        
        path = getPathTo(monsterPos, playerPos, [], [], [], 0)
        
        if path == True or path == False:
            isAlive = False
            return
       
        # Obtenemos el vector de movimiento
        mVector = getMovementVector(monstersPaths[i], math.floor(mX[i]), math.floor(mY[i])) 
        
        # Evitar que queden abajito al subir       
        if mY[i] > math.floor(mY[i]) and mVector[0] != 0:
            mY[i] = math.floor(mY[i])
             
        # Lo sumamos        
        if mVector[0] != 0:
            mX[i] += mSpeedX[i] * mVector[0]            
        elif mVector[1] != 0:
            mY[i] += mSpeedY[i] * mVector[1] # Calculamos primero la nueva Y antes de asignarla para evitar bug
        
        setMonsterActualTexture(mVector[0], i)
            
    monstersCheckCollision()



# Metodo para pintar los monstruos
def renderMonsters():    
    # Pintamos todos los monstruos
    for i in range(0, len(monstersInLevel)):
        if respawnArray[i] == 0:
            status, imgId = monstersActualImageToDraw[i]
            drawImageR(allMonstersImages[monstersInLevel[i]][status][imgId], mX[i], mY[i], mWidth[i], mHeight[i])
            #drawRect(mX[i], mY[i], mWidth[i], mHeight[i], getColor("green"))
            #drawString(mX[i]-(mWidth[i]/2.8), mY[i]-15, mNames[i], "Consolas", getColor("white"), 12)   
        

# =====================================================================================
# =====================================================================================
# ============================ Menu Creacion usuario ==================================
# =====================================================================================
# =====================================================================================

def inputSelectingUser(e):
    global selectingProfileStates, strWritten, userSelected, userWritten, isSelectingProfile
    
    chr = e.unicode
    key = e.key
    
    if key == KEY_BACKSPACE:
        strWritten = strWritten[:len(strWritten)-1]
    elif key == KEY_ENTER or key == KEY_NUMPADENTER: 
        for i in range(0, len(selectingProfileStates)):
            if selectingProfileStates[i] == True:
                selectingProfileStates[i] = False
                userWritten[i] = strWritten
                strWritten = ""
                # Activo el siguiente estado si hay..
                if i+1 < len(selectingProfileStates):
                    selectingProfileStates[i+1] = True                    
                    break
                else:
                    userSelected = doLogin(userWritten[0], userWritten[1])
                    isSelectingProfile = False
                
    else:
        strWritten += chr
    
def inputCreatingUser(e):
    global creatingNewProfileStates, isCreatingNewProfile, strWritten, newUserWritten, infoMessage, infoMessageTimer
    
    chr = e.unicode
    key = e.key
    
    if key == KEY_BACKSPACE:
        strWritten = strWritten[:len(strWritten)-1]
    elif key == KEY_ENTER or key == KEY_NUMPADENTER:
        for i in range(0, len(creatingNewProfileStates)):
            if creatingNewProfileStates[i] == True:
                creatingNewProfileStates[i] = False
                newUserWritten[0][i] = strWritten
                strWritten = ""
                # Activo el sig estado si hay
                if i+1 < len(creatingNewProfileStates):
                    creatingNewProfileStates[i+1] = True
                    break
                else:
                    # Chequeamos si el usuario no existe ya
                    if not userExists(newUserWritten[0][0]):
                        # Creamos el nuevo usuario en memoria
                        users.append(newUserWritten)
                        print(users)
                        isCreatingNewProfile = False
                        rewriteUsersFile()
                        print(users)
                    else: # Ya existe
                        isCreatingNewProfile = False
                        infoMessage = "El usuario ya existe"
                        infoMessageTimer = time.time()
    else:
        strWritten += chr
                    
                
                
def inputUserMenu(e):
    global userMenuSelectedOption, isInUserMenu, isInMenu, isCreatingNewProfile, isSelectingProfile, creatingNewProfileStates, selectingProfileStates

    chr = e.unicode
    key = e.key
    
    # Chequeo si estoy seleccionando o creando primero
    if selectingProfileStates[0] or selectingProfileStates[1]:
        inputSelectingUser(e)
        return
    elif (creatingNewProfileStates[0] or creatingNewProfileStates[1] or creatingNewProfileStates[2] or creatingNewProfileStates[3]
          or creatingNewProfileStates[4] or creatingNewProfileStates[5]):
        inputCreatingUser(e)
        return
    
    if (key == KEY_UP or chr == "w" or chr == "W") and (userMenuSelectedOption > 1):
        userMenuSelectedOption -= 1
    elif (key == KEY_DOWN or chr == "s" or chr == "S") and (userMenuSelectedOption < USERMENU_MAXOPTIONS):
        userMenuSelectedOption += 1
        
    if key == KEY_ENTER or key == KEY_NUMPADENTER:
        if userMenuSelectedOption == USERMENU_BACK:
            isInMenu = True
            isInUserMenu = False
        elif userMenuSelectedOption == USERMENU_SELECT:
            isSelectingProfile = True
            selectingProfileStates[0] = True
        elif userMenuSelectedOption == USERMENU_CREATE:
            isCreatingNewProfile = True
            creatingNewProfileStates[0] = True
        
    
# El menu de seleccionar usuario
def renderSelectingUser():
    # Optimizar a un simple for...
    
    # Introduciendo usuario
    if selectingProfileStates[0]:
        drawString(10, 10, "Usuario", "Consolas", getColor("white"), 60)
    # Introduciendo contrasena
    elif selectingProfileStates[1]:
        drawString(10, 10, "Clave", "Consolas", getColor("white"), 60)    
    
    drawRect(10, 15, 20, 2, getColor("white"))
    drawString(11, 15.5, strWritten, "Consolas", getColor("black"), 24)
    
    
    
# El menu de creacion de usuario
def renderCreatingUser():
    # Optimizar a un simple for...
    
    # Introduciendo Nickname
    if creatingNewProfileStates[0]:
        drawString(10, 10, "Usuario", "Consolas", getColor("white"), 60)
    # Introduciendo clave
    elif creatingNewProfileStates[1]:
        drawString(10, 10, "Clave", "Consolas", getColor("white"), 60)
    # Introduciendo nombre
    elif creatingNewProfileStates[2]:
        drawString(10, 10, "Nombre", "Consolas", getColor("white"), 60)
    # Introduciendo apellido
    elif creatingNewProfileStates[3]:
        drawString(10, 10, "Apellido", "Consolas", getColor("white"), 60)
    # Introduciendo email
    elif creatingNewProfileStates[4]:
        drawString(10, 10, "Email", "Consolas", getColor("white"), 60)
    # Introduciendo telefono
    elif creatingNewProfileStates[5]:
        drawString(10, 10, "Numero", "Consolas", getColor("white"), 60)
    
    drawRect(10, 15, 20, 2, getColor("white"))
    drawString(11, 15.5, strWritten, "Consolas", getColor("black"), 24)



# El menu de seleccion de usuario
def renderMenuUser(): 
    global MENU_TITLE_TWO
    
    if MENU_TITLE_TWO == None:
        MENU_TITLE_TWO = pygame.image.load("../res/logo.jpg")
    # Pintamos el titulo
    drawImageR(MENU_TITLE_TWO, 5, 0.2, 30, 10)
    
    
    
    for i in range(0, len(userMenuOptions)):
        if userMenuSelectedOption-1 == i:
            color = getRandomColor()
        else:
            color = getColor("white")
        drawString(userMenuX[i], userMenuY[i], userMenuOptions[i], "Consolas", color, 40)
    


def renderUserMenu():
    if isSelectingProfile: 
        renderSelectingUser()
    elif isCreatingNewProfile:
        renderCreatingUser()
    else:
        renderMenuUser()
        
    # Pintamos el usuario actual
    if userSelected[0][0] == "Login Failed":
        drawString(9, 28, "Usuario o clave incorrecta!", "Consolas", getColor("red"), 30)        
    elif userSelected[0][0] == "No Seleccionado":
        drawString(11, 28, "No has iniciado sesion!", "Consolas", getColor("red"), 30)
    else:
        drawString(15, 28, "Hola " + userSelected[0][0] + "!", "Consolas", getColor("green"), 30)
        
    # Pintamos el mensaje
    drawString (9, 26, infoMessage, "Consolas", getColor("red"), 40)
    resetInfoMessage()
    

# =====================================================================================
# =====================================================================================
# ================================== Otros Menus ======================================
# =====================================================================================
# =====================================================================================

def getHighscores(level):
    # Devolveremos un arreglo de strings
    usernames = []
    highscores = []
    
    # Si queremos los highscores globales
    if level == "T":
        # Recorremos todos los usuarios
        for user in users:
            # Pegamos el nombre y un nuevo puntaje
            usernames.append(user[0][0])
            highscores.append(0)
            # Recorremos todos los niveles
            for lvl in user[1]:
                # Recorremos todos los puntajes del nivel actual y guardamos el mayor
                higher = 0
                for pts in lvl:
                    if int(pts) > higher:
                        higher = int(pts)
                # Luego que tengamos el puntaje mas alto de ese nivel, lo sumamos
                highscores[len(highscores)-1] += higher
    # Sino, es porque queremos de un nivel en especifico
    # Entonces anadiremos todos los puntajes de todos los jugadores al arreglo, y despues sacaremos los mas grandes
    else:
        lvlWanted = int(level)
        numberOfScoresFound = 0
        # Recorremos todos los usuarios
        for user in users:
            # Pegamos el nombre y un nuevo puntaje
            usernames.append(user[0][0])
            highscores.append([])
            # Recorremos todos los puntajes del nivel que quiero
            for pts in user[1][lvlWanted-1]:
                highscores[len(highscores)-1].append(int(pts))
                numberOfScoresFound += 1
        # Luego de haber anadido todos los puntajes de todos los usuarios
        # Creamos unos auxiliares donde pegaremos lo que nos importa
        newUsernames = []
        newHighscores = []
        # Haremos un for para mostrar 10 highscores
        for i in range(0, numberOfScoresFound):     
            # Solo queremos 10
            if i >= 10:
                break
                   
            # Creamos una variable para guardar el mas alto
            higher = 0
            # Y otra para el nombre
            usernameNumber = -1
            # Recorremos todos los usernames con sus highscores
            for u in range(0, len(usernames)):
                for k in range(0, len(highscores[u])):
                    if highscores[u][k] > higher:
                        higher = highscores[u][k]
                        usernameNumber = u
            # Luego de haber obtenido el puntaje mas alto con su usuario, sacamos ese puntaje
            highscores[usernameNumber].remove(higher)
            # Lo sumamos a nuestro arreglo BIEN
            newUsernames.append(usernames[usernameNumber])
            newHighscores.append(higher)         

        usernames = newUsernames
        highscores = newHighscores
    
    return (usernames, highscores)
                
    
    

def renderHighscores():
    drawString(1, 2, "Presiona 1,2,3,4,5,6,7,8,T para ver los puntajes", "Consolas", getColor("cyan"), 29)
    usernames, highscores = getHighscores(actualHighscore)
    
    # Pintamos el titulo
    if actualHighscore == "T":
        drawString(8, 5, "Altos puntajes globales", "Consolas", getColor("red"), 40)
    else:
        drawString(5, 5, "Altos puntajes del nivel: " + str(actualHighscore), "Consolas", getColor("red"), 40)
    
    drawString(6, 8, "Nombre", "Consolas", getColor("blue"), 30)
    drawString(22, 8, "Puntaje", "Consolas", getColor("blue"), 30)
    
    yPaint = 10   
    
    # Pintamos cada puntuacion
    for i in range(0, len(highscores)):
        drawString(6, yPaint, str(usernames[i]), "Consolas", getColor("white"), 25)
        drawString(22, yPaint, str(highscores[i]), "Consolas", getColor("white"), 25)
        yPaint += 2
        
    
    
    
def renderHowToPlay():
    drawString(10, 2, "Como jugar?", "Consolas", getColor("white"), 70)
    drawString(9, 8, "W,A,S,D o las flechas para moverte", "Consolas", getColor("white"), 25)
    drawString(12, 11, "F para disparar pimienta", "Consolas", getColor("white"), 25)
    drawString(10, 14, "Barra espaciadora para saltar", "Consolas", getColor("white"), 25)
    drawString(16, 17, "P para pausar", "Consolas", getColor("white"), 25)
    
    drawString(2.8, 28.5, "Mas informacion en http://www.salazarseijas.com/burgertime", "Consolas", getColor("cyan"), 22)
    

def renderOtherMenus():
    if isInHighscores:
        renderHighscores()
    elif isInHowToPlay:
        renderHowToPlay()
        
    drawString(8.5, 28.5, "Presiona ESC para volver al menu principal", "Consolas", getColor("white"), 20)
    
def inputOtherMenus(e):
    global isInMenu, isInHighscores, isInHowToPlay, actualHighscore
    print(e)
    if e == KEY_ESC:
        isInMenu = True
        isInHighscores = False
        isInHowToPlay = False
        
    # Para lo de highscore actualHighscore
    if e == KEY_T:
        actualHighscore = "T"
    elif e == KEY_1 or e == KEY_NUMPAD1:
        actualHighscore = "1"
    elif e == KEY_2 or e == KEY_NUMPAD2:
        actualHighscore = "2"
    elif e == KEY_3 or e == KEY_NUMPAD3:
        actualHighscore = "3"
    elif e == KEY_4 or e == KEY_NUMPAD4:
        actualHighscore = "4"
    elif e == KEY_5 or e == KEY_NUMPAD5:
        actualHighscore = "5"
    elif e == KEY_6 or e == KEY_NUMPAD6:
        actualHighscore = "6"
    elif e == KEY_7 or e == KEY_NUMPAD7:
        actualHighscore = "7"
    elif e == KEY_8 or e == KEY_NUMPAD8:
        actualHighscore = "8"


# =====================================================================================
# =====================================================================================
# ================================= Menu del Juego ====================================
# =====================================================================================
# =====================================================================================

# Metodo para cargar un nivel
def loadLevel(level):
    global map    
    map = loadMap("level" + str(level) + ".png")


    
# Metodo para pintar el menu de seleccion de nivel
def renderLevelSelection():
    coordRect = 18.0
    drawString(3, 10, "Introduzca el numero del nivel que desea jugar", "Consolas", getColor("white"), 28)
    drawRect(coordRect, 12, 4, 4, getColor("white"))
    drawString(coordRect + 1.2, 13, str(levelSelected), "Consolas", getColor("black"), 52)
    
# Metodo para activar el teclado en la seleccion de nivel
def inputLevelSelection(e):
    global enterPressed, isPlaying, isSelectingLevel, levelSelected, actualLevel
    
    if e == KEY_1 or e == KEY_NUMPAD1:
        levelSelected = 1
    elif e == KEY_2 or e == KEY_NUMPAD2:
        levelSelected = 2
    elif e == KEY_3 or e == KEY_NUMPAD3:
        levelSelected = 3
    elif e == KEY_4 or e == KEY_NUMPAD4:
        levelSelected = 4
    elif e == KEY_5 or e == KEY_NUMPAD5:
        levelSelected = 5
    elif e == KEY_6 or e == KEY_NUMPAD6:
        levelSelected = 6
    elif e == KEY_7 or e == KEY_NUMPAD7:
        levelSelected = 7
    elif e == KEY_8 or e == KEY_NUMPAD8:
        levelSelected = 8
        
    if e == KEY_ENTER:
        isSelectingLevel = False
        actualLevel = levelSelected
        loadLevel(levelSelected)
        isPlaying = True
        initActors()


# Metodo para actualizar el menu
def tickMenu():
    malditoPythonQueNoDejaInicializarFuncionesVacias = 1 # Aqui van a ir los efectos al menu
    
# Metodo para pintar el menu
def renderMenu():     
    global selectedOptionX, MENU_TITLE
    
    if MENU_TITLE == None:
        MENU_TITLE = pygame.image.load("../res/mainName.jpg")
    
    # Pintamos el mensaje principal "MENU"
    #drawString(15, 1.5, "Menu", "Consolas", getColor("white"), 102)
    drawImageR(MENU_TITLE, 3, 0.5, 35, 10)
    
    # Pintamos todas las opciones del menu
    for i in range(0, len(optionNames)):
        if i+1 == selectedOption:
            color = getRandomColor()
        else:
            color = getColor("white")
        drawString(optionXCoords[i], optionYCoords[i], optionNames[i], "Consolas", color, 38)     

    
    # Pintamos el usuario actual

    if userSelected[0][0] == "Login Failed":
        drawString(9, 28, "Usuario o clave incorrecta!", "Consolas", getColor("red"), 30)        
    elif userSelected[0][0] == "No Seleccionado":
        drawString(11, 28, "No has iniciado sesion!", "Consolas", getColor("red"), 30)
    else:
        drawString(15, 28, "Hola " + userSelected[0][0] + "!", "Consolas", getColor("green"), 30)
        
    # Pintamos el mensaje
    drawString (5, 26, infoMessage, "Consolas", getColor("red"), 30)
    resetInfoMessage()
    
    
# Metodo para activar el teclado en modo Menu
def inputMenu(e):
    global isInHighscores, isInHowToPlay, selectedOptionY, selectedOption, enterPressed, isInMenu, isPlaying, isSelectingLevel, isInUserMenu,infoMessage, infoMessageTimer

    # Movemos el cursor del menu segun sea la tecla
    if (e == KEY_DOWN or e == KEY_S or e == KEY_s) and (selectedOption > 1):
        selectedOptionY += distanceBetweenOptions
        selectedOption -= 1
    elif (e == KEY_W or e == KEY_UP or e == KEY_w) and (selectedOption < MAX_OPTIONS):
        selectedOptionY -= distanceBetweenOptions
        selectedOption += 1
    
    # Chequeamos si se presiono ENTER
    if e == KEY_ENTER or e == KEY_NUMPADENTER:
        if selectedOption == MENU_PLAY:
            print(userSelected[0][0])
            if userSelected[0][0] != "No Seleccionado" and userSelected[0][0] != "Login Failed":
                isInMenu = False
                isSelectingLevel = True
            else:
                infoMessage = "Debes seleccionar un usuario primero"
                infoMessageTimer = time.time()
        elif selectedOption == MENU_SELECTUSER:
            isInMenu = False
            isInUserMenu = True    
            infoMessage = ""   
        elif selectedOption == MENU_HIGHSCORES:
            isInMenu = False
            isInHighscores = True     
        elif selectedOption == MENU_HOWTOPLAY:
            isInMenu = False
            isInHowToPlay = True
        elif selectedOption == MENU_EXIT:
            sys.exit()
    
        
        
        

# =====================================================================================
# =====================================================================================
# ============================== Metodos del Juego ====================================
# =====================================================================================
# =====================================================================================

# Metodo para ver si se completo el nivel
def tickLevel():    
    global actualLevel, isPlaying, isInMenu
    
    for p in range(0, len(breadTopPositions)):
        x, y = breadTopPositions[p][0]
        
        if y < INGREDIENTS_FLOOR:
            return
    
    # Si llega aqui es porque terminamos el nivel
    addFinalScore(userSelected[0][0], actualLevel)
    rewriteUsersFile()
    
    actualLevel += 1
    print(str(actualLevel) + " de " + str(TOTALLEVELS))
    
    if actualLevel <= TOTALLEVELS:
        loadLevel(actualLevel)
        initActors()
    else:        
        isPlaying = False
        isInMenu = True
    


# Pintar todo lo referente al juego (cuando se esta jugando)
def renderGame():    
    # Pintamos el mapa
    drawMap()
    
     # Luego de haber pintado el mapa, pintamos las hamburguesas
    renderHamburguers()
    
    # Pintamos el jugador
    renderPlayer()
    
    # Pintamos los monstruos
    renderMonsters()
    
    # Si esta pausado el juego, pintamos un Texto que nos lo diga
    if isPaused:
        drawString(mapWidth/4, mapHeight/4, "PAUSA", "Consolas", getColor("white"), 140)
    
    
# Actualizar el juego (cuando se esta jugando)
def tickGame():
    tickLevel()
    # Actualizamos solo si el juego no esta pausado
    if not isPaused:
        tickMonsters()
        tickPlayer()
        tickHamburguers()



# Tick method (Aqui va a suceder toda la logica del juego)
def tick():
    if isInMenu:
        tickMenu()
    elif isPlaying:
        tickGame()
        
        
# Input method (Aqui va a controlarse todo lo referente a el teclado/mouse)
def input(e):   
    key = e.key 

    if isInMenu:
        inputMenu(key)
    elif isSelectingLevel:
        inputLevelSelection(key)
    elif isInUserMenu:
        inputUserMenu(e)
    elif isInHighscores or isInHowToPlay:
        inputOtherMenus(key)
    else:
        inputPlayer(key)       
        
    
# Render method (Aqui se pinta el mapa de juego en base a la matriz)
def render():          
    if isInMenu:
        renderMenu()
    elif isSelectingLevel:
        renderLevelSelection()
    elif isInUserMenu:
        renderUserMenu()
    elif isInHighscores or isInHowToPlay:
        renderOtherMenus()
    elif isPlaying:
        renderGame()



# Loop principal
def mainLoop():
    global window, pygameClock
    
    # Iniciamos pygame
    pygame.init()
    
    # Creamos la ventana, el primer parametro son las dimensiones, el segundo NPI, el tercero los bits
    window = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
    
    # Setteamos el titulo
    pygame.display.set_caption(windowTitle)
    
    # Setteamos el icono
    icon = pygame.image.load("../res/icon.png").convert_alpha()
    pygame.display.set_icon(icon)
    
    
    # Setteamos nuestro reloj para manejar el tiempo
    pygameClock = pygame.time.Clock()
    
    # Fps counter mierdero xd
    startTime = time.time()
    lastTime = startTime
    deltaTime = 0
    secAcum = 0
    fps = 0
    
    while True:
        startTime = time.time()
        deltaTime = startTime - lastTime
        lastTime = startTime
        secAcum += deltaTime
        if secAcum > 1.0:
            print(fps, " fps")
            fps = 0
            secAcum = 0
        else:
            fps += 1
            
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                releaseKeys()
            elif event.type == KEYDOWN:
                input(event)
            
        
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().set_alpha(255)     
        tick()
        render()      
        pygameClock.tick(5000)
        pygame.display.update()



# =====================================================================================
# =====================================================================================
# =============================== COMENZAR EL JUEGO ===================================
# =====================================================================================
# =====================================================================================

# No se conecta :(
#dbConnection = pymssql.connect(host="host.racksystem2.com", user="salazars_btime", password="21115476eD2567641", database="salazars_burgertime")

loadUsers()
loadGameObjects()

# Iniciamos el juego
mainLoop()


















