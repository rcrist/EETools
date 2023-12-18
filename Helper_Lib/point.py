class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point: (" + str(self.x) + ", " + str(self.y) + ")"

