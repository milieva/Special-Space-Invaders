import unittest
import logics

class TestUnit(unittest.TestCase):

    def setUp(self):
        self.unit = logics.Unit(5, (10,10))


    def test_is_dead(self):
        self.unit.health = 0
        self.assertTrue(self.unit.is_dead)

    def test_unit_move(self):
        self.unit.move((11,11))
        self.assertEqual(self.unit.coordinates, (11,11))

    def test_take_a_hit(self):
        self.unit.take_a_hit()
        self.assertEqual(self.unit.health, 4)

class TestBullet(unittest.TestCase):
    def setUp(self):
        self.bullet = logics.Bullet(1,1,(0,0))

    def test_bullet_move(self):
        self.bullet.move()
        self.assertEqual(self.bullet.coordinates, (0,30))

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = logics.Player('TEST', (0,0))

    def test_player_shoot(self):
        self.player.shoot()
        bullet = self.player.bullets[0]
        self.assertEqual(bullet.coordinates,(0, -30))

class TestMonster(unittest.TestCase):
    def setUp(self):
        self.monster = logics.Monster((0,0))

    def test_monster_shoot(self):
        self.monster.shoot()
        bullet = self.monster.bullets[0]
        self.assertEqual(bullet.coordinates, (0,0))


class TestGame(unittest.TestCase):
    def setUp(self):
        self.player = logics.Player('Test', (0,0))
        self.game = logics.Game(0, 20, self.player)

    def test_spawn_monsters(self):
        self.game.spawn_monsters([(1,1), (2,2), (3,3)])
        monster_coordinates = []
        for monster in self.game.monsters:
            monster_coordinates.append(monster.coordinates)

        self.assertEqual(monster_coordinates, [(1,1), (2,2), (3,3)])

if __name__ == '__main__':
    unittest.main()
