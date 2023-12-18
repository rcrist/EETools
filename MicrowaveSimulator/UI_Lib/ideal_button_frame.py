import customtkinter as ctk
from tktooltip import ToolTip
from pathlib import Path
from PIL import Image

from Comp_Lib import Inport, Outport


class IdealButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.button_id = None

        self.button_list = [("inport", "../icons/inport.png"),
                            ("outport", "../icons/outport.png")]

        self.init_frame_widgets()

    def init_frame_widgets(self):
        frame_name_label = ctk.CTkLabel(self, text="Ideal", font=("Helvetica", 10), height=20)
        frame_name_label.grid(row=0, column=0, columnspan=3, sticky=ctk.W, padx=2, pady=2)

        row_num, col_num = 1, 0
        for button in self.button_list:
            a_image = ctk.CTkImage(light_image=Image.open
                                    (Path(__file__).parent / button[1]),
                                    dark_image=Image.open
                                    (Path(__file__).parent / button[1]),
                                    size=(24, 24))
            self.button_id = ctk.CTkButton(self, text="", image=a_image, width=30,
                                           command=lambda a_name=button[0]:self.create_events(a_name))
            self.button_id.grid(row=row_num, column=col_num, sticky=ctk.W, padx=2, pady=2)
            ToolTip(self.button_id, msg=button[0])
            row_num, col_num = self.update_grid_numbers(row_num, col_num)

    def create_events(self, name):
        comp = None
        if name == "inport":
            comp = Inport(self.canvas, 100, 100)
        elif name == "outport":
            comp = Outport(self.canvas, 100, 100)
        self.canvas.comp_list.append(comp)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    @staticmethod
    def update_grid_numbers(row, column):
        column += 1
        if column > 2:
            column = 0
            row += 1
        return row, column
