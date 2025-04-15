import math

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 5:  # Collision
            self.target.health -= 10
            if self.target.health <= 0:
                return (self.x, self.y)  # Retourner la position de l'impact
            return (self.x, self.y)

        else:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
        return None

import math

class MortarProjectile(Projectile):
    def __init__(self, x, y, target, enemies):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.enemies = enemies  # Stocker la liste des ennemis

    def move(self):
        # Logique pour se déplacer vers la cible
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 5:  # Collision
            self.explode()  # Appeler la méthode d'explosion
            return (self.x, self.y)  # Retourner la position de l'impact

        else:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
        return None

    def explode(self):
        explosion_radius_sq = 50**2  # Éviter le sqrt
        for enemy in list(self.enemies):  # Copie explicite
            dx = self.x - enemy.x
            dy = self.y - enemy.y
            if dx**2 + dy**2 <= explosion_radius_sq:
                enemy.health -= 10  # Ne pas supprimer l'ennemi ici