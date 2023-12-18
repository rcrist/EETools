from Helper_Lib import Point
from Wire_Lib import Connection  # Added import for connection class
from IC_Lib import SevenSegment


class Mouse:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_comp = None
        self.current_wire_obj = None

        self.start = Point(0, 0)
        self.offset1 = Point(0, 0)
        self.offset2 = Point(0, 0)

    def unbind_mouse_events(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def move_mouse_bind_events(self):
        self.unbind_mouse_events()
        self.canvas.bind("<Button-1>", self.move_left_down)
        self.canvas.bind("<B1-Motion>", self.move_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_left_up)

    def draw_wire_mouse_events(self):  # Added method to bind draw wire methods
        self.unbind_mouse_events()
        self.canvas.bind("<Button-1>", self.draw_left_down)
        self.canvas.bind("<B1-Motion>", self.draw_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.draw_left_up)

    def move_left_down(self, event):
        x, y = event.x, event.y
        self.select_hit_test(x, y)

        if self.selected_comp:
            if self.canvas.gettags(self.selected_comp.id)[0] == 'wire':
                x1, y1 = self.selected_comp.x1, self.selected_comp.y1
                x2, y2 = self.selected_comp.x2, self.selected_comp.y2
                self.offset1.set(x - x1, y - y1)
                self.offset2.set(x - x2, y - y2)
            else:
                x1, y1 = self.selected_comp.x1, self.selected_comp.y1
                self.offset1.x, self.offset1.y = self.canvas.grid.snap_to_grid(self.offset1.x, self.offset1.y)
                self.offset1.set(x - x1, y - y1)

    def move_left_drag(self, event):
        if self.selected_comp:
            if self.canvas.gettags(self.selected_comp.id)[0] == 'wire':
                x1 = event.x - self.offset1.x
                y1 = event.y - self.offset1.y
                x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
                x2 = event.x - self.offset2.x
                y2 = event.y - self.offset2.y
                x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
                self.selected_comp.x1, self.selected_comp.y1 = x1, y1
                self.selected_comp.x2, self.selected_comp.y2 = x2, y2
                self.canvas.redraw()
            else:
                x = event.x - self.offset1.x
                y = event.y - self.offset1.y
                x, y = self.canvas.grid.snap_to_grid(x, y)
                self.selected_comp.x1, self.selected_comp.y1 = x, y
                self.canvas.redraw()

    def move_left_up(self, _event):
        if self.selected_comp:
            self.offset1.set(0, 0)
            self.offset2.set(0, 0)

    def draw_left_down(self, event):  # Added method for draw left down
        if self.current_wire_obj:
            self.unselect_all()
            self.start.x = event.x
            self.start.y = event.y
            self.start.x, self.start.y = self.canvas.grid.snap_to_grid(self.start.x, self.start.y)

            self.current_wire_obj.x1, self.current_wire_obj.y1 = self.start.x, self.start.y
            self.current_wire_obj.x2, self.current_wire_obj.y2 = self.start.x, self.start.y

            if self.current_wire_obj is not None:
                self.select_connector(self.current_wire_obj, "begin", self.start.x, self.start.y)

    def draw_left_drag(self, event):  # Added method for draw left drag
        if self.current_wire_obj:
            shape = self.current_wire_obj
            x, y = event.x, event.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            shape.x1, shape.y1 = self.start.x, self.start.y
            shape.x2, shape.y2 = x, y
            self.canvas.redraw()

    def draw_left_up(self, event):  # Added method for draw left up
        self.select_connector(self.current_wire_obj, "end", event.x, event.y)
        self.canvas.hide_connectors()
        self.move_mouse_bind_events()

    def select_hit_test(self, x, y):
        for s in self.canvas.comp_list:
            if s.bbox[0] <= x <= s.bbox[2] and s.bbox[1] <= y <= s.bbox[3]:
                # print("Shape hit: ", s)
                self.selected_comp = s
                s.is_selected = True
                self.canvas.redraw()
                return

        # No shape hit - unselect all
        self.selected_comp = None
        self.unselect_all()

    def unselect_all(self):
        for s in self.canvas.comp_list:
            s.is_selected = False
        self.canvas.redraw()

    def select_connector(self, wire_obj, wire_end, x, y):  # Added method to see if line end hits a gate connector
        for comp in self.canvas.comp_list:
            if not self.canvas.gettags(comp.id)[0] == 'wire':
                conn = comp.check_connector_hit(x, y)
                if conn:
                    if wire_end == "begin":
                        wire_obj.x1, wire_obj.y1 = conn.x, conn.y
                    elif wire_end == "end":
                        wire_obj.x2, wire_obj.y2 = conn.x, conn.y
                    a_conn = Connection(conn, self.current_wire_obj, wire_end)
                    comp.wire_list.append(a_conn)
                    self.canvas.redraw()