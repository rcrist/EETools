from Helper_Lib import Point
from Shape_Lib.shape import Shape
from Shape_Lib.selector import Selector
from Shape_Lib.connector import Connector


class Oval(Shape):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.type = "oval"

        self.s1_id, self.s2_id, self.s3_id, self.s4_id = None, None, None, None
        self.c1_id, self.c2_id, self.c3_id, self.c4_id, self.c5_id = None, None, None, None, None

        self.create_shape()
        self.create_selectors()
        self.create_connectors()

    def create_shape(self):
        """Create the shape here"""
        self.id = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                                               fill=self.fill_color,
                                               outline=self.border_color,
                                               width=self.border_width)

    def update(self):
        """Update the shape here"""
        self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)
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
        self.s1_id = Selector(self.canvas, "s1", self.x1, self.y1)
        self.s2_id = Selector(self.canvas, "s2", self.x2, self.y1)
        self.s3_id = Selector(self.canvas, "s3", self.x2, self.y2)
        self.s4_id = Selector(self.canvas, "s4", self.x1, self.y2)

        self.sel_list = [self.s1_id, self.s2_id, self.s3_id, self.s4_id]
        for s in self.sel_list:
            self.canvas.itemconfig(s.id, state='hidden')

    def update_selectors(self):
        """Update the position of all selectors here"""
        self.s1_id.x, self.s1_id.y = self.x1, self.y1
        self.s1_id.update()

        self.s2_id.x, self.s2_id.y = self.x2, self.y1
        self.s2_id.update()

        self.s3_id.x, self.s3_id.y = self.x2, self.y2
        self.s3_id.update()

        self.s4_id.x, self.s4_id.y = self.x1, self.y2
        self.s4_id.update()

    def create_connectors(self):
        """Create connectors here"""
        # Calculate the shape geometry
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        center = Point(self.x1+w/2, self.y1+h/2)

        self.c1_id = Connector(self.canvas, "c1", center.x, center.y)          # Shape Center
        self.c2_id = Connector(self.canvas, "c2", center.x, center.y - h/2)    # Top Center
        self.c3_id = Connector(self.canvas, "c3", center.x + w/2, center.y)    # Right Center
        self.c4_id = Connector(self.canvas, "c4", center.x, center.y + h/2)    # Bottom Center
        self.c5_id = Connector(self.canvas, "c5", center.x - w/2, center.y)    # Left Center

        self.conn_list = [self.c1_id, self.c2_id, self.c3_id, self.c4_id, self.c5_id]
        for c in self.conn_list:
            self.canvas.itemconfig(c.id, state='hidden')

    def update_connectors(self):
        """Update the position of all connectors here"""
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        center = Point(self.x1+w/2, self.y1+h/2)

        self.c1_id.x, self.c1_id.y = center.x, center.y
        self.c1_id.update()

        self.c2_id.x, self.c2_id.y = center.x, center.y - h/2
        self.c2_id.update()

        self.c3_id.x, self.c3_id.y = center.x + w/2, center.y
        self.c3_id.update()

        self.c4_id.x, self.c4_id.y = center.x, center.y + h/2
        self.c4_id.update()

        self.c5_id.x, self.c5_id.y = center.x - w/2, center.y
        self.c5_id.update()

    def rotate(self):
        w, h = self.x2 - self.x1, self.y2 - self.y1
        center = Point(self.x1 + w / 2, self.y1 + h / 2)
        self.x1, self.y1 = center.x - h/2, center.y - w/2
        self.x2, self.y2 = center.x + h/2, center.y + w/2

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "s1":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            self.x1, self.y1 = x1, y1
        elif self.selector == "s2":
            x2 = event.x - offset_x2
            y1 = event.y - offset_y1
            x2, y1 = self.canvas.grid.snap_to_grid(x2, y1)
            self.x2, self.y1 = x2, y1
        elif self.selector == "s3":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.x2, self.y2 = x2, y2
        elif self.selector == "s4":
            x1 = event.x - offset_x1
            y2 = event.y - offset_y2
            x1, y2 = self.canvas.grid.snap_to_grid(x1, y2)
            self.x1, self.y2 = x1, y2


    def __repr__(self):
        return ("Oval: x1, y1, x2, y2 = " + "(" + str(self.x1) + ", " + str(self.y1) + ", " + str(self.y2) + ", " +
                str(self.y2) + ")\nfill color: " + self.fill_color + "\nborder_color: " + self.border_color +
                "\nborder_width: " + str(self.border_width))
