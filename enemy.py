from PIL import Image, ImageTk
import math

class Enemy:
    def __init__(self, path, sprites_folder, speed, max_health, animation_delay, width=64, height=64):
        self.x = path[0][0]
        self.y = path[0][1]
        self.speed = speed
        self.max_health = max_health
        self.health = self.max_health
        self.path = path
        self.path_index = 0
        self.canvas_id = None
        self.sprites = self.load_sprites(sprites_folder)
        self.current_direction = 'down'
        self.current_frame = 0
        self.animation_delay = animation_delay
        self.frame_counter = 0

    def load_sprites(self, folder):
        SCALE_FACTOR = 0.25
        directions = ['up', 'right', 'down', 'left']
        sprites = {}
        for direction in directions:
            try:
                img = Image.open(f"{folder}/walk_{direction}.png")
                frames = []
                for i in range(4):
                    cropped = img.crop((i * 120, 0, (i + 1) * 120, 120))
                    resized = cropped.resize((int(120 * SCALE_FACTOR), int(120 * SCALE_FACTOR)), Image.LANCZOS)
                    frames.append(ImageTk.PhotoImage(resized))
                sprites[direction] = frames
            except Exception as e:
                size = int(120 * SCALE_FACTOR)
                placeholder = Image.new('RGBA', (size, size), (255, 0, 0, 255))
                sprites[direction] = [ImageTk.PhotoImage(placeholder)] * 4
        return sprites

    def move(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            dx = target[0] - self.x
            dy = target[1] - self.y

            if abs(dx) > abs(dy):
                self.current_direction = 'right' if dx > 0 else 'left'
            else:
                self.current_direction = 'down' if dy > 0 else 'up'

            angle = math.atan2(dy, dx)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

            self.frame_counter += 1
            if self.frame_counter >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % 4
                self.frame_counter = 0

            if math.hypot(dx, dy) < 5:
                self.path_index += 1

    def get_image(self):
        frames = self.sprites[self.current_direction]
        return frames[self.current_frame % len(frames)]

    def has_reached_end(self):
        return self.path_index == len(self.path) - 1