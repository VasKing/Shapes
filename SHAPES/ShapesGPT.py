import tkinter as tk
from tkinter import ttk
import random
import os
import math
def draw_square():
    size = random.randint(50, min(screen_width, screen_height) // 4)
    x1, y1 = random.randint(1, screen_width-size), random.randint(1, screen_height-size)
    color = random.choice(colors)
    canvas.create_rectangle(x1, y1, x1+size, y1+size, fill=color, outline=color)

def draw_circle():
    size = random.randint(50, min(screen_width, screen_height) // 4)
    x1, y1 = random.randint(1, screen_width-size), random.randint(1, screen_height-size)
    color = random.choice(colors)
    canvas.create_oval(x1, y1, x1+size, y1+size, fill=color, outline=color)

def draw_oval():
    # Random size for the oval. Width and height will vary, creating the oval effect.
    width = random.randint(50, min(screen_width, screen_height) // 4)
    height = random.randint(50, min(screen_width, screen_height) // 4)
    x1, y1 = random.randint(1, screen_width-width), random.randint(1, screen_height-height)
    color = random.choice(colors)
    canvas.create_oval(x1, y1, x1+width, y1+height, fill=color, outline=color)

def draw_rectangle():
    width = random.randint(50, screen_width // 3)
    height = random.randint(50, screen_height // 3)
    x1, y1 = random.randint(1, screen_width-width), random.randint(1, screen_height-height)
    color = random.choice(colors)
    canvas.create_rectangle(x1, y1, x1+width, y1+height, fill=color, outline=color)

def draw_triangle():
    size = random.randint(50, min(screen_width, screen_height) // 4)
    x1, y1 = random.randint(1, screen_width-size), random.randint(1, screen_height-size)
    points = [x1, y1, x1 + size, y1, x1 + size / 2, y1 - size]
    color = random.choice(colors)
    canvas.create_polygon(points, fill=color, outline=color)

def draw_star():
    size = random.randint(50, min(screen_width, screen_height) // 4)
    x1, y1 = random.randint(1, screen_width-size), random.randint(1, screen_height-size)
    points = [
        x1 + size * 0.5, y1,
        x1 + size * 0.6, y1 + size * 0.4,
        x1 + size, y1 + size * 0.4,
        x1 + size * 0.65, y1 + size * 0.6,
        x1 + size * 0.75, y1 + size,
        x1 + size * 0.5, y1 + size * 0.75,
        x1 + size * 0.25, y1 + size,
        x1 + size * 0.35, y1 + size * 0.6,
        x1, y1 + size * 0.4,
        x1 + size * 0.4, y1 + size * 0.4
    ]
    color = random.choice(colors)
    canvas.create_polygon(points, fill=color, outline=color)

def draw_hexagon():
    side_length = random.randint(50, min(screen_width, screen_height) // 8)
    x_center, y_center = random.randint(side_length, screen_width - side_length), random.randint(side_length,
                                                                                                 screen_height - side_length)

    # Calculate the points for a hexagon
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append(x_center + side_length * math.cos(angle_rad))
        points.append(y_center + side_length * math.sin(angle_rad))

    color = random.choice(colors)
    canvas.create_polygon(points, fill=color, outline=color)


def draw_octagon():
    side_length = random.randint(50, min(screen_width, screen_height) // 8)
    x_center, y_center = random.randint(side_length, screen_width - side_length), random.randint(side_length,
                                                                                                 screen_height - side_length)

    # Calculate the points for an octagon
    points = []
    for i in range(8):
        angle_deg = 45 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append(x_center + side_length * math.cos(angle_rad))
        points.append(y_center + side_length * math.sin(angle_rad))

    color = random.choice(colors)
    canvas.create_polygon(points, fill=color, outline=color)

def clear_canvas():
    canvas.delete("all")

window = tk.Tk()
window.title("Shapes! (V.Aristotelous@2024")
window.state('zoomed')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

colors = ['Red', 'Yellow', 'Blue', 'Green', 'Orange', 'Purple', 'Black', 'Gray']
canvas = tk.Canvas(window, width=screen_width-100, height=screen_height)
canvas.pack(side='right', fill='both', expand=True)

buttons_frame = tk.Frame(window, width=100, height=screen_height)
buttons_frame.pack(side='left', fill='y')

# Assuming a standard button size, modify as needed
button_height = 75  # Height in pixels
button_width = 75  # Width in pixels, adjust based on your image aspect ratios

def create_image_button(frame, image_path, command, width, height):
    img = tk.PhotoImage(file=image_path).subsample(2, 2)  # Adjust subsample as needed to fit the button size
    button = tk.Button(frame, image=img, command=command, width=width, height=height)
    button.image = img  # Keep a reference!
    button.pack(pady=10)
    return button

image_names = ["circle", "square", "oval", "rectangle", "triangle", "star", "hexagon", "octagon"]
shape_functions = [draw_circle, draw_square, draw_oval, draw_rectangle, draw_triangle, draw_star, draw_hexagon, draw_octagon]

for name, func in zip(image_names, shape_functions):
    img_path = os.path.join("Images", f"{name}.png")
    create_image_button(buttons_frame, img_path, func, button_width, button_height)

# Clean button
clean_img_path = os.path.join("Images", "Clean.png")
create_image_button(buttons_frame, clean_img_path, clear_canvas, button_width, button_height).pack(side='bottom', pady=10)

window.mainloop()
