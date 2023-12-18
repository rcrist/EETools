from Shape_Lib.shape import Shape


class Oval(Shape):
    def __init__(self, canvas, x1, y1, x2, y2, fill_color="white",
                 border_color="black", border_width=3):
        super().__init__(canvas, x1, y1, x2, y2, fill_color, border_color,
                 border_width)

    def draw(self):
        w, h = self.x2 - self.x1, self.y2 - self.y1
        w = w * self.scale
        h = h * self.scale
        center = self.x1 + w/2, self.y1 + h/2
        if self.angle == 90 or self.angle == 180:
            points = [center[0] - h/2, center[1] - w/2,
                      center[0] + h/2, center[1] + w/2]
        else:
            points = [center[0] - w/2, center[1] - h/2,
                      center[0] + w/2, center[1] + h/2]

        self.id = self.canvas.create_oval(points,
                                   fill=self.fill_color,
                                   outline=self.border_color,
                                   width=self.border_width)

        if self.is_selected:
            sel_points = [points[0]-5, points[1]-5,
                          points[2]+5, points[3]+5]
            self.canvas.create_rectangle(sel_points, fill=None,
                                         outline="red", width=2)
