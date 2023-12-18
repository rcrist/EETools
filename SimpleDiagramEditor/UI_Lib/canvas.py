import customtkinter as ctk
from tkinter import filedialog
from UI_Lib.mouse import Mouse
from Shape_Lib import Text
from Shape_Lib.grid import Grid


class Canvas(ctk.CTkCanvas):
    def __init__(self, master):
        super().__init__(master)
        self.shape_list = []
        self.mouse = Mouse(self)
        self.line_direction = "horizontal"
        self.grid_size = 10
        self.grid = Grid(self, self.grid_size)
        self.grid.draw()

    def redraw_shapes(self):
        self.delete('grid_line')
        self.grid.draw()
        self.tag_lower('grid_line')
        for s in self.shape_list:
            s.update()

    def edit_shape(self, _event):
        if self.mouse.selected_shape is not None:
            shape = self.mouse.selected_shape
            if self.gettags("current")[0] == "pics":
                filename = filedialog.askopenfilename(initialdir="../images", title="select a file",
                                                      filetypes=(("png files", "*.png"), ("all file", "*.*")))
                shape.filename = filename
                shape.update()
            elif isinstance(shape, Text):
                dialog = ctk.CTkInputDialog(text="Enter new text", title="Edit Text")
                shape.text = dialog.get_input()
                self.redraw_shapes()
