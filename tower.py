import math
from projectile import Projectile  # Import the Projectile class

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 10
        self.cooldown = 0
        self.level = 1  # Niveau de la tour
        self.technologies = self.load_technologies()  # Technologies débloquables
        self.experience = 0  # Expérience de la tour
        self.points = 10  # Points pour débloquer des technologies
        self.canvas_id = None  # ID du canvas pour le rendu
        
    def load_technologies(self):
        """
        Charge les technologies disponibles pour cette tour.
        Retourne un dictionnaire avec les technologies débloquables.
        """
        return {
            "base_attack": {
                "name": "Attaque de Base",
                "cost": 10,
                "dependencies": [],
                "effects": {
                    "damage": 1,
                    "description": "Augmente les dégâts de base"
                },
                "max_level": 5,
                "level": 0,
                "unlocked": True
            },
            "rapid_fire": {
                "name": "Tir Rapide",
                "cost": 20,
                "dependencies": ["base_attack"],
                "effects": {
                    "speed": 0.2,
                    "description": "Augmente la vitesse de tir"
                },
                "max_level": 3,
                "level": 0,
                "unlocked": False
            }
        }
        
    def gain_experience(self, amount):
        """
        Ajoute de l'expérience à la tour.
        Convertit l'expérience en points tant qu'elle dépasse 100.
        """
        self.experience += amount
        while self.experience >= 100:
            self.points += 1
            self.experience -= 100
            
    def unlock_technology(self, tech_name):
        """
        Débloque une technologie si possible.
        """
        tech = self.technologies[tech_name]
        if not tech["unlocked"]:
            if self.can_unlock(tech):
                if self.points >= tech["cost"]:
                    tech["unlocked"] = True
                    self.points -= tech["cost"]
                    self.apply_effects(tech)
                    
    def can_unlock(self, tech):
        """
        Vérifie si toutes les dépendances d'une technologie sont débloquées.
        """
        for dependency in tech.get("dependencies", []):
            if not self.technologies[dependency]["unlocked"]:
                return False
        return True
        
    def upgrade_technology(self, tech_name):
        """
        Améliore une technologie si possible.
        """
        tech = self.technologies[tech_name]
        if tech["level"] < tech["max_level"]:
            cost = tech["cost"] * (tech["level"] + 1)
            if self.points >= cost:
                tech["level"] += 1
                self.points -= cost
                self.apply_effects(tech)
                
    def apply_effects(self, tech):
        """
        Applique les effets d'une technologie à la tour.
        """
        if "damage" in tech["effects"]:
            self.damage += tech["effects"]["damage"]
        if "speed" in tech["effects"]:
            self.cooldown = max(1, self.cooldown - tech["effects"]["speed"])
        if "range" in tech["effects"]:
            self.range += tech["effects"]["range"]
            

    def attack(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.range:
                projectiles.append(Projectile(self.x, self.y, enemy, tower=self))  # Ajoutez tower=self
                self.cooldown = 20  # Temps de recharge
                break
                
    def upgrade(self):
        """
        Méthode de mise à niveau générale de la tour.
        """
        if self.level < 10:  # Niveau maximum
            self.level += 1
            self.damage += 5
            self.range += 10
            print(f"Tour améliorée au niveau {self.level}")