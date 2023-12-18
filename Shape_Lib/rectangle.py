from Shape_Lib.shape import Shape
from Shape_Lib.selector import Selector
from Shape_Lib.connector import Connector
from Helper_Lib.point import Point


class Rectangle(Shape):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.selector = None

        self.fill_color = "cyan"
        self.border_color = "black"
        self.border_width = 3

        # Create 4 selectors
        self.s1, self.s2, self.s3, self.s4 = None, None, None, None
        self.create_selectors()

        # Create 5 connectors
        self.c1, self.c2, self.c3, self.c4, self.c5 = None, None, None, None, None
        self.create_connectors()

    def draw(self):
        self.points = [self.x1, self.y1, self.x2, self.y2]
        self.canvas.create_rectangle(self.points, fill=self.fill_color, outline=self.border_color,
                                     width=self.border_width)

        if self.is_selected:
            self.draw_selectors()
            self.draw_connectors()

        if self.canvas.mouse.mode == "line_draw":
            self.draw_connectors()

    def create_selectors(self):
        # Calculate position of selectors from current shape position
        x1, y1, x2, y2 = self.points

        # Create 4 selector objects: 4 corner of shape
        self.s1 = Selector(self.canvas, "s1", x1, y1)
        self.s2 = Selector(self.canvas, "s2", x2, y1)
        self.s3 = Selector(self.canvas, "s3", x2, y2)
        self.s4 = Selector(self.canvas, "s4", x1, y2)

        # Update the selector list
        self.sel_list = [self.s1, self.s2, self.s3, self.s4]

    def draw_selectors(self):
        # Recalculate position of selectors from current shape position
        x1, y1, x2, y2 = self.points

        # Define 5 selectors: 4 shape corner - number of selectors is unique to each shape
        self.s1.x, self.s1.y = x1, y1
        self.s2.x, self.s2.y = x2, y1
        self.s3.x, self.s3.y = x2, y2
        self.s4.x, self.s4.y = x1, y2

        # Draw the selectors
        for s in self.sel_list:
            s.draw()

    def create_connectors(self):
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.points
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 5 connectors: shape center, 4 side centers - number of connectors is unique to each shape
        self.c1 = Connector(self.canvas, "c1", center.x, center.y)
        self.c2 = Connector(self.canvas, "c2", center.x, center.y - h / 2)
        self.c3 = Connector(self.canvas, "c3", center.x + w / 2, center.y)
        self.c4 = Connector(self.canvas, "c4", center.x, center.y + h / 2)
        self.c5 = Connector(self.canvas, "c5", center.x - w / 2, center.y)

        # Update the connector list
        self.conn_list = [self.c1, self.c2, self.c3, self.c4, self.c5]

    def draw_connectors(self):
        # Recalculate position of connectors from current shape position and size
        self.points = [self.x1, self.y1, self.x2, self.y2]
        x1, y1, x2, y2 = self.points
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 5 connectors: shape center, 4 side centers - number of connectors is unique to each shape
        self.c1.x, self.c1.y = center.x, center.y
        self.c2.x, self.c2.y = center.x, center.y - h / 2
        self.c3.x, self.c3.y = center.x + w / 2, center.y
        self.c4.x, self.c4.y = center.x, center.y + h / 2
        self.c5.x, self.c5.y = center.x - w / 2, center.y

        # Draw the connectors
        for c in self.conn_list:
            c.draw()

        self.move_connected_lines()

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
