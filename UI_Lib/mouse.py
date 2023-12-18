from Helper_Lib.point import Point
from Helper_Lib.connection import Connection
from Shape_Lib.rectangle import Rectangle
from Shape_Lib.line import Line
from Shape_Lib.segment_line import SegmentLine
from Shape_Lib.elbow_line import ElbowLine


class Mouse:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_obj = None
        self.current_shape = None
        self.current_shape_obj = None
        self.mode = None  # Set to 'line_draw' to show shape connectors

        self.start = Point(0,0)
        self.offset1 = Point(0,0)
        self.offset2 = Point(0,0)

    def unbind_mouse_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def draw_bind_mouse_events(self):
        self.canvas.bind("<Button-1>", self.draw_left_down)
        self.canvas.bind("<B1-Motion>", self.draw_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.draw_left_up)

    def move_bind_mouse_events(self):
        self.unbind_mouse_events()
        self.canvas.bind("<Button-1>", self.move_left_down)
        self.canvas.bind("<B1-Motion>", self.move_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_left_up)

    def draw_left_down(self, event):
        self.unselect_all_shapes()
        self.start.x = event.x
        self.start.y = event.y
        self.start.x, self.start.y = self.canvas.grid.snap_to_grid(self.start.x, self.start.y)

        if self.current_shape == "rectangle":
            self.current_shape_obj = Rectangle(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
        elif self.current_shape == "line":
            self.current_shape_obj = Line(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)
        elif self.current_shape == "segment":
            self.current_shape_obj = SegmentLine(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)
        elif self.current_shape == "elbow":
            self.current_shape_obj = ElbowLine(self.canvas, self.start.x, self.start.y, self.start.x, self.start.y)
            self.select_connector(self.current_shape_obj, "begin", self.start.x, self.start.y)

        if self.current_shape_obj is not None:
            self.canvas.shape_list.append(self.current_shape_obj)
            self.canvas.draw_shapes()

    def draw_left_drag(self, event):
        if self.current_shape_obj:
            x, y = event.x, event.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.current_shape_obj.x1, self.current_shape_obj.y1 = self.start.x, self.start.y
            self.current_shape_obj.x2, self.current_shape_obj.y2 = x, y
            self.canvas.draw_shapes()

    def draw_left_up(self, event):
        if isinstance(self.current_shape_obj, Line) or isinstance(self.current_shape_obj, SegmentLine) or \
                      isinstance(self.current_shape_obj, ElbowLine):
            self.select_connector(self.current_shape_obj, "end", event.x, event.y)
        self.current_shape = None
        self.current_shape_obj = None
        self.unbind_mouse_events()
        self.move_bind_mouse_events()

    def move_left_down(self, event):
        if self.selected_obj:
            x, y = event.x, event.y
            sel = self.selected_obj.check_selector_hit(x, y)
            if sel:
                self.selected_obj.selector = sel.name
                self.unbind_mouse_events()
                self.bind_resize_mouse_events()
                self.resize_left_down(event)
                return
            else:
                a_shape = self.selected_obj
                a_shape.is_selected = False
                self.selected_obj = None
                self.canvas.draw_shapes()

        x, y = event.x, event.y
        self.select_shape(x, y)
        if self.selected_obj:
            if not isinstance(self.selected_obj, Line):
                self.mode = None
            x1, y1 = self.selected_obj.x1, self.selected_obj.y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            x2, y2 = self.selected_obj.x2, self.selected_obj.y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.offset1.x = x - x1
            self.offset1.y = y - y1
            self.offset2.x = x - x2
            self.offset2.y = y - y2
            self.canvas.draw_shapes()

    def move_left_drag(self, event):
        if self.selected_obj:
            x = event.x - self.offset1.x
            y = event.y - self.offset1.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.selected_obj.x1, self.selected_obj.y1 = x, y
            x = event.x - self.offset2.x
            y = event.y - self.offset2.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            self.selected_obj.x2, self.selected_obj.y2 = x, y
            self.canvas.draw_shapes()

    def move_left_up(self, _event):
        self.offset1.x, self.offset1.y = 0, 0
        self.offset2.x, self.offset2.y = 0,0

    def bind_resize_mouse_events(self):
        self.canvas.bind("<Button-1>", self.resize_left_down)
        self.canvas.bind("<B1-Motion>", self.resize_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.resize_left_up)

    def resize_left_down(self, event):
        if self.selected_obj:
            if not isinstance(self.selected_obj, Line):
                self.mode = None
            x1, y1 = self.selected_obj.x1, self.selected_obj.y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            x2, y2 = self.selected_obj.x2, self.selected_obj.y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.offset1.x = event.x - x1
            self.offset1.y = event.y - y1
            self.offset2.x = event.x - x2
            self.offset2.y = event.y - y2
            self.canvas.draw_shapes()

    def resize_left_drag(self, event):
        if self.selected_obj:
            offsets = [self.offset1.x, self.offset1.y, self.offset2.x, self.offset2.y]
            self.selected_obj.resize(offsets, event)
            self.canvas.draw_shapes()

    def resize_left_up(self, _event):
        self.offset1.x, self.offset1.y = 0, 0
        self.offset2.x, self.offset2.y = 0, 0
        self.canvas.mouse.unbind_mouse_events()
        self.canvas.mouse.move_bind_mouse_events()

    def select_shape(self, x, y):
        self.unselect_all_shapes()
        for shape in self.canvas.shape_list:
            # print("Select shape: ", shape, " select x,y: ", x, y)
            if shape.x1 <= x <= shape.x2 and shape.y1 <= y <= shape.y2:
                shape.is_selected = True
                self.selected_obj = shape
                self.canvas.draw_shapes()

    def unselect_all_shapes(self):
        for shape in self.canvas.shape_list:
            shape.is_selected = False

        self.selected_obj = None
        self.canvas.draw_shapes()

    def select_connector(self, line_obj, line_end, x, y):
        for shape in self.canvas.shape_list:
            conn = shape.check_connector_hit(x, y)
            if conn:
                if line_end == "begin":
                    line_obj.x1, line_obj.y1 = conn.x, conn.y
                elif line_end == "end":
                    line_obj.x2, line_obj.y2 = conn.x, conn.y
                a_conn = Connection(conn, line_obj, line_end)
                shape.line_list.append(a_conn)
                self.canvas.draw_shapes()
                return
