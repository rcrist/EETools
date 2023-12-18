import customtkinter as ctk
from UI_Lib import LeftFrame, TopFrame, Canvas

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    """ctk.CTk is a CustomTkinter main window, similar to tk.Tk tkinter main window"""
    def __init__(self):
        super().__init__()
        self.geometry("1200x800x100x100")  # w, h, x, y
        self.title("Analog Simulator")

        self.canvas = Canvas(self)
        self.left_frame = LeftFrame(self, self.canvas)
        self.top_frame = TopFrame(self, self.canvas)

        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)
        self.canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Add bindings here
        self.bind("<Configure>", self.on_window_resize)
        self.bind('<r>', self.rotate_comp)
        self.bind('<h>', self.canvas.set_horiz_dir)
        self.bind('<v>',self.canvas.set_vert_dir)
        self.canvas.bind('<Button-3>', self.canvas.edit_shape)

    def on_window_resize(self, _event):
        self.canvas.redraw()

    def rotate_comp(self, _event=None):
        if self.canvas.mouse.selected_comp:
            self.canvas.mouse.selected_comp.rotate()
            self.canvas.redraw()


if __name__ == "__main__":
    """Instantiate the Microwave Simulator app and run the main loop"""
    app = App()
    app.mainloop()
