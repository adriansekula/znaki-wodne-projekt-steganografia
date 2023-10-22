import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def draw_watermark():
    global img, img_path
    # Open a new window for drawing the watermark
    draw_win = tk.Toplevel(root)
    draw_win.title("Draw Watermark")
    # Display the image in the new window
    draw_img = ImageTk.PhotoImage(img)
    draw_label = tk.Label(draw_win, image=draw_img)
    draw_label.image = draw_img
    draw_label.pack()
    # Add a button to save the watermark
    save_button = tk.Button(draw_win, text="Save Watermark", command=save_watermark)
    save_button.pack()

def open_image():
    global img_path, img
    img_path = filedialog.askopenfilename()
    img = Image.open(img_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

def save_watermark():
    global img, img_path
    # Convert the image to a numpy array
    img_np = np.array(img)
    # TODO: Implement the least significant bit method to embed the watermark into the image
    # Save the image with the watermark
    img_np.save(img_path)
    # Close the drawing window
    draw_win.destroy()



root = tk.Tk()
root.title("Image Watermarker")

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

draw_button = tk.Button(root, text="Draw Watermark", command=draw_watermark)
draw_button.pack()

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

root.mainloop()