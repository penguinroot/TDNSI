import math
from projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 10
        self.cooldown = 0
        self.level = 1  # Niveau de la tour
        self.upgrade_cost = 20  # Coût de mise à niveau

    def attack(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.range:
                projectiles.append(Projectile(self.x, self.y, enemy))
                self.cooldown = 20
                break
    def upgrade(self):  # <-- Méthode absente
        if self.level < 10:
            self.level += 1
            self.damage += 5
            self.range += 10
            self.upgrade_cost *= 2
