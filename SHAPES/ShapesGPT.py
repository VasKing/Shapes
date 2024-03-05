import tkinter as tk
from tkinter import ttk
import random

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

# Screen size and colors
screen_width, screen_height = 1920, 1080  # Placeholder values, will be updated dynamically
colors = ['Red', 'Yellow', 'Blue', 'Green', 'Orange', 'Purple', 'Black', 'Gray']

window = tk.Tk()
window.title("Shapes Drawing Program")

# Dynamically adjusting to the screen size
window.state('zoomed')  # This makes the window maximized
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Create a canvas for drawing
canvas = tk.Canvas(window, width=screen_width-100, height=screen_height)
canvas.pack(side='right', fill='both', expand=True)

# Shape buttons with icons (using simple text for demonstration)
buttons_frame = tk.Frame(window, width=100, height=screen_height)
buttons_frame.pack(side='left', fill='y')

# Adding buttons for each shape
shapes = [('□', draw_square), ('○', draw_circle), ('⬭', draw_oval), ('▭', draw_rectangle)]
for shape_text, shape_func in shapes:
    button = ttk.Button(buttons_frame, text=shape_text, command=shape_func)
    button.pack(pady=20)

window.mainloop()

