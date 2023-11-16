import tkinter as tk
import requests
from tkinter import messagebox, filedialog
from bs4 import BeautifulSoup
import hashlib


class WebWatermarksApp:

    def __init__(self, root):
        self.root = root
        self.url_label = tk.Label(root, text="URL:")
        self.url_entry = tk.Entry(root, width=30)

        self.generate_button = tk.Button(
            root, text="Wygeneruj i zapisz", command=self.add_watermark_and_save)

        self.info_button = tk.Button(
            root, text="Pomoc", command=self.show_help_box)

    def add_watermark_and_save(self):
        url = self.url_entry.get()

        # Make a request to the website
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Calculate the center position
            center_position = {
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'position': 'fixed',
                'opacity': '0.2',  # Adjust opacity to your preference
                'pointer-events': 'none'
            }

            # Calculate the hash of the original HTML body content
            body_content_hash = self.calculate_hash(soup.body.encode('utf-8'))

            # Add the hash to the head section as a meta tag
            hash_meta_tag = soup.new_tag(
                'meta', attrs={'name': 'body_hash', 'content': body_content_hash})
            soup.head.append(hash_meta_tag)

            # Save the modified HTML to a new file
            save_path = filedialog.asksaveasfilename(
                defaultextension=".html", filetypes=[("Pliki HTML", "*.html")])
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(str(soup.prettify()))
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}")

    def calculate_hash(self, data):
        # Calculate SHA-256 hash of the data
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
        return sha256_hash.hexdigest()

    def pack_elements(self):
        self.url_label.pack()
        self.url_entry.pack()
        self.generate_button.pack()
        self.info_button.pack()

    def show_help_box(self):
        help_info = '''
        Ukryty watermark w meta tagu HTML

        Podprogram słuzy do dodania ukrytego znaku wodnego w <meta> tagu pliku HTML
        <!> W adresie strony nalezy zawrzec przedrostek http:// lub https://

        Aby dodać ukryty znak wodny:
        1) W polu "URL:" podaj adres strony internetowej do której chcesz dodać znak wodny
        2) Kliknij w przycisk "Wygeneruj i zapisz"
        3) Wybierz miejsce oraz nazwę dla wygenerowanego pliku HTML
        '''
        messagebox.showinfo("Pomoc", help_info)
