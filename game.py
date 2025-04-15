import tkinter as tk
import json
from enemy import Enemy
from enemyfast import Enemy as EnemyFast  # Import EnemyFast
from enemyslow import Enemy as EnemySlow  # Import EnemyTank
from tower import Tower
from projectile import Projectile, MortarProjectile  # Import MortarProjectile
from PIL import Image, ImageTk  # Importer Pillow pour le redimensionnement
from MortarTower import MortarTower  # Ajoutez cette ligne pour importer MortarTower
from tkinter import simpledialog  # Import simpledialog correctly


class TowerDefense:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="white")
        self.canvas.pack()

        # Charger les données de niveau
        with open("d:/TDNSI/path.json", "r") as file:
            level_data = json.load(file)
        level_info = level_data.get("levelS", {})
        self.path = level_info.get("path", [])
        self.tower_positions = level_info.get("tower_positions", [])  # Charger les positions des tours
        print(f"Path: {self.path}")
        print(f"Tower Positions: {self.tower_positions}")
        
        if not self.path:
            print("No path found in level data.")
            return
        self.draw_path()
        self.draw_tower_positions()  # Dessiner les positions des tours

        # Liste des ennemis
        self.enemies = []

        # Liste des tours
        self.towers = []
        self.canvas.bind("<Button-1>", self.place_tower)

        # Liste des projectiles
        self.projectiles = []

        # Variables pour les vagues
        self.wave_number = 1
        self.wave_delay = 5000  # 5 secondes entre les vagues
        self.wave_in_progress = False

        self.tower_health = 100
        self.health_text = self.canvas.create_text(50, 20, text=f"Health: {self.tower_health}", font=("Arial", 16), fill="black")

        self.money = 200
        self.money_text = self.canvas.create_text(750, 20, text=f"Money: {self.money}", font=("Arial", 16), fill="black")

                # Dans TowerDefense.__init__() :
        self.selected_tower = None
        self.canvas.tag_bind("tower", "<Button-1>", self.select_tower)


        self.waves_data = self.load_waves_data()

        self.effects = []  # New list to store explosion effects

        # Lancer la première vague
        self.start_wave()

        # Mettre à jour le jeu
        self.update_game()
        # Nouvelle méthode de sélection
    def select_tower(self, event):
        x, y = event.x, event.y
        for tower in self.towers:
            if (abs(x - tower.x) < 15) and (abs(y - tower.y) < 15):
                self.selected_tower = tower
                self.show_upgrade_dialog(tower)
                break

    def draw_path(self):
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=20)

    def draw_tower_positions(self):
        for pos in self.tower_positions:
            x, y = pos
            self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="green", width=2)  # Cercle vert pour indiquer la position

    def load_waves_data(self):
        with open("d:/TDNSI/waves.json", "r") as file:
            return json.load(file)
    def spawn_enemy(self):
        current_wave_key = f"wave{self.wave_number}"
        wave_data = self.waves_data.get(current_wave_key)
        if not wave_data:
            print(f"No data found for {current_wave_key}")
            self.wave_in_progress = False
            return

        if not hasattr(self, "spawn_queue"):
            self.spawn_queue = []
            for enemy_info in wave_data["enemies"]:
                enemy_type = enemy_info["type"]
                count = enemy_info["count"]
                self.spawn_queue.extend([enemy_type] * count)
            print(f"Spawn queue for {current_wave_key}: {self.spawn_queue}")

        if self.spawn_queue:
            enemy_type = self.spawn_queue.pop(0)
            if enemy_type == "enemy":
                self.enemies.append(Enemy(self.path, sprites_folder="sprites/enemy", speed=2, max_health=50, animation_delay=8))
            elif enemy_type == "enemyslow":
                self.enemies.append(EnemySlow(self.path, sprites_folder="sprites/enemyslow", speed=1.5, max_health=100, animation_delay=15))
            elif enemy_type == "enemyfast":
                self.enemies.append(EnemyFast(self.path, sprites_folder="sprites/enemyfast", speed=3, max_health=25, animation_delay=5))
            self.root.after(1000, self.spawn_enemy)
        else:
            del self.spawn_queue
            self.wave_in_progress = False
            print(f"Wave {self.wave_number} spawn completed")
    def start_wave(self):
        print(f"Starting wave {self.wave_number}")
        self.wave_in_progress = True
        self.spawn_enemy()

    def next_wave(self):
        if self.wave_in_progress:
            return
        print(f"Preparing wave {self.wave_number + 1}")
        self.wave_number += 1
        self.start_wave()

    def move_enemies(self):
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += 10
                self.canvas.itemconfig(self.money_text, text=f"Money: {self.money}")
            elif enemy.has_reached_end():
                self.enemies.remove(enemy)
                self.tower_health -= 10
                self.canvas.itemconfig(self.health_text, text=f"Health: {self.tower_health}")
                if self.tower_health <= 0:
                    print("Game Over!")
                    self.canvas.create_text(400, 300, text="Game Over", font=("Arial", 32), fill="red")

    def draw_enemies(self):
        self.canvas.delete("enemy")
        for enemy in self.enemies:
            # Dessiner l'ennemi
            img = self.canvas.create_image(enemy.x, enemy.y, image=enemy.get_image(), tags="enemy")  
            # Déterminer la couleur en fonction du type
            if isinstance(enemy, EnemyFast):  # Adapter les imports
                color = "orange"
            elif isinstance(enemy, EnemySlow):
                color = "blue"
            else:
                color = "red"
            # Calculer la largeur de la barre
            health_width = 30 * (enemy.health / enemy.max_health)
            # Dessiner la barre de vie
            self.canvas.create_rectangle(
                enemy.x - 15, enemy.y - 25,  # Position
                enemy.x - 15 + health_width, enemy.y - 20,
                fill=color, outline="black",
                tags=("enemy", "healthbar")  # Tag pour suppression facile
            )
    def place_tower(self, event):
        # Vérification de la position valide
        tolerance = 20
        valid_pos = None
        for pos in self.tower_positions:
            tx, ty = pos
            if abs(event.x - tx) <= tolerance and abs(event.y - ty) <= tolerance:
                valid_pos = pos
                break

        if valid_pos:
            # Vérifier si la position est libre
            if any(tower.x == valid_pos[0] and tower.y == valid_pos[1] for tower in self.towers):
                print("Une tour existe déjà ici")
                return

            # Créer la fenêtre de sélection
            dialog = tk.Toplevel(self.root)
            dialog.title("Choisir une tour")
            dialog.attributes('-topmost', True)
            dialog.grab_set()

            # Charger les images (à adapter à vos fichiers)
            try:
                icon1 = ImageTk.PhotoImage(Image.open("tower1_icon.png").resize((64, 64)))
                icon2 = ImageTk.PhotoImage(Image.open("MortarTower_icon.png").resize((64, 64)))
            except FileNotFoundError:
                icon1 = tk.PhotoImage()  # Image vide si fichier manquant
                icon2 = tk.PhotoImage()

            # Configuration du style
            btn_frame = tk.Frame(dialog, padx=20, pady=20)
            btn_frame.pack()

            # Bouton Tour Basique
            tower1_btn = tk.Button(
                btn_frame,
                image=icon1,
                text=f"Basique\n20$",
                compound='top',
                font=('Arial', 10, 'bold'),
                fg='blue' if self.money >= 20 else 'gray',
                command=lambda: self.create_tower(valid_pos, "tower1", dialog)
            )
            tower1_btn.image = icon1  # Garder une référence
            tower1_btn.grid(row=0, column=0, padx=10)
            if self.money < 20:
                tower1_btn.config(state='disabled')

            # Bouton Tour Mortier
            MortarTower_btn = tk.Button(
                btn_frame,
                image=icon2,
                text=f"Mortier\n30$",
                compound='top',
                font=('Arial', 10, 'bold'),
                fg='red' if self.money >= 30 else 'gray',
                command=lambda: self.create_tower(valid_pos, "MortarTower", dialog)
            )
            MortarTower_btn.image = icon2  # Garder une référence
            MortarTower_btn.grid(row=0, column=1, padx=10)
            if self.money < 30:
                MortarTower_btn.config(state='disabled')
            # Centrage de la fenêtre
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = self.root.winfo_screenwidth() // 2 - width // 2
            y = self.root.winfo_screenheight() // 2 - height // 2
            dialog.geometry(f"+{x}+{y}")

        else:
            print("Position invalide pour une tour")

    def create_tower(self, position, tower_type, dialog):
        dialog.destroy()
        x, y = position
        
        if tower_type == "tower1" and self.money >= 20:
            new_tower = Tower(x, y)
            self.towers.append(new_tower)
            # Stocker l'ID du canvas dans l'objet Tower
            new_tower.canvas_id = self.canvas.create_rectangle(x-15, y-15, x+15, y+15, fill="blue", tags="tower")
            self.money -= 20
        elif tower_type == "MortarTower" and self.money >= 30:
            new_tower = MortarTower(x, y)
            self.towers.append(new_tower)
            new_tower.canvas_id = self.canvas.create_rectangle(x-15, y-15, x+15, y+15, fill="red", tags="tower")
            self.money -= 30
    def upgrade_tower(self, tower, dialog):
        if self.money >= tower.upgrade_cost:
            tower.upgrade()
            self.money -= tower.upgrade_cost
            self.canvas.itemconfig(self.money_text, text=f"Money: {self.money}")
            dialog.destroy()
            # Mettre à jour l'affichage de la tour
            self.update_tower_display(tower)
        else:
            print("Fonds insuffisants")

    def update_tower_display(self, tower):
        colors = {1: "blue", 2: "purple", 3: "gold"}
        # Utiliser l'ID canvas spécifique à la tour
        self.canvas.itemconfigure(tower.canvas_id, fill=colors.get(tower.level, "blue"))
    def attack_enemies(self):
        for tower in self.towers:
            tower.attack(self.enemies, self.projectiles)

    def show_damage_effect(self, x, y):
        # Ajouter un effet visuel pour les dégâts
        damage_effect = self.canvas.create_oval(x-10, y-10, x+10, y+10, outline="red", width=2, tags="effect")
        self.root.after(200, lambda: self.canvas.delete(damage_effect))

    def show_explosion_effect(self, x, y, radius):
        # Add explosion effect to the effects list
        self.effects.append({
            'type': 'explosion',
            'x': x,
            'y': y,
            'radius': radius,
            'max_radius': 50,  # Ensure max_radius is initialized
            'lifetime': 10
        })

    def move_projectiles(self):
        for projectile in self.projectiles[:]:
            if projectile.target not in self.enemies:
                self.projectiles.remove(projectile)
                continue
            impact_position = projectile.move()
            if impact_position:
                if isinstance(projectile, MortarProjectile):
                    self.show_explosion_effect(*impact_position, radius=50)  # Adjust radius as needed
                else:
                    self.show_damage_effect(*impact_position)
                self.projectiles.remove(projectile)

    def draw_projectiles(self):
        self.canvas.delete("projectile")
        for projectile in self.projectiles:
            self.canvas.create_oval(projectile.x-5, projectile.y-5, projectile.x+5, projectile.y+5, fill="black", tags="projectile")
    def show_upgrade_dialog(self, tower):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Upgrade Tour Niveau {tower.level}")
        
        tk.Label(dialog, text=f"Coût: {tower.upgrade_cost}$").pack(padx=20, pady=5)
        
        btn = tk.Button(
            dialog,
            text="Améliorer",
            command=lambda: self.upgrade_tower(tower, dialog),
            state='normal' if self.money >= tower.upgrade_cost else 'disabled'
        )
        btn.pack(pady=10)
        
        # Positionnement au centre
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = self.root.winfo_screenwidth()//2 - width//2
        y = self.root.winfo_screenheight()//2 - height//2
        dialog.geometry(f"+{x}+{y}")
    def update_game(self):
        self.canvas.delete("healthbar")
        self.move_enemies()
        self.attack_enemies()
        self.move_projectiles()
        self.draw_enemies()
        self.draw_projectiles()

        # Vérifier si on peut passer à la vague suivante
        if not self.enemies and not self.wave_in_progress:
            self.root.after(self.wave_delay, self.next_wave)

        # Remplacer la partie explosion par :
        for effect in self.effects[:]:
            if effect['type'] == 'explosion':
                effect['radius'] = min(effect['radius'] + 5, 50)
                effect['lifetime'] -= 1
                if effect['lifetime'] <= 0:
                    self.effects.remove(effect)
        # Dessiner les explosions
        self.canvas.delete("explosion")
        for effect in self.effects:
            if effect['type'] == 'explosion':
                x = effect['x']
                y = effect['y']
                radius = effect['radius']
                self.canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    outline="orange", width=3, tags="explosion"
                )

        self.root.after(50, self.update_game)