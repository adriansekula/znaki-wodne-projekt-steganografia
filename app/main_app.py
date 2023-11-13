import tkinter as tk
from visible_watermarks import VisibleWatermarks
from LSB_password_gui import LSB_Watermark_Password
from mp3_watermarker_tags import MP3_Watermarker


class ZnakiWodneAplikacja():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x200")
        self.root.title("Znaki wodne - Widoczne i Niewidoczne")

        self.title_label = tk.Label(
            self.root, text="Wybierz jedną z ponizszych metod dodawania znaku wodnego:")
        self.title_label.pack()

        self.launch_button = tk.Button(
            self.root, text="Znak wodny widoczny (tekst/obraz)", command=self.visible_watermarks)
        self.launch_button.pack()

        self.launch_button = tk.Button(
            self.root, text="Znak wodny ukryty - LSB z hasłem", command=self.lsb_watermark_password)
        self.launch_button.pack()

        self.launch_button = tk.Button(
            self.root, text="Ukryty znak wodny w tagu pliku MP3", command=self.mp3_watermarker)
        self.launch_button.pack()

    def launch_app(self):
        self.root.mainloop()

    def visible_watermarks(self):
        # Create new window
        newWindow = tk.Toplevel(self.root)
        newWindow.grab_set()  # This line prevents interaction with the main window

        # Move new window to be on top of the parent window
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        newWindow.geometry("+%d+%d" % (x, y))

        app = VisibleWatermarks(newWindow)
        app.pack_elements()

    def lsb_watermark_password(self):
        newWindow = tk.Toplevel(self.root)
        newWindow.grab_set()

        x = self.root.winfo_x()
        y = self.root.winfo_y()
        newWindow.geometry("+%d+%d" % (x, y))

        app = LSB_Watermark_Password(newWindow)
        app.pack_elements()

    def mp3_watermarker(self):
        newWindow = tk.Toplevel(self.root)
        newWindow.grab_set()

        x = self.root.winfo_x()
        y = self.root.winfo_y()
        newWindow.geometry("+%d+%d" % (x, y))

        app = MP3_Watermarker(newWindow)
        app.pack_elements()


if __name__ == "__main__":
    app = ZnakiWodneAplikacja()
    app.launch_app()
