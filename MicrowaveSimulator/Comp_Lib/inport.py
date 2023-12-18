from pathlib import Path

from Comp_Lib.component import Component
from Helper_Lib import Point
from Comp_Lib.connector import Connector


class Inport(Component):
    """Model for input port"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = 'inport'
        self.filename = Path(__file__).parent / "../images/ports/in_port.png"

        self.text = "In"
        self.text_id = None

        self.create()

    def create(self):
        self.create_image(self.filename)
        self.update_bbox()
        self.create_text()
        self.create_selector()
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_text()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def create_text(self):
        self.text_id = self.canvas.create_text(self.x1-35, self.y1,
                                text=self.text, fill="black",
                                font='Helvetica 10 bold',
                                angle=self.angle, tags="text")

    def update_text(self):
        self.canvas.coords(self.text_id, self.x1-35, self.y1)

    def create_connectors(self):  # Override base class method
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        self.out = Connector(self.canvas, "out", center.x + w / 2, center.y)

        # Update the connector list
        self.conn_list = [self.out]

    def update_connectors(self):  # Override base class method
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        if self.angle == 0:
            self.out.x, self.out.y = center.x + w / 2, center.y
        elif self.angle == 90:
            self.out.x, self.out.y = center.x, center.y - h / 2
        elif self.angle == 180:
            self.out.x, self.out.y = center.x - w / 2, center.y
        elif self.angle == 270:
            self.out.x, self.out.y = center.x, center.y + h / 2

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def __repr__(self):
        return ("Type: " + self.type + " x1: " + str(self.x1) + " y1: " + str(self.y1) +
                " wire list: " + str(self.wire_list.__repr__()))

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
