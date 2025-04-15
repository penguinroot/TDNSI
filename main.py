import tkinter as tk
from game import TowerDefense

root = tk.Tk()
root.attributes('-fullscreen', True)  # Enable fullscreen mode
game = TowerDefense(root)
root.mainloop()
