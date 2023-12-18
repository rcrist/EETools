import customtkinter as ctk
from PIL import Image, ImageTk
from UI_Lib import Canvas, TopFrame, LeftFrame, BottomFrame, Keyboard


class SimpleDiagramEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600x100x100")  # w, h, x, y
        self.title("Simple Diagram Editor")
        self.iconbitmap('D:/EETools/SimpleDiagramEditor/icons/shapes_color.ico')

        self.canvas = Canvas(self)
        self.top_frame = TopFrame(self, self.canvas)
        self.left_frame = LeftFrame(self, self.canvas)
        self.bottom_frame = BottomFrame(self)

        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH)
        self.bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)
        self.canvas.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        self.keyboard = Keyboard(self, self.canvas)
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, _event):
        self.canvas.redraw_shapes()


if __name__ == "__main__":
    app = SimpleDiagramEditorApp()
    app.mainloop()
