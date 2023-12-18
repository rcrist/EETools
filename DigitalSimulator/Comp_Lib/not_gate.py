from pathlib import Path

from Comp_Lib.component import Comp
from Wire_Lib import Connector
from Helper_Lib import Point


class NotGate(Comp):
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.in_state = False
        self.out_state = True

        self.filename = Path(__file__).parent / "../images/gates/not_50x40.png"
        self.create_image(self.filename)
        self.update_bbox()
        self.create_selector()

        # Create 2 connectors
        self.in1_id, self.out1_id = None, None
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.set_logic_level()
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def create_connectors(self):
        """Create connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        self.out1_id = Connector(self.canvas, "out1", center.x + w / 2, center.y)  # Out1
        self.in1_id = Connector(self.canvas, "in1", center.x - w / 2, center.y)  # In1
        self.conn_list = [self.out1_id, self.in1_id]

    def update_connectors(self):
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        if self.angle == 0 or self.angle == 180:
            sign_x = lambda x: -1 if (self.angle == 180) else 1  # Lambda function to set sign of x
            self.out1_id.set_pos(center.x + sign_x(self.angle) * w / 2, center.y)
            self.in1_id.set_pos(center.x - sign_x(self.angle) * w / 2, center.y)
        elif self.angle == 90 or self.angle == 270:
            sign_y = lambda y: -1 if (self.angle == 270) else 1  # Lambda function to set sign of y
            self.out1_id.set_pos(center.x, center.y - sign_y(self.angle) * h / 2)
            self.in1_id.set_pos(center.x, center.y + sign_y(self.angle) * h / 2)

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_logic_level(self):
        for wire in self.wire_list:
            if wire.connector_obj.name == "in1":
                self.in_state = wire.wire_obj.state
                self.out_state = not self.in_state
            elif wire.connector_obj.name == "out1":
                wire.wire_obj.state = self.out_state
