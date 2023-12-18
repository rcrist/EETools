import customtkinter as ctk
from pathlib import Path
from PIL import Image

from IC_Lib import IC74161, IC74273, IC28C16, SevenSegment


class ICButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add frame widgets here
        frame_name_label = ctk.CTkLabel(self, text="ICs", font=("Helvetica", 10), height=20)
        frame_name_label.grid(row=0, column=0, columnspan=3, sticky=ctk.W, padx=2, pady=2)

        ic_image = ctk.CTkImage(light_image=Image.open
                (Path(__file__).parent / "../icons/ic.png"),
               dark_image=Image.open
               (Path(__file__).parent / "../icons/ic.png"),
               size=(24, 24))

        ic_button = ctk.CTkButton(self, text="74161", image=ic_image, width=30,
                                             command=self.create_ic_74161)
        ic_button.grid(row=1, column=0, sticky=ctk.W, padx=2, pady=2)

        ic_button = ctk.CTkButton(self, text="74273", image=ic_image, width=30,
                                             command=self.create_ic_74273)
        ic_button.grid(row=2, column=0, sticky=ctk.W, padx=2, pady=2)

        ic_button = ctk.CTkButton(self, text="28C16", image=ic_image, width=30,
                                             command=self.create_ic_28C16)
        ic_button.grid(row=3, column=0, sticky=ctk.W, padx=2, pady=2)

        seven_segment_image = ctk.CTkImage(light_image=Image.open
                (Path(__file__).parent / "../icons/7-segment-display.png"),
                dark_image=Image.open
                (Path(__file__).parent / "../icons/7-segment-display.png"),
                size=(24, 24))

        seven_segment_button = ctk.CTkButton(self, text="", image=seven_segment_image, width=30,
                                  command=self.create_seven_segment)
        seven_segment_button.grid(row=4, column=0, sticky=ctk.W, padx=2, pady=2)

    def create_ic_74161(self):
        ic = IC74161(self.canvas, 100, 100)
        self.canvas.comp_list.append(ic)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    def create_ic_74273(self):
        ic = IC74273(self.canvas, 105, 100)
        self.canvas.comp_list.append(ic)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    def create_ic_28C16(self):
        ic = IC28C16(self.canvas, 100, 150)
        self.canvas.comp_list.append(ic)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    def create_seven_segment(self):
        ic = SevenSegment(self.canvas, 100, 150)
        self.canvas.comp_list.append(ic)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()
