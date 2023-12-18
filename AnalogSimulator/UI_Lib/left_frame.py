import customtkinter as ctk
from UI_Lib.lump_button_frame import LumpButtonFrame
from UI_Lib.sources_button_frame import SourcesButtonFrame
from UI_Lib.active_button_frame import ActiveButtonFrame
from UI_Lib.wire_button_frame import WireButtonFrame


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.canvas = canvas

        self.comp_button_frame = LumpButtonFrame(self, self.canvas)
        self.comp_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.sources_button_frame = SourcesButtonFrame(self, self.canvas)
        self.sources_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.active_button_frame = ActiveButtonFrame(self, self.canvas)
        self.active_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        self.wire_button_frame = WireButtonFrame(self, self.canvas)
        self.wire_button_frame.pack(side=ctk.TOP, padx=5, pady=5)
