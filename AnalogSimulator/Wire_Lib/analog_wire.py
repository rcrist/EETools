from Wire_Lib.wire import Wire


class AnalogWire(Wire):
    def __init__(self, canvas, wire_type, x1, y1, x2, y2):
        super().__init__(canvas, wire_type, x1, y1, x2, y2)

        self.seg1, self.seg2, self.seg3 = None, None, None
        self.segment_list = []

        self.create_wire()
        self.update_bbox()
        self.create_selectors()
        self.update_selection()

    def create_wire(self):
        if self.wire_type == 'straight':
            self.create_straight_wire()
        elif self.wire_type == 'elbow':
            self.create_elbow_wire()
        elif self.wire_type == 'segment':
            self.create_segment_wire()

    def create_straight_wire(self):
        self.id = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=self.width)

    def create_elbow_wire(self):
        if self.wire_dir == "H":  # Horizontal
            self.id = self.canvas.create_line(self.x1, self.y1, self.x2, self.y1,
                                              self.x2, self.y1, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width, tags="wire")
        elif self.wire_dir == "V":  # Vertical
            self.id = self.canvas.create_line(self.x1, self.y1, self.x1, self.y2,
                                              self.x1, self.y2, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width, tags="wire")

    def create_segment_wire(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1

        if self.wire_dir == "H":  # Horizontal
            self.seg1 = self.x1, self.y1, self.x1 + w / 2, self.y1
            self.seg2 = self.x1 + w / 2, self.y1, self.x1 + w / 2, self.y2
            self.seg3 = self.x1 + w / 2, self.y2, self.x2, self.y2
        elif self.wire_dir == "V":  # Vertical
            self.seg1 = self.x1, self.y1, self.x1, self.y1 + h / 2
            self.seg2 = self.x1, self.y1 + h / 2, self.x2, self.y1 + h / 2
            self.seg3 = self.x2, self.y1 + h / 2, self.x2, self.y2
        self.segment_list = [self.seg1, self.seg2, self.seg3]
        self.draw_segments()

    def draw_segments(self):
        for s in self.segment_list:
            self.id = self.canvas.create_line(s, fill=self.fill_color, width=self.border_width, tags='wire')

    def update(self):
        self.update_position()
        self.update_bbox()
        self.update_selectors()
        self.update_selection()

    def update_position(self):
        if self.wire_type == 'straight':
            self.update_straight_position()
        elif self.wire_type == 'elbow':
            self.update_elbow_position()
        elif self.wire_type == 'segment':
            self.update_segment_position()

    def update_straight_position(self):
        """Update the position when the attached component is moved"""
        self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)

    def update_elbow_position(self):
        """Update the position when the attached component is moved"""
        if self.wire_dir == "H":
            self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y1,
                                        self.x2, self.y1, self.x2, self.y2)
        elif self.wire_dir == "V":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1, self.y2,
                                        self.x1, self.y2, self.x2, self.y2)

    def update_segment_position(self):
        """Update the position when the attached component is moved"""
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        if self.wire_dir == "H":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1 + w / 2, self.y1,
                               self.x1 + w / 2, self.y1, self.x1 + w / 2, self.y2,
                               self.x1 + w / 2, self.y2, self.x2, self.y2)
        elif self.wire_dir == "V":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1, self.y1 + h / 2,
                               self.x1, self.y1 + h / 2, self.x2, self.y1 + h / 2,
                               self.x2, self.y1 + h / 2, self.x2, self.y2)

    def hit_test(self, x, y):
        # 2-Point Line equation: y = m * (x - x1) + y1
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2

        # Calculate the slope: m = (y2 - y1) / (x2 - x1)
        if (x2 - x1) == 0:
            m = 0
        else:
            m = (y2 - y1)/(x2 - x1)

        # Check to see if the point (x, y) is on the line and between the two end points
        tol = 10
        if y - tol <= m*(x - x1) + y1 <= y + tol:
            if (min(x1, x2) <= x <= max(x1, x2)) and (min(y1, y2) <= y <= max(y1, y2)):
                self.is_selected = True
        else:
            self.is_selected = False

    def __repr__(self):
        return ("Type: " + self.wire_type + " node_num: " + self.node_num +
                " x1: " + str(self.x1) + " y1: " + str(self.y1) +
                " x2: " + str(self.x2) + " y2: " + str(self.y2))

    def reprJson(self):
        return dict(type=self.wire_type, wire_dir=self.wire_dir, node_num=self.node_num, x1=self.x1, y1=self.y1,
                    x2=self.x2, y2=self.y2, name=self.name)
