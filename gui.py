import pygame
import time
from logics import *
import os

pygame.init()
WIDTH = 600
HEIGHT = 600
MONSTER_HEIGHT = 64
MONSTER_WIDTH = 65
BIG_MONSTER_HEIGHT = 100
BIG_MONSTER_WIDTH = 100
PLAYER_HEIGHT = 53
PLAYER_WIDTH = 60
BULLET_HEIGHT = 32
BULLET_WIDTH = 32

surface = pygame.display.set_mode((HEIGHT, WIDTH))
surface.fill((255, 255, 255))
MOVE_SIDE = 1000
MOVE_BULLET = 1000
clock = pygame.time.Clock()
move_side_event = pygame.USEREVENT + 1
move_player_bullet_event = pygame.USEREVENT + 2

pygame.time.set_timer(move_side_event, MOVE_SIDE)

monster_sprite = pygame.image.load(os.path.join('resources', 'monster.png'))
player_sprite = pygame.image.load(os.path.join('resources', 'crown.png'))
big_monster_sprite = pygame.image.load(os.path.join('resources', 'big_monster.png'))
bullet_sprite = pygame.image.load(os.path.join('resources', 'bullet.png'))

new_player = Player("Pencho", (250, 550))
new_game = Game(0, 20, new_player)
surface.blit(player_sprite, new_player.coordinates)

def monster_coordinates(level):
	if level == 0:
		return [(75, 20), (225, 20), (375, 20), (525, 20)]
	#else if level == 1:
	#else if level == 2:
	#else if level == 3:

move_left = True
move_right = False

def move_monsters_left(monsters):
	for monster in monsters:
		x = monster.coordinates[0]
		y = monster.coordinates[1]
		pygame.draw.rect(surface, [255,255,255], (x, y, MONSTER_WIDTH,MONSTER_HEIGHT))
		monster.move((x - 50, y))
		surface.blit(monster_sprite, monster.coordinates)

def move_monsters_right(monsters):
	for monster in monsters:
		x = monster.coordinates[0]
		y = monster.coordinates[1]
		pygame.draw.rect(surface, [255,255,255], (x, y, MONSTER_WIDTH,MONSTER_HEIGHT))
		monster.move((x + 50, y))
		surface.blit(monster_sprite, monster.coordinates)

def move_player_left(player):
	x = player.coordinates[0]
	y = player.coordinates[1]
	if x - 20 > 0:
		pygame.draw.rect(surface, [255,255,255], (x, y, PLAYER_WIDTH,PLAYER_HEIGHT))
		player.move((x - 20, y))
		surface.blit(player_sprite, player.coordinates)

def move_player_right(player):
	x = player.coordinates[0]
	y = player.coordinates[1]
	if x + 20 < 550:
		pygame.draw.rect(surface, [255,255,255], (x, y, PLAYER_WIDTH,PLAYER_HEIGHT))
		player.move((x + 20, y))
		surface.blit(player_sprite, player.coordinates)

def move_player_bullet(bullets):
	for bullet in bullets:
		x = bullet.coordinates[0]
		y = bullet.coordinates[1]
		#if x - 20 > 0:
		pygame.draw.rect(surface, [255,255,255], (x, y, BULLET_WIDTH, BULLET_HEIGHT))
		bullet.move()
		surface.blit(bullet_sprite, bullet.coordinates)

def player_shoot(player):
	x = new_player.coordinates[0]
	y = new_player.coordinates[1]
	player.shoot()
	for bullet in player.bullets:
		surface.blit(bullet_sprite, bullet.coordinates)
	move_player_bullet(player.bullets)

new_game.spawn_monsters(monster_coordinates(new_game.level))
for monster in new_game.monsters:
	surface.blit(monster_sprite, monster.coordinates)

class Quit(Exception): pass
try:
	while True:
		clock.tick(40)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise Quit()
			elif event.type == move_side_event:
				if move_left:
					move_monsters_left(new_game.monsters)
					move_left = not(move_left)
					move_right = True
				elif move_right: 
					move_monsters_right(new_game.monsters)
					move_right = not(move_right)
					move_left = True
			else:
				if event.type == pygame.KEYDOWN:
					if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
						move_player_left(new_player)
					if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
						move_player_right(new_player)
					if pygame.key.get_pressed()[pygame.K_SPACE] != 0:
						player_shoot(new_player)
				pygame.display.update()


		time.sleep(0.1)
		pygame.display.flip()

except Quit:
	print('quit')

finally:
	pygame.quit()