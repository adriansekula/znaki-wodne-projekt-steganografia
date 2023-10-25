import sys
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

np.set_printoptions(threshold=sys.maxsize)


class LSB_Watermark_Password:
    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)
        self.root.title("Znak Wodny LSB z hasłem")

        self.encode_tab = ttk.Frame(self.notebook)
        self.decode_tab = ttk.Frame(self.notebook)
        self.src_filename = None
        self.src_filename_decode = None

    def Encode(self, src, message, dest, password):
        img = Image.open(src, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size // n

        message += password
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > (total_pixels * 3):
            print("ERROR: Need a larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                for q in range(0, 3):
                    if index < req_pixels:
                        array[p][q] = int(
                            bin(array[p][q])[2:9] + b_message[index], 2)
                        index += 1

            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest)
            messagebox.showinfo("Sukces", "Znak wodny dodany prawidłowo!")

    def Decode(self, src, password):
        img = Image.open(src, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size // n

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                hidden_bits += (bin(array[p][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i+8]
                       for i in range(0, len(hidden_bits), 8)]

        message = ""
        hiddenmessage = ""
        for i in range(len(hidden_bits)):
            x = len(password)
            if message[-x:] == password:
                break
            else:
                message += chr(int(hidden_bits[i], 2))
                message = f'{message}'
                hiddenmessage = message
        if password in message:
            messagebox.showinfo(
                "Success", f"Ukryty znak wodny:\n {hiddenmessage[:-x]}")
        else:
            messagebox.showerror(
                "Błąd", "Podałeś złe hasło, spróbuj ponownie.")

    def pack_elements(self):
        def get_src_file():
            self.src_filename = filedialog.askopenfilename(title="Wybierz plik zrodlowy",
                                                           filetypes=[('image files', '.png')])

        def get_src_file_decode():
            self.src_filename_decode = filedialog.askopenfilename(title="Wybierz plik zrodlowy",
                                                                  filetypes=[('image files', '.png')])

        self.notebook.add(self.encode_tab, text="Dodaj znak wodny")
        self.notebook.add(self.decode_tab, text="Odczytaj znak wodny")
        self.notebook.pack()

        tk.Label(self.encode_tab, text="Obraz źródłowy (PNG)").grid(row=0)
        tk.Label(self.encode_tab, text="Znak wodny do ukrycia").grid(row=1)
        tk.Label(self.encode_tab, text="Hasło").grid(row=2)

        src_entry_encode = tk.Button(
            self.encode_tab, text="Wybierz", command=get_src_file)
        src_entry_encode.grid(row=0, column=1)

        message_entry_encode = tk.Entry(self.encode_tab)
        message_entry_encode.grid(row=1, column=1)
        password_entry_encode = tk.Entry(self.encode_tab, show="*")
        password_entry_encode.grid(row=2, column=1)

        def encode():
            dest = filedialog.asksaveasfilename()
            message = message_entry_encode.get()
            password = password_entry_encode.get()
            self.Encode(self.src_filename, message, dest, password)

        tk.Button(self.encode_tab, text="Zakoduj",
                  command=encode).grid(row=4, column=1)

        tk.Label(self.decode_tab, text="Obraz źródłowy (PNG)").grid(row=0)
        tk.Label(self.decode_tab, text="Hasło").grid(row=1)

        src_entry_decode = tk.Button(self.decode_tab, text="Wybierz",
                                     command=get_src_file_decode)
        src_entry_decode.grid(row=0, column=1)
        password_entry_decode = tk.Entry(self.decode_tab, show="*")
        password_entry_decode.grid(row=1, column=1)

        def decode():
            password = password_entry_decode.get()
            self.Decode(self.src_filename_decode, password)

        tk.Button(self.decode_tab, text="Zdekoduj",
                  command=decode).grid(row=2, column=1)
