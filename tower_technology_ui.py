import tkinter as tk
from collections import defaultdict
class TowerTechnologyUI:
    def __init__(self, root, tower):
        self.root = root
        self.tower = tower
        self.window = tk.Toplevel(self.root)
        self.window.title(f"Technologies - Tour {id(tower)}")
        self.window.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        # Affichage des technologies
        self.display_technologies()
        
        # Affichage des points
        self.points_label = tk.Label(self.window, text=f"Points : {tower.points}")
        self.points_label.pack()
        
    def display_technologies(self):
        canvas = tk.Canvas(self.window, width=800, height=600)
        canvas.pack()
        
        # Calcul des profondeurs et des couches
        depth_cache = {}
        layers = defaultdict(list)
        for tech_name in self.tower.technologies:
            deps = self.tower.technologies[tech_name].get("dependencies", [])
            if not deps:
                depth = 0
            else:
                depth = 1 + max(depth_cache[dep] for dep in deps)
            depth_cache[tech_name] = depth
            layers[depth].append(tech_name)
        
        button_positions = {}
        x_spacing = 160  # Espacement horizontal entre les nœuds
        y_spacing = 100  # Espacement vertical entre les couches
        
        # Organisation des nœuds par couche
        max_depth = max(layers.keys(), default=0)
        for depth in sorted(layers.keys()):
            techs = layers[depth]
            desired_x = {}
            
            # Calcul des positions désirées
            for tech in techs:
                deps = self.tower.technologies[tech].get("dependencies", [])
                if deps:
                    dep_x = [button_positions[dep][0] for dep in deps]
                    desired_x[tech] = sum(dep_x) / len(dep_x)
                else:
                    desired_x[tech] = 400  # Centré si racine
            
            # Tri par position désirée
            sorted_techs = sorted(techs, key=lambda x: desired_x[x])
            
            # Ajustement des positions pour éviter les chevauchements
            x_positions = []
            current_x = None
            for tech in sorted_techs:
                desired = desired_x[tech]
                if current_x is None:
                    current_x = desired - (x_spacing * (len(sorted_techs)-1))/2
                else:
                    current_x = max(current_x + x_spacing, desired)
                x_positions.append(current_x)
            
            # Centrage de la couche
            min_x = min(x_positions)
            max_x = max(x_positions)
            offset = (800 - (max_x - min_x)) / 2 - min_x
            x_positions = [x + offset for x in x_positions]
            
            # Enregistrement des positions
            y = 100 + depth * y_spacing
            for tech, x in zip(sorted_techs, x_positions):
                button_positions[tech] = (x, y)
        
        # Création des boutons
        for tech, (x, y) in button_positions.items():
            color = "blue" if self.tower.technologies[tech]["unlocked"] else "red"
            btn = tk.Button(canvas, text=tech, bg=color,
                        command=lambda t=tech: self.try_unlock_technology(t))
            canvas.create_window(x, y, window=btn, width=100, height=30)
        
        # Dessin des liens
        for tech in button_positions:
            deps = self.tower.technologies[tech].get("dependencies", [])
            for dep in deps:
                if dep in button_positions:
                    x1, y1 = button_positions[dep]
                    x2, y2 = button_positions[tech]
                    canvas.create_line(x1, y1+15, x2, y2-15, arrow=tk.LAST, smooth=True)


    def try_unlock_technology(self, tech_name):
        tech = self.tower.technologies[tech_name]
        
        if tech["unlocked"]:
            unlocked_label = tk.Label(self.window, text="Technologie déjà débloquée", fg="orange")
            unlocked_label.pack()
            self.window.after(1000, unlocked_label.destroy)  # Supprime le message après 1 seconde
            return
        
        if not self.tower.can_unlock(tech):
            print("Dépendances non satisfaites")
            return
        
        if self.tower.points >= tech["cost"]:
            self.tower.unlock_technology(tech_name)
            self.points_label.config(text=f"Points : {self.tower.points}")
            self.update_technology_display(tech_name)
        else:
            insufficient_label = tk.Label(self.window, text="Points insuffisants", fg="red")
            insufficient_label.pack()
            self.window.after(1000, insufficient_label.destroy)  # Supprime le message après 2 secondes

    def update_technology_display(self, tech_name):
        # Détruit tous les widgets de la fenêtre et réaffiche tout
        for widget in self.window.winfo_children():
            widget.destroy()
        self.display_technologies()
        self.points_label = tk.Label(self.window, text=f"Points : {self.tower.points}")
        self.points_label.pack()
