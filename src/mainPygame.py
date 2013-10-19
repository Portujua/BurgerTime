# Imports
import sys
import math
import time
import pygame
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
optionXCoords = [340, 340]
optionYCoords = [310, 210]


# Estados del juego
isInMenu = True
isCreatingNewProfile = False
isSelectingProfile = False
isPlaying = False
isPaused = False
isRunning = True


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

KEY_A = 65
KEY_S = 83
KEY_D = 68
KEY_W = 87
KEY_P = 80
KEY_ENTER = 13
KEY_SPACE = 32



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



### Propiedades del mapa
map = []
global mapWidth
global mapHeight
blockSize = 20 # Tamano de cada imagen

# Constantes mapa
TILE_NULL = -1
TILE_NONE = 0
TILE_FLOOR = 1
TILE_STAIRS = 2
TILE_PLAYER = 3
TILE_MONSTER = 4
TILE_BOTTOMSTAIRS = 5



### ---------- Propiedades del Jugador ----------

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
           [0,0,0], # PIMAGE_WRIGHT   Como tenemos 3 imagenes para caminar a la derecha, inicializamos con 3 ceros
           [0,0,0], # PIMAGE_WLEFT
           [0,0] # PIMAGE_CLIMBING
           ]

# Info del jugador
playerLives = 3


# Restricciones
canClimb = False
canWalk = True
canJump = True


# Estados
isAlive = True
isClimbing = False
isWalking = False
isJumping = False


# Posicion
playerX = 120 # Posicion inicial X
playerY = 400 # Posuicion inicial Y



# Tamano
playerHeight = 60
playerWidth = 40



# Movimiento
speedX = 3
speedY = 2
movementVector = [0,0] # [x,y] --> x {-1,0,1} ... y {-1,0,1}

# Salto
jumpHeight = 40
jumpTimer = 0
jumpOffset = 0
jumpSpeed = 3.5




### ---------- Propiedades los Monstruos ----------
# Para anadir un monstruo simplemente se anade un valor extra a cada arreglo a gusto de consumidor XD

# Imagen que contiene todas las imagenes de los monstruos
monstersGridName = ["grid.png", "grid.png"]

# Tamano del grid (ancho, alto)
mGridSizeX = [2, 2]
mGridSizeY = [2, 2]

# Aqui se guardaran las imagenes leidas de cada monstruo (es usado al pintar)
# La primera corresponde a 0,0, la segunda 1,0, la tercera 2,0... n,0 ... 0,1 , 0,2 , ..., 0,m ... n,m
mImages = [[], []] 

# Nombres
mNames = ["Enemigo"] # "CuboRojo", "CuboAzul"

# Colores (Provisional)
mColors = ["red", "blue"]

# Restricciones
mCanClimb = [False, False]
mCanWalk = [True, True]


# Estados
mIsClimbing = [False, False]
mIsWalking = [False, False]


# Posicion
mX = [520, 710] # Posicion inicial X
mY = [400, 400] # Posuicion inicial Y



# Tamano
mHeight = [60, 60]
mWidth = [40, 40]



# Movimiento
mSpeedX = [1, 2.5]
mSpeedY = [1, 1]



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
    


# Metodo para resetear monstruos al morir
def resetThings():
    global mX, mY, playerX, playerY
    mX = [520, 710] # Posicion inicial X
    mY = [400, 400] # Posuicion inicial Y
    
    playerX = 120 # Posicion inicial X
    playerY = 400 # Posuicion inicial Y

    
# Metodo para "soltar" las teclas del teclado
def releaseKeys():
    global movementVector, isWalking
    
    movementVector = [0,0]
    isWalking = False


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
    
# Metodo para cargar una imagen
def loadImage(filePath):
    return pygame.image.load(filePath)


# Metodo para cargar el mapa de una imagen (pixel a pixel)
def loadMap(filePath):
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

    # Recorremos todos los pixels de la imagen
    for y in range(0, iy):
        for x in range(0, ix):
            # Obtenemos las componentes del vector RGB
            r, g, b = pixels[x, y]

            # Creamos el color RGB
            rgb = (r << 16) | (g << 8) | b

            # Chequeamos si es el color
            if (rgb & 0xFFFFFF) == 0: # Negro (Nada)
                mapReaded.append(TILE_NONE)
            elif (rgb ^ 0xFFFFFF) == 0x00FF00: # Rosado (Piso)
                mapReaded.append(TILE_FLOOR)
            elif (rgb ^ 0xFFFFFF) == 0xFF00FF: # Verde (Escaleras)
                mapReaded.append(TILE_STAIRS)
            elif rgb == 0x00FE00:
                mapReaded.append(TILE_BOTTOMSTAIRS)
            else:
                mapReaded.append(TILE_NULL)
            # Faltan los otros colores....
            
    # Retornamos el mapa leido
    return mapReaded


# Metodo para obtener el valor del mapa en la posicion x,y
def getMapValue(x, y):
    # Chequeamos que no nos salgamos de la matriz
    if getXMapValue(x) + getYMapValue(y) * mapWidth >= 0 and getXMapValue(x) < mapWidth:
        return map[getXMapValue(x) + getYMapValue(y) * mapWidth]
    return 0

# Metodo para obtener el valor del mapa dadas las coordenadas del mapa
def getMapValueAt(x, y):
    if x >= 0 and x < mapWidth and y >= 0 and y < mapHeight:
        return map[x + y * mapWidth]
    return 0


# Metodo para obtener la X dentro del mapa
def getXMapValue(x):
    return int(math.fabs(x/blockSize))


# Metodo para obtener la Y dentro del mapa
def getYMapValue(y):
    return int(math.fabs(y/blockSize))



# Metodo para evitar que se meta por el piso al bajar
def fixStairsBug(ex, ey, eWidth, eHeight):
    # Si en la entidad hay piso, y abajo tambien, entonces le resto el offset que baja a la pos actual
    # Se puede ver cual es el bug desactivandola, posicionandose en una escalera y en vez de subir
    # bajen... Van a ver que se mete por el piso 1 cuadro hacia abajo y luego vuelve a aparecer arriba
    if (getMapValue(ex+(eWidth/2), ey+eHeight+blockSize) == TILE_FLOOR) and (getMapValue(ex+(eWidth/2), ey+eHeight) == TILE_FLOOR):
        return -(ey - getYMapValue(ey)*blockSize)
    return 0

# Metodo para saber si podemos movernos a un recuadro x,y
def canMoveTo(x, y, movementVector):
    # Obtenemos las coordenadas del vector movimiento
    vx = movementVector[0]
    vy = movementVector[1]
    
    if getMapValue(x + vx, (y + vy)) == TILE_FLOOR or getMapValue(x + vx, (y + vy)) == TILE_STAIRS:
        #print("Si me puedo mvoverr")
        return True
    elif isClimbing:
        #print("Si me puedo mover, estoy en escaleras")
        return True
    else:
        #print("NO PUEDO")
        return False
    

# Metodo para obtener los "hijos" de una coordenada dentro de la matriz
# Los hijos de una coordenada son aquellos valores que son caminables dentro de la matriz (piso, escaleras)
def getChilds(x, y, visited):
    # Como solamente nos podemos mover en 4 direcciones solo debemos ver esas direcciones
    # Creamos la matriz de hijos que vamos a devolver
    allChilds = []
    
    # Obtenemos todos los valores de las direcciones (para no escribir tanto en los if)
    up = getMapValueAt(x, y-1)
    down = getMapValueAt(x, y+1)
    left = getMapValueAt(x-1, y)
    right = getMapValueAt(x+1, y)
    
    # Si arriba hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (up == TILE_STAIRS or up == TILE_BOTTOMSTAIRS) and not((x, y-1) in visited):
        allChilds.append((x, y-1))
        
    # Si abajo hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (down == TILE_STAIRS or down == TILE_BOTTOMSTAIRS) and not((x, y+1) in visited):
        allChilds.append((x, y+1))
        
    # Si a la izquierda hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (left == TILE_FLOOR or left == TILE_STAIRS) and not((x-1, y) in visited):
        allChilds.append((x-1, y))
        
    # Si a la derecha hay piso/escalera y no he visitado ese nodo, es un hijo valido
    if (right == TILE_FLOOR or right == TILE_STAIRS) and not((x+1, y) in visited):
        allChilds.append((x+1, y))
        
    return allChilds
    

# Metodo para ir de una coordenada A a una coordenada B dentro de la matriz
# de manera recursiva
# a,b son vectores (x,y), path es la matriz de matrices de todos los caminos posibles (la que vamos a devolver)
# visited son los nodos que ya visitamos, al llamar la funcion por primera vez se envia Vacio
# Le enviamos dos puntos A,B en coordenadas del mapa
def getPathTo(a, b, path, visited, iteration):     
    # Marcamos como visitado el nodo actual
    visited.append(a)
    # Obtenemos las componentes de A
    ax, ay = a

    # Buscamos los hijos
    aChilds = getChilds(ax, ay, visited)
    
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
            arrived = getPathTo(child, b, path, visited, iteration+1)
            # Chequeamos si llegamos por alguno de los hijos
            # Si no llegamos, sacamos al nodo actual del camino
            if not arrived:
                path.remove(child)
            # Si en efecto llegamos, devolvemos TRUE para finalizar todo
            else:
                # Chequeamos, si iteration = 0 es que estamos en el primer loop
                # Y debemos devolver el camino en vez de True
                if iteration == 0:
                    print("Camino: ", path)
                    print("")
                    return path
                else:
                    return True
    # Si terminamos de recorrer todos los hijos y no llegamos, devolvemos FALSE
    # Chequeamos si estamos en el loop principal, si es asi entonces devolvemos el mismo punto donde estabamos
    if iteration == 0:
        path = []
        path.append(a)
        return path
    else: # Sino, devolvemos falso para notificar que termino el loop y no encontro camino con ese hijo
        return False
    
# Este metodo es para calcular el vector movimiento dado un punto hacia donde ir
# Es usado para ir a los distintos puntos que nos genera la busqueda de camino
# Le enviamos el array de puntos para llegar al destino, a pesar que solo usaremos el primero
# La posicion X,Y del objeto a mover, la velocidad X,Y para ese objeto
# Devuelve un vector movimiento
def getMovementVector(p, ex, ey):
    # Obtenemos las coordenadas del punto p
    px, py = p[0]
    
    # Convertimos las coordenadas a coordenadas de mapa
    eMapX = getXMapValue(ex)
    eMapY = getYMapValue(ey)
    
    # Creamos el vector movimiento (sin movimiento, por ahora)
    mVector = [0,0]
    
    if eMapX < px:
        mVector[0] = 1
    elif eMapX > px:
        mVector[0] = -1
    elif eMapY < py:
        mVector[1] = -1
    elif eMapY > py:
        mVector[1] = 1
        
    return mVector
    
    

# =====================================================================================
# =====================================================================================
# ============================= Metodos para Pintar ===================================
# =====================================================================================
# =====================================================================================

# Pintar rectangulos (por tenerlo.)
def drawRect(x, y, width, height, rgbColor):
    pygame.draw.rect(window, rgbColor, (x, y, width, height))
    
    

# Pintar lineas (Por tenerlo..)
def drawLines(px, py, qx, qy, rgbColor, weight):
    pygame.draw.line(window, rgbColor, (px, py), (qx, qy), weight)
    

# Metodo para pintar string, el string sera pintado centrado en el punto x,y dado.. Ejemplo:
# Si se da como punto window.width/2, window.height/2 entonces saldra centrado en la pantalla
def drawString(x, y, string, font, rgbColor, size):
    str = pygame.font.SysFont(font, size)
    lbl = str.render(string, 1, rgbColor)
    window.blit(lbl, (x, y))


# Metodo para pintar imagenes sin redimensionar
def drawImage(image, x, y):
    window.blit(image, (x,y))
    
# Metodo para pintar imagenes redimensionadas
def drawImageR(image, x, y, width, height): 
    window.blit(pygame.transform.scale(image, (width, height)), (x, y))
    
    
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
                xOffset += blockSize
                continue
            
            # Variable para la textura actual
            actColor = None
            
            # Setteamos el color segun el numero en la matriz
            if actCoord == TILE_FLOOR:
                actColor = "blue"
            elif actCoord == TILE_STAIRS:
                actColor = "red"
            else:
                actColor = "black"
            
            # Pintamos el bloque
            drawRect(xOffset, yOffset, blockSize, blockSize, getColor(actColor))
            
            # Actualizamos los offset
            xOffset += blockSize # Podriamos tener 1 solo offset ya que son iguales
            
        xOffset = 0 # Reiniciamos el offset del eje X para comenzar a pintar desde 0
        yOffset += blockSize # Sumamos blockSize al offset del eje Y para pintar abajo

        


# =====================================================================================
# =====================================================================================
# ================================= Metodos Jugador ===================================
# =====================================================================================
# =====================================================================================

# Metodo para actualizar el jugador
def tickPlayer():
    global canClimb, playerX, playerY, isClimbing, isAlive, isInMenu, isPlaying, playerLives
    
    # Revisamos primero que nada si no estamos vivos para reiniciar todo
    if not isAlive:
        isAlive = True
        playerLives -= 1
        if playerLives < 0:
            isInMenu = True
            isPlaying = False
            playerLives = 3
        else:
            resetThings()
        
    
    if canMoveTo(playerX + playerWidth/2 + movementVector[0] * speedX, playerY + playerHeight + movementVector[1] * speedY, movementVector):
        # Movemos al jugador segun el vector movimiento
        playerX += movementVector[0] * speedX
        playerY += movementVector[1] * speedY
    
    # Chequeo si no me sali de la ventana
    if playerX+playerWidth > windowWidth:
        playerX = windowWidth-playerWidth
    elif playerX < 0:
        playerX = 0
    
    # Como todo aqui tiene que ver con escalar, si isJumping entonces saltamos todo este codigo
    if isJumping:
        return
    
    # Revisamos si esta parado sobre una escalera para permitirle subir (Con el observador en los pies, izquierda)
    if (getMapValue(playerX+(playerWidth/2), playerY+playerHeight) == TILE_STAIRS) or (getMapValue(playerX+(playerWidth/2), playerY+(playerHeight/2)) == TILE_STAIRS):
        canClimb = True
    else:
        canClimb = False
    
    # Si esta subiendo y ya no puede subir, entonces es porque termino de subir y "se paso" de la escalera
    # Por lo que hay que "bajarlo" al piso, para que pueda seguir moviendose
    if isClimbing and not canClimb:
        # Nueva posicion en funcion del mapa
        newYPos = getYMapValue(playerY)
        
        # Esto arregla el bug al subir
        # Si el actual no es nada, y el actual mas la altura del jugador mas el tamano de un bloque extra hay escalera, entonces sumar 1 a la posicion...
        if (getMapValue(playerX+(playerWidth/2), playerY) == TILE_NONE) and (getMapValue(playerX+(playerWidth/2), playerY+playerHeight+blockSize) == TILE_STAIRS):
            newYPos += 1
        
        # Creo la nueva posicion para pintar
        playerY = newYPos*blockSize
        isClimbing = False
    
    # Guardamos el valor previo de la Y, por si se cambia quiere decir que estaba bugeada
    # la posicion, y se debe desactivar el isClimbing
    prevPos = playerY
    
    # Revisamos si esta bugeada la posicion, y la arreglamos
    if getMapValue(playerX+(playerWidth/2), playerY+playerHeight) == TILE_FLOOR:
        playerY += fixStairsBug(playerX, playerY, playerWidth, playerHeight)
    
    # Chequeamos si la posicion previa es distinta a la posicion nueva, entonces desactivamos isClimbing
    if prevPos != playerY:
        isClimbing = False
        

# Metodo para pintar el HUD del jugador
def renderHUD():
    drawString(15, 15, "Vidas: " + str(playerLives), "Consolas", getColor("white"), 32)  


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
            # Sino, setteamos el nuevo spritesheet y comenzamos de 0
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
    
    # Finalmente, pintamos
    status, imgId = actualImageToDraw
    drawImageR(pImages[status][imgId], playerX, playerY + jumpOffset, playerWidth, playerHeight)
    
    # Centro del jugador (Provisional)
    #drawRect(playerX, y, width, height, rgbColor)

    drawString(playerX-(playerWidth/2), playerY + jumpOffset-15, playerName, "Consolas", getColor("white"), 12)
        
    # Pintamos el HUD del jugador
    renderHUD()
    
    

# Metodo para activar el teclado en modo jugador
def inputPlayer(e):
    global playerX, playerY, enterPressed, isClimbing, canJump, isJumping, jumpTimer, canClimb, isPaused, movementVector, isWalking

    # Primero chequeamos si se pauso el juego, para asi saltar todo este codigo
    if e == KEY_P or e == KEY_p:
        # Invertimos el valor de isPaused
        isPaused = not(isPaused)
        
        # Si al invertirlo es TRUE, quiere decir que el juego esta pausado, saltamos todo este codigo
        if isPaused:
            return
    
    if (e == KEY_D or e == KEY_RIGHT or e == KEY_d) and not (isClimbing):
        movementVector = [1,0]
        isWalking = True
    elif (e == KEY_A or e == KEY_LEFT or e == KEY_a) and not (isClimbing):
        movementVector = [-1,0]
        isWalking = True
    elif (e == KEY_S or e == KEY_DOWN or e == KEY_s) and (canClimb):
        movementVector = [0,1]
        isWalking = False
        isClimbing = True
        canJump = False
    elif (e == KEY_W or e == KEY_UP or e == KEY_w) and (canClimb):
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
    
        
    if e == KEY_ENTER:
        enterPressed = True
    else:
        enterPressed = False
        
        

# =====================================================================================
# =====================================================================================
# ============================ Inteligencia Articial ==================================
# =====================================================================================
# =====================================================================================

# Metodo para arreglar la posicion del monstruo al subir
def getYFixed(mx, my, mHeight):
    if getMapValue(mx, my+mHeight) == TILE_NONE:
        return my+blockSize
    return my

# Metodo para que se muevan los monstruos
def tickMonsters():
    global isAlive
    
    # Recorremos todos los monstruos
    for i in range(0, len(mNames)):
        # Obtenemos la posicion del jugador respecto al mapa
        playerPos = (getXMapValue(playerX+playerWidth/2), getYMapValue(playerY+playerHeight))
        
        # Arreglamos la Y del monstruo por si esta bugeada
        mY[i] = getYFixed(mX[i], mY[i], mHeight[i])
        
        # Obtenemos la posicion del monstruo respecto al mapa
        monsterPos = (getXMapValue(mX[i]), getYMapValue(mY[i]+mHeight[i]))
        
        # Calculamos el camino
        path = getPathTo(monsterPos, playerPos, [], [], 0)
        
        if path == True or path == False:
            isAlive = False
            return
       
        # Obtenemos el vector de movimiento
        mVector = getMovementVector(path, mX[i], mY[i])            
        # Lo sumamos        
        if mVector[0] != 0:
            mX[i] += mSpeedX[i] * mVector[0]
        elif mVector[1] != 0:
            mY[i] += mSpeedY[i] * mVector[1] # Calculamos primero la nueva Y antes de asignarla para evitar bug



# Metodo para pintar los monstruos
def renderMonsters():
    monstersSurface = pygame.Surface((windowWidth, windowHeight), pygame.SRCALPHA)
    
    # Pintamos todos los monstruos
    for i in range(0, len(mNames)):
        drawRect(mX[i], mY[i], mWidth[i], mHeight[i], getColor("green"))
        drawString(mX[i]-(mWidth[i]/2.8), mY[i]-15, mNames[i], "Consolas", getColor("white"), 12)
        
        
        
        


# =====================================================================================
# =====================================================================================
# ================================= Menu del Juego ====================================
# =====================================================================================
# =====================================================================================


# Metodo para actualizar el menu
def tickMenu():
    malditoPythonQueNoDejaInicializarFuncionesVacias = 1 # Aqui van a ir los efectos al menu
    
# Metodo para pintar el menu
def renderMenu():        
    # Pintamos el mensaje principal "MENU"
    drawString(290, 30, "Menu", "Consolas", getColor("white"), 102)
    
    # Pintamos todas las opciones del menu
    for i in range(0, len(optionNames)):
        drawString(optionXCoords[i], optionYCoords[i], optionNames[i], "Consolas", getColor("white"), 38)     
    
    
    menuArrowCoords = [(260, selectedOptionY),
                      (260, selectedOptionY+40),
                      (300, selectedOptionY+20)]
    drawPolygon(menuArrowCoords, getColor("white"))  
    
    
# Metodo para activar el teclado en modo Menu
def inputMenu(e):
    global selectedOptionY, selectedOption, enterPressed, isInMenu, isPlaying

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
            isPlaying = True
        elif selectedOption == MENU_EXIT:
            sys.exit()
    
        
        
        

# =====================================================================================
# =====================================================================================
# ============================== Metodos del Juego ====================================
# =====================================================================================
# =====================================================================================


# Pintar todo lo referente al juego (cuando se esta jugando)
def renderGame():    
    # Pintamos el mapa
    drawMap()
    
    # Pintamos el jugador
    renderPlayer()
    
    # Pintamos los monstruos
    renderMonsters()
    
    # Si esta pausado el juego, pintamos un Texto que nos lo diga
    if isPaused:
        drawString(windowWidth/4, windowHeight/4, "PAUSA", "Consolas", getColor("white"), 140)
    
    
# Actualizar el juego (cuando se esta jugando)
def tickGame():
    # Actualizamos solo si el juego no esta pausado
    if not isPaused:
        tickMonsters()
        tickPlayer()



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

# Leemos el mapa del archivo
map = loadMap("newlevel.png")    

loadGameObjects()

# Iniciamos el juego
mainLoop()


















