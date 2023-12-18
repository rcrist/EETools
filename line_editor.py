import customtkinter as ctk
from UI_Lib import *


class LineEditorApp(ctk.CTk):
    """ctk.CTk is a CustomTkinter main window, similar to tk.Tk tkinter main window"""
    def __init__(self):
        super().__init__()
        self.geometry("800x600x100x100")  # w, h, x, y
        self.title("Line Editor")

        # Create Canvas widget
        self.canvas = Canvas()
        a_top_frame = TopFrame(self, self.canvas)
        a_left_frame = LeftFrame(self, self.canvas)

        a_top_frame.pack(side=ctk.TOP, fill=ctk.BOTH)
        a_left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)
        self.canvas.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        # Declare mouse bindings
        self.bind('<r>', self.canvas.rotate_shape)
        self.bind('<h>', self.canvas.set_horizontal_line_direction)
        self.bind('<v>', self.canvas.set_vertical_line_direction)
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, _event):
        self.canvas.draw_shapes()


if __name__ == "__main__":
    # Instantiate the Line Editor application and run the main loop
    app = LineEditorApp()
    app.mainloop()
