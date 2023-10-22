import tkinter as tk
from visible_watermarks import VisibleWatermarks


class ZnakiWodneAplikacja():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x200")
        self.root.title("Znaki wodne - Widoczne i niewidoczne")
        self.launch_button = tk.Button(
            self.root, text="Znak wodny widoczny", command=self.visible_watermarks)
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


if __name__ == "__main__":
    app = ZnakiWodneAplikacja()
    app.launch_app()