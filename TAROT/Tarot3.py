import tkinter as tk
from PIL import Image, ImageTk

# Function to load and resize an image to fit within the specified size
def load_image(file_path, size):
    # Open the image file
    image = Image.open(file_path)
    # Resize the image to the specified size while keeping the aspect ratio
    image.thumbnail((size, size))
    # Return the PhotoImage object
    return ImageTk.PhotoImage(image)

# Initialize the main window
window = tk.Tk()
window.title("Tarot Reader")

# Set the window size to your preference
window_width = 1300
window_height = 800
window.geometry(f'{window_width}x{window_height}')

# Function to display the card image and description based on the card name
def display_card(card_name):
    # Calculate the panel widths based on the window size
    left_panel_width = window_width // 3  # Give 1/3 of the window to the card image
    right_panel_width = window_width - left_panel_width  # And the rest to the description

    # Load and display the card image
    card_image_file = f'Images/{card_name}.png'
    card_photo = load_image(card_image_file, left_panel_width)
    card_image_label.config(image=card_photo)
    card_image_label.image = card_photo  # Keep a reference to the image

    # Load and display the description image
    description_image_file = f'Descriptions/{card_name}_description.jpg'
    description_photo = load_image(description_image_file, right_panel_width)
    description_image_label.config(image=description_photo)
    description_image_label.image = description_photo  # Keep a reference

# Left panel for card image
left_panel = tk.Frame(window)
left_panel.pack(side='left', fill='both', expand=True)

# Right panel for description image
right_panel = tk.Frame(window)
right_panel.pack(side='right', fill='both', expand=True)

# Label to display the card image
card_image_label = tk.Label(left_panel)
card_image_label.pack(fill='both', expand=True)

# Label to display the description image
description_image_label = tk.Label(right_panel)
description_image_label.pack(fill='both', expand=True)

# Display the first card by default
display_card('The_Fool')

window.mainloop()
