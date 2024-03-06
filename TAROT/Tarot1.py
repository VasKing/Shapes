import tkinter as tk
from PIL import Image, ImageTk
import os
import glob

# Load all card images from the 'Images' directory
def load_card_images(image_folder='Images'):
    image_files = glob.glob(os.path.join(image_folder, '*.png'))
    images = []
    for file in image_files:
        image = Image.open(file)
        photo = ImageTk.PhotoImage(image)
        images.append(photo)
    return images

# Display the next card in the list
def show_next_card(event=None):
    global current_card_index, card_images, card_label
    current_card_index = (current_card_index + 1) % len(card_images)  # Cycle through the cards
    card_label.config(image=card_images[current_card_index])  # Update the label to show the next card

# Initialize the main window
window = tk.Tk()
window.title("Tarot Card Viewer")

# Load card images
card_images = load_card_images()
current_card_index = 0  # Start with the first card

# Setup a label to display card images
card_label = tk.Label(window, image=card_images[current_card_index])
card_label.pack()

# Bind the right arrow key to the show_next_card function
window.bind('<Right>', show_next_card)

window.mainloop()
