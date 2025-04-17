import tkinter as tk
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
        # Création d'un canvas pour dessiner l'arbre technologique
        canvas = tk.Canvas(self.window, width=400, height=200)
        canvas.pack()
        
        # Dessin des technologies
        for tech_name, tech in self.tower.technologies.items():
            x, y = 100, 100  # Position à adapter
            
            # Couleur en fonction de l'état
            if not tech["unlocked"]:
                color = "red"
            else:
                color = "blue"
            
            # Création d'un bouton pour la technologie
            btn = tk.Button(canvas, 
                           text=tech["name"],
                           bg=color,
                           command=lambda name=tech_name: self.try_unlock_technology(name))
            btn.place(x=x, y=y)


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
