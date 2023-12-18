class WireSelector:
    def __init__(self, canvas, name, x, y):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y
        self.is_selected = False

        self.id = self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5,
                                          state='normal', fill="white")

    def update(self):
        self.update_position()
        self.update_selection()

    def update_position(self):
        """Update the selector position"""
        sel_points = [self.x - 5, self.y - 5, self.x + 5, self.y + 5]
        self.canvas.coords(self.id, sel_points)

    def update_selection(self):
        if self.is_selected:
            self.canvas.itemconfigure(self.id, fill="yellow")
        else:
            self.canvas.itemconfigure(self.id, fill="white")

    def selector_hit_test(self, event_x, event_y):
        if self.x-5 <= event_x <= self.x+5 and self.y-5 <= event_y <= self.y+5:
            self.is_selected = True
            self.update_selection()
            return True
        else:
            self.is_selected = False
            self.update_selection()
            return False
