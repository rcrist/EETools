class Selector:
    def __init__(self, a_canvas, name, _x, _y):
        self.canvas = a_canvas
        self.name = name
        self.x = _x
        self.y = _y

        self.radius = 5
        self.x1, self.y1, self.x2, self.y2 = (self.x - self.radius, self.y - self.radius,
                                              self.x + self.radius, self.y + self.radius)

        self.id = None
        self.create()

    def create(self):
        """Create the shape here"""
        sel_points = [self.x1, self.y1, self.x2, self.y2]
        self.id = self.canvas.create_oval(sel_points, fill="red", outline="black", width=2, tags='selector')

    def update(self):
        """Update the shape here"""
        self.x1, self.y1, self.x2, self.y2 = (self.x - self.radius, self.y - self.radius,
                                              self.x + self.radius, self.y + self.radius)
        sel_points = [self.x1, self.y1, self.x2, self.y2]
        self.canvas.coords(self.id, sel_points)

    def selector_hit_test(self, event_x, event_y):
        if self.x1 <= event_x <= self.x2 and self.y1 <= event_y <= self.y2:
            return True
        else:
            return False

    def __repr__(self):
        return ("Selector: " + self.name + " (" + str(self.x1) + ", " + str(self.y1) + ")" +
                " (" + str(self.x2) + ", " + str(self.y2) + ")")
