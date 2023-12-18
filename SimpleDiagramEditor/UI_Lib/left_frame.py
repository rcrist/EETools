import customtkinter as ctk
from UI_Lib.shape_button_frame import ShapeButtonFrame
from UI_Lib.line_button_frame import LineButtonFrame


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add left frame widgets here
        shape_button_frame = ShapeButtonFrame(self, self.canvas)
        shape_button_frame.pack(side=ctk.TOP, padx=5, pady=5)

        line_button_frame = LineButtonFrame(self, self.canvas)
        line_button_frame.pack(side=ctk.TOP, padx=5, pady=5)
