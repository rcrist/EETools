import customtkinter as ctk
from UI_Lib import LeftFrame, TopFrame, Canvas

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class MicrowaveSimulatorApp(ctk.CTk):
    """ctk.CTk is a CustomTkinter main window, similar to tk.Tk tkinter main window"""
    def __init__(self):
        super().__init__()
        self.geometry("1200x800x100x100")  # w, h, x, y
        self.title("Microwave Simulator")

        self.canvas = Canvas(self)
        self.left_frame = LeftFrame(self, self.canvas)
        self.top_frame = TopFrame(self, self.canvas)

        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)
        self.canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Add bindings here
        self.bind("<Configure>", self.on_window_resize)
        self.bind('<r>', self.rotate_comp)

    def on_window_resize(self, _event):
        self.canvas.redraw()

    def rotate_comp(self, _event=None):
        if self.canvas.mouse.selected_comp:
            self.canvas.mouse.selected_comp.rotate()
            self.canvas.redraw()


if __name__ == "__main__":
    """Instantiate the Microwave Simulator app and run the main loop"""
    app = MicrowaveSimulatorApp()
    app.mainloop()
