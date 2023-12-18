import customtkinter as ctk
from tktooltip import ToolTip
from pathlib import Path
from PIL import Image

from Wire_Lib import AnalogWire, Node


class WireButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.wire = None
        self.wire_count = 0

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
        ToolTip(straight_wire_button, msg='Straight wire')

        segment_wire_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/segment_line.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/segment_line.png"),
                                size=(24, 24))

        segment_wire_button = ctk.CTkButton(self, text="", image=segment_wire_image, width=30,
                                        command=self.create_segment_wire)
        segment_wire_button.grid(row=1, column=1, sticky=ctk.W, padx=2, pady=2)
        ToolTip(segment_wire_button, msg='Segment wire')

        elbow_wire_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/elbow_line.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/elbow_line.png"),
                                size=(24, 24))

        elbow_wire_button = ctk.CTkButton(self, text="", image=elbow_wire_image, width=30,
                                        command=self.create_elbow_wire)
        elbow_wire_button.grid(row=1, column=2, sticky=ctk.W, padx=2, pady=2)
        ToolTip(elbow_wire_button, msg='Elbow wire')

        node_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/node.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/node.png"),
                                size=(24, 24))

        node_button = ctk.CTkButton(self, text="", image=node_image, width=30,
                                        command=self.create_node)
        node_button.grid(row=2, column=0, sticky=ctk.W, padx=2, pady=2)
        ToolTip(node_button, msg='Node')

    # Shape button handlers
    def create_straight_wire(self):
        wire = AnalogWire(self.canvas, 'straight', 0, 0, 0, 0)
        self.create_wire(wire)

    def create_segment_wire(self):
        wire = AnalogWire(self.canvas, 'segment', 0, 0, 0, 0)
        self.create_wire(wire)

    def create_elbow_wire(self):
        wire = AnalogWire(self.canvas, 'elbow', 0, 0, 0, 0)
        self.create_wire(wire)

    def create_node(self):
        node = Node(self.canvas, 100, 100)
        self.canvas.comp_list.append(node)
        self.canvas.redraw()
        self.canvas.mouse.move_mouse_bind_events()

    def create_wire(self, wire):
        self.assign_wire_name(wire)
        self.canvas.mouse.current_wire_obj = wire
        self.canvas.show_connectors()
        self.canvas.comp_list.append(wire)
        self.canvas.mouse.draw_wire_mouse_events()

    def assign_wire_name(self, wire):
        self.wire_count += 1
        wire_name = 'wire' + str(self.wire_count)
        wire.name = wire_name
        self.canvas.wire_dict[wire_name] = wire
