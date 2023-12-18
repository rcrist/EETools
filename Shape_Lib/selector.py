class Selector:
    def __init__(self, canvas, name, x, y):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y

        self.radius = 5

    def selector_hit_test(self, event_x, event_y):
        x1, y1 = self.x - self.radius, self.y - self.radius
        x2, y2 = self.x + self.radius, self.y + self.radius
        if x1 <= event_x <= x2 and y1 <= event_y <= y2:
            return True
        else:
            return False

    def draw(self):
        sel_points = [self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius]
        self.canvas.create_oval(sel_points, fill="red", outline="black", width=2)
