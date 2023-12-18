from Wire_Lib.wire import Wire


class ElbowWire(Wire):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.type = 'elbow'

        self.create_wire()
        self.update_bbox()
        self.create_selectors()
        self.update_selection()

    def create_wire(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1

        if abs(w) >= abs(h):  # Horizontal
            self.id = self.canvas.create_line(self.x1, self.y1, self.x2, self.y1,
                                              self.x2, self.y1, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width, tags="wire")
        else:  # Vertical
            self.id = self.canvas.create_line(self.x1, self.y1, self.x1, self.y2,
                                              self.x1, self.y2, self.x2, self.y2,
                                              fill=self.fill_color,
                                              width=self.border_width, tags="wire")

    def update(self):
        self.update_position()
        self.update_bbox()
        self.update_selectors()
        self.update_selection()

    def update_position(self):
        """Update the position when the gate object is moved"""
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        if abs(w) >= abs(h):
            self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y1,
                                        self.x2, self.y1, self.x2, self.y2)
        else:
            self.canvas.coords(self.id, self.x1, self.y1, self.x1, self.y2,
                                        self.x1, self.y2, self.x2, self.y2)

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2, name=self.name)
