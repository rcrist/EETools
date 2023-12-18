import customtkinter as ctk
from UI_Lib.lump_button_frame import LumpButtonFrame
from UI_Lib.ideal_button_frame import IdealButtonFrame
from UI_Lib.wire_button_frame import WireButtonFrame


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.canvas = canvas

        self.comp_button_frame = LumpButtonFrame(self, self.canvas)
        self.comp_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.ideal_button_frame = IdealButtonFrame(self, self.canvas)
        self.ideal_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.wire_button_frame = WireButtonFrame(self, self.canvas)
        self.wire_button_frame.pack(side=ctk.TOP, padx=5, pady=5)
