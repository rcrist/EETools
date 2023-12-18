import customtkinter as ctk

from UI_Lib.canvas import Canvas
from UI_Lib.top_frame import TopFrame
from UI_Lib.left_frame import LeftFrame


class ShapeEditorApp(ctk.CTk):
    """ctk.CTk is a CustomTkinter main window, similar to tk.Tk tkinter main window"""
    def __init__(self):
        super().__init__()
        self.geometry("1200x800x100x100")  # w, h, x, y
        self.title("Shape Editor")

        self.shape_list = []

        # Add widgets to the app here
        self.canvas = Canvas()
        self.top_frame = TopFrame(self, self.canvas)
        self.left_frame = LeftFrame(self, self.canvas)

        self.top_frame.pack(side=ctk.TOP, fill="both", padx=5, pady=2)
        self.left_frame.pack(side=ctk.LEFT, fill="both", padx=5, pady=2)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        # Mouse & keyboard bindings
        self.bind('<r>', self.canvas.rotate_shape_ccw)
        self.bind('<e>', self.canvas.rotate_shape_cw)
        self.bind('+', self.canvas.scale_up)
        self.bind('-', self.canvas.scale_down)
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, _event):
        self.canvas.draw_shapes()


if __name__ == "__main__":
    """Instantiate the Shape Editor application and run the main loop"""
    app = ShapeEditorApp()
    app.mainloop()
