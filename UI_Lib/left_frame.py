import customtkinter as ctk


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add left frame widgets here
        rect_button = ctk.CTkButton(self,
                                    text="Rectangle",
                                    command=self.create_rectangle)
        rect_button.pack(side=ctk.TOP, padx=5, pady=5)

        line_button = ctk.CTkButton(self,
                                    text="Straight Line",
                                    command=self.create_line)
        line_button.pack(side=ctk.TOP, padx=5, pady=5)

        segment_line_button = ctk.CTkButton(self,
                                    text="Segment Line",
                                    command=self.create_segment_line)
        segment_line_button.pack(side=ctk.TOP, padx=5, pady=5)

        elbow_line_button = ctk.CTkButton(self,
                                    text="Elbow Line",
                                    command=self.create_elbow_line)
        elbow_line_button.pack(side=ctk.TOP, padx=5, pady=5)

    def create_rectangle(self):
        self.canvas.mouse.mode = None
        self.canvas.draw_shapes()
        self.canvas.mouse.current_shape = "rectangle"
        self.canvas.mouse.draw_bind_mouse_events()

    def create_line(self):
        self.canvas.mouse.mode = "line_draw"
        self.canvas.draw_shapes()
        self.canvas.mouse.current_shape = "line"
        self.canvas.mouse.draw_bind_mouse_events()

    def create_segment_line(self):
        self.canvas.mouse.mode = "line_draw"
        self.canvas.draw_shapes()
        self.canvas.mouse.current_shape = "segment"
        self.canvas.mouse.draw_bind_mouse_events()

    def create_elbow_line(self):
        self.canvas.mouse.mode = "line_draw"
        self.canvas.draw_shapes()
        self.canvas.mouse.current_shape = "elbow"
        self.canvas.mouse.draw_bind_mouse_events()
