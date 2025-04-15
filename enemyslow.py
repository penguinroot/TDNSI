from enemy import Enemy

class EnemySlow(Enemy):
    def __init__(self, path):
        super().__init__(path, sprites_folder="sprites/enemytank", speed=1.5, max_health=100, animation_delay=15)