import customtkinter as ctk
from tktooltip import ToolTip
from pathlib import Path
from PIL import Image

from Comp_Lib import AndGate, OrGate, NotGate, NandGate, NorGate, XorGate, XnorGate
from Comp_Lib import LED, Switch, Text, Clock


class CompButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.button_id = None

        self.button_list = [("and_gate", "../icons/and.png"),
                            ("or_gate", "../icons/or.png"),
                            ("not_gate", "../icons/not.png"),
                            ("nand_gate", "../icons/nand.png"),
                            ("nor_gate", "../icons/nor.png"),
                            ("xor_gate", "../icons/xor.png"),
                            ("xnor_gate", "../icons/xnor.png"),
                            ("led", "../icons/led.png"),
                            ("switch", "../icons/switch.png"),
                            ("text", "../icons/text.png"),
                            ("clock", "../icons/clock.png")]

        self.init_frame_widgets()

    def init_frame_widgets(self):
        frame_name_label = ctk.CTkLabel(self, text="Components", font=("Helvetica", 10), height=20)
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
        gate = None
        if name == "and_gate":
            gate = AndGate(self.canvas, 100, 100)
        elif name == "or_gate":
            gate = OrGate(self.canvas, 100, 100)
        elif name == "not_gate":
            gate = NotGate(self.canvas, 100, 100)
        elif name == "nand_gate":
            gate = NandGate(self.canvas, 100, 100)
        elif name == "nor_gate":
            gate = NorGate(self.canvas, 100, 100)
        elif name == "xor_gate":
            gate = XorGate(self.canvas, 100, 100)
        elif name == "xnor_gate":
            gate = XnorGate(self.canvas, 100, 100)
        elif name == "led":
            gate = LED(self.canvas, 100, 100)
        elif name == "switch":
            gate = Switch(self.canvas, 100, 100)
        elif name == "text":
            gate = Text(self.canvas, 100, 100)
        elif name == "clock":
            gate = Clock(self.canvas, 100, 100)
        self.canvas.comp_list.append(gate)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    @staticmethod
    def update_grid_numbers(row, column):
        column += 1
        if column > 2:
            column = 0
            row += 1
        return row, column
