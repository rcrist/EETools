import customtkinter as ctk
from tkinter import filedialog as fd
import json
from PIL import Image

from Shape_Lib import Rectangle, Oval, Triangle, Text, Picture
from Shape_Lib import StraightLine, SegmentLine, ElbowLine


class FileMenuFrame(ctk.CTkFrame):
    def __init__(self, window, parent, canvas):
        super().__init__(parent)
        self.canvas = canvas
        self.obj_type_dict = {'rectangle': Rectangle,
                              'oval': Oval,
                              'triangle': Triangle,
                              'text': Text,
                              'straight': StraightLine,
                              'segment': SegmentLine,
                              'elbow': ElbowLine,
                              'picture': Picture}

        self.menu_on = False

        self.menu_frame = ctk.CTkFrame(window, height=100, bg_color="white")

        new_btn = ctk.CTkButton(self.menu_frame, text="New", width=150, command=self.new_diagram)
        new_btn.pack(pady=5)

        open_btn = ctk.CTkButton(self.menu_frame, text="Open", width=150, command=self.load_diagram)
        open_btn.pack(pady=5)

        save_btn = ctk.CTkButton(self.menu_frame, text="Save", width=150, command=self.save_diagram)
        save_btn.pack(pady=5)

        exit_btn = ctk.CTkButton(self.menu_frame, text="Exit", width=150, command=window.destroy)
        exit_btn.pack(pady=5)

        my_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/DiagramEditor/icons/hamburger_menu.png"),
                                dark_image=Image.open
                                ("D:/EETools/DiagramEditor/icons/hamburger_menu.png"),
                                size=(24, 24))

        button = ctk.CTkButton(self, text="", image=my_image, width=30, command=self.show_menu)
        button.pack(side=ctk.LEFT, padx=5, pady=10)

    def new_diagram(self):
        self.save_diagram()
        self.canvas.delete("all")
        self.canvas.shape_list = []

    def load_diagram(self):
        try:
            filetypes = (('json files', '*.json'), ('All files', '*.*'))
            f = fd.askopenfilename(filetypes=filetypes, initialdir="./")
            with open(f) as file:
                obj_dict = json.load(file)
                for obj_type, attributes in obj_dict.items():
                    obj = self.obj_type_dict[obj_type.split()[0]](self.canvas, attributes[0], attributes[1],
                                                                  attributes[2], attributes[3])
                    self.canvas.shape_list.append(obj)
                self.canvas.redraw_shapes()

        except FileNotFoundError:
            with open('untitled.canvas', 'w') as _file:
                pass
            self.canvas.shape_list = []

    def save_diagram(self):
        filetypes = (('json files', '*.json'), ('All files', '*.*'))
        f = fd.asksaveasfilename(filetypes=filetypes, initialdir="./")
        with open(f, 'w') as file:
            obj_dict = {f'{obj.type} {id}': (obj.x1, obj.y1, obj.x2, obj.y2) for id, obj in
                        enumerate(self.canvas.shape_list)}
            json.dump(obj_dict, file)

    def show_menu(self):
        if not self.menu_on:
            self.menu_frame.place(x=15, y=60)
            self.menu_frame.tkraise()
            self.menu_on = True
        else:
            self.menu_frame.place_forget()
            self.menu_on = False
