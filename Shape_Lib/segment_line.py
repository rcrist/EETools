from Shape_Lib.selector import Selector
from Shape_Lib.shape import Shape


class SegmentLine(Shape):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.fill_color = "black"
        self.border_width = 3
        self.line_direction = self.canvas.line_direction
        self.type = "segment"

        self.seg1_id, self.seg2_id, self.seg3_id = None, None, None

        self.s1_id, self.s2_id = None, None

        self.create_shape()
        self.create_selectors()

    def create_shape(self):
        """Create the shape here"""
        w = self.x2 - self.x1
        h = self.y2 - self.y1

        if self.line_direction == "horizontal":
            self.id = self.canvas.create_line(self.x1, self.y1, self.x1 + w / 2, self.y1,
                                              self.x1 + w / 2, self.y1, self.x1 + w / 2, self.y2,
                                              self.x1 + w / 2, self.y2, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width)
        elif self.line_direction == "vertical":
            self.id = self.canvas.create_line(self.x1, self.y1, self.x1, self.y1 + h / 2,
                                              self.x1, self.y1 + h / 2, self.x2, self.y1 + h / 2,
                                              self.x2, self.y1 + h / 2, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width)

    def update(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1

        if self.line_direction == "horizontal":
            self.canvas.coords(self.id,self.x1, self.y1, self.x1 + w / 2, self.y1,
                               self.x1 + w / 2, self.y1, self.x1 + w / 2, self.y2,
                               self.x1 + w / 2, self.y2, self.x2, self.y2)
        elif self.line_direction == "vertical":
            self.canvas.coords(self.id, self.x1, self.y1, self.x1, self.y1 + h / 2,
                               self.x1, self.y1 + h / 2, self.x2, self.y1 + h / 2,
                               self.x2, self.y1 + h / 2, self.x2, self.y2)
        self.canvas.itemconfig(self.id, fill=self.fill_color)
        self.canvas.itemconfig(self.id, width=self.border_width)

        self.update_selectors()
        if self.is_selected:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='normal')
        else:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='hidden')

    def create_selectors(self):
        """Create four selectors at the corners here"""
        self.s1_id = Selector(self.canvas, "begin", self.x1, self.y1)
        self.s2_id = Selector(self.canvas, "end", self.x2, self.y2)

        self.sel_list = [self.s1_id, self.s2_id]
        for s in self.sel_list:
            self.canvas.itemconfig(s.id, state='hidden')

    def update_selectors(self):
        """Update the position of all selectors here"""
        self.s1_id.x, self.s1_id.y = self.x1, self.y1
        self.s1_id.update()

        self.s2_id.x, self.s2_id.y = self.x2, self.y2
        self.s2_id.update()

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "end":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            self.x2, self.y2 = x2, y2
        elif self.selector == "begin":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            self.x1, self.y1 = x1, y1

    def check_selector_hit(self, x, y):
        for sel in self.sel_list:
            if sel.selector_hit_test(x, y):
                return sel
        return None

    def __repr__(self):
        return "Line: x1, y1: " + str(self.x1) + ", " + str(self.y1) + " x2, y2: " + str(self.x2) + ", " + str(self.y2)
