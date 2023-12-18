import customtkinter as ctk
from CTkColorPicker import *


class TopFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add top frame widgets here
        self.fill_color_button = ctk.CTkButton(self,
                                   text="Fill Color",
                                   command=self.set_fill_color)
        self.fill_color_button.pack(side=ctk.LEFT, padx=3, pady=3)

        self.border_color_button = ctk.CTkButton(self,
                                   text="Border Color",
                                   command=self.set_border_color)
        self.border_color_button.pack(side=ctk.LEFT, padx=3, pady=3)

        border_width_optionmenu = ctk.CTkOptionMenu(self,
               values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
               command=self.set_border_width)
        border_width_optionmenu.pack(side=ctk.LEFT, padx=3, pady=3)
        border_width_optionmenu.set("3")

        self.switch_var = ctk.StringVar(value="on")
        switch = ctk.CTkSwitch(self, text="Grid Visible",
                               command=self.grid_visibility,
                               variable=self.switch_var,
                               onvalue="on", offvalue="off")
        switch.pack(side=ctk.LEFT, padx=3, pady=3)

        grid_size_optionmenu = ctk.CTkOptionMenu(self,
               values=["5", "10", "15", "20", "25", "40", "50",
                       "60", "70", "80", "90", "100"],
               command=self.set_grid_size)
        grid_size_optionmenu.pack(side=ctk.LEFT, padx=3, pady=3)
        grid_size_optionmenu.set("10")

    def set_fill_color(self):
        if self.canvas.mouse.selected_obj:
            pick_color = AskColor()  # open the color picker
            color = pick_color.get()  # get the color string
            self.canvas.mouse.selected_obj.fill_color = color
            self.canvas.draw_shapes()

    def set_border_color(self):
        if self.canvas.mouse.selected_obj:
            pick_color = AskColor()  # open the color picker
            color = pick_color.get()  # get the color string
            self.canvas.mouse.selected_obj.border_color = color
            self.canvas.draw_shapes()

    def set_border_width(self, choice):
        if self.canvas.mouse.selected_obj:
            self.canvas.mouse.selected_obj.border_width = choice
            self.canvas.draw_shapes()

    def grid_visibility(self):
        if self.switch_var.get() == "on":
            self.canvas.grid.grid_visible = True
        elif self.switch_var.get() == "off":
            self.canvas.grid.grid_visible = False
        self.canvas.draw_shapes()

    def set_grid_size(self, choice):
        self.canvas.grid.grid_size = int(choice)
        self.canvas.draw_shapes()
