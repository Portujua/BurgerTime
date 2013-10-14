# Imports
import sys
import math
import time
import pyHook
import pyglet
from pyglet.window import key
from pyglet.gl import *

import PIL.Image
import PIL.ImageTk
from tkinter import *
from msvcrt import *

# ============================== Variables ==============================

# Constantes MENU
MENU_PLAY = 2
MENU_EXIT = 1
MAX_OPTIONS = 2

# Propiedades del menu
# Para crear una opcion nueva es igual que los monstruos, se anade 1 item a cada arreglo de opciones
# se modifica arriba MAX_OPTIONS, y se anade la opcion nueva

selectedOption = 1              # Opcion seleccionada por defecto
selectedOptionY = 240           # Coordenada Y del cursor en el menu
selectedOptionX  = 260          # Coordenada X del cursor del menu
selectedOptionWidth = 50        # Ancho del cursor del menu
selectedOptionHeight = 50       # Alto del cursor del menu
distanceBetweenOptions = 100    # Distancia entre cada opcion del menu (para mover el triangulo)

optionNames = ["Jugar", "Salir"]
optionXCoords = [400, 400]
optionYCoords = [370, 270]


# Estados del juego
isInMenu = True
isPlaying = False
isPaused = False
isRunning = True


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



### ---------- Propiedades del Jugador ----------

# Imagen que contiene el Grid del jugador
playerGrid = "grid.png"

# Tamano del grid
pGridSizeX = 2
pGridSizeY = 2

# Imagenes del jugador
pImages = []


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

# Imagen que contiene todas las imagenes de los monstruos
monstersGridName = ["grid.png", "grid.png"]

# Tamano del grid (ancho, alto)
mGridSizeX = [2, 2]
mGridSizeY = [2, 2]

# Aqui se guardaran las imagenes leidas de cada monstruo (es usado al pintar)
# La primera corresponde a 0,0, la segunda 1,0, la tercera 2,0... n,0 ... 0,1 , 0,2 , ..., 0,m ... n,m
mImages = [[], []] 

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


# Inicializar la ventana
def initDisplay():
    global window
    
    # Creamos la ventana OpenGL
    window = pyglet.window.Window(resizable=True, vsync=False)
    window.set_caption(windowTitle) 
    window.set_size(windowWidth, windowHeight)  
    
    #pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.clock.set_fps_limit(9999)

    
    

# La inicializamos
initDisplay()


# =====================================================================================
# =====================================================================================
# =========================== Modificaciones OpenGL ===================================
# =====================================================================================
# =====================================================================================


# Reemplazamos la funcion onKeyPress del pyglet
@window.event
def on_key_press(e, modifiers):    
    
    #inputPlayer(e)
    #return
    
    # Esta funcion VVVV nos devuelve el String de la tecla que presionamos
    #print(pyglet.window.key.symbol_string(e))
    
    if isInMenu:
        inputMenu(e)
    elif isPlaying:
        inputPlayer(e)
    
    



# =====================================================================================
# =====================================================================================
# ================================== Funcionales ======================================
# =====================================================================================
# =====================================================================================


# Metodo para cargar una imagen
def openImage(filePath):
    # Cargamos la imagen
    image = pyglet.image.load(filePath)  
    return image


# Metodo leer un grid de imagenes y devolverlo como array de imagenes
def loadGridImage(filePath, x, y):
    grid = openImage(filePath)
    imageGrid = pyglet.image.ImageGrid(grid, x, y)
    return imageGrid


# Metodo para cargar imagenes de menu
def loadMenuTexture(fileName, x, y):
    filePath = "../res/textures/menu/" + fileName
    return loadGridImage(filePath, x, y)


# Metodo para cargar imagenes de juego
def loadGameTexture(fileName, x, y):
    filePath = "../res/textures/game/" + fileName
    return loadGridImage(filePath, x, y)



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

# Pintar lineas (Por tenerlo..)
def drawLines(px, py, qx, qy, rgb):
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Convertimos de RGB a R,G,B
    r = (rgb << 16) & 0xFFFFFF
    b = (rgb << 8) & 0xFFFFFF
    g = rgb & 0xFFFFFF
    
    # Setteamos el color
    pyglet.gl.glColor3f(r, g, b)
    # Pintamos basandonos en los puntos P,Q
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (px, py, qx, qy)))
    

# Metodo para pintar string, el string sera pintado centrado en el punto x,y dado.. Ejemplo:
# Si se da como punto window.width/2, window.height/2 entonces saldra centrado en la pantalla
def drawString(xx, yy, string, font, color, size):
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    t = pyglet.text.Label(string, font_name=font, font_size=size, x=xx, y=yy,
                          anchor_x='center', anchor_y='center')
    t.draw()


# Metodo para pintar imagenes (Innecesario pero se hace mas facil de entender
def drawImage(image, x, y):
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    image.blit(x, y)
    

# Parecibo a pintar una imagen, pero en este podemos especificar el tamano que queremos que sea pintada
# Le pasamos una imagen y aqui la convertiremos a textura para posteriormente redimensionarla
def drawTexture(image, x, y, width, height):
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Obtenemos la textura de la imagen
    texture = image.get_texture()
    
    # Setteamos el modo de conversion del OpenGL
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    
    # Setteamos el nuevo tamano
    texture.width = width
    texture.height = height
    
    # La pintamos
    texture.blit(x, y)
    
    
    

# Metodo que pinta el mapa basandose en la matriz del mapa y el tamano de cada bloque
# Aqui hay un problema, le toma 0.5 seg renderizar esto
def drawMap():
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Creamos dos variables para ir llevando el offset
    # Cada bloque se pintara en una coordenada X mas el OFFSET total
    xOffset = 0
    yOffset = 0
    
    # Creamos una variable para la textura
    mapTexture = loadGridImage("../res/textures/map/grid.png", 2, 2)
    
    # Recorremos todo el mapa
    for y in range(0, mapHeight):
        for x in range(0, mapWidth):
            # Chequeamos para no pintar cosas innecesarias
            if (xOffset > window.width) or (yOffset > window.height): continue
            
            # Wtf
            if (x + y*mapWidth) < 0 or (x + y*mapWidth) >= len(map):
                continue
            
            # Obtenemos la coordenada actual
            actCoord = map[x + y*mapWidth]
            
            if actCoord == TILE_NONE or actCoord == TILE_NULL:
                xOffset += blockSize
                continue
            
            # Variable para la textura actual
            actTexture = None
            
            # Setteamos el color segun el numero en la matriz
            if actCoord == TILE_FLOOR:
                actTexture = mapTexture[2]
            elif actCoord == TILE_STAIRS:
                actTexture = mapTexture[3]
            else:
                actTexture = mapTexture[1]
            
            # Pintamos el bloque
            drawTexture(actTexture, xOffset, yOffset, blockSize, blockSize)
            
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
def renderPlayer():
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
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
    drawTexture(pImages[0], playerX, playerY + jumpOffset, playerWidth, playerHeight + jumpOffset)
    #drawRect(playerX, playerY + jumpOffset, playerWidth, playerHeight + jumpOffset, "white", window)
    
    # Centro del jugador (Provisional)
    #drawRect(playerX, playerY + jumpOffset, 5, 5, "red", window)

    drawString(playerX-(playerWidth/2), playerY + jumpOffset-15, playerName, "Consolas", "white", 12)
    
    

# Metodo para activar el teclado en modo jugador
def inputPlayer(e):
    global playerX, playerY, enterPressed, isClimbing, canJump, isJumping, jumpTimer, canClimb, isPaused

    # Primero chequeamos si se pauso el juego, para asi saltar todo este codigo
    if e == key.P:
        # Invertimos el valor de isPaused
        isPaused = not(isPaused)
        
        # Si al invertirlo es TRUE, quiere decir que el juego esta pausado, saltamos todo este codigo
        if isPaused:
            return
    
    
    if (e == key.D or e == key.RIGHT) and not (isClimbing):
        playerX += speedX
    elif (e == key.A or e == key.LEFT) and not (isClimbing):
        playerX -= speedX
    elif (e == key.S or e == key.DOWN) and (canClimb):
        playerY += speedY
        isClimbing = True
        canJump = False
    elif (e == key.W or e == key.UP) and (canClimb):
        playerY -= speedY
        isClimbing = True
        canJump = False
    elif not isClimbing:
        canJump = True
        
    # Chequeo si no me sali de la ventana
    if playerX+playerWidth > window.width:
        playerX = window.width-playerWidth
    elif playerX < 0:
        playerX = 0
        
    # Si va a saltar, le prohibo que escale y salte nuevamente hasta que vuelva a caer
    # Ademas, obtengo el tiempo actual (ms) para usarlo al calcular el offset de salto
    # mediante la funcion seno, que entre [0,pi] es positiva, entonces, este tiempo
    # que se guarde aqui menos el tiempo actual van a dar numeros que comenzaran en 0
    # e iran subiendo, para asi obtener la curva del seno como salto
    if e == key.SPACE and canJump and not isJumping:
        canJump = False
        isJumping = True
        canClimb = False
        jumpTimer = time.time() # Parametro para el seno
    
        
    if e == key.ENTER:
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
def renderMonsters():
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Pintamos todos los monstruos
    for i in range(0, len(mNames)):
        drawTexture(mImages[i][0], mX[i], mY[i], mWidth[i], mHeight[i])
        drawString(mX[i]-(mWidth[i]/2.8), mY[i]-15, mNames[i], "Consolas", "white", 12)
        
        
        
        


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
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Pintamos el mensaje principal "MENU"
    drawString(window.width/2, window.height-70, "Menu", "Consolas", "white", 82)
    
    # Pintamos todas las opciones del menu
    for i in range(0, len(optionNames)):
        drawString(optionXCoords[i], optionYCoords[i], optionNames[i], "Consolas", "white", 38)     
    
    #menuArrow = openImage("../res/textures/menu/gameArrow.jpg")
    #menuArrow = loadMenuTexture("gameArrow.jpg", 1, 1)
    #drawTexture(menuArrow[0], selectedOptionX, selectedOptionY, selectedOptionWidth, selectedOptionHeight)    
    
    
    
# Metodo para activar el teclado en modo Menu
def inputMenu(e):
    global selectedOptionY, selectedOption, enterPressed, isInMenu, isPlaying
    
    # Movemos el cursor del menu segun sea la tecla
    if (e == key.S or e == key.DOWN) and (selectedOption > 1):
        selectedOptionY -= distanceBetweenOptions
        selectedOption -= 1
        print("Restando a opcion ", selectedOption)
    elif (e == key.W or e == key.UP) and (selectedOption < MAX_OPTIONS):
        selectedOptionY += distanceBetweenOptions
        selectedOption += 1
        print("Sumando a opcion ", selectedOption)
        
    if e == key.ENTER:
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


# Inicializamos los objetos del juego
def initGameObjects():
    # ===== Creamos los monstruos ===== 
    # Para cada monstruo, hacemos:
    for m in range(0, len(mNames)):         
        # Cargamos el grid
        tempTexture = loadGameTexture(monstersGridName[m], mGridSizeX[m], mGridSizeY[m])
              
        # Pegamos todas las texturas en el arreglo de textura de ese monstruo
        for i in range(0, len(tempTexture)):            
            mImages[m].append(tempTexture[i])
        
    
    # ===== Creamos el jugador =====
    # Cargamos el grid
    tempTexture = loadGameTexture(playerGrid, pGridSizeX, pGridSizeY)
    
    # Pegamos todas las texturas en el arreglo de texturas del jugador
    for i in range(0, len(tempTexture)):
        pImages.append(tempTexture[i])



# Pintar todo lo referente al juego (cuando se esta jugando)
def renderGame():
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    # Pintamos el mapa
    drawMap()
    
    # Pintamos el jugador
    renderPlayer()
    
    # Pintamos los monstruos
    renderMonsters()
    
    # Si esta pausado el juego, pintamos un Texto que nos lo diga
    if isPaused:
        drawString(window.width/2, window.height/2, "PAUSA", "Consolas", "white", 100)
    
    
# Actualizar el juego (cuando se esta jugando)
def tickGame():
    # Actualizamos solo si el juego no esta pausado
    if not isPaused:
        tickMonsters()
        tickPlayer()



# Tick method (Aqui va a suceder toda la logica del juego)
def tick():
    #print("Tickea")
    #tickPlayer()
    #tickMonsters()
    #return
    
    if isInMenu:
        tickMenu()
    elif isPlaying:
        tickGame()
    
    
    
# Render method (Aqui se pinta el mapa de juego en base a la matriz)
def render():    
    #drawMap()
    #renderPlayer()
    #renderMonsters()
    
    #drawMap()
    #print(time.time())
    #return
    
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    window.clear()
    
    if isInMenu:
        renderMenu()
    elif isPlaying:
        renderGame()
        
    fps = int(pyglet.clock.get_fps()) 
    drawString(80, window.height-30, str(fps) + " fps", "Consolas", "white", 24)


# Metodo para actualizar todo, el parametro es necesario por el pyglet
def update(dt): 
       
    # Tickeamos aqui, antes de pintar
    tick()
    
    # Limpiamos la pantalla actual
    #window.clear()
    #pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    
    # Pintamos
    #render()
    
    #fps = int(pyglet.clock.get_fps())    
    #drawString(80, window.height-30, str(fps) + " fps", "Consolas", "white", 24)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    window.clear()
    render()  
    fps = int(pyglet.clock.get_fps()) 
    drawString(80, window.height-30, str(fps) + " fps", "Consolas", "white", 24)
    
    


# =====================================================================================
# =====================================================================================
# =============================== COMENZAR EL JUEGO ===================================
# =====================================================================================
# =====================================================================================

# Leemos el mapa del archivo
map = loadMap("newlevel.png")    

initGameObjects()

# Iniciamos el juego
if __name__ == '__main__':
    # Iniciamos nuestro update
    pyglet.clock.schedule_interval(update, 1/500000.0)
    # Corremos la aplicacion
    pyglet.app.run()


















