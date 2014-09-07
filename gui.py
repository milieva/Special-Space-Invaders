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
MOVE_PLAYER_BULLET = 500
MOVE_MONSTER_BULLETS = 5000
TIMER_UP = 1000000

clock = pygame.time.Clock()
move_side_event = pygame.USEREVENT + 1
move_player_bullet_event = pygame.USEREVENT + 2
move_monster_bullet_event = pygame.USEREVENT + 3
timer_up_event = pygame.USEREVENT + 4

pygame.time.set_timer(move_side_event, MOVE_SIDE)
pygame.time.set_timer(move_player_bullet_event, MOVE_PLAYER_BULLET)
pygame.time.set_timer(move_monster_bullet_event, MOVE_MONSTER_BULLETS)
pygame.time.set_timer(timer_up_event, TIMER_UP)


monster_sprite = pygame.image.load(os.path.join('resources', 'monster.png'))
player_sprite = pygame.image.load(os.path.join('resources', 'crown.png'))
big_monster_sprite = pygame.image.load(os.path.join('resources', 'big_monster.png'))
player_bullet_sprite = pygame.image.load(os.path.join('resources', 'bullet.png'))
monster_bullet_sprite = pygame.image.load(os.path.join('resources', 'rabbit_bullet.png'))
end_game_winner = pygame.image.load(os.path.join('resources', 'winner.png'))
end_game_loser = pygame.image.load(os.path.join('resources', 'loser.jpg'))

new_player = Player("Pencho", (250, 550))
new_game = Game(0, 4, new_player)
surface.blit(player_sprite, new_player.coordinates)

def monster_coordinates(level):
    if level == 0:
        new_game.timer = 4
        return [(75, 20), (225, 20), (375, 20), (525, 20)]
    elif level == 1:
        new_game.timer = 8
        return [(75, 20), (225, 20), (375, 20), (525, 20)
            (75, 100), (225, 100), (375, 100), (525, 100)]
    elif level == 2:
        new_game.timer = 12
        return [(75, 20), (225, 20), (375, 20), (525, 20)
            (75, 100), (225, 100), (375, 100), (525, 100)
            (75, 180), (225, 180), (375, 180), (525, 180)]
    elif level == 3:
        new_game.timer = 16
        return [(75, 20), (225, 20), (375, 20), (525, 20)
            (75, 100), (225, 100), (375, 100), (525, 100)
            (75, 180), (225, 180), (375, 180), (525, 180)
            (75, 260), (225, 260), (375, 260), (525, 260)]

move_left = True
move_right = False

def collide_with_monster(bullet, monster):
    bullet_rect = surface.get_rect(topleft = bullet.coordinates, width = BULLET_WIDTH, height = BULLET_HEIGHT)
    monster_rect = surface.get_rect(topleft = monster.coordinates, width = MONSTER_WIDTH, height = MONSTER_HEIGHT)

    if (monster_rect.colliderect(bullet_rect)):
        pygame.draw.rect(surface, [255, 255, 255], bullet_rect)
        pygame.draw.rect(surface, [255, 255, 255], monster_rect)
        return True

def collide_with_player(bullet, player):
    bullet_rect = surface.get_rect(topleft = bullet.coordinates, width = BULLET_WIDTH, height = BULLET_HEIGHT)
    player_rect = surface.get_rect(topleft = new_player.coordinates, width = PLAYER_WIDTH, height = PLAYER_HEIGHT)

    if(player_rect.colliderect(bullet_rect)):
        pygame.draw.rect(surface, [255, 255, 255], bullet_rect)
        pygame.draw.rect(surface, [255, 255, 255], player_rect)
        return True

def move_monsters_left(monsters):
    for monster in monsters:
        x = monster.coordinates[0]
        y = monster.coordinates[1]
        pygame.draw.rect(surface, [255,255,255], (x, y, MONSTER_WIDTH,MONSTER_HEIGHT))
        monster.move((x - 50, y))
        if not(monster.is_dead()):
            surface.blit(monster_sprite, monster.coordinates)

def move_monsters_right(monsters):
    for monster in monsters:
        x = monster.coordinates[0]
        y = monster.coordinates[1]
        pygame.draw.rect(surface, [255,255,255], (x, y, MONSTER_WIDTH,MONSTER_HEIGHT))
        monster.move((x + 50, y))
        if not(monster.is_dead()):
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

def move_player_bullets(bullets):
    for bullet in bullets:
        x = bullet.coordinates[0]
        y = bullet.coordinates[1]
        pygame.draw.rect(surface, [255,255,255], (x, y, BULLET_WIDTH, BULLET_HEIGHT))
        bullet.move()
        if not(bullet.is_dead()):
            surface.blit(player_bullet_sprite, bullet.coordinates)
            for monster in new_game.monsters:
                if collide_with_monster(bullet, monster):
                    bullet.take_a_hit()
                    monster.take_a_hit()
                    new_game.timer -=1

def move_monster_bullets(bullets):
    for bullet in bullets:
        x = bullet.coordinates[0]
        y = bullet.coordinates[1]
        pygame.draw.rect(surface, [255,255,255], (x, y, BULLET_WIDTH, BULLET_HEIGHT))
        bullet.move()
        if not(bullet.is_dead()):
            surface.blit(monster_bullet_sprite, bullet.coordinates)
            if collide_with_player(bullet, new_game.player):
                bullet.take_a_hit()
                new_game.player.take_a_hit()
        
def player_shoot(player):
    x = new_player.coordinates[0]
    y = new_player.coordinates[1]
    player.shoot()
    for monster in new_game.monsters:
        for bullet in new_game.player.bullets:
            surface.blit(player_bullet_sprite, bullet.coordinates)
    move_player_bullets(player.bullets)


def monster_shoot(monster):
    x = monster.coordinates[0]
    y = monster.coordinates[1]
    monster.shoot()
    for bullet in monster.bullets:
        surface.blit(player_bullet_sprite, bullet.coordinates)
    move_monster_bullets(monster.bullets)


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
            elif event.type == move_player_bullet_event:
                move_player_bullets(new_player.bullets)
                if new_game.timer == 0:
                    new_game.spawn_big_monster()
                    pygame.draw.rect(surface, [255,255,255], (0, 0, 600, 600))
                    #surface.blit()
            elif event.type == move_monster_bullet_event:
                for monster in new_game.monsters:
                    monster_shoot(monster)
                    if new_player.is_dead():
                        surface.blit(end_game_loser, (0, 0))
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
