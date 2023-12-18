import customtkinter as ctk
from tktooltip import ToolTip
from PIL import Image


class ShapeButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add left frame widgets here
        frame_name_label = ctk.CTkLabel(self, text="Shapes", font=("Helvetica", 10), height=20)
        frame_name_label.grid(row=0, column=0, columnspan=3, sticky=ctk.W, padx=2, pady=2)

        rect_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/rectangle.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/rectangle.png"),
                                size=(24, 24))
        rect_button = ctk.CTkButton(self, text="", image=rect_image, width=30, command=self.create_rect)
        rect_button.grid(row=1, column=0, sticky=ctk.W, padx=2, pady=2)
        ToolTip(rect_button, msg="Rectangle")

        oval_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/oval.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/oval.png"),
                                size=(24, 24))
        oval_button = ctk.CTkButton(self, text="", image=oval_image, width=30, command=self.create_oval)
        oval_button.grid(row=1, column=1, sticky=ctk.W, padx=2, pady=2)
        ToolTip(oval_button, msg="Oval")

        tri_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/triangle.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/triangle.png"),
                                size=(24, 24))
        tri_button = ctk.CTkButton(self, text="", image=tri_image, width=30, command=self.create_tri)
        tri_button.grid(row=1, column=2, sticky=ctk.W, padx=2, pady=2)
        ToolTip(tri_button, msg="Triangle")

        text_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/text.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/text.png"),
                                size=(24, 24))
        text_button = ctk.CTkButton(self, text="", image=text_image, width=30, command=self.create_text)
        text_button.grid(row=2, column=0, sticky=ctk.W, padx=2, pady=2)
        ToolTip(text_button, msg="Text")

        pic_image = ctk.CTkImage(light_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/picture.png"),
                                dark_image=Image.open
                                ("D:/EETools/SimpleDiagramEditor/icons/picture.png"),
                                size=(24, 24))
        pic_button = ctk.CTkButton(self, text="", image=pic_image, width=30, command=self.create_picture)
        pic_button.grid(row=2, column=1, sticky=ctk.W, padx=2, pady=2)
        ToolTip(pic_button, msg="Image")

    # Shape button handlers
    def create_rect(self):
        self.canvas.mouse.current_shape = "rectangle"
        self.hide_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing Rectangle"
        self.parent.parent.bottom_frame.update()

    def create_oval(self):
        self.canvas.mouse.current_shape = "oval"
        self.hide_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing Oval"
        self.parent.parent.bottom_frame.update()

    def create_tri(self):
        self.canvas.mouse.current_shape = "tri"
        self.hide_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing Triangle"
        self.parent.parent.bottom_frame.update()

    def create_text(self):
        self.canvas.mouse.current_shape = "text"
        self.hide_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing Text"
        self.parent.parent.bottom_frame.update()

    def create_picture(self):
        self.canvas.mouse.current_shape = "pic"
        self.hide_connectors()
        self.canvas.mouse.draw_bind_mouse_events()
        self.parent.parent.bottom_frame.text = "Drawing Picture"
        self.parent.parent.bottom_frame.update()

    def hide_connectors(self):
        for s in self.canvas.shape_list:
            s.is_drawing = False
        self.canvas.redraw_shapes()
