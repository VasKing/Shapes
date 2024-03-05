import tkinter as tk
import turtle
import random

# List of colors
colors = ["red", "yellow", "blue", "green", "orange", "purple", "black", "gray"]
current_color = "black"

# Function to choose a random color
def choose_random_color():
    global current_color
    current_color = random.choice(colors)

# Function for drawing a random filled square
def draw_random_square():
    print("Drawing a square!")
    choose_random_color()
    size = random.randint(10, 100)

    # Random Starting Position
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.color(current_color)
    turtle.shapesize(size / 10)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.left(90)
    turtle.end_fill()

# Function for drawing a random filled circle
def draw_random_circle():
    print("Drawing a circle!")
    choose_random_color()
    size = random.randint(10, 100)

    # Random Starting Position
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.color(current_color)
    turtle.circle(size)
    turtle.begin_fill()
    turtle.circle(size)
    turtle.end_fill()

# Setting up TKinter window
root = tk.Tk()
root.title("Random Shapes!")

# Frame for shape buttons
shape_frame = tk.Frame(root)
shape_frame.pack()

# Create shape buttons
tk.Button(shape_frame, text="Square", command=draw_random_square).pack()
tk.Button(shape_frame, text="Circle", command=draw_random_circle).pack()

# Canvas for the drawing area
drawing_canvas = tk.Canvas(root, bg="white")
drawing_canvas.pack()

# Setup turtle within the canvas
screen = turtle.TurtleScreen(drawing_canvas)
turtle.speed(6)  # Adjust drawing speed as desired
turtle.penup()
turtle.hideturtle()

# Force drawing window to be on top
screen.getcanvas().winfo_toplevel().attributes('-topmost', 1)

root.mainloop()
