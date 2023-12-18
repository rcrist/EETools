class WireSelector:
    def __init__(self, canvas, name, x, y):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y

        self.radius = 5
        self.x1, self.y1, self.x2, self.y2 = (self.x - self.radius, self.y - self.radius,
                                              self.x + self.radius, self.y + self.radius)

        self.id = None
        self.create_selector()

    def create_selector(self):
        # Create the selector here
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
