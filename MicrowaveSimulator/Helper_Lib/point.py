class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
    # Test block
    pt1 = Point(10, 10)
    pt2 = Point(100, 100)
    print("pt1: ", pt1)
    print("pt2: ", pt2)
