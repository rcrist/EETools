import customtkinter as ctk

from UI_Lib.mouse import Mouse
from UI_Lib.grid import Grid
from Comp_Lib import Switch, Text


class Canvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent)

        self.led_color = "red"
        self.led_size = "large"
        self.line_direction = "horizontal"
        self.comp_list = []
        self.mouse = Mouse(self)
        self.mouse.move_mouse_bind_events()

        self.grid = Grid(self, 10)

    def redraw(self):
        self.delete('grid_line')
        self.grid.draw()
        self.tag_lower("grid_line")
        for c in self.comp_list:
            c.update()

    def redraw_no_grid(self):
        for c in self.comp_list:
            c.update()

    def show_connectors(self):
        for s in self.comp_list:
            s.is_drawing = True
        self.redraw()

    def hide_connectors(self):
        for s in self.comp_list:
            s.is_drawing = False
        self.redraw()

    def edit_shape(self, _event=None):
        if isinstance(self.mouse.selected_comp, Switch):
            self.mouse.selected_comp.toggle_state()
            self.redraw()
        elif isinstance(self.mouse.selected_comp, Text):
            pass
