import pygame, sys, os
from pygame.locals import *

# Variables

WINDOW_SIZE = (400, 400) # Stores the size of the window
player_location = [50,50] # Storing player location
background_colour = (146, 244, 255)
alpha = (68, 255, 0)
ani = 4

# Objects

class Enemy(pygame.sprite.Sprite):
	
	def __init__(self, x, y, enemy_img):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for i in range(1, 8):
			img = pygame.image.load(os.path.join('images/Enemy', enemy_img + str(i) + '.png')).convert()
			img.convert_alpha()
			img.set_colorkey(alpha)
			self.images.append(img)
			self.image = self.images[0]
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y


class Player(pygame.sprite.Sprite):
	"""
		Spawn Player
	"""

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.movex = 0
		self.movey = 0
		self.frame = 0
		self.images = []
		for i in range(1, 5):
			img = pygame.image.load(os.path.join('images/player', 'player_right' + str(i) + '.png')).convert()
			img.convert_alpha()
			img.set_colorkey(alpha)
			self.images.append(img)
			self.image = self.images[0]
			self.rect = self.image.get_rect()

	def control(self, x, y):
		"""
			Control player movement	
		"""
		self.movex += xaa
		self.movey += y

	def update(self):
		"""
			Update sprite position
		"""
		self.rect.x = self.rect.x + self.movex
		self.rect.y = self.rect.y + self.movey

		# moving left
		if self.movex < 0:
			self.frame += 1
			if self.frame > 3*ani:
				self.frame = 0
			self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

		# moving right
		if self.movex > 0:
			self.frame += 1
			if self.frame > 3*ani:
				self.frame = 0
			self.image = self.images[self.frame//ani]



class Level():
	
	def bad(lvl, eloc):
		if lvl == 1:
			enemy = Enemy(eloc[0], eloc[1], 'enemy')
			enemy_list = pygame.sprite.Group()
			enemy_list.add(enemy)
		if lvl == 2:
			print("Level " + str(lvl))

		return enemy_list
			

# Setup

clock = pygame.time.Clock() # initialises clock object to use in controlling frame rate
pygame.init() # initialises all the pygame modules that need to be initialised
pygame.display.set_caption('Platformer') # sets the name of the window
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # creates the window passing in the width and height dimensions, as well as any additional options and the number of bits used for colour

# Creating/Spawning player

player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 5

# Create Level

eloc = []
eloc = [200, 15]
enemy_list = Level.bad(1, eloc)

# Loading background

backdrop = pygame.image.load(os.path.join('images/background', 'stage.png'))
backdrop_box = screen.get_rect()

# Main Loop

while True:

	screen.fill(background_colour) # fills with the rgb colour defined
	#screen.blit(backdrop, backdrop_box)
	player.update()
	player_list.draw(screen)
	enemy_list.draw(screen)

	for event in pygame.event.get(): # checks for any keyboard and mouse events
		if event.type == QUIT: # forces the program to quit if the uses clicks the exit icon
			pygame.quit()
			sys.exit()

		# defining what happens when a key is pressed down
		if event.type == KEYDOWN:
			if event.key == K_w:
				print("jump")
			if event.key == K_d:
				player.control(steps, 0)
			if event.key == K_a:
				player.control(-steps, 0)
				
		# defining what happens when a key is not pressed
		if event.type == KEYUP:
			if event.key == K_w:
				pass
			if event.key == K_d:
				player.control(-steps, 0)
				player.image = player.images[0]
			if event.key == K_a:
				player.control(steps, 0)
				player.image = pygame.transform.flip(player.images[0], True, False)


	pygame.display.update() # continually checking for updates
	clock.tick(60) # ensures that the game is runnig out 60 fps, but also caps it at 60