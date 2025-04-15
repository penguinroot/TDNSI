from enemy import Enemy

class EnemyFast(Enemy):
    def __init__(self, path):
        super().__init__(path, sprites_folder="sprites/enemyfast", speed=3, max_health=25, animation_delay=5)