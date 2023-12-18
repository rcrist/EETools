from Helper_Lib.point import Point
from Shape_Lib import Rectangle, Oval, Triangle, Text, Picture
from Shape_Lib import StraightLine, SegmentLine, ElbowLine, Connection


class Mouse:
    def __init__(self, a_canvas):
        """Class to manage mouse events"""
        self.canvas = a_canvas
        self.selected_shape = None
        self.current_shape = None
        self.current_shape_obj = None

        self.start = Point(0, 0)
        self.offset1 = Point(0, 0)
        self.offset2 = Point(0, 0)

        self.canvas.bind('<Button-3>', self.canvas.edit_shape)

    def unbind_mouse_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def move_bind_mouse_events(self):
        self.unbind_mouse_events()
        self.canvas.bind("<Button-1>", self.move_left_down)
        self.canvas.bind("<B1-Motion>", self.move_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_left_up)

    def draw_bind_mouse_events(self):
        self.canvas.bind("<Button-1>", self.draw_left_down)
        self.canvas.bind("<B1-Motion>", self.draw_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.draw_left_up)

    def bind_resize_mouse_events(self):
        self.canvas.bind("<Button-1>", self.resize_left_down)
        self.canvas.bind("<B1-Motion>", self.resize_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.resize_left_up)

    def move_left_down(self, event):
        x, y = event.x, event.y
        self.select_hit_test(x, y)
        if self.selected_shape:
            # print("Shape found: ", self.selected_shape)
            sel = self.selected_shape.check_selector_hit(x, y)
            if sel:
                self.selected_shape.selector = sel.name
                self.unbind_mouse_events()
                self.bind_resize_mouse_events()
                self.resize_left_down(event)
                return
            else:
                x1, y1 = self.selected_shape.x1, self.selected_shape.y1
                x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
                x2, y2 = self.selected_shape.x2, self.selected_shape.y2
                x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
                self.offset1.x = x - x1
                self.offset1.y = y - y1
                self.offset2.x = x - x2
                self.offset2.y = y - y2

    def move_left_drag(self, event):
        if self.selected_shape:
            x = event.x - self.offset1.x
            y = event.y - self.offset1.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.selected_shape.x1, self.selected_shape.y1 = x, y
            x = event.x - self.offset2.x
            y = event.y - self.offset2.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.selected_shape.x2, self.selected_shape.y2 = x, y
            self.canvas.redraw_shapes()

    def move_left_up(self, _event):
        self.offset1.x, self.offset1.y = 0, 0
        self.offset2.x, self.offset2.y = 0, 0

    def draw_left_down(self, event):
        self.unselect_all()
        self.start.x = event.x
        self.start.y = event.y
        self.start.x, self.start.y = self.canvas.grid.snap_to_grid(self.start.x, self.start.y)

        if self.current_shape == "rectangle":
            self.current_shape_obj = Rectangle(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "oval":
            self.current_shape_obj = Oval(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "tri":
            self.current_shape_obj = Triangle(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "text":
            self.current_shape_obj = Text(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "pic":
            self.current_shape_obj = Picture(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "straight":
            self.current_shape_obj = StraightLine(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)
        elif self.current_shape == "segment":
            self.current_shape_obj = SegmentLine(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)
        elif self.current_shape == "elbow":
            self.current_shape_obj = ElbowLine(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)

        if self.current_shape_obj is not None:
            self.canvas.shape_list.append(self.current_shape_obj)

    def draw_left_drag(self, event):
        if self.current_shape_obj:
            shape = self.current_shape_obj
            x, y = event.x, event.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            shape.x1, shape.y1 = self.start.x, self.start.y
            shape.x2, shape.y2 = x, y
            self.canvas.redraw_shapes()

    def draw_left_up(self, event):
        if (isinstance(self.current_shape_obj, StraightLine) or isinstance(self.current_shape_obj, SegmentLine)
                or isinstance(self.current_shape_obj, ElbowLine)):
            self.select_connector(self.current_shape_obj, "end", event.x, event.y)

        self.current_shape = None
        self.current_shape_obj = None
        self.unbind_mouse_events()
        self.move_bind_mouse_events()

    def resize_left_down(self, event):
        if self.selected_shape:
            shape = self.selected_shape
            x1, y1 = shape.x1, shape.y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            x2, y2 = shape.x2, shape.y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.offset1.x = event.x - x1
            self.offset1.y = event.y - y1
            self.offset2.x = event.x - x2
            self.offset2.y = event.y - y2

    def resize_left_drag(self, event):
        if self.selected_shape:
            offsets = [self.offset1.x, self.offset1.y, self.offset2.x, self.offset2.y]
            self.selected_shape.resize(offsets, event)
            self.canvas.redraw_shapes()

    def resize_left_up(self, _event):
        self.offset1.x, self.offset1.y = 0, 0
        self.offset2.x, self.offset2.y = 0, 0
        self.canvas.mouse.unbind_mouse_events()
        self.canvas.mouse.move_bind_mouse_events()

    def select_hit_test(self, x, y):
        for s in self.canvas.shape_list:
            if isinstance(s, Text) or isinstance(s, Picture):
                if s.bbox[0] <= x <= s.bbox[2] and s.bbox[1] <= y <= s.bbox[3]:
                    self.selected_shape = s
                    s.is_selected = True
                    self.canvas.redraw_shapes()
                    return
            elif s.x1 <= x <= s.x2 and s.y1 <= y <= s.y2:
                self.selected_shape = s
                s.is_selected = True
                self.canvas.redraw_shapes()
                return

        # No shape hit - unselect all
        self.selected_shape = None
        self.unselect_all()

    def unselect_all(self):
        # print("Unselect all")
        for s in self.canvas.shape_list:
            s.is_selected = False
            self.canvas.redraw_shapes()

    def select_connector(self, line_obj, line_end, x, y):
        for shape in self.canvas.shape_list:
            if not isinstance(shape, StraightLine) or not isinstance(shape, SegmentLine)\
                    or not isinstance(shape, ElbowLine):
                conn = shape.check_connector_hit(x, y)
                if conn:
                    if line_end == "begin":
                        line_obj.x1, line_obj.y1 = conn.x, conn.y
                    elif line_end == "end":
                        line_obj.x2, line_obj.y2 = conn.x, conn.y
                    a_conn = Connection(conn, line_obj, line_end)
                    shape.line_list.append(a_conn)
                    self.canvas.redraw_shapes()
                    return
