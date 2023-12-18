import customtkinter as ctk
from UI_Lib.comp_button_frame import CompButtonFrame
from UI_Lib.wire_button_frame import WireButtonFrame
from UI_Lib.ic_button_frame import ICButtonFrame


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.canvas = canvas

        self.comp_button_frame = CompButtonFrame(self, self.canvas)
        self.comp_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.wire_button_frame = WireButtonFrame(self, self.canvas)
        self.wire_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.ic_button_frame = ICButtonFrame(self, self.canvas)
        self.ic_button_frame.pack(side=ctk.TOP, padx=5, pady=5)
