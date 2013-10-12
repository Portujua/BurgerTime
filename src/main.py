# Imports
import sys
import math
import time
import pyHook

import PIL.Image
import PIL.ImageTk
from tkinter import *
from msvcrt import *

# ============================== Variables ==============================

# Constantes MENU
MENU_PLAY = 1
MENU_EXIT = 2
MAX_OPTIONS = 2

# Propiedades del menu
# Para crear una opcion nueva es igual que los monstruos, se anade 1 item a cada arreglo de opciones
# se modifica arriba MAX_OPTIONS, y se anade la opcion nueva

selectedOption = 1 # Opcion seleccionada por defecto
selectedOptionY = 230 # Altura del triangulo que funciona como cursor en el menu
distanceBetweenOptions = 100 # Distancia entre cada opcion del menu (para mover el triangulo)

optionNames = ["Jugar", "Salir"]
optionXCoords = [320, 320]
optionYCoords = [250, 350]



# Estados del juego
isInMenu = True
isPlaying = False
isPaused = False


# "Constantes" Teclado
KEY_UP = 38
KEY_LEFT = 37
KEY_DOWN = 40
KEY_RIGHT = 39
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



# Propiedades de la ventana
windowTitle = "BurgerTime"
windowWidth = "800"
windowHeight = "600"
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



### ---------- Propiedades del Jugador ----------
# Restricciones
canClimb = False
canWalk = True
canJump = True


# Estados
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
jumpHeight = 20
jumpTimer = 0
jumpOffset = 0




### ---------- Propiedades los Monstruos ----------
# Para anadir un monstruo simplemente se anade un valor extra a cada arreglo a gusto de consumidor XD

# Nombres
mNames = ["CuboRojo", "CuboAzul"]

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


# =====================================================================================
# =====================================================================================
# ================================== Funcionales ======================================
# =====================================================================================
# =====================================================================================


# Lectura de teclas presionadas
def onKeyPressed(e):
    global charLastKey
    
    key = e.KeyID
    charLastKey = chr(e.Ascii) # Useless atm.
    #print(key)
    
    if isInMenu:
        inputMenu(key)
    elif isPlaying:
        inputPlayer(key)

    return True # Necesario para que el programa no se cierre al presionar una tecla

keyManager = pyHook.HookManager() # Creamos el objeto
keyManager.KeyDown = onKeyPressed # que maneja las
keyManager.HookKeyboard() # teclas presionadas



# Metodo para cargar una imagen
def openImage(filePath):
    # Cargamos la imagen
    image = PIL.Image.open(filePath)
    image.load()
    
    # Es necesaria cierta transformacion, pero no se que hace esto...
    image = PIL.ImageTk.PhotoImage(image)
    
    # Retornamos la imagen
    return image



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
            else:
                mapReaded.append(TILE_NULL)
            # Faltan los otros colores....
            
    # Retornamos el mapa leido
    return mapReaded



# Metodo para obtener el valor del mapa en la posicion x,y
def getMapValue(x, y):
    return map[getXMapValue(x) + getYMapValue(y) * mapWidth]


# Metodo para obtener la X dentro del mapa
def getXMapValue(x):
    return int(math.fabs(x/blockSize))


# Metodo para obtener la Y dentro del mapa
def getYMapValue(y):
    return int(math.fabs(y/blockSize))



# Metodo para evitar que se meta por el piso al bajar
def fixFloorBug(ex, ey, eWidth, eHeight):
    # Si en la entidad hay piso, y abajo tambien, entonces le resto el offset que baja a la pos actual
    # Se puede ver cual es el bug desactivandola, posicionandose en una escalera y en vez de subir
    # bajen... Van a ver que se mete por el piso 1 cuadro hacia abajo y luego vuelve a aparecer arriba
    if (getMapValue(ex+(eWidth/2), ey+eHeight+blockSize) == TILE_FLOOR) and (getMapValue(ex+(eWidth/2), ey+eHeight) == TILE_FLOOR):
        return -(ey - getYMapValue(ey)*blockSize)
    return 0

# =====================================================================================
# =====================================================================================
# ============================= Metodos para Pintar ===================================
# =====================================================================================
# =====================================================================================

# Metodo para pintar string
def drawString(x, y, string, color, size, window):
    window.create_text(x, y, anchor=W, fill=color, font=("Consolas", size), text=string)



# Metodo para pintar una figura
def drawRect(x, y, xSize, ySize, color, window):
    window.create_rectangle(x, y, x + xSize, y + ySize, fill=color)



# Metodo para pintar imagenes
def drawImage(filePath, x, y, window): # ARREGLAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    sprite = openImage("../res/" + filePath)
    window.create_image(x, y, anchor=NW, image=sprite)
    
    

# Metodo que pinta el mapa basandose en la matriz del mapa y el tamano de cada bloque
def drawMap(window):
    # Creamos dos variables para ir llevando el offset
    # Cada bloque se pintara en una coordenada X mas el OFFSET total
    xOffset = 0
    yOffset = 0
    
    # Recorremos todo el mapa
    for y in range(0, mapHeight):
        for x in range(0, mapWidth):
            # Wtf
            if (x + y*mapWidth) < 0 or (x + y*mapWidth) >= len(map):
                continue
            
            # Obtenemos la coordenada actual
            actCoord = map[x + y*mapWidth]
            
            # Creamos una variable para el color actual
            actColor = "black" # Por defecto negro
            
            # Setteamos el color segun el numero en la matriz
            if actCoord == TILE_FLOOR:
                actColor = "blue"
            elif actCoord == TILE_STAIRS:
                actColor = "brown"
            else:
                actColor = "black"

            # Pintamos el bloque
            drawRect(xOffset, yOffset, xOffset + blockSize, yOffset + blockSize, actColor, window)
            
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
    global canClimb, playerX, playerY, isClimbing
    
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
    playerY += fixFloorBug(playerX, playerY, playerWidth, playerHeight)
    
    # Chequeamos si la posicion previa es distinta a la posicion nueva, entonces desactivamos isClimbing
    if prevPos != playerY:
        isClimbing = False
        
        


# Metodo para pintar el jugador
def renderPlayer(window):
    global jumpOffset, canJump, isJumping, canClimb
    
    # Si estoy saltando, entonces obtengo el offset de salto y le cambio el signo
    if isJumping:
        jumpOffset = -math.sin(time.time() - jumpTimer) * jumpHeight
    
    # Si el offset de salto es positivo, quiere decir que termino el salto (grafica del seno entre 0 y pi)
    # entonces, reseteo todos los valores para poder escalar y saltar de nuevo..
    if jumpOffset > 0:
        jumpOffset = 0
        canJump = True
        canClimb = True
        isJumping = False
        
    
    # Pintamos el jugador
    drawRect(playerX, playerY + jumpOffset, playerWidth, playerHeight + jumpOffset, "white", window)
    
    # Centro del jugador (Provisional)
    drawRect(playerX, playerY + jumpOffset, 5, 5, "red", window)
    
    drawString(playerX-(playerWidth/1.7), playerY+ jumpOffset-15, windowTitle, "white", 12, window)
    
    

# Metodo para activar el teclado en modo jugador
def inputPlayer(key):
    global playerX, playerY, enterPressed, isClimbing, canJump, isJumping, jumpTimer, canClimb, isPaused
    
    # Primero chequeamos si se pauso el juego, para asi saltar todo este codigo
    if key == KEY_p or key == KEY_P:
        # Invertimos el valor de isPaused
        isPaused = not(isPaused)
        
        # Si al invertirlo es TRUE, quiere decir que el juego esta pausado, saltamos todo este codigo
        if isPaused:
            return
    
    
    if (key == KEY_d or key == KEY_D or key == KEY_RIGHT) and not (isClimbing):
        playerX += speedX
    elif (key == KEY_a or key == KEY_A or key == KEY_LEFT) and not (isClimbing):
        playerX -= speedX
    elif (key == KEY_s or key == KEY_S or key == KEY_DOWN) and (canClimb):
        playerY += speedY
        isClimbing = True
        canJump = False
    elif (key == KEY_w or key == KEY_W or key == KEY_UP) and (canClimb):
        playerY -= speedY
        isClimbing = True
        canJump = False
    elif not isClimbing:
        canJump = True
        
    # Si va a saltar, le prohibo que escale y salte nuevamente hasta que vuelva a caer
    # Ademas, obtengo el tiempo actual (ms) para usarlo al calcular el offset de salto
    # mediante la funcion seno, que entre [0,pi] es positiva, entonces, este tiempo
    # que se guarde aqui menos el tiempo actual van a dar numeros que comenzaran en 0
    # e iran subiendo, para asi obtener la curva del seno como salto
    if key == KEY_SPACE and canJump and not isJumping:
        canJump = False
        isJumping = True
        canClimb = False
        jumpTimer = time.time() # Parametro para el seno
    
        
    if key == KEY_ENTER:
        enterPressed = True
    else:
        enterPressed = False
        
        

# =====================================================================================
# =====================================================================================
# ============================ Inteligencia Articial ==================================
# =====================================================================================
# =====================================================================================

# Metodo para que se muevan los monstruos
def tickMonsters():
    # Recorremos todos los monstruos
    for i in range(0, len(mNames)):
        # Movemos segun posicion actual del jugador
        if mX[i] > playerX:
            mX[i] -= mSpeedX[i]
        elif mX[i] < playerX:
            mX[i] += mSpeedX[i]



# Metodo para pintar los monstruos
def renderMonsters(window):
    # Pintamos todos los monstruos
    for i in range(0, len(mNames)):
        drawRect(mX[i], mY[i], mWidth[i], mHeight[i], mColors[i], window)
        drawString(mX[i]-(mWidth[i]/2.8), mY[i]-15, mNames[i], "white", 12, window)
        
        
        
        


# =====================================================================================
# =====================================================================================
# ================================= Menu del Juego ====================================
# =====================================================================================
# =====================================================================================


# Metodo para actualizar el menu
def tickMenu():
    malditoPythonQueNoDejaInicializarFuncionesVacias = 1 # Aqui van a ir los efectos al menu
    
# Metodo para pintar el menu
def renderMenu(window):
    # Pintamos el mensaje principal "MENU"
    drawString(280, 90, "Menu", "white", 82, window)
    
    # Pintamos todas las opciones del menu
    for i in range(0, len(optionNames)):
        drawString(optionXCoords[i], optionYCoords[i], optionNames[i], "white", 38, window)
    
    #drawString(window.winfo_width() / 3 + 15, window.winfo_height() / 9, "Menu", "white", 82, window)
    
    
    
    points = [260, selectedOptionY,
              260, selectedOptionY+40,
              300, selectedOptionY+20]
    window.create_polygon(points, outline="red", fill="green", width=2)
    
    
    
    
# Metodo para activar el teclado en modo Menu
def inputMenu(key):
    global selectedOptionY, selectedOption, enterPressed, isInMenu, isPlaying
    
    # Movemos el cursor del menu segun sea la tecla
    if (key == KEY_s or key == KEY_S or key == KEY_DOWN) and (selectedOption < MAX_OPTIONS):
        selectedOptionY += distanceBetweenOptions
        selectedOption += 1
    elif (key == KEY_w or key == KEY_W or key == KEY_UP) and (selectedOption > 1):
        selectedOptionY -= distanceBetweenOptions
        selectedOption -= 1
        
    if key == KEY_ENTER:
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
def renderGame(window):
    # Pintamos el mapa
    drawMap(window)
    
    # Pintamos el jugador
    renderPlayer(window)
    
    # Pintamos los monstruos
    renderMonsters(window)
    
    # Si esta pausado el juego, pintamos un Texto que nos lo diga
    if isPaused:
        drawString(250, 200, "PAUSE", "white", 80, window)
    
    
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
    
    
    
# Render method (Aqui se pinta el mapa de juego en base a la matriz)
def render(window):
    if isInMenu:
        renderMenu(window)
    elif isPlaying:
        renderGame(window)



# Loop principal
def gameLoop():
    # Creamos el objeto ventana
    mainComponent = Tk()
    # Setteamos las dimensiones
    mainComponent.geometry(windowWidth + 'x' + windowHeight)
    # Setteamos el titulo
    mainComponent.title(windowTitle)
    # Desactivamos la opcion para cambiar el tamano
    mainComponent.resizable(0, 0)
    # Creamos un objeto canvas y le pasamos la informacion del objeto ventana
    window = Canvas(mainComponent, bg="black", width=int(windowWidth), height=int(windowHeight))
    
    
    # Setteamos el tiempo que le debe tomar actualizar 1 vez
    frameTime = float(1.0 / frameCap)
    
    # Tomamos el tiempo en que se pinto por primera vez
    lastTime = time.time()
    
    # Contador para saber cuantas veces todavia necesito actualizar el juego
    unprocessedTime = 0
    
    # Contador de FPS
    fps = 0
    frameCounter = 0
    
    window.pack()
    window.update()
    
    # Cargamos el mapa para iniciar el juego (Provisional)
    
    # Loop principal
    while True:
        # Para llevar cuenta si debe pintar o no
        shouldRender = False
        
        # Tomamos el tiempo en que comenzo a pintarse en este loop
        startTime = time.time()
        
        # Calculamos el tiempo que le tomo pintar el ciclo pasado
        passedTime = startTime - lastTime
        
        # Guardamos el tiempo actual como tiempo pasado para ser usado en el proximo ciclo
        lastTime = startTime
        
        unprocessedTime += passedTime / float(SECOND)
        frameCounter += passedTime
        #print("unpro ", unprocessedTime, " .... y frameTime ", frameTime)
        while unprocessedTime > frameTime:
            #print("ENTROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            # Activamos para que pinte
            shouldRender = True
            unprocessedTime -= frameTime
            
            # Tickeamos aqui para actualizar varias veces por segundo
            tick()
            
            # Si paso un segundo, imprimimos la cantidad de FPS
            if (frameCounter >= SECOND):
                print(fps, " fps")
                fps = 0
                frameCounter = 0
        
        if shouldRender:
            window.delete(ALL)
            render(window)
            window.pack()
            window.update()
            fps += 1
        else:
            time.sleep(0.001)

    # fin del loop principal
    


# =====================================================================================
# =====================================================================================
# =============================== COMENZAR EL JUEGO ===================================
# =====================================================================================
# =====================================================================================

# Leemos el mapa del archivo
map = loadMap("newlevel.png")

# Iniciamos el juego
gameLoop()