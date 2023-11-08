import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from mutagen.id3 import ID3, TXXX
from shutil import copy2
import os


class MP3_Watermarker:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Watermark")
        self.notebook = tk.ttk.Notebook(self.root)
        self.notebook.pack(pady=10)

        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Dodaj znak wodny')

        self.label_tab1 = tk.Label(self.tab1, text="Tekst znaku wodnego:")

        self.watermark = tk.StringVar()
        self.entry_tab1 = tk.Entry(self.tab1, textvariable=self.watermark)

        self.button_tab1 = tk.Button(
            self.tab1, text="Wybierz plik i dodaj znak wodny", command=self.add_watermark_tab1)

        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Odczytaj znak wodny')

        self.button_tab2 = tk.Button(self.tab2, text="Wybierz plik i odczytaj znak wodny",
                                     command=self.read_watermark_tab2)

    def pack_elements(self):
        self.label_tab1.pack()
        self.entry_tab1.pack()
        self.button_tab1.pack()
        self.button_tab2.pack()

    def open_file_tab1(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Pliki MP3", "*.mp3")])
        return filename

    def open_file_tab2(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Pliki MP3", "*.mp3")])
        return filename

    def add_watermark_tab1(self):
        filename = self.open_file_tab1()

        if filename:
            original_file = filename
            original_file_copy = original_file + "_original"
            copy2(original_file, original_file_copy)

            audio = ID3(original_file)
            if "TXXX:Watermark" in audio:
                audio["TXXX:Watermark"].text = [self.watermark.get()]
            else:
                audio["TXXX:Watermark"] = TXXX(
                    encoding=3, text=self.watermark.get())
            audio.save()

            watermarked_file = original_file[:-4] + "_watermarked.mp3"
            os.rename(original_file, watermarked_file)
            os.rename(original_file_copy, original_file)

    def read_watermark_tab2(self):
        filename = self.open_file_tab2()
        if filename:
            audio = ID3(filename)
            watermark = audio.getall("TXXX")
            if watermark:
                messagebox.showinfo("Znak wodny", watermark[0].text[0])
            else:
                messagebox.showinfo(
                    "Znak wodny", "Nie znaleziono znaku wodnego!")
