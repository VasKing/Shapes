import tkinter as tk
from PIL import Image, ImageTk
import os

# Function to load and resize an image to fit within the specified size
def load_image(file_path, size):
    image = Image.open(file_path)
    image.thumbnail(size)  # Resize the image
    return ImageTk.PhotoImage(image)

# Initialize the main window
window = tk.Tk()
window.title("Tarot Reader")

# Define the size of the window
window_width = 1050
window_height = 600
window.geometry(f'{window_width}x{window_height}')

# Calculate panel widths
left_panel_width = window_width // 3
right_panel_width = window_width - left_panel_width

# Define a list of card names
card_names = ['The_Fool', 'The_Magician', 'The_High_Priestess', 'The_Empress', 'The_Emperor']
current_card_index = 0

# Function to display the card image and description based on the card name
def display_card(card_index):
    card_name = card_names[card_index]

    # Load and display the card image
    card_image_path = os.path.join('Images', f'{card_name}.png')
    card_photo = load_image(card_image_path, (left_panel_width, window_height))
    card_image_label.config(image=card_photo)
    card_image_label.image = card_photo  # Keep a reference

    # Load and display the description image
    description_image_path = os.path.join('Descriptions', f'{card_name}_description.jpg')
    description_photo = load_image(description_image_path, (right_panel_width, window_height))
    description_image_label.config(image=description_photo)
    description_image_label.image = description_photo  # Keep a reference

# Function to show the next card
def show_next_card(event=None):
    global current_card_index
    current_card_index = (current_card_index + 1) % len(card_names)
    display_card(current_card_index)

# Function to show the previous card
def show_previous_card(event=None):
    global current_card_index
    current_card_index = (current_card_index - 1) % len(card_names)
    display_card(current_card_index)

# Create the left panel for the card image
left_panel = tk.Frame(window, width=left_panel_width, height=window_height)
left_panel.pack(side='left', fill='both', expand=True)
left_panel.pack_propagate(False)

# Create the right panel for the description image
right_panel = tk.Frame(window, width=right_panel_width, height=window_height)
right_panel.pack(side='right', fill='both', expand=True)
right_panel.pack_propagate(False)

# Create labels to display the images
card_image_label = tk.Label(left_panel)
card_image_label.pack(fill='both', expand=True)

description_image_label = tk.Label(right_panel)
description_image_label.pack(fill='both', expand=True)

# Bind arrow keys to show the next/previous card
window.bind('<Right>', show_next_card)
window.bind('<Left>', show_previous_card)

# Display the first card
display_card(current_card_index)

window.mainloop()
