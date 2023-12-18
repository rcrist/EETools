from IC_Lib.ic import IC
from Helper_Lib.point import Point
from Wire_Lib.connector import Connector
from Comp_Lib import Text


class Segment:
    def __init__(self, canvas, x1, y1, orientation):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.orientation = orientation

        if self.orientation == "H":
            self.w = 40
            self.h = 8
        elif self.orientation == "V":
            self.w = 8
            self.h = 35

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h
        self.id = None
        self.state = False

        self.create_segment()

    def create_segment(self):
        self.id = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="light gray")

    def update(self):
        self.update_position()
        self.update_color()

    def update_position(self):
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h
        """Update the position when the object is moved"""
        self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)

    def update_color(self):
        if self.state:
            self.canvas.itemconfig(self.id, fill="red")
        else:
            self.canvas.itemconfig(self.id, fill="light gray")


class SevenSegment(IC):
    """Model for 7-Segment Display - 7-pin package"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "7_segment"

        # IC dimensions
        self.w = 80
        self.h = 120
        self.bbox = None

        self.conn_inc = 15
        self.label_list = []
        self.logic_dict = {'a': False, 'b': False, 'c': False, 'd': False, 'e': False, 'f': False, 'g': False,
                           'EN': False}

        # Initialize shape ids
        self.id = None
        self.seg_a, self.seg_b, self.seg_c, self.seg_d, self.seg_e, self.seg_f, self.seg_g = (
            None, None, None, None, None, None, None)
        self.seg_list = []

        self.create_display()
        self.create_segments()
        self.update_bbox()
        self.create_selector()
        self.create_connectors()
        self.set_connector_visibility()
        self.create_labels()

    def create_display(self):
        # Assume black background with red segments
        self.id = self.canvas.create_rectangle(self.x1 - self.w/2, self.y1 - self.h/2,
                                               self.x1 + self.w/2, self.y1 + self.h/2,
                                               fill="black", outline="black", width=3, tags='display')

    def update(self):
        self.set_logic_level()
        self.update_position()
        self.update_bbox()
        self.update_segments()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()
        self.update_labels()

    def update_position(self):
        """Update the position when the object is moved"""
        self.canvas.coords(self.id, self.x1 - self.w/2, self.y1 - self.h/2,
                           self.x1 + self.w/2, self.y1 + self.h/2)

    def create_segments(self):
        # Horizontal segments
        self.seg_a = Segment(self.canvas, self.x1 - self.w/2 + 25, self.y1 - self.h/2 + 15, "H")
        self.seg_list.append(self.seg_a)
        self.seg_g = Segment(self.canvas, self.x1 - self.w/2 + 25, self.y1, "H")
        self.seg_list.append(self.seg_g)
        self.seg_d = Segment(self.canvas, self.x1 - self.w/2 + 25, self.y1 + self.h/2 - 15, "H")
        self.seg_list.append(self.seg_d)

        # Vertical segments
        self.seg_f = Segment(self.canvas, self.x1 - self.w/2 + 15, self.y1 - self.h/2 + 25, "V")
        self.seg_list.append(self.seg_f)
        self.seg_b = Segment(self.canvas, self.x1 + self.w/2 - 25, self.y1 - self.h/2 + 25, "V")
        self.seg_list.append(self.seg_b)
        self.seg_e = Segment(self.canvas, self.x1 - self.w/2 + 15, self.y1 + 10, "V")
        self.seg_list.append(self.seg_e)
        self.seg_c = Segment(self.canvas, self.x1 + self.w/2 - 25, self.y1 + 10, "V")
        self.seg_list.append(self.seg_c)

    def update_segments(self):
        self.seg_a.x1, self.seg_a.y1 = self.x1 - self.w/2 + 25, self.y1 - self.h/2 + 15
        self.seg_b.x1, self.seg_b.y1 = self.x1 + self.w/2 - 15, self.y1 - self.h/2 + 25
        self.seg_c.x1, self.seg_c.y1 = self.x1 + self.w/2 - 15, self.y1 + 10
        self.seg_d.x1, self.seg_d.y1 = self.x1 - self.w/2 + 25, self.y1 + self.h/2 - 15
        self.seg_e.x1, self.seg_e.y1 = self.x1 - self.w/2 + 15, self.y1 + 10
        self.seg_f.x1, self.seg_f.y1 = self.x1 - self.w/2 + 15, self.y1 - self.h/2 + 25
        self.seg_g.x1, self.seg_g.y1 = self.x1 - self.w/2 + 25, self.y1
        for s in self.seg_list:
            s.update()

    def create_connectors(self):
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc

        # Left side connectors
        self.conn_list.append(Connector(self.canvas, "a", center.x - w / 2, center.y - conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "b", center.x - w / 2, center.y - conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "c", center.x - w / 2, center.y - conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "d", center.x - w / 2, center.y))
        self.conn_list.append(Connector(self.canvas, "e", center.x - w / 2, center.y + conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "f", center.x - w / 2, center.y + conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "g", center.x - w / 2, center.y + conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "EN", center.x, center.y - h / 2))

    def update_connectors(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc

        self.conn_list[0].x, self.conn_list[0].y = center.x - w / 2, center.y - conn_inc * 3
        self.conn_list[1].x, self.conn_list[1].y = center.x - w / 2, center.y - conn_inc * 2
        self.conn_list[2].x, self.conn_list[2].y = center.x - w / 2, center.y - conn_inc * 1
        self.conn_list[3].x, self.conn_list[3].y = center.x - w / 2, center.y
        self.conn_list[4].x, self.conn_list[4].y = center.x - w / 2, center.y + conn_inc * 1
        self.conn_list[5].x, self.conn_list[5].y = center.x - w / 2, center.y + conn_inc * 2
        self.conn_list[6].x, self.conn_list[6].y = center.x - w / 2, center.y + conn_inc * 3

        self.conn_list[7].x, self.conn_list[7].y = center.x, center.y - h / 2

        # Draw the connectors
        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def create_labels(self):
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc
        pos = 10

        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y - conn_inc * 3,
                                    text='a', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y - conn_inc * 2,
                                    text='b', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y - conn_inc * 1,
                                    text='c', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y,
                                    text='d', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y + conn_inc * 1,
                                    text='e', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y + conn_inc * 2,
                                    text='f', fill="white"))
        self.label_list.append(Text(self.canvas, center.x - w / 2 + pos, center.y + conn_inc * 3,
                                    text='g', fill="white"))
        self.label_list.append(Text(self.canvas, center.x, center.y - h / 2  + pos,
                                    text='EN', fill="white"))

    def update_labels(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc
        pos = 10

        self.label_list[0].x1, self.label_list[0].y1 = center.x - w / 2 + pos, center.y - conn_inc * 3
        self.label_list[1].x1, self.label_list[1].y1 = center.x - w / 2 + pos, center.y - conn_inc * 2
        self.label_list[2].x1, self.label_list[2].y1 = center.x - w / 2 + pos, center.y - conn_inc * 1
        self.label_list[3].x1, self.label_list[3].y1 = center.x - w / 2 + pos, center.y
        self.label_list[4].x1, self.label_list[4].y1 = center.x - w / 2 + pos, center.y + conn_inc * 1
        self.label_list[5].x1, self.label_list[5].y1 = center.x - w / 2 + pos, center.y + conn_inc * 2
        self.label_list[6].x1, self.label_list[6].y1 = center.x - w / 2 + pos, center.y + conn_inc * 3
        self.label_list[7].x1, self.label_list[7].y1 = center.x, center.y - h / 2  + pos

        for label in self.label_list:
            self.canvas.coords(label.id, label.x1, label.y1)

    def set_logic_level(self):
        for wire in self.wire_list:
            if wire.connector_obj.name == "a":
                self.seg_a.state = wire.wire_obj.state
            elif wire.connector_obj.name == "b":
                self.seg_b.state = wire.wire_obj.state
            elif wire.connector_obj.name == "c":
                self.seg_c.state = wire.wire_obj.state
            elif wire.connector_obj.name == "d":
                self.seg_d.state = wire.wire_obj.state
            elif wire.connector_obj.name == "e":
                self.seg_e.state = wire.wire_obj.state
            elif wire.connector_obj.name == "f":
                self.seg_f.state = wire.wire_obj.state
            elif wire.connector_obj.name == "g":
                self.seg_g.state = wire.wire_obj.state
            elif wire.connector_obj.name == "EN":
                pass

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
