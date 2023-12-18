import customtkinter as ctk
from UI_Lib import Canvas, LeftFrame, TopFrame

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class DigitalSimulatorApp(ctk.CTk):
    """ctk.CTk is a CustomTkinter main window, similar to tk.Tk tkinter main window"""
    def __init__(self):
        super().__init__()
        self.geometry("1200x800x100x100")  # w, h, x, y
        self.title("Digital Simulator")

        self.canvas = Canvas(self)
        self.top_frame = TopFrame(self, self.canvas)
        self.left_frame = LeftFrame(self, self.canvas)
        self.bottom_frame = ctk.CTkFrame(self)

        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH)
        self.bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)
        self.canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Add widgets to frames to cause the frames to auto-size
        self.bottom_frame_label = ctk.CTkLabel(self.bottom_frame, text="Digital simulator ready...")
        self.bottom_frame_label.pack(side=ctk.LEFT, padx=5, pady=5)

        # Add bindings here
        self.bind('<r>', self.rotate_comp)
        self.bind("<Configure>", self.on_window_resize)
        self.canvas.bind('<Button-3>', self.canvas.edit_shape)

    def rotate_comp(self, _event=None):
        if self.canvas.mouse.selected_comp:
            self.canvas.mouse.selected_comp.rotate()
            self.canvas.redraw()

    def on_window_resize(self, _event):
        self.canvas.redraw()


if __name__ == "__main__":
    """Instantiate the Digital Simulator app and run the main loop"""
    app = DigitalSimulatorApp()
    app.mainloop()
