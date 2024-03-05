import tkinter as tk
from tkinter import ttk
import random
import os
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

# Load images and create buttons
image_names = ["circle", "square", "oval", "rectangle"]  # Add the rest of your shape names here
shape_functions = [draw_circle, draw_square, draw_oval, draw_rectangle]  # Add the rest of your drawing functions here

for name, func in zip(image_names, shape_functions):
    img_path = os.path.join("Images", f"{name}.png")
    img = tk.PhotoImage(file=img_path)
    button = tk.Button(buttons_frame, image=img, command=func)
    button.image = img  # Keep a reference!
    button.pack(pady=10)

window.mainloop()

