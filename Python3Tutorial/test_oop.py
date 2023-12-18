# Define a class
class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = (x, y)

        print("Shape Class initialized")

    def draw(self):
        print("Drawing shape at x,y:", self.loc)


class Rectangle(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)

        print("Rectangle Class initialized")

    def draw(self):
        print("Drawing rectangle at x,y:", self.loc)


# Instantiate the class object called rect
rect = Rectangle(10,10)

# Use the rect object
rect.draw()
