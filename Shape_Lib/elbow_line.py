from Shape_Lib.shape import Shape
from Shape_Lib.selector import Selector


class ElbowLine(Shape):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.selector = None
        self.segment_list = None
        self.line_direction = self.canvas.line_direction

        self.fill_color = "black"
        self.border_width = 3

        # Create 2 selectors
        self.s1, self.s2 = None, None
        self.create_selectors()

    def draw(self):
        self.points = [self.x1, self.y1, self.x2, self.y2]
        self.create_elbow_line()

        if self.is_selected:
            self.draw_selectors()

    def create_elbow_line(self):
        segment1, segment2 = None, None
        if self.line_direction == "horizontal":
            segment1 = self.x1, self.y1, self.x2, self.y1
            segment2 = self.x2, self.y1, self.x2, self.y2
        elif self.line_direction == "vertical":
            segment1 = self.x1, self.y1, self.x1, self.y2
            segment2 = self.x1, self.y2, self.x2, self.y2
        self.segment_list = [segment1, segment2]
        self.draw_segments()

    def draw_segments(self):
        for s in self.segment_list:
            self.canvas.create_line(s, fill=self.fill_color, width=self.border_width)

    def check_connector_hit(self, x, y):
        pass

    def create_selectors(self):
        # Calculate position of selectors from current shape position
        x1, y1, x2, y2 = self.points

        # Create 2 selector objects: 2 ends of the line
        self.s1 = Selector(self.canvas, "begin", x1, y1)
        self.s2 = Selector(self.canvas, "end", x2, y2)

        # Update the selector list
        self.sel_list = [self.s1, self.s2]

    def draw_selectors(self):
        # Recalculate position of selectors from current shape position
        x1, y1, x2, y2 = self.points

        # Define 2 selectors: 2 ends of the line
        self.s1.x, self.s1.y = x1, y1
        self.s2.x, self.s2.y = x2, y2

        # Draw the selectors
        for s in self.sel_list:
            s.draw()

    def move(self):
        pass

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "end":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            x2, y2 = self.canvas.grid.snap_to_grid(x2, y2)
            self.x2, self.y2 = x2, y2
            self.canvas.mouse.select_connector(self, "end", x2, y2)
        elif self.selector == "begin":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            x1, y1 = self.canvas.grid.snap_to_grid(x1, y1)
            self.x1, self.y1 = x1, y1
            self.canvas.mouse.select_connector(self, "begin", x1, y1)

    def __repr__(self):
        return "Line: x1, y1: " + str(self.x1) + ", " + str(self.y1) + " x2, y2: " + str(self.x2) + ", " + str(self.y2)
