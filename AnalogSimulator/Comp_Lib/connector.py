class Connector:
    def __init__(self, canvas, name, x, y):
        """Connector class"""
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y

        self.id = None

        self.radius = 5
        self.x1, self.y1, self.x2, self.y2 = (self.x - self.radius, self.y - self.radius,
                                              self.x + self.radius, self.y + self.radius)

        self.create_connector()

    def create_connector(self):
        # Create the connector here
        points = [self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius]
        self.id = self.canvas.create_oval(points, fill="white", outline="black", width=2, tags='connector')

    def update(self):
        """Update the connector here"""
        self.x1, self.y1, self.x2, self.y2 = (self.x - self.radius, self.y - self.radius,
                                              self.x + self.radius, self.y + self.radius)
        points = [self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius]
        self.canvas.coords(self.id, points)

    def set_pos(self, x, y):
        """Set the connector position here"""
        self.x = x
        self.y = y

    def connector_hit_test(self, x, y):
        """Connector hit test"""
        if self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
            return True
        else:
            return False

    def __repr__(self):
        return ("Connector: " + self.name + " (" + str(self.x1) + ", " + str(self.y1) + ")" +
                " (" + str(self.x2) + ", " + str(self.y2) + ")")
