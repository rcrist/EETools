import customtkinter as ctk
from pathlib import Path
from PIL import Image

from Wire_Lib import Wire, SegmentWire


class WireButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.wire = None

        # Add frame widgets here
        frame_name_label = ctk.CTkLabel(self, text="Wires", font=("Helvetica", 10), height=20)
        frame_name_label.grid(row=0, column=0, columnspan=3, sticky=ctk.W, padx=2, pady=2)

        straight_wire_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/straight_line.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/straight_line.png"),
                                size=(24, 24))

        straight_wire_button = ctk.CTkButton(self, text="", image=straight_wire_image, width=30,
                                        command=self.create_straight_wire)
        straight_wire_button.grid(row=1, column=0, sticky=ctk.W, padx=2, pady=2)

        segment_wire_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/segment_line.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/segment_line.png"),
                                size=(24, 24))

        segment_wire_button = ctk.CTkButton(self, text="", image=segment_wire_image, width=30,
                                        command=self.create_segment_wire)
        segment_wire_button.grid(row=1, column=1, sticky=ctk.W, padx=2, pady=2)

    # Shape button handlers
    def create_straight_wire(self):
        wire = Wire(self.canvas, 0, 0, 0, 0)
        self.canvas.comp_list.append(wire)
        self.canvas.mouse.current_wire_obj = wire
        self.canvas.show_connectors()
        self.canvas.mouse.draw_wire_mouse_events()

    def create_segment_wire(self):
        wire = SegmentWire(self.canvas, 0, 0, 0, 0)
        self.canvas.comp_list.append(wire)
        self.canvas.mouse.current_wire_obj = wire
        self.canvas.show_connectors()
        self.canvas.mouse.draw_wire_mouse_events()
