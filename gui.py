import pygame
import time
from logics import *
import os

pygame.init()
WIDTH = 600
HEIGHT = 600

surface = pygame.display.set_mode((HEIGHT, WIDTH))
#surface.fill((255, 255, 255))

monster_sprite = pygame.image.load(os.path.join('resources', 'monster.jpg'))
player_sprite = pygame.image.load(os.path.join('resources', 'player.png'))
big_monster_sprite = pygame.image.load(os.path.join('resources', 'big_monster.png'))

new_player = Player("Pencho", (130, 300))
new_game = Game(0, 20, new_player)
surface.blit(player_sprite, new_player.coordinates)
new_game.spawn_monsters([(0, 0), (200, 0)])
for monster in new_game.monsters:
	surface.blit(monster_sprite, monster.coordinates)

class Quit(Exception): pass
try:
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise Quit()
			else:
				if event.type == pygame.KEYDOWN:
					if pygame.key.get_pressed()[pygame.K_LEFT] != 0 :
						x = new_player.coordinates[0]
						y = new_player.coordinates[1]
						new_player.move((x + 100, y))
						surface.blit(player_sprite, new_player.coordinates)
					if pygame.key.get_pressed()[pygame.K_RIGHT] != 0 :
						x = new_player.coordinates[0]
						y = new_player.coordinates[1]
						new_player.move((x - 100, y))
						surface.blit(player_sprite, new_player.coordinates)
					if pygame.key.get_pressed()[pygame.K_SPACE] != 0 :
						x = new_player.coordinates[0]
						y = new_player.coordinates[1]
						new_player.shoot()
						surface.blit(big_monster_sprite, (x, y))
				pygame.display.update()


		time.sleep(0.1)
		pygame.display.flip()

except Quit:
	print('quit')

finally:
	pygame.quit()