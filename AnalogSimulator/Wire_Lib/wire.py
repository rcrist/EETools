from Wire_Lib.wire_selector import WireSelector


class Wire:
    """Base class for wire classes"""
    def __init__(self, canvas, wire_type, x1, y1, x2, y2):
        self.canvas = canvas
        self.wire_type = wire_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.fill_color = "black"
        self.border_width = 2
        self.wire_dir = self.canvas.wire_dir

        self.name = None
        self.id = None
        self.is_selected = False
        self.selector = None
        self.width = 2
        self.bbox = None
        self.node_num = '0'

        # Connections for wire list
        self.in_cnx = None
        self.out_cnx = None
        self.cnx = []

        self.sel1, self.sel2 = None, None

    def update_bbox(self):
        self.bbox = self.canvas.bbox(self.id)

    def create_selectors(self):
        self.sel1 = WireSelector(self.canvas, "begin", self.x1, self.y1)
        self.sel2 = WireSelector(self.canvas, "end", self.x2, self.y2)

    def update_selectors(self):
        self.sel1.x, self.sel1.y = self.x1, self.y1
        self.sel2.x, self.sel2.y = self.x2, self.y2
        self.sel1.update()
        self.sel2.update()

    def update_selection(self):
        if self.is_selected:
            self.canvas.itemconfigure(self.id, fill="red")
            self.canvas.itemconfigure(self.sel1.id, state='normal')
            self.canvas.itemconfigure(self.sel2.id, state='normal')
        else:
            self.canvas.itemconfigure(self.id, fill="black")
            self.canvas.itemconfigure(self.sel1.id, state='hidden')
            self.canvas.itemconfigure(self.sel2.id, state='hidden')

    def hit_test(self, x, y):
        x1, y1 = self.bbox[0], self.bbox[1]
        x2, y2 = self.bbox[2], self.bbox[3]
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.is_selected = True
        else:
            self.is_selected = False

    def sel_hit_test(self, x, y):
        if self.sel1.selector_hit_test(x, y):
            self.selector = self.sel1.name
            return self.sel1
        elif self.sel2.selector_hit_test(x, y):
            self.selector = self.sel2.name
            return self.sel2
        else:
            return None

    def resize(self, offsets, event):
        offset_x1, offset_y1, offset_x2, offset_y2 = offsets
        if self.selector == "end":
            x2 = event.x - offset_x2
            y2 = event.y - offset_y2
            self.x2, self.y2 = x2, y2
            self.x2, self.y2 = self.canvas.grid.snap_to_grid(self.x2, self.y2)
        elif self.selector == "begin":
            x1 = event.x - offset_x1
            y1 = event.y - offset_y1
            self.x1, self.y1 = x1, y1
            self.x1, self.y1 = self.canvas.grid.snap_to_grid(self.x1, self.y1)

    def set_node_num(self, node_num):
        self.node_num = node_num
