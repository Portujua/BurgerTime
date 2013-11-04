# Imports
import sys
import math
import time
import pygame
import random
from pygame.locals import *

import PIL.Image

# ============================== Variables ==============================

# Constantes MENU
MENU_PLAY = 2
MENU_EXIT = 1
MAX_OPTIONS = 2

# Propiedades del menu
# Para crear una opcion nueva es igual que los monstruos, se anade 1 item a cada arreglo de opciones
# se modifica arriba MAX_OPTIONS, y se anade la opcion nueva

selectedOption = 2              # Opcion seleccionada por defecto
selectedOptionY = 200           # Coordenada Y del cursor en el menu
selectedOptionX  = 260          # Coordenada X del cursor del menu
selectedOptionWidth = 50        # Ancho del cursor del menu
selectedOptionHeight = 50       # Alto del cursor del menu
distanceBetweenOptions = 100    # Distancia entre cada opcion del menu (para mover el triangulo)

optionNames = ["Salir", "Jugar"]
optionXCoords = [17, 17]
optionYCoords = [15.5, 10.5]


# Estados del juego
isInMenu = True
isCreatingNewProfile = False
isSelectingProfile = False
isPlaying = False
isPaused = False
isRunning = True
isSelectingLevel = False
isSwitchingLevel = False
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
KEY_ENTER = 13
KEY_SPACE = 32

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
COLOR_BREAD = 0xFF9D00
COLOR_LETTUCE = 0x62D551

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
WALKABLE_TILES = [1,2,6,7,8]


# Propiedades de la pimienta
pepperPos = [0, 0]
pepperTime = 0
pepperSize = 0.4
pepperLastDir = 0
PEPPER_SPEED = 0.08


### ---------- Propiedades de la/s hamburguesas ------------
# Imagenes
BREAD_PATH = "../res/textures/game/hamburguer/bread/"
LETTUCE_PATH = "../res/textures/game/hamburguer/lettuce/"
MEAT_PATH = "../res/textures/game/hamburguer/meat/"

breadImages = []
lettuceImages = []
meatImages = []

# Posiciones
breadPositions = []
lettucePositions = []
meatPositions = []

# Temporizadores para controlar el pisado
breadTimers = []
lettuceTimers = []
meatTimers = []

# Destinos (para ver si un ingrediente esta bajando..)
breadDestination = []
lettuceDestination = []
meatDestination = []

breadFloors = []
lettuceFloors = []
meatFloors = []

# Otros
TIMETORESET = 2.000000000
offsetWhenWalked = 0.2
fallSpeed = 0.1
INGREDIENTS_FLOOR = 29


### ---------- Propiedades del Jugador ----------

SCORE = 0

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
playerPosition = [3., 23.]



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
                        "../res/textures/game/monsters/climbing/" # MIMAGE_CLIMBING
                        ]


# Imagenes del jugador, crearemos solamente los array en blanco con el numero de imagenes que son
mImages = [[0,0,0,0], # MIMAGE_WRIGHT   Inicializamos con la cantidad de imagenes
           [0,0,0,0], # MIMAGE_WLEFT
           #[0,0] # MIMAGE_CLIMBING
           ]


# Nombres (sera usado para saber la cantidad de monstruos y seran anadidos mediante el archivo del mapa)
mNames = []

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
MONSTER_SAUSAGE_SIZE = [1, 2]
MONSTER_GHERKIN_SIZE = [1, 2]

# Nro de imagenes
MONSTER_EGG_NUMBEROFIMAGES_WALKING = 3
MONSTER_EGG_NUMBEROFIMAGES_CLIMBING = 2
MONSTER_SAUSAGE_NUMBEROFIMAGES_WALKING = 4
MONSTER_SAUSAGE_NUMBEROFIMAGES_CLIMBING = 2
MONSTER_GHERKIN_NUMBEROFIMAGES_WALKING = 4
MONSTER_GHERKIN_NUMBEROFIMAGES_CLIMBING = 2

## --------- Imagenes de cada monstruo
# Arreglo de las direcciones de cada imagen de cada monstruo en orden d elos monster ID
allMonstersFolderPath = ["../res/textures/game/monsters/egg/",
                         "../res/textures/game/monsters/gherkin/",
                         "../res/textures/game/monsters/sausage/"]

# Constantes de las imagenes
MIMAGE_WRIGHT = 0
MIMAGE_WLEFT = 1
MIMAGE_CLIMBING = 2


# Imagen que estamos pintando actualmente
monstersActualImageToDraw = [] #(MIMAGE_WRIGHT, 0) # (id, nroImagen)

# Todos los estados de los monstruos
allMonstersStates = ["walking"]

# ============================== Funciones y procedimientos ==============================       

# Metodo para cargar todos los objetos y texturas del juego
def loadGameObjects():
    global pImages
    # Cargamos las imagenes del jugador
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
        
    # Hamburguesa
    global breadImages, lettuceImages, meatImages
    # Pan
    breadImages.append(pygame.image.load(BREAD_PATH + "left.png"))
    breadImages.append(pygame.image.load(BREAD_PATH + "center.png"))
    breadImages.append(pygame.image.load(BREAD_PATH + "right.png"))
    
    # Lechuga
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "left.png"))
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "center.png"))
    lettuceImages.append(pygame.image.load(LETTUCE_PATH + "right.png"))
    
    # Carne
    meatImages.append(pygame.image.load(MEAT_PATH + "left.png"))
    meatImages.append(pygame.image.load(MEAT_PATH + "center.png"))
    meatImages.append(pygame.image.load(MEAT_PATH + "right.png"))
    
    
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
    
# Metodo para cargar una imagen
def loadImage(filePath):
    return pygame.image.load(filePath)


# Metodo para cargar el mapa de una imagen (pixel a pixel)
def loadMap(filePath):
    global breadPositions, meatPositions, lettucePositions, monstersInLevel
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
    cBread = -1 
    cLettuce = -1
    cMeat = -1
    
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
            # ========== PAN ==========
            elif rgb == COLOR_BREAD:
                mapReaded.append(TILE_FLOOR)
                # Si NO es el mismo objeto previo que estabamos anadiendo, entonces
                # Es porque este es un nuevo objeto y debemos crearlo..
                # La siguiente vez que entre (con el siguiente pixel) si es igual un pan
                # Entonces va a pegar el pan en la posicion actual en vez de "crear" un 
                # nuevo objeto de pan
                if not sameObject: 
                    sameObject = True
                    cBread += 1
                    breadPositions.append([])
                    breadTimers.append([])
                    breadDestination.append(0)
                    breadFloors.append(0)

                breadPositions[cBread].append((x, y))
                breadTimers[cBread].append(0)
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
            else:
                if rgb == COLOR_EGG:
                    monstersInLevel.append(MONSTER_EGG)
                elif rgb == COLOR_SAUSAGE:
                    monstersInLevel.append(MONSTER_SAUSAGE)
                elif rgb == COLOR_GHERKIN:
                    monstersInLevel.append(MONSTER_GHERKIN)
                sameObject = False
                mapReaded.append(TILE_NULL)
            
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
        r = random.randint(0, mapWidth*mapHeight)
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


def getImageArray(id, path, n):
    imageArray = []
    for i in range(0, n):
        imageArray.append(pygame.image.load())
        


# Metodo para agregar un monstruo
def addMonster(id):
    global mNames, mX, mY, mHeight, mWidth, mSpeedX, mSpeedY, monstersActualImageToDraw, mImages
    if id == MONSTER_EGG:
        mNames.append("Huevo")
        mSpeedX.append(MONSTER_EGG_SPEED[0])
        mSpeedY.append(MONSTER_EGG_SPEED[1])
        mWidth.append(MONSTER_EGG_SIZE[0])
        mHeight.append(MONSTER_EGG_SIZE[1])
    elif id == MONSTER_SAUSAGE:
        mNames.append("Salchicha")
    elif id == MONSTER_GHERKIN:
        mNames.append("Pepinillo")
        
    mX.append(0)
    mY.append(0)
    maitd = (MIMAGE_WRIGHT, 0)
    monstersActualImageToDraw.append(maitd)
    
    newMonster = []
    for state in range(0, len(allMonstersStates)):
        if allMonstersStates[state] == "walking":
            rightWalk = []
            leftWalk = []
            rightWalk.append(pygame.image.load())
            newMonster.append()
    mImages.append([])
 
    

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
    
    # Le asignamos una posicion random al jugador
    r = getRandomMapPosition()
    playerPosition = [convertToMapX(r), convertToMapY(r)]    
    
    # Cargamos los monstruos
    global respawnArray, mImages 
    
    # Carga de imagenes
    for n in range(0, len(monstersInLevel)):
        mid = monstersInLevel[n]
        addMonster(mid)
        # Anadimos un arreglo de estado por cada estado que haya
        for state in range(0, len(allMonstersStates)):
            if allMonstersStates[state] == "walking":
                mImages[]
        
        
        
        
        
    
    # Inicializamos todos los arreglos segun la cantidad de monstruos (nombres)
    for m in range(0, len(mNames)):
        respawnArray.append(0)
        mX.append(0)
        mY.append(0)   
    
    
    
    
    
    
    
    
    # Inicializamos en vacio las posiciones de los monstruos
    #mX = []
    #mY = []
    
    # Le asignamos una posicion random a cada monstruo
    #for m in range(0, len(mNames)):
    #    r = getRandomMapPosition()
    #    mX.append(convertToMapX(r))
    #    mY.append(convertToMapY(r))


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
        
    #print("Va a bajar ", total)
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
    global breadDestination, lettuceDestination, meatDestination
    
    # Obtenemos las coordenadas del parametro
    ix, iy = ingredient[0]
    
    # Chequeamos colision en los panes
    for p in range(0, len(breadPositions)):
        if ingredient == breadPositions[p]:
            continue
        px, py = breadPositions[p][0]
        if ix == px and math.floor(iy+1) == py:
            breadDestination[p] = moveDown(breadPositions[p], numberOfFloors)
            addScore(500 + int(breadDestination[p] / 10) * 200)
            
    
    # Chequeamos colision en las lechugas
    for l in range(0, len(lettucePositions)):
        if ingredient == lettucePositions[l]:
            continue
        lx, ly = lettucePositions[l][0]
        if ix == lx and math.floor(iy+1) == ly:
            lettuceDestination[l] = moveDown(lettucePositions[l], numberOfFloors)
            addScore(500 + int(lettuceDestination[l] / 10) * 200)
    
    # Chequeamos colision en las carnes
    for c in range(0, len(meatPositions)):
        if ingredient == meatPositions[c]:
            continue
        cx, cy = meatPositions[c][0]
        if ix == cx and math.floor(iy+1) == cy:
            meatDestination[c] = moveDown(meatPositions[c], numberOfFloors)
            addScore(500 + int(meatDestination[c] / 10) * 200)
        
        
    
    

# Metodo para actualizar las posiciones de los ingredientes que estan cayendo
def tickIngredients():
    global breadDestination, breadPositions, lettuceDestination, lettucePositions, meatDestination, meatPositions
    
    # Recorremos todos los panes
    for p in range(0, len(breadDestination)):
        if breadDestination[p] == 0:
            continue
        # Recorremos todas las posiciones para ir bajandolas
        for i in range(0, len(breadPositions[p])):
            x, y = breadPositions[p][i]
            y += fallSpeed
            if y > breadDestination[p]:
                y = breadDestination[p]                
            # Asignamos el nuevo valor
            breadPositions[p][i] = (x, y)
        # Chequeamos la colision
        checkCollision(breadPositions[p], breadFloors)
        # Vemos si llegamos al destino para quitar el "destino"
        x, y = breadPositions[p][0]
        if y == breadDestination[p]:
            breadDestination[p] = 0
            
    
    # Recorremos todas las lechugas
    for l in range(0, len(lettuceDestination)):
        if lettuceDestination[l] == 0:
            continue
        # Recorremos todas las posiciones para ir bajandolas
        for i in range(0, len(lettucePositions[l])):
            x, y = lettucePositions[l][i]
            y += fallSpeed
            if y > lettuceDestination[l]:
                y = lettuceDestination[l]                
            # Asignamos el nuevo valor
            lettucePositions[l][i] = (x, y)
        # Chequeamos la colision
        checkCollision(lettucePositions[l], lettuceFloors)
        # Vemos si llegamos al destino para quitar el "destino"
        x, y = lettucePositions[l][0]
        if y == lettuceDestination[l]:
            lettuceDestination[l] = 0
            
            
    # Recorremos todas las carnes
    for c in range(0, len(meatDestination)):
        if meatDestination[c] == 0:
            continue
        # Recorremos todas las posiciones para ir bajandolas
        for i in range(0, len(meatPositions[c])):
            x, y = meatPositions[c][i]
            y += fallSpeed
            if y > meatDestination[c]:
                y = meatDestination[c]                
            # Asignamos el nuevo valor
            meatPositions[c][i] = (x, y)
        # Chequeamos la colision
        checkCollision(meatPositions[c], meatFloors)
        # Vemos si llegamos al destino para quitar el "destino"
        x, y = meatPositions[c][0]
        if y == meatDestination[c]:
            meatDestination[c] = 0
            
        
    

# Metodo para poder llevar a cabo el "bajar" las partes
def tickHamburguers():
    global breadTimers, lettuceTimers, meatTimers, breadDestination, lettuceDestination, meatDestination, breadFloors, lettuceFloors, meatFloors
    # Revisamos si pisamos alguno de los cuadros de los objetos primero.. 
    # De ser asi, iniciamos un temporizador para mantener ese cuadro pisado por X tiempo
    # Y ver si el ingrediente cae
    
    # Primero setteamos el timer de lo que estemos pisando y reiniciamos los que no
    # Recorremos todos los panes
    for p in range(0, len(breadPositions)):
        # Recorremos todas las posiciones del pan actual
        for i in range(0, len(breadPositions[p])):
            # Vemos si estamos pisando el actual para settearle el tiempo
            x, y = breadPositions[p][i]
            if math.floor(playerPosition[0]) == x and math.floor(playerPosition[1]) == y:
                breadTimers[p][i] = time.time()
            
            # Vemos si se cumplio el tiempo para resetear el tiempo
            if time.time() - breadTimers[p][i] > TIMETORESET:
                breadTimers[p][i] = 0
    
    
    # Recorremos todas las lechugas
    for l in range(0, len(lettucePositions)):
        # Recorremos todas las posiciones de la lechuga actual
        for i in range(0, len(lettucePositions[l])):
            # Vemos si estamos pisando el actual para settearle el tiempo
            x, y = lettucePositions[l][i]
            if math.floor(playerPosition[0]) == x and math.floor(playerPosition[1]) == y:
                lettuceTimers[l][i] = time.time()
                
            # Vemos si se cumplio el tiempo para resetear el tiempo
            if time.time() - lettuceTimers[l][i] > TIMETORESET:
                lettuceTimers[l][i] = 0


    # Recorremos todas las carnes
    for c in range(0, len(meatPositions)):
        # Recorremos todas las posiciones de la carne actual
        for i in range(0, len(meatPositions[c])):
            # Vemos si estamos pisando el actual para settearle el tiempo
            x, y = meatPositions[c][i]
            if math.floor(playerPosition[0]) == x and math.floor(playerPosition[1]) == y:
                meatTimers[c][i] = time.time()
                
            # Vemos si se cumplio el tiempo para resetear el tiempo
            if time.time() - meatTimers[c][i] > TIMETORESET:
                meatTimers[c][i] = 0
                
                
    # Luego vemos si algun ingrediente ya fue todo pisado para bajarlo
    
    # Revisamos los panes
    for p in range(0, len(breadTimers)):
        # Creamos una variable para ver cuantos items del objeto actual
        # Estan pisados
        checkedItems = 0
        # Recorremos todos los cuadros del ingrediente actual
        for i in range(0, len(breadTimers[p])):
            # Si es distinto de cero, esta pisado y sumo 1 al contador
            if breadTimers[p][i] != 0:
                checkedItems += 1
        # Luego, verifico si el numero de pisados es igual a la longitud del ingrediente
        if checkedItems == len(breadTimers[p]):
            breadFloors = getNumberOfEntitiesOn(breadPositions[p])
            breadDestination[p] = moveDown(breadPositions[p], breadFloors)
            breadTimers[p] = resetTimer(breadTimers[p])
            addScore(breadFloors * 200 + int(breadDestination[p] / 10) * 300)
            
            
    # Revisamos las lechugas
    for l in range(0, len(lettuceTimers)):
        # Creamos una variable para ver cuantos items del objeto actual
        # Estan pisados
        checkedItems = 0
        # Recorremos todos los cuadros del ingrediente actual
        for i in range(0, len(lettuceTimers[l])):
            # Si es distinto de cero, esta pisado y sumo 1 al contador
            if lettuceTimers[l][i] != 0:
                checkedItems += 1
        # Luego, verifico si el numero de pisados es igual a la longitud del ingrediente
        if checkedItems == len(lettuceTimers[l]):
            lettuceFloors = getNumberOfEntitiesOn(lettucePositions[l])
            lettuceDestination[l] = moveDown(lettucePositions[l], lettuceFloors)
            lettuceTimers[l] = resetTimer(lettuceTimers[l])
            addScore(lettuceFloors * 200 + int(lettuceDestination[l] / 10) * 300)
            
            
    # Revisamos las carnes
    for c in range(0, len(meatTimers)):
        # Creamos una variable para ver cuantos items del objeto actual
        # Estan pisados
        checkedItems = 0
        # Recorremos todos los cuadros del ingrediente actual
        for i in range(0, len(meatTimers[c])):
            # Si es distinto de cero, esta pisado y sumo 1 al contador
            if meatTimers[c][i] != 0:
                checkedItems += 1
        # Luego, verifico si el numero de pisados es igual a la longitud del ingrediente
        if checkedItems == len(meatTimers[c]):
            meatFloors = getNumberOfEntitiesOn(meatPositions[c])
            meatDestination[c] = moveDown(meatPositions[c], meatFloors)
            meatTimers[c] = resetTimer(meatTimers[c])
            addScore(meatFloors * 200 + int(meatDestination[c] / 10) * 300)
    
    tickIngredients()
    

# Metodo para pintar las hamburguesas
def renderHamburguers():
    # Pintamos los panes
    # Recorremos todos los panes
    for p in range(0, len(breadPositions)):
        # Recorremos todas las posiciones del pan actual
        for i in range(0, len(breadPositions[p])):
            x, y = breadPositions[p][i]
            # Si el ingrediente esta pisado, lo pintaremos 10px mas abajo
            offset = 0
            if breadTimers[p][i] != 0:
                offset = offsetWhenWalked
            
            # Pintamos la textura izquierda si i = 0
            # Si i = len-1 pintamos la textura derecha
            # Sino la textura central
            textureToUse = 0
            if i == 0:
                textureToUse = 0
            elif i == len(breadPositions[p]) - 1:
                textureToUse = 2
            else:
                textureToUse = 1
            drawImageR(breadImages[textureToUse], x, y + offset, TILE_SIZE, TILE_SIZE)

    
    # Pintamos las lechugas
    # Recorremos todas las lechugas
    for l in range(0, len(lettucePositions)):
        # Recorremos todas las posiciones de la lechuga actual
        for i in range(0, len(lettucePositions[l])):
            x, y = lettucePositions[l][i]            
            # Si el ingrediente esta pisado, lo pintaremos 10px mas abajo
            offset = 0
            if lettuceTimers[l][i] != 0:
                offset = offsetWhenWalked
                
            # Pintamos la textura izquierda si i = 0
            # Si i = len-1 pintamos la textura derecha
            # Sino la textura central
            textureToUse = 0
            if i == 0:
                textureToUse = 0
            elif i == len(lettucePositions[l]) - 1:
                textureToUse = 2
            else:
                textureToUse = 1
            drawImageR(lettuceImages[textureToUse], x, y + offset, TILE_SIZE, TILE_SIZE)


    # Pintamos las carnes
    # Recorremos todas las carnes
    for c in range(0, len(meatPositions)):
        # Recorremos todas las posiciones de la carne actual
        for i in range(0, len(meatPositions[c])):
            x, y = meatPositions[c][i]
            # Si el ingrediente esta pisado, lo pintaremos 10px mas abajo
            offset = 0
            if meatTimers[c][i] != 0:
                offset = offsetWhenWalked
            
            # Pintamos la textura izquierda si i = 0
            # Si i = len-1 pintamos la textura derecha
            # Sino la textura central
            textureToUse = 0
            if i == 0:
                textureToUse = 0
            elif i == len(meatPositions[c]) - 1:
                textureToUse = 2
            else:
                textureToUse = 1
            drawImageR(meatImages[textureToUse], x, y + offset, TILE_SIZE, TILE_SIZE)



# =====================================================================================
# =====================================================================================
# ================================= Metodos Jugador ===================================
# =====================================================================================
# =====================================================================================

# Metodo para activar el disparo
def shootPepper():
    global canShoot, isShooting, pepperTime
    if canShoot and not isShooting:
        canShoot = False
        isShooting = True
        pepperTime = time.time()
        

# Metodo para pintar la pimienta
def renderPepper():
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
    drawRect(pepperPos[0], pepperPos[1] + cos, pepperSize, pepperSize, getColor("cyan"))
    
    

# Metodo para mover la pimienta
def tickPepper():
    global pepperPos, playerPosition, pepperLastDir
    
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
    
    # Revisamos primero que nada si no estamos vivos para reiniciar todo
    if not isAlive:
        isAlive = True
        playerLifes -= 1
        if playerLifes < 0:
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
    drawString(1, 1, "Vidas: " + str(playerLifes), "Consolas", getColor("white"), 32)  
    drawString(30, 1, "Score: " + str(SCORE), "Consolas", getColor("white"), 28)
    drawString(mapWidth/2.0 - 1.0, 0.5, "Nivel " + str(actualLevel), "Tahoma", getColor("white"), 20)
    #drawString(20, 1, "x = " + str(playerPosition[0]), "Consolas", getColor("white"), 28)
    #drawString(20, 2, "y = " + str(playerPosition[1]), "Consolas", getColor("white"), 28)
    
  
    
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

# Metodo para ver si la pimienta lanzada colisiona con algun monstruo
def monstersCheckCollision():
    global respawnArray, mX, mY
    
    if isShooting:
        for m in range(0, len(mNames)):
            #print("Pepper X = ", pepperPos[0])
            #print("mx = ", mX[m])
            if ((pepperPos[0] + pepperSize/2.0 >= mX[m]) 
                and (pepperPos[0] + pepperSize/2.0 <= mX[m] + mWidth[m])
                and (pepperPos[1] + pepperSize/2.0 >= mY[m])
                and (pepperPos[1] + pepperSize/2.0 <= mY[m] + mHeight[m])):
                # Si entra aqui, la pimienta le pego
                addScore(350)
                respawnArray[m] = time.time()
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

# Metodo para que se muevan los monstruos
def tickMonsters():
    global isAlive
    
    respawnMonsters()
    
    # Recorremos todos los monstruos
    for i in range(0, len(mNames)):
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
        path = getPathTo(monsterPos, playerPos, [], [], [], 0)
        
        if path == True or path == False:
            isAlive = False
            return
       
        # Obtenemos el vector de movimiento
        mVector = getMovementVector(path, math.floor(mX[i]), math.floor(mY[i]))            
        # Lo sumamos        
        if mVector[0] != 0:
            mX[i] += mSpeedX[i] * mVector[0]
        elif mVector[1] != 0:
            mY[i] += mSpeedY[i] * mVector[1] # Calculamos primero la nueva Y antes de asignarla para evitar bug
            
    monstersCheckCollision()



# Metodo para pintar los monstruos
def renderMonsters():    
    # Pintamos todos los monstruos
    for i in range(0, len(mNames)):
        if respawnArray[i] == 0:
            drawRect(mX[i], mY[i], mWidth[i], mHeight[i], getColor("green"))
            #drawString(mX[i]-(mWidth[i]/2.8), mY[i]-15, mNames[i], "Consolas", getColor("white"), 12)   
        


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
    # Pintamos el mensaje principal "MENU"
    drawString(15, 1.5, "Menu", "Consolas", getColor("white"), 102)
    
    # Pintamos todas las opciones del menu
    for i in range(0, len(optionNames)):
        drawString(optionXCoords[i], optionYCoords[i], optionNames[i], "Consolas", getColor("white"), 38)     
    
    
    menuArrowCoords = [(260, selectedOptionY),
                      (260, selectedOptionY+40),
                      (300, selectedOptionY+20)]
    drawPolygon(menuArrowCoords, getColor("white"))  
    
    
# Metodo para activar el teclado en modo Menu
def inputMenu(e):
    global selectedOptionY, selectedOption, enterPressed, isInMenu, isPlaying, isSelectingLevel

    # Movemos el cursor del menu segun sea la tecla
    if (e == KEY_DOWN or e == KEY_S or e == KEY_s) and (selectedOption > 1):
        selectedOptionY += distanceBetweenOptions
        selectedOption -= 1
    elif (e == KEY_W or e == KEY_UP or e == KEY_w) and (selectedOption < MAX_OPTIONS):
        selectedOptionY -= distanceBetweenOptions
        selectedOption += 1
    
    # Chequeamos si se presiono ENTER
    if e == KEY_ENTER:
        if selectedOption == MENU_PLAY:
            isInMenu = False
            isSelectingLevel = True
            #initActors()
        elif selectedOption == MENU_EXIT:
            sys.exit()
    
        
        
        

# =====================================================================================
# =====================================================================================
# ============================== Metodos del Juego ====================================
# =====================================================================================
# =====================================================================================

# Metodo para ver si se completo el nivel
def tickLevel():    
    for p in range(0, len(breadPositions)):
        x, y = breadPositions[p][0]
        
        if y < INGREDIENTS_FLOOR:
            return
    
    # Si llega aqui es porque terminamos el nivel
    drawString(mapWidth/2, mapHeight/3, "TERMINO", "Consolas", getColor("white"), 100) 


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
    if isInMenu:
        inputMenu(e)
    elif isSelectingLevel:
        inputLevelSelection(e)
    else:
        inputPlayer(e)       
        
    
# Render method (Aqui se pinta el mapa de juego en base a la matriz)
def render():      
    #drawRect(10, 10, 300, 400, convertToRGB(255,0,255))
    #drawLines(10, 20, 150, 190, convertToRGB(255,255,255), 5)
    #x = math.sin((time.time() * 5000.0 / 5000.0 * math.pi * 2)) * 200
    #y = math.cos((time.time() * 5000.0 / 5000.0 * math.pi * 2)) * 100
    #img = pygame.image.load("../res/textures/grid.png")
    #drawImage(img, 300 + x, 200 + y)
    #drawString(200, 200, "string", "Consolas", (255, 255, 255), 28)
    
    if isInMenu:
        renderMenu()
    elif isSelectingLevel:
        renderLevelSelection()
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
                input(event.key)
            
        
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

loadGameObjects()

# Iniciamos el juego
mainLoop()


















