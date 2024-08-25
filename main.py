import pygame
import random
import math
from pygame import mixer
import io

# Inicializar pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800,600))


#agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# Titulo e icono

pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

#Jugador
img_jugador = pygame.image.load('cohete.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

#enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigo = 8

for e in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(1)
    enemigo_y_cambio.append(55)



#bala
balas= []
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_y_cambio = 3
bala_visible = False

def texto_final():
    mi_fuente_final= fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (100, 200)) #para que se vean al centro de la pantalla

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, enemigo):
    pantalla.blit(img_enemigo[enemigo], (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    #se le agregan 16 y 10 para que aparezcan en el centro de la nave
    pantalla.blit(img_bala,(x + 16, y + 10))

def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}',True, (255,255,255))
    pantalla.blit(texto, (x, y))


#funcion detectar colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1,2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        return False

#funcion para pasar la funet de string a byte
def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()

    return io.BytesIO(ttf_bytes)

#puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_como_bytes,32)
texto_x = 10
texto_y = 10

fuente_final = pygame.font.Font(fuente_como_bytes, 50)

# Loop para salir del juego
se_ejecuta = True
while se_ejecuta:
    #RGB
    #pantalla.fill((205, 144, 228))
    pantalla.blit(fondo,(0,0))


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = +1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                    'x': jugador_x,
                    'y': jugador_y,
                    'velocidad' : -5
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)


        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0



    #modificar movimiento jugador
    jugador_x += jugador_x_cambio

    #matener dentro de bordes al jugador:
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar movimiento enemigo
    for e in range(cantidad_enemigo):

        #fin del juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigo):
                enemigo_y[k] = 1000
            texto_final()
            break



        enemigo_x[e] += enemigo_x_cambio[e]
        # matener dentro de bordes al enemigo:
        if enemigo_x[e]  <= 0:
            enemigo_x_cambio[e]  = 1.2
            enemigo_y[e]  += enemigo_y_cambio[e]
        elif enemigo_x[e]  >= 736:
            enemigo_x_cambio[e]  = -1.2
            enemigo_y[e]  += enemigo_y_cambio[e]

        '''
        colision = hay_colision(enemigo_x[e] , enemigo_y[e] , bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e]  = random.randint(0, 736)
            enemigo_y[e]  = random.randint(50, 200)
        '''
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)


    #movimiento bala
    '''
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio
        '''
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)


    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    #actualizar juego
    pygame.display.update()