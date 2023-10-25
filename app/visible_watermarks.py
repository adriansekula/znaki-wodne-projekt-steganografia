import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np


class VisibleWatermarks():

    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)
        self.text_tab = tk.Frame(self.notebook)
        self.image_tab = tk.Frame(self.notebook)
        self.notebook.add(self.text_tab, text='Text Watermark')
        self.notebook.add(self.image_tab, text='Image Watermark')

        self.watermark_entry_label = tk.Label(
            self.text_tab, text="Tekst znaku wodnego:")
        self.watermark_entry = tk.Entry(self.text_tab, width=30)
        self.watermark_color_label = tk.Label(
            self.text_tab, text="Kolor znaku wodnego:")
        self.watermark_color_var = tk.StringVar()
        self.black_color_radio = tk.Radiobutton(
            self.text_tab, text="Czarny", variable=self.watermark_color_var, value="black")
        self.red_color_radio = tk.Radiobutton(
            self.text_tab, text="Czerwony", variable=self.watermark_color_var, value="red")
        self.blue_color_radio = tk.Radiobutton(
            self.text_tab, text="Niebieski", variable=self.watermark_color_var, value="blue")

        self.watermark_position_label_text = tk.Label(
            self.text_tab, text="Położenie znaku wodnego:")
        self.watermark_position_label_image = tk.Label(
            self.image_tab, text="Położenie znaku wodnego:")

        self.watermark_position_var_text = tk.StringVar()
        self.watermark_position_var_image = tk.StringVar()

        self.top_left_radio_text = tk.Radiobutton(
            self.text_tab, text="Góra lewo", variable=self.watermark_position_var_text, value="Góra lewo")
        self.top_left_radio_image = tk.Radiobutton(
            self.image_tab, text="Góra lewo", variable=self.watermark_position_var_image, value="Góra lewo")

        self.top_right_radio_text = tk.Radiobutton(
            self.text_tab, text="Góra prawo", variable=self.watermark_position_var_text, value="Góra prawo")
        self.top_right_radio_image = tk.Radiobutton(
            self.image_tab, text="Góra prawo", variable=self.watermark_position_var_image, value="Góra prawo")

        self.bottom_left_radio_text = tk.Radiobutton(
            self.text_tab, text="Dół lewo", variable=self.watermark_position_var_text, value="Dół lewo")
        self.bottom_left_radio_image = tk.Radiobutton(
            self.image_tab, text="Dół lewo", variable=self.watermark_position_var_image, value="Dół lewo")

        self.bottom_right_radio_text = tk.Radiobutton(
            self.text_tab, text="Dół prawo", variable=self.watermark_position_var_text, value="Dół prawo")
        self.bottom_right_radio_image = tk.Radiobutton(
            self.image_tab, text="Dół prawo", variable=self.watermark_position_var_image, value="Dół prawo")

        self.watermark_size_label = tk.Label(
            self.text_tab, text="Rozmiar znaku wodnego:")
        self.watermark_size_entry = tk.Entry(self.text_tab, width=5)

        self.generate_and_save_button_text = tk.Button(
            self.text_tab, text="Generuj i zapisz obraz z znakiem wodnym", command=self.add_watermark_and_save)
        self.generate_and_save_button_image = tk.Button(
            self.image_tab, text="Generuj i zapisz obraz z znakiem wodnym", command=self.add_watermark_and_save)

    def pack_elements(self):
        # Pack the notebook with two tabs
        self.notebook.pack()

        # Label pola tekstowego na znak wodny
        self.watermark_entry_label.pack()

        # Pole tekstowe na znak wodny
        self.watermark_entry.pack()

        # Przyciski wyboru koloru znaku wodnego
        self.watermark_color_label.pack()
        self.watermark_color_var.set("black")
        self.black_color_radio.pack()
        self.red_color_radio.pack()
        self.blue_color_radio.pack()

        # Przyciski wyboru położenia znaku wodnego
        self.watermark_position_label_image.pack()
        self.watermark_position_label_text.pack()
        self.watermark_position_var_text.set("Góra lewo")
        self.watermark_position_var_image.set("Góra lewo")
        self.top_right_radio_text.pack()
        self.top_right_radio_image.pack()
        self.top_left_radio_text.pack()
        self.top_left_radio_image.pack()
        self.bottom_left_radio_text.pack()
        self.bottom_left_radio_image.pack()
        self.bottom_right_radio_text.pack()
        self.bottom_right_radio_image.pack()

        # Pole wprowadzenia rozmiaru znaku wodnego
        self.watermark_size_label.pack()
        self.watermark_size_entry.pack()
        self.watermark_size_entry.insert(0, "24")

        # Przycisk do generowania i zapisywania obrazu z znakiem wodnym
        self.generate_and_save_button_text.pack()
        self.generate_and_save_button_image.pack()

    def add_watermark_and_save(self):

        file_path = filedialog.askopenfilename()
        source_image = Image.open(file_path)

        # Skopiuj obraz źródłowy, aby nie modyfikować oryginału
        marked_image = source_image.copy()
        marked_image.convert('RGBA')
        width_marked_image, height_marked_image = marked_image.size

        # Check which tab is currently selected
        selected_tab = self.notebook.select()

        if selected_tab == self.text_tab._w:
            # Ustaw parametry znaku wodnego
            watermark_position = self.watermark_position_var_text.get()

            # Wprowadź tekst znaku wodnego
            watermark_text = self.watermark_entry.get()

            # Ustaw parametry znaku wodnego
            watermark_color = self.watermark_color_var.get()
            watermark_position = self.watermark_position_var_text.get()
            watermark_size = int(self.watermark_size_entry.get())

            # Skopiuj obraz źródłowy, aby nie modyfikować oryginału
            marked_image = source_image.copy()

            # Przygotuj obraz do rysowania na nim znaku wodnego
            draw = ImageDraw.Draw(marked_image)
            # Use truetype to specify the font size
            font = ImageFont.truetype("/Library/Fonts/Arial", watermark_size)

            # Określ pozycję znaku wodnego
            if watermark_position == "Góra lewo":
                position = (10, 10)
            elif watermark_position == "Góra prawo":
                position = (source_image.width - watermark_size - 10, 10)
            elif watermark_position == "Dół lewo":
                position = (10, source_image.height - watermark_size - 10)
            else:
                position = (source_image.width - watermark_size - 10,
                            source_image.height - watermark_size - 10)

            # Rysuj znak wodny
            draw.text(position, watermark_text,
                      fill=watermark_color, font=font)

            # Zapisz obraz z dodanym znakiem wodnym
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("Pliki PNG", "*.png")])
            if save_path:
                marked_image.save(save_path)

        elif selected_tab == self.image_tab._w:

            # Ustaw parametry znaku wodnego
            watermark_position = self.watermark_position_var_image.get()

            # Open dialog to choose watermark image
            watermark_image_path = filedialog.askopenfilename()
            watermark_image = Image.open(watermark_image_path).convert('RGBA')
            width_watermark_image, height_watermark_image = watermark_image.size
            watermark_image_aspect_ratio = width_watermark_image / height_watermark_image
            watermark_image = watermark_image.resize((int(width_marked_image / 10),
                                                      int((width_marked_image / 10) / watermark_image_aspect_ratio)))

            # Określ pozycję znaku wodnego
            if watermark_position == "Góra lewo":
                position = (10, 10)
            elif watermark_position == "Góra prawo":
                position = (source_image.width -
                            watermark_image.width - 10, 10)
            elif watermark_position == "Dół lewo":
                position = (10, source_image.height -
                            watermark_image.height - 10)
            else:
                position = (source_image.width - watermark_image.width - 10,
                            source_image.height - watermark_image.height - 10)

            # Add the watermark image
            marked_image.paste(watermark_image, position,
                               mask=watermark_image)
            # Zapisz obraz z dodanym znakiem wodnym
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("Pliki PNG", "*.png")])
            if save_path:
                marked_image.save(save_path)
