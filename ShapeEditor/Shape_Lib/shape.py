class Shape:
    def __init__(self, canvas, x1, y1, x2, y2, fill_color, border_color,
                 border_width):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

        self.id = None
        self.is_selected = False
        self.angle = 0
        self.scale = 1.0  # Default is 100% scale factor, range 0.1 to 10.0
