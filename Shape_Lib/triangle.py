from Helper_Lib import Point
from Shape_Lib.shape import Shape
from Shape_Lib.selector import Selector
from Shape_Lib.connector import Connector


class Triangle(Shape):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.points = []
        self.type = "triangle"
        self.angle = 0

        self.s1_id, self.s2_id, self.s3_id = None, None, None
        self.c1_id, self.c2_id, self.c3_id, self.c4_id = None, None, None, None

        self.create_shape()
        self.create_selectors()
        self.create_connectors()

    def create_shape(self):
        """Create the shape once!"""
        w = self.x2 - self.x1
        self.points = [self.x1 + w / 2, self.y1, self.x2, self.y2, self.x1, self.y2]
        self.id = self.canvas.create_polygon(self.points, fill=self.fill_color, outline=self.border_color,
                                   width=self.border_width)

    def update(self):
        w = self.x2 - self.x1
        self.rotation_points()
        self.canvas.coords(self.id, self.points[0], self.points[1], self.points[2], self.points[3],
                           self.points[4], self.points[5])
        self.canvas.itemconfig(self.id, fill=self.fill_color)
        self.canvas.itemconfig(self.id, outline=self.border_color)
        self.canvas.itemconfig(self.id, width=self.border_width)

        self.update_selectors()
        if self.is_selected:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='normal')
        else:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='hidden')

        self.update_connectors()
        if self.is_drawing:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='normal')
        else:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='hidden')

        self.move_connected_lines()

    def create_selectors(self):
        """Create four selectors at the corners here"""
        w = self.x2 - self.x1
        self.s1_id = Selector(self.canvas, "s1", self.x1 + w / 2, self.y1)
        self.s2_id = Selector(self.canvas, "s2", self.x2, self.y2)
        self.s3_id = Selector(self.canvas, "s3", self.x1, self.y2)

        self.sel_list = [self.s1_id, self.s2_id, self.s3_id]
        for s in self.sel_list:
            self.canvas.itemconfig(s.id, state='hidden')

    def update_selectors(self):
        """Update the position of all selectors here"""
        x1, y1, x2, y2, x3, y3 = self.points
        w = x2 - x1
        self.s1_id.x, self.s1_id.y = x1, y1
        self.s1_id.update()

        self.s2_id.x, self.s2_id.y = x2, y2
        self.s2_id.update()

        self.s3_id.x, self.s3_id.y = x3, y3
        self.s3_id.update()

    def create_connectors(self):
        """Create connectors here"""
        # Calculate the shape geometry
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        center = Point(self.x1+w/2, self.y1+h/2)

        self.c1_id = Connector(self.canvas, "c1", center.x, center.y)          # Shape Center
        self.c2_id = Connector(self.canvas, "c2", center.x, center.y - h / 2)    # Right Center
        self.c3_id = Connector(self.canvas, "c3", center.x + w / 4, center.y)    # Left Center
        self.c4_id = Connector(self.canvas, "c4", center.x, center.y + h / 2)    # Bottom Center

        self.conn_list = [self.c1_id, self.c2_id, self.c3_id, self.c4_id]
        for c in self.conn_list:
            self.canvas.itemconfig(c.id, state='hidden')

    def update_connectors(self):
        """Update the position of all connectors here"""
        x1, y1, x2, y2, x3, y3 = self.points


        if self.angle == 0 or self.angle == 180:
            w = x2 - x3
            h = y2 - y1
            center = Point(x1 + w / 2, y1 + h / 2)
            self.c1_id.x, self.c1_id.y = x1, y1+h/2
            self.c1_id.update()
            self.c2_id.x, self.c2_id.y = x1 - w/4, center.y
            self.c2_id.update()
            self.c3_id.x, self.c3_id.y = x1 + w/4, center.y
            self.c3_id.update()
            self.c4_id.x, self.c4_id.y = x1, y2
            self.c4_id.update()
        elif self.angle == 90 or self.angle == 270:
            w = x2 - x1
            h = y2 - y3
            center = Point(x1 + w / 2, y1)
            self.c1_id.x, self.c1_id.y = x1 + w/2, y1
            self.c1_id.update()
            self.c2_id.x, self.c2_id.y = center.x, center.y - h/4
            self.c2_id.update()
            self.c3_id.x, self.c3_id.y = center.x, center.y + h/4
            self.c3_id.update()
            self.c4_id.x, self.c4_id.y = x2, y1
            self.c4_id.update()

    def rotate(self):
        # Calculate rotation angle
        self.angle += 90
        if self.angle > 270:
            self.angle = 0

    def rotation_points(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        if self.angle == 0:
            self.points = [self.x1 + w / 2, self.y1, self.x2, self.y2, self.x1, self.y2]
        elif self.angle == 90:
            self.points = [self.x1, self.y1 + h/2, self.x2, self.y1, self.x2, self.y2]
        elif self.angle == 180:
            self.points = [self.x1 + w/2, self.y2, self.x1, self.y1, self.x2, self.y1]
        elif self.angle == 270:
            self.points = [self.x2, self.y1 + h/2, self.x1, self.y2, self.x1, self.y1]

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "s1":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            self.x1, self.y1 = x1, y1
        elif self.selector == "s2":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.x2, self.y2 = x2, y2
        elif self.selector == "s3":
            x1 = event.x - offset_x1
            y2 = event.y - offset_y2
            x1, y2 = self.canvas.grid.snap_to_grid(x1, y2)
            self.x1, self.y2 = x1, y2

    def __repr__(self):
        return ("Triangle: x1, y1, x2, y2 = " + "(" + str(self.x1) + ", " + str(self.y1) + ", " + str(self.y2) + ", " +
                str(self.y2) + ")\nfill color: " + self.fill_color + "\nborder_color: " + self.border_color +
                "\nborder_width: " + str(self.border_width))
