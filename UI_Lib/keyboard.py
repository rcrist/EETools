class Keyboard:
    def __init__(self, parent, canvas):
        """Class to manage keyboard events"""
        self.parent = parent
        self.canvas = canvas
        self.selected_shape = None

        # Declare keyboard bindings
        self.parent.bind('<r>', self.rotate_shape)
        self.parent.bind('<h>', self.set_horizontal)
        self.parent.bind('<v>', self.set_vertical)

    def rotate_shape(self, _event):
        for s in self.canvas.shape_list:
            if s.is_selected:
                s.rotate()
        self.canvas.redraw_shapes()

    def set_horizontal(self, _event):
        self.canvas.line_direction = "horizontal"

    def set_vertical(self, _event):
        self.canvas.line_direction = "vertical"
