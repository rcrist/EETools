from Wire_Lib.wire_selector import WireSelector


class SegmentWire:
    def __init__(self, canvas, x1, y1, x2, y2):
        """3-Segment Wire"""
        self.type = "segment_wire"
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Wire appearance variables
        self.fill_color = "black"
        self.border_width = 3
        self.line_direction = self.canvas.line_direction

        self.id = None
        self.state = False

        self.bbox = None
        self.is_selected = False
        self.sel_list = []
        self.segment_list = None
        self.points = None
        self.selector = None

        self.points = [self.x1, self.y1, self.x2, self.y2]
        self.create_segmented_line()

        self.s1_id, self.s2_id = None, None
        self.create_selectors()
        self.set_selector_visibility()

    def create_segmented_line(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        segment1, segment2, segment3 = None, None, None

        if self.line_direction == "horizontal":
            segment1 = self.x1, self.y1, self.x1 + w/2, self.y1
            segment2 = self.x1 + w/2, self.y1, self.x1 + w/2, self.y2
            segment3 = self.x1 + w/2, self.y2, self.x2, self.y2
        elif self.line_direction == "vertical":
            segment1 = self.x1, self.y1, self.x1, self.y1 + h/2
            segment2 = self.x1, self.y1 + h/2, self.x2, self.y1 + h/2
            segment3 = self.x2, self.y1 + h/2, self.x2, self.y2
        self.segment_list = [segment1, segment2, segment3]
        self.draw_segments()

    def draw_segments(self):
        for s in self.segment_list:
            if self.state:
                self.id = self.canvas.create_line(s, fill="#00ff00", width=self.border_width, tags='wire')
            else:
                self.id = self.canvas.create_line(s, fill=self.fill_color, width=self.border_width, tags='wire')

    def create_selectors(self):
        """Create selectors at the ends of the wire here"""
        self.s1_id = WireSelector(self.canvas, "begin", self.x1, self.y1)
        self.s2_id = WireSelector(self.canvas, "end", self.x2, self.y2)

        self.sel_list = [self.s1_id, self.s2_id]

    def update(self):
        self.update_position()
        self.update_bbox()
        self.update_wire_color()
        self.update_selectors()
        self.set_selector_visibility()

    def update_position(self):
        """Update the position when the gate object is moved"""
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        if self.line_direction == "horizontal":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1 + w / 2, self.y1,
                               self.x1 + w / 2, self.y1, self.x1 + w / 2, self.y2,
                               self.x1 + w / 2, self.y2, self.x2, self.y2)
        elif self.line_direction == "vertical":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1, self.y1 + h / 2,
                               self.x1, self.y1 + h / 2, self.x2, self.y1 + h / 2,
                               self.x2, self.y1 + h / 2, self.x2, self.y2)

    def update_bbox(self):
        self.bbox = self.canvas.bbox(self.id)

    def update_wire_color(self):
        if self.state:
            self.canvas.itemconfig(self.id, fill="#00ff00")
        else:
            self.canvas.itemconfig(self.id, fill=self.fill_color)

    def update_border_width(self):
        self.canvas.itemconfig(self.id, width=self.border_width)

    def update_selectors(self):
        """Update the position of all selectors here"""
        self.s1_id.x, self.s1_id.y = self.x1, self.y1
        self.s1_id.update()

        self.s2_id.x, self.s2_id.y = self.x2, self.y2
        self.s2_id.update()

    def set_selector_visibility(self):
        if self.is_selected:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='normal')
        else:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='hidden')

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "end":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            self.x2, self.y2 = x2, y2
            # self.x2, self.y2 = self.canvas.grid.snap_to_grid(self.x2, self.y2)
        elif self.selector == "begin":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            self.x1, self.y1 = x1, y1
            # self.x1, self.y1 = self.canvas.grid.snap_to_grid(self.x1, self.y1)

    def check_selector_hit(self, x, y):
        for sel in self.sel_list:
            if sel.selector_hit_test(x, y):
                return sel
        return None

    def __repr__(self):
        return "Wire: " + " x1: " + str(self.x1) + " y1: " + str(self.y1) + \
            " x2: " + str(self.x2) + " y2: " + str(self.y2)

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2)
