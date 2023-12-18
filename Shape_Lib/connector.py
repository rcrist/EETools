class Connector:
    def __init__(self, canvas, name, x, y):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y

        self.radius = 5

    def conn_hit_test(self, event_x, event_y):
        x1, y1 = self.x - self.radius, self.y - self.radius
        x2, y2 = self.x + self.radius, self.y + self.radius
        if x1 <= event_x <= x2 and y1 <= event_y <= y2:
            return True
        else:
            return False

    def draw(self):
        conn_points = [self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius]
        self.canvas.create_oval(conn_points, fill="cyan", outline="black", width=2)

    def __repr__(self):
        return "Connector " + self.name + " x: " + str(self.x) + " y: " + str(self.y)
