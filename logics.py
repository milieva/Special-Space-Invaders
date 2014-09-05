DAMAGE = 1
FAST_SPEED = 50
NORMAL_SPEED = 30
PLAYER_LIVES = 3

class Unit:
	def __init__(self, health, coordinates):
		self.health = health
		self.coordinates = coordinates

	def is_dead(self):
		return self.health == 0

	def move(self, new_coordinates):
		self.coordinates = new_coordinates

	def take_a_hit(self):
		self.health -= DAMAGE


class Bullet(Unit):
	def __init__(self, direction, health, coordinates):
		Unit.__init__(self, health, coordinates)
		self.speed = NORMAL_SPEED
		self.direction = direction
		self.is_normal = True

	def change_speed(self):
		if self.is_normal:
			self.is_normal = False
			self.speed = FAST_SPEED
		else:
			self.is_normal = True
			self.speed = NORMAL_SPEED

	def move(self):
		self.coordinates[1] += self.direction

class Player(Unit):
	def __init__(self, name, coordinates):
		Unit.__init__(self, PLAYER_LIVES, coordinates)
		self.name = name
		self.score = 0
		self.bullets = []

	def increase_score(self):
		self.score += 1

	def shoot(self):
		bullet = Bullet(1, 1, self.coordinates)
		self.bullets.append(bullet)
		self.bullets = list(filter(lambda x: not(x.is_dead()), self.bullets))

class Monster(Unit):
	def __init__(self, coordinates):
		Unit.__init__(self, 1, coordinates)
		self.bullets = []

	def shoot(self):
		bullet = Bullet(-1, 1, self.coordinates)
		self.bullets.append(bullet)
		self.bullets = list(filter(lambda x: not(x.is_dead()), self.bullets))

class BigMonster(Unit):
	def __init__(self, health, coordinates):
		Unit.__init__(self, health, coordinates)
		self.bullets = []

	def shoot(self):
		bullet = Bullet(-1, 1, self.coordinates)
		bullet.change_speed()
		self.bullets.append(bullet)
		self.bullets = list(filter(lambda x: not(x.is_dead()), self.bullets))

class Game:
	def __init__(self, level, timer, player):
		self.level = level
		self.timer = timer
		self.player = player
		self.monsters = []

	def spawn_monsters(self, coordinates):
		for coordinate in coordinates:
			monster = Monster(coordinate)
			self.monsters.append(monster)

	def spawn_big_monster(self):
		if self.timer == 0:
			monster_health = len(self.monsters)
			big_monster = BigMonster(monster_health, (0, 0))
			self.monsters = [big_monster]

	def spawn_player(self, name):
		player = Player(name, (0, 0))

	def start(self):
		self.spawn_player(name)
		self.spawn_monsters()

	def level_up(self):
		if self.monsters == []:
			level += 1

	def end(self):
		if self.level == 5 or self.player.is_dead():
			return True 

