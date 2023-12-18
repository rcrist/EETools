import customtkinter as ctk
from CTkColorPicker import *
from tktooltip import ToolTip
from PIL import Image


class ShapeAppearanceFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        self.fill_label = None
        self.border_label = None

        self.init_fill_color_control(self)
        self.init_border_color_control(self)
        self.init_border_width_control(self)

    def init_fill_color_control(self, shape_appearance_frame):
        # Fill color frame
        fill_frame = ctk.CTkFrame(shape_appearance_frame, width=150)
        fill_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        # Add fill color picker
        def ask_fill_color():
            pick_color = AskColor()  # open the color picker
            color = pick_color.get()  # get the color string
            self.fill_label.configure(fg_color=color)
            for item in self.canvas.shape_list:
                if item.is_selected:
                    item.fill_color = color
                    self.canvas.itemconfig(item.id, fill=color)

        fill_color_button = ctk.CTkButton(fill_frame, text="Fill", text_color="black", width=50,
                                          command=ask_fill_color)
        fill_color_button.pack(side=ctk.LEFT, padx=5, pady=5)
        self.fill_label = ctk.CTkLabel(fill_frame, text="", width=30, height=30, bg_color="white")
        self.fill_label.pack(side=ctk.LEFT, padx=5, pady=5)

        ToolTip(fill_color_button, msg="Fill color")

    def init_border_color_control(self, shape_appearance_frame):
        # Border color frame
        border_frame = ctk.CTkFrame(shape_appearance_frame, width=150)
        border_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        # Add border (outline) color picker
        def ask_border_color():
            pick_color = AskColor()  # open the color picker
            color = pick_color.get()  # get the color string
            self.border_label.configure(fg_color=color)
            for item in self.canvas.shape_list:
                if item.is_selected:
                    item.border_color = color
                    self.canvas.itemconfig(item.id, outline=color)

        border_color_button = ctk.CTkButton(border_frame, text="Border", text_color="black", width=50,
                                            command=ask_border_color)
        border_color_button.pack(side=ctk.LEFT, padx=10, pady=5)
        self.border_label = ctk.CTkLabel(border_frame, text="", width=30, height=30, bg_color="white")
        self.border_label.pack(side=ctk.LEFT, padx=5, pady=5)

        ToolTip(border_color_button, msg="Border color")

    def init_border_width_control(self, shape_appearance_frame):
        # Border width frame
        width_frame = ctk.CTkFrame(shape_appearance_frame, width=150)
        width_frame.configure(fg_color=("gray28", "gray28"))  # set frame color
        width_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        my_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/DiagramEditor/icons/line-width.png"),
                                dark_image=Image.open
                                ("D:/EETools/DiagramEditor/icons/line-width.png"),
                                size=(24, 24))

        image_label = ctk.CTkLabel(width_frame, image=my_image, text="", corner_radius=10)
        image_label.pack(side=ctk.LEFT)

        # Add OptionMenu to top frame
        def option_menu_callback(choice):
            for item in self.canvas.shape_list:
                if item.is_selected:
                    item.border_width = choice
                    self.canvas.itemconfig(item.id, width=choice)

        option_menu = ctk.CTkOptionMenu(width_frame, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                        width=32, command=option_menu_callback)
        option_menu.pack(side=ctk.LEFT)
        option_menu.set("3")

        ToolTip(option_menu, msg="Border width")
