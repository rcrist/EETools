import customtkinter as ctk
from UI_Lib.mouse import Mouse
from Shape_Lib.line import Line
from Shape_Lib.grid import Grid


class Canvas(ctk.CTkCanvas):
    def __init__(self):
        super().__init__()
        self.shape_list = []
        self.mouse = Mouse(self)
        self.grid_size = 10
        self.grid = Grid(self, self.grid_size)
        self.grid.draw()
        self.line_direction = "horizontal"

    def draw_shapes(self):
        self.delete('all')
        self.grid.draw()
        for shape in self.shape_list:
            shape.draw()

    def rotate_shape(self, _event):
        if not isinstance(self.mouse.selected_obj, Line):
            self.mouse.selected_obj.rotate()
            self.draw_shapes()

    def set_horizontal_line_direction(self, _event):
        self.line_direction = "horizontal"

    def set_vertical_line_direction(self, _event):
        self.line_direction = "vertical"
