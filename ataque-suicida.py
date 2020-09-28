import pygame, sys, random
from pygame.locals import *
from pygame_functions import *

pygame.init()
#clases
class Nave:
	def __init__(self,width,height,x,y,velocity,imagen):
		self.width=width
		self.height=height
		self.x=x
		self.y=y
		self.velocity=velocity
		self.imagen=imagen

class Proyectil:
	def __init__(self,width,height,x,y,velocity,imagen):
		self.width=width
		self.height=height
		self.x=x
		self.y=y
		self.velocity=velocity
		self.imagen=imagen

#conf
vent_w=480
vent_h=720
pygame.display.set_caption("Ataque en el espacio")
ventana = pygame.display.set_mode((vent_w, vent_h))
GameOver = False
reloj=0
j1 = Nave(44,37,round(vent_w/2),vent_h-50,4,pygame.image.load('data/nave1.png'))
enemigos = []
balas = []
balasEnemigas = []
colisionado = False
vidas = []
explosion = [pygame.image.load('data/explosion1.png'),pygame.image.load('data/explosion2.png'),pygame.image.load('data/explosion3.png'),pygame.image.load('data/explosion4.png'),pygame.image.load('data/explosion5.png'),pygame.image.load('data/explosion6.png'),pygame.image.load('data/explosion7.png'),pygame.image.load('data/explosion8.png'),pygame.image.load('data/explosion9.png'),pygame.image.load('data/explosion10.png'),pygame.image.load('data/explosion11.png'),pygame.image.load('data/explosion12.png'),pygame.image.load('data/explosion13.png'),pygame.image.load('data/explosion14.png'),]
cuadro=0

#funciones
def spawn():
	if reloj%200 == 0:
		enemigos.append(Nave(40,40,random.randint(10,vent_w-50),-40,2,pygame.image.load('data/enemigo.png')))

def colision(nave,bala,balas):
	dx=abs(nave.x - bala.x)
	dy=abs(nave.y - bala.y)
	if dx < 20 and dy < 20:
		print('ouch')
		balas.pop(balas.index(bala))
		enemigos.pop(enemigos.index(nave))

def gameover(nave):
	for balaEnemiga in balasEnemigas:
		dx=abs(nave.x - balaEnemiga.x)
		dy=abs(nave.y - balaEnemiga.y)
		if dx < 20 and dy < 20:
			return True

def Controles():
	keys = pygame.key.get_pressed()
	delay=pygame.key.set_repeat(10,10)
	if keys[pygame.K_UP] and j1.y > j1.height:
		j1.y -= j1.velocity
	if keys[pygame.K_DOWN] and j1.y < vent_h-50:
		j1.y += j1.velocity
	if keys[pygame.K_LEFT] and j1.x > j1.width:
		j1.x -= j1.velocity
	if keys[pygame.K_RIGHT] and j1.x < vent_w-j1.width:
		j1.x += j1.velocity

def disparar():
	if evento.type == pygame.KEYDOWN:
		if evento.key == pygame.K_SPACE:
			balas.append(Proyectil(9,30,j1.x,j1.y-15,15,pygame.image.load('data/laser1.png')))
	for bala in balas:
		if bala.y < 0-bala.height:
			balas.pop(balas.index(bala))

def disparoEnemigo():
	for enemigo in enemigos:
		if abs(enemigo.x - j1.x) < 50 and reloj % 25 == 0:
			balasEnemigas.append(Proyectil(9,30,enemigo.x,enemigo.y+enemigo.height/2,8,pygame.image.load('data/laser.png')))

def ReglaMovimiento(sujeto):
	sujeto.y += sujeto.velocity

def DibujarPantalla():
	#fondo
	ventana.fill([0,0,0])
	#ventana.blit(pygame.image.load('data/bg.jpg'),(0,0))
	#jugador
	ventana.blit(j1.imagen, (round(j1.x-j1.width/2),round(j1.y-j1.height/2)))
	#proyectiles
	for bala in balas:
		bala.y -= bala.velocity
		ventana.blit(bala.imagen, (bala.x-round(bala.width/2),bala.y-round(j1.height/2)+10))
	for balaEnemiga in balasEnemigas:
		balaEnemiga.y += balaEnemiga.velocity
		ventana.blit(balaEnemiga.imagen, (round(balaEnemiga.x-balaEnemiga.width/2),round(balaEnemiga.y-balaEnemiga.height/2)))
		if balaEnemiga.y > vent_h:
				balasEnemigas.pop(balasEnemigas.index(balaEnemiga))
	for enemigo in enemigos:
		ReglaMovimiento(enemigo)
		ventana.blit(enemigo.imagen, (round(enemigo.x-enemigo.width/2), round(enemigo.y-enemigo.height/2)))
		if enemigo.y > vent_h:
				enemigos.pop(enemigos.index(enemigo))
	cuadro = 8
	if gameover(j1) and cuadro <= 14:
		ventana.blit(explosion[cuadro], (round(j1.x-j1.width),round(j1.y-j1.height)))
		cuadro += 1
	pygame.display.update()

while not GameOver:
	#events
	disparoEnemigo()
	for bala in balas:
		for enemigo in enemigos:
			colision(enemigo, bala, balas)
	spawn()
	for evento in pygame.event.get():
		disparar()
		if evento.type == pygame.QUIT:
			GameOver = True
	Controles()
	#loop
	pygame.time.delay(15)
	reloj += 1
	for bala in balas:
		if bala.y < 0 - bala.height:
			balas.pop(balas.index(bala))
	if gameover(j1):
		adios = reloj
		if adios == reloj - 100:
			GameOver = True
	#render
	DibujarPantalla()

pygame.quit()
sys.exit()
