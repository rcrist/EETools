from Shape_Lib.rectangle import Rectangle
from Shape_Lib.oval import Oval
from Shape_Lib.triangle import Triangle


class Mouse:
    def __init__(self, canvas):
        self.canvas = canvas

        self.selected_obj = None
        self.current_shape = None
        self.current_shape_obj = None

        self.start_x, self.start_y = 0, 0
        self.offset_x1, self.offset_y1 = 0, 0
        self.offset_x2, self.offset_y2 = 0, 0

    def unbind_mouse_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def draw_bind_mouse_events(self):
        self.canvas.bind("<Button-1>", self.draw_left_down)
        self.canvas.bind("<B1-Motion>", self.draw_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.draw_left_up)

    def bind_move_mouse_events(self):
        self.canvas.bind("<Button-1>", self.move_left_down)
        self.canvas.bind("<B1-Motion>", self.move_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_left_up)

    def move_left_down(self, event):
        x, y = event.x, event.y
        x, y = self.canvas.grid.snap_to_grid(x, y)
        self.select_shape(x, y)
        if self.canvas.selected:
            x1, y1 = self.canvas.selected.x1, self.canvas.selected.y1
            x2, y2 = self.canvas.selected.x2, self.canvas.selected.y2
            self.offset_x1 = event.x - x1
            self.offset_y1 = event.y - y1
            self.offset_x2 = event.x - x2
            self.offset_y2 = event.y - y2
            self.canvas.draw_shapes()

    def move_left_drag(self, event):
        if self.canvas.selected:
            x = event.x - self.offset_x1
            y = event.y - self.offset_y1
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.canvas.selected.x1, self.canvas.selected.y1 = x, y
            x = event.x - self.offset_x2
            y = event.y - self.offset_y2
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.canvas.selected.x2, self.canvas.selected.y2 = x, y
            self.canvas.draw_shapes()

    def move_left_up(self, _event):
        self.offset_x1 = 0
        self.offset_y1 = 0
        self.offset_x2 = 0
        self.offset_y2 = 0

    def draw_left_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.start_x, self.start_y = \
            (self.canvas.grid.snap_to_grid(self.start_x, self.start_y))

        if self.current_shape == "rectangle":
            self.current_shape_obj = Rectangle(self.canvas,
                self.start_x, self.start_y,
                self.start_x, self.start_y,
                fill_color="white",
                border_color="black",
                border_width=3)
        elif self.current_shape == "oval":
            self.current_shape_obj = Oval(self.canvas,
                self.start_x, self.start_y,
                self.start_x, self.start_y,
                fill_color="white",
                border_color="black",
                border_width=3)
        elif self.current_shape == "triangle":
            self.current_shape_obj = Triangle(self.canvas,
                self.start_x, self.start_y,
                self.start_x + 100, self.start_y + 100,
                fill_color="white",
                border_color="black",
                border_width=3)

        if self.current_shape_obj is not None:
            self.canvas.shape_list.append(self.current_shape_obj)
            self.canvas.draw_shapes()

    def draw_left_drag(self, event):
        if self.current_shape_obj:
            x, y = event.x, event.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.current_shape_obj.x1, self.current_shape_obj.y1 = self.start_x, self.start_y
            self.current_shape_obj.x2, self.current_shape_obj.y2 = x, y
            self.canvas.draw_shapes()

    def draw_left_up(self, event):
        self.current_shape = None
        self.current_shape_obj = None
        self.unbind_mouse_events()
        self.bind_move_mouse_events()

    def select_shape(self, x, y):
        for s in self.canvas.shape_list:
            w = s.x2 - s.x1
            h = s.y2 - s.y1
            if (
                    s.x1 <= x <= s.x2 + w
                    and s.y1 <= y <= s.y2 + h
            ):
                self.unselect_all_objects()
                self.canvas.selected = s
                self.canvas.selected.is_selected = True

    def unselect_all_objects(self):
        for s in self.canvas.shape_list:
            s.is_selected = False
        self.canvas.draw_shapes()
