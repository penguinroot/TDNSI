import math
from projectile import MortarProjectile  # Importer le nouveau projectile

class MortarTower:
    """
    Classe représentant une tour de mortier dans le jeu.
    La tour de mortier est une version améliorée de la tour de base, avec une portée et des dégâts accrus.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 150  # Portée de la tour
        self.damage = 5  # Dégâts de la tour
        self.cooldown = 0
        self.level = 1  # Niveau de la tour
        self.upgrade_cost = {
            'damage': 60,
            'range': 50,
            'speed': 40
        }
    def attack(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.range:
                projectiles.append(MortarProjectile(self.x, self.y, enemy, enemies))  # Passer la liste des ennemis
                self.cooldown = 20  # Temps de recharge
                break
    def upgrade(self):
        if self.level < 3:  # Limiter le niveau maximum
            self.level += 1
            self.damage += 5  # Augmenter les dégâts
            self.range += 10  # Augmenter la portée
            self.upgrade_cost *= 2  # Doubler le coût de mise à niveau