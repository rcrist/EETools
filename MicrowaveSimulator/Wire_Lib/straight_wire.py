from Wire_Lib.wire import Wire


class StraightWire(Wire):
    def __init__(self, canvas, x1, y1, x2, y2):
        super().__init__(canvas, x1, y1, x2, y2)
        self.type = 'straight'

        self.create_wire()
        self.create_selectors()
        self.update_selection()

    def create_wire(self):
        self.id = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=self.width)

    def update(self):
        self.update_position()
        self.update_selectors()
        self.update_selection()

    def update_position(self):
        self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)

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

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2, name=self.name)
