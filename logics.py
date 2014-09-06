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
		self.coordinates = (self.coordinates[0], self.coordinates[1] + self.direction) 

class Player(Unit):
	def __init__(self, name, coordinates):
		Unit.__init__(self, PLAYER_LIVES, coordinates)
		self.name = name
		self.score = 0
		self.bullets = []

	def increase_score(self):
		self.score += 1

	def shoot(self):
		bullet = Bullet(-50, 1, (self.coordinates[0], self.coordinates[1] - 30))
		self.bullets.append(bullet)
		self.bullets = list(filter(lambda x: not(x.is_dead()), self.bullets))

class Monster(Unit):
	def __init__(self, coordinates):
		Unit.__init__(self, 1, coordinates)
		self.bullets = []

	def shoot(self):
		bullet = Bullet(50, 1, self.coordinates)
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
		if self.level != 4 and self.timer == 0:
			monster_health = len(self.monsters)
			big_monster = BigMonster(monster_health, (250, 250))
			self.monsters = [big_monster]
		elif self.level == 4:
			monster_health = 10
			big_monster1 = BigMonster(monster_health, (150, 50))
			big_monster2 = BigMonster(monster_health, (450, 50))
			big_monster3 = BigMonster(monster_health, (250, 200))
			self.monsters = [big_monster1, big_monster2, big_monster3]

	def spawn_player(self, name):
		player = Player(name, (0, 0))

	def decrease_timer(self):
		self.timer -=1

	def start(self):
		self.spawn_player(name)
		self.spawn_monsters()

	def level_up(self):
		if self.monsters == []:
			level += 1

	def end(self):
		if self.level == 5 or self.player.is_dead():
			return True 