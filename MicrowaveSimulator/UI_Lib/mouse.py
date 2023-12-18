from Helper_Lib import Point
from Wire_Lib import StraightWire, SegmentWire, ElbowWire
from Comp_Lib import Connection


class Mouse:
    def __init__(self, canvas):
        self.canvas = canvas

        self.selected_comp = None
        self.current_wire_obj = None
        self.start = Point(0, 0)
        self.offset1 = Point(0, 0)
        self.offset2 = Point(0, 0)

        self.move_mouse_bind_events()

    def move_mouse_bind_events(self):
        self.canvas.bind("<Button-1>", self.move_left_down)
        self.canvas.bind("<B1-Motion>", self.move_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_left_up)

    def draw_wire_mouse_events(self):  # Added method to bind draw wire methods
        self.canvas.bind("<Button-1>", self.draw_left_down)
        self.canvas.bind("<B1-Motion>", self.draw_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.draw_left_up)

    def resize_wire_mouse_events(self):
        self.canvas.bind("<Button-1>", self.resize_left_down)
        self.canvas.bind("<B1-Motion>", self.resize_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.resize_left_up)

    def move_left_down(self, event):
        x, y = event.x, event.y
        self.comp_hit_test(x, y)
        if self.selected_comp:
            if (isinstance(self.selected_comp, StraightWire) or
                    isinstance(self.selected_comp, SegmentWire) or
                    isinstance(self.selected_comp, ElbowWire)):
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
            if (isinstance(self.selected_comp, StraightWire) or
                    isinstance(self.selected_comp, SegmentWire) or
                    isinstance(self.selected_comp, ElbowWire)):
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
        self.offset1.set(0, 0)
        self.offset2.set(0, 0)
        self.canvas.redraw()

    def draw_left_down(self, event):  # Added method for draw left down
        if self.current_wire_obj:
            # self.unselect_all()
            self.start.x = event.x
            self.start.y = event.y
            self.start.x, self.start.y = self.canvas.grid.snap_to_grid(self.start.x, self.start.y)

            self.current_wire_obj.x1, self.current_wire_obj.y1 = self.start.x, self.start.y
            self.current_wire_obj.x2, self.current_wire_obj.y2 = self.start.x, self.start.y

            self.select_connector(self.current_wire_obj, "begin", self.start.x, self.start.y)

    def draw_left_drag(self, event):  # Added method for draw left drag
        if self.current_wire_obj:
            wire = self.current_wire_obj
            x, y = event.x, event.y
            x, y = self.canvas.grid.snap_to_grid(x, y)
            wire.x1, wire.y1 = self.start.x, self.start.y
            wire.x2, wire.y2 = x, y
            self.current_wire_obj.update()

    def draw_left_up(self, event):  # Added method for draw left up
        self.select_connector(self.current_wire_obj, "end", event.x, event.y)
        self.canvas.hide_connectors()
        self.current_wire_obj = None
        self.move_mouse_bind_events()

    def resize_left_down(self, event):
        if self.selected_comp:
            x1, y1 = self.selected_comp.x1, self.selected_comp.y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1, "resize")
            x2, y2 = self.selected_comp.x2, self.selected_comp.y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2, "resize")
            self.offset1.x = event.x - x1
            self.offset1.y = event.y - y1
            self.offset2.x = event.x - x2
            self.offset2.y = event.y - y2
            self.selected_comp.update()

    def resize_left_drag(self, event):
        if self.selected_comp:
            offsets = [self.offset1.x, self.offset1.y, self.offset2.x, self.offset2.y]
            self.selected_comp.resize(offsets, event)
            self.selected_comp.update()

    def resize_left_up(self, _event):
        self.offset1.x, self.offset1.y = 0, 0
        self.offset2.x, self.offset2.y = 0, 0
        self.move_mouse_bind_events()

    def comp_hit_test(self, x, y):
        for comp in self.canvas.comp_list:
            comp.hit_test(x, y)
            if comp.is_selected:
                if (isinstance(comp, StraightWire) or isinstance(comp, SegmentWire) or
                        isinstance(self.selected_comp, ElbowWire)):
                    result = comp.sel_hit_test(x, y)
                    if result is not None:
                        self.resize_wire_mouse_events()
                comp.update()
                self.selected_comp = comp
                return

        # No shape hit - unselect all
        self.selected_comp = None
        self.unselect_all()

    def unselect_all(self):
        for comp in self.canvas.comp_list:
            comp.is_selected = False
            comp.update()

    def select_connector(self, wire_obj, wire_end, x, y):
        for comp in self.canvas.comp_list:
            if not (isinstance(comp, StraightWire) or isinstance(comp, SegmentWire) or
                        isinstance(self.selected_comp, ElbowWire)):
                conn = comp.check_connector_hit(x, y)
                if conn:
                    if wire_end == "begin":
                        wire_obj.x1, wire_obj.y1 = conn.x, conn.y
                    elif wire_end == "end":
                        wire_obj.x2, wire_obj.y2 = conn.x, conn.y
                    a_conn = Connection(conn.name, self.current_wire_obj.name, wire_end)
                    wire_obj.create_wire_list_cnx(comp.type, conn.name)
                    comp.wire_list.append(a_conn)
                    self.canvas.redraw()

