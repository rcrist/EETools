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

        oval_button = ctk.CTkButton(self,
                                    text="Oval",
                                    command=self.create_oval)
        oval_button.pack(side=ctk.TOP, padx=5, pady=5)

        tri_button = ctk.CTkButton(self,
                                    text="Triangle",
                                    command=self.create_triangle)
        tri_button.pack(side=ctk.TOP, padx=5, pady=5)

    def create_rectangle(self):
        self.canvas.mouse.current_shape = "rectangle"
        self.canvas.mouse.draw_bind_mouse_events()

    def create_oval(self):
        self.canvas.mouse.current_shape = "oval"
        self.canvas.mouse.draw_bind_mouse_events()

    def create_triangle(self):
        self.canvas.mouse.current_shape = "triangle"
        self.canvas.mouse.draw_bind_mouse_events()