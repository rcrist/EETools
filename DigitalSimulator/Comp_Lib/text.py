from Comp_Lib.component import Comp


class Text(Comp):
    def __init__(self, canvas, x1, y1, text='Hello World', fill="black"):
        super().__init__(canvas, x1, y1)
        self.type = "text"
        self.text = text

        self.fill_color = fill
        self.border_color = "black"
        self.border_width = 3

        self.id = self.canvas.create_text(self.x1, self.y1,
                                text=self.text, fill=self.fill_color,
                                font='Helvetica 8 bold',
                                angle=self.angle, tags="text")

        self.update_bbox()
        self.create_selector()

    def update(self):
        self.update_position()
        self.update_rotation()
        self.update_bbox()
        self.update_selector()

    def update_rotation(self):
        self.canvas.itemconfig(self.id, angle=self.angle)

