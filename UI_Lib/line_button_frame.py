import customtkinter as ctk
from tktooltip import ToolTip
from PIL import Image


class LineButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add left frame widgets here
        frame_name_label = ctk.CTkLabel(self, text="Lines", font=("Helvetica", 10), height=20)
        frame_name_label.grid(row=0, column=0, columnspan=3, sticky=ctk.W, padx=2, pady=2)

        straight_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/line.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/line.png"),
                                size=(24, 24))
        straight_button = ctk.CTkButton(self, text="", image=straight_image, width=30,
                                        command=self.create_straight_line)
        straight_button.grid(row=1, column=0, sticky=ctk.W, padx=2, pady=2)
        ToolTip(straight_button, msg="Straight Line")

        segment_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/segment_line.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/segment_line.png"),
                                size=(24, 24))
        segment_button = ctk.CTkButton(self, text="", image=segment_image, width=30,
                                        command=self.create_segment_line)
        segment_button.grid(row=1, column=1, sticky=ctk.W, padx=2, pady=2)
        ToolTip(segment_button, msg="Segment Line")

        elbow_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/elbow.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/elbow.png"),
                                size=(24, 24))
        elbow_button = ctk.CTkButton(self, text="", image=elbow_image, width=30,
                                        command=self.create_elbow_line)
        elbow_button.grid(row=1, column=2, sticky=ctk.W, padx=2, pady=2)
        ToolTip(elbow_button, msg="Elbow Line")

    # Shape button handlers
    def create_straight_line(self):
        self.canvas.mouse.current_shape = "straight"
        self.show_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing straight line"
        self.parent.parent.bottom_frame.update()

    def create_segment_line(self):
        self.canvas.mouse.current_shape = "segment"
        self.show_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing segment line"
        self.parent.parent.bottom_frame.update()

    def create_elbow_line(self):
        self.canvas.mouse.current_shape = "elbow"
        self.show_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing elbow line"
        self.parent.parent.bottom_frame.update()


    def show_connectors(self):
        for s in self.canvas.shape_list:
            s.is_drawing = True
        self.canvas.redraw_shapes()
