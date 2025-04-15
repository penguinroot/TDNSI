import math
from projectile import Projectile

class MachineGunTower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100  # Portée de la tour
        self.damage = 5  # Dégâts par tir
        self.cooldown = 0
        self.level = 1  # Niveau de la tour
        self.upgrade_cost = 30  # Coût de mise à niveau

    def attack(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.range:
                projectiles.append(Projectile(self.x, self.y, enemy))
                self.cooldown = 5  # Temps de recharge plus court pour une mitrailleuse
                break

    def upgrade(self):
        if self.level < 3:  # Limiter le niveau maximum
            self.level += 1
            self.damage += 3  # Augmenter les dégâts
            self.range += 5  # Augmenter la portée
            self.upgrade_cost *= 2  # Doubler le coût de mise à niveau