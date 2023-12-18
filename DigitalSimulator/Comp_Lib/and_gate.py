from pathlib import Path
from Comp_Lib.component import Comp
from Helper_Lib import Point
from Wire_Lib.connector import Connector


class AndGate(Comp):
    """And Gate Model"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)

        self.filename = Path(__file__).parent / "../images/gates/and_50x40.png"
        self.create_image(self.filename)
        self.update_bbox()
        self.create_selector()
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def create_connectors(self):
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 3 connectors: in1, in2, out
        self.out = Connector(self.canvas, "out", center.x + w / 2, center.y)
        self.in1 = Connector(self.canvas, "in1", center.x - w / 2, center.y - h/4)
        self.in2 = Connector(self.canvas, "in2", center.x - w / 2, center.y + h/4)

        # Update the connector list
        self.conn_list = [self.out, self.in1, self.in2]

    def update_connectors(self):
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        if self.angle == 0:
            self.out.x, self.out.y = center.x + w / 2, center.y
            self.in1.x, self.in1.y = center.x - w / 2, center.y - h/4
            self.in2.x, self.in2.y = center.x - w / 2, center.y + h/4
        elif self.angle == 90:
            self.out.x, self.out.y = center.x, center.y - h/2
            self.in1.x, self.in1.y = center.x + w / 4, center.y + h/2
            self.in2.x, self.in2.y = center.x - w / 4, center.y + h/2
        elif self.angle == 180:
            self.out.x, self.out.y = center.x - w / 2, center.y
            self.in1.x, self.in1.y = center.x + w / 2, center.y - h/4
            self.in2.x, self.in2.y = center.x + w / 2, center.y + h/4
        elif self.angle == 270:
            self.out.x, self.out.y = center.x, center.y + h / 2
            self.in1.x, self.in1.y = center.x + w / 4, center.y - h / 2
            self.in2.x, self.in2.y = center.x - w / 4, center.y - h / 2

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()
