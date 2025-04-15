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
        super().__init__(x, y, target)
        self.enemies = enemies  # Stocker la liste des ennemis
        self.damage = 20  # Dégâts maximum

    def move(self):
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
        explosion_radius_sq = 50**2  # Rayon d'explosion au carré
        for enemy in list(self.enemies):  # Copie explicite
            dx = self.x - enemy.x
            dy = self.y - enemy.y
            distance_sq = dx**2 + dy**2  # Distance au carré

            if distance_sq <= explosion_radius_sq:
                # Calculer la distance réelle
                distance = math.sqrt(distance_sq)
                # Calculer les dégâts en fonction de la distance
                # Dégâts maximum à l'impact, réduction linéaire jusqu'à zéro à la limite du rayon
                damage = max(0, self.damage * (1 - (distance / 50)))  # 50 est le rayon d'explosion
                enemy.health -= damage  # Appliquer les dégâts
                print(f"Enemy at ({enemy.x}, {enemy.y}) took {damage} damage. Remaining health: {enemy.health}")
                print(f"Distance: {distance}, Damage: {damage}")
                if enemy.health <= 0:
                    self.enemies.remove(enemy)  # Supprimer l'ennemi si sa santé est à zéro