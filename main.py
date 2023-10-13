import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

def add_watermark_and_save():
    # Wczytaj obraz źródłowy
    file_path = filedialog.askopenfilename()
    source_image = Image.open(file_path)

    # Wprowadź tekst znaku wodnego
    watermark_text = watermark_entry.get()

    # Ustaw parametry znaku wodnego
    watermark_color = watermark_color_var.get()
    watermark_position = watermark_position_var.get()
    watermark_size = int(watermark_size_entry.get())

    # Skopiuj obraz źródłowy, aby nie modyfikować oryginału
    marked_image = source_image.copy()

    # Przygotuj obraz do rysowania na nim znaku wodnego
    draw = ImageDraw.Draw(marked_image)
    font = ImageFont.load_default()  # Domyślna czcionka

    # Określ pozycję znaku wodnego
    if watermark_position == "Góra lewo":
        position = (10, 10)
    elif watermark_position == "Góra prawo":
        position = (source_image.width - watermark_size - 10, 10)
    elif watermark_position == "Dół lewo":
        position = (10, source_image.height - watermark_size - 10)
    else:
        position = (source_image.width - watermark_size - 10, source_image.height - watermark_size - 10)

    # Rysuj znak wodny
    draw.text(position, watermark_text, fill=watermark_color, font=font)

    # Zapisz obraz z dodanym znakiem wodnym
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Pliki JPEG", "*.jpg")])
    if save_path:
        marked_image.save(save_path)

    # Wyświetl obraz w interfejsie
    marked_photo = ImageTk.PhotoImage(marked_image)
    marked_image_label.config(image=marked_photo)
    marked_image_label.photo = marked_photo

# Tworzenie głównego okna
root = tk.Tk()
root.title("Aplikacja do dodawania znaku wodnego")

# Przycisk wyboru obrazu źródłowego
# select_image_button = tk.Button(root, text="Wybierz obraz źródłowy", command=add_watermark)
# select_image_button.pack()

# Pole tekstowe na znak wodny
watermark_entry = tk.Entry(root, width=30)
watermark_entry.pack()
watermark_entry.insert(0, "Znak wodny")

# Przyciski wyboru koloru znaku wodnego
watermark_color_label = tk.Label(root, text="Kolor znaku wodnego:")
watermark_color_label.pack()

watermark_color_var = tk.StringVar()
watermark_color_var.set("black")

black_color_radio = tk.Radiobutton(root, text="Czarny", variable=watermark_color_var, value="black")
black_color_radio.pack()
red_color_radio = tk.Radiobutton(root, text="Czerwony", variable=watermark_color_var, value="red")
red_color_radio.pack()
blue_color_radio = tk.Radiobutton(root, text="Niebieski", variable=watermark_color_var, value="blue")
blue_color_radio.pack()

# Przyciski wyboru położenia znaku wodnego
watermark_position_label = tk.Label(root, text="Położenie znaku wodnego:")
watermark_position_label.pack()

watermark_position_var = tk.StringVar()
watermark_position_var.set("Góra lewo")

top_left_radio = tk.Radiobutton(root, text="Góra lewo", variable=watermark_position_var, value="Góra lewo")
top_left_radio.pack()
top_right_radio = tk.Radiobutton(root, text="Góra prawo", variable=watermark_position_var, value="Góra prawo")
top_right_radio.pack()
bottom_left_radio = tk.Radiobutton(root, text="Dół lewo", variable=watermark_position_var, value="Dół lewo")
bottom_left_radio.pack()
bottom_right_radio = tk.Radiobutton(root, text="Dół prawo", variable=watermark_position_var, value="Dół prawo")
bottom_right_radio.pack()

# Pole wprowadzenia rozmiaru znaku wodnego
watermark_size_label = tk.Label(root, text="Rozmiar znaku wodnego:")
watermark_size_label.pack()

watermark_size_entry = tk.Entry(root, width=5)
watermark_size_entry.pack()
watermark_size_entry.insert(0, "24")

# Przycisk do generowania i zapisywania obrazu z znakiem wodnym
generate_and_save_button = tk.Button(root, text="Generuj i zapisz obraz z znakiem wodnym", command=add_watermark_and_save)
generate_and_save_button.pack()

# Wyświetlanie obrazu
marked_image_label = tk.Label(root)
marked_image_label.pack()

root.mainloop()