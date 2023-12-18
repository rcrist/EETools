import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class HelpFrame(ctk.CTkFrame):
    def __init__(self, window, parent, canvas):
        super().__init__(parent)
        self.window = window
        self.parent = parent
        self.canvas = canvas

        self.menu_on = False

        self.menu_frame = ctk.CTkFrame(window, height=100, bg_color="white")

        about_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/about.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/about.png"),
                                size=(24, 24))

        about_button = ctk.CTkButton(self.menu_frame, text="About", image=about_image, width=30,
                                     command=self.show_about_dialog)
        about_button.pack(side=ctk.TOP,padx=5, pady=5)

        my_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/help.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/help.png"),
                                size=(24, 24))

        button = ctk.CTkButton(self, text="", image=my_image, width=30, command=self.show_menu)
        button.pack(side=ctk.LEFT, padx=5, pady=10)

    def show_menu(self):
        if not self.menu_on:
            menu_pos_x = self.canvas.winfo_width()
            self.menu_frame.place(x=menu_pos_x + 50, y=60)
            self.menu_frame.tkraise()
            self.menu_on = True
        else:
            self.menu_frame.place_forget()
            self.menu_on = False

    @staticmethod
    def show_about_dialog():
        messagebox.showinfo("About Digital Simulator", "RF/Microwave Simulator v0.1\n" +
                            "Author: Rick A. Crist\n" + "2023")
