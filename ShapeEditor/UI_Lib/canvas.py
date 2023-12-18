import customtkinter as ctk
from UI_Lib.mouse import Mouse
from Shape_Lib.grid import Grid


class Canvas(ctk.CTkCanvas):
    def __init__(self):
        super().__init__()

        self.shape_list = []
        self.mouse = Mouse(self)
        self.selected = None

        self.grid_size = 10
        self.grid = Grid(self, self.grid_size)
        self.grid.draw_grid()

    def draw_shapes(self):
        self.delete('all')
        self.grid.draw_grid()
        for s in self.shape_list:
            s.draw()

    def rotate_shape_ccw(self, _event):
        if self.selected is not None:
            self.selected.angle -= 90
            if self.selected.angle < 0:
                self.selected.angle = 270
            self.draw_shapes()

    def rotate_shape_cw(self, _event):
        if self.selected is not None:
            self.selected.angle += 90
            if self.selected.angle > 270:
                self.selected.angle = 0
            self.draw_shapes()

    def scale_up(self, _event):
        if self.selected and self.selected.scale < 10:
            self.selected.scale += 0.1
            self.draw_shapes()

    def scale_down(self, _event):
        if self.selected and self.selected.scale > 0.1:
            self.selected.scale -= 0.1
            self.draw_shapes()
