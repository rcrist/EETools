from pathlib import Path
from PIL import Image

from Comp_Lib.component import Comp
from Wire_Lib.connector import Connector
from Helper_Lib import Point


class Switch(Comp):
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "switch"
        self.out_state = False  # OFF state
        self.subckt_conn = None

        self.filename_sw_on = Path(__file__).parent / "../images/switch/switch_on.png"
        self.on_image = Image.open(self.filename_sw_on)
        self.filename_sw_off = Path(__file__).parent / "../images/switch/switch_off.png"
        self.off_image = Image.open(self.filename_sw_off)
        self.filename = self.filename_sw_off

        self.create_image(self.filename)
        self.update_bbox()
        self.create_selector()

        # Create 2 connectors
        self.out1_id = None
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def toggle_switch(self):
        if self.filename == self.filename_sw_off:
            self.filename = self.filename_sw_on
        else:
            self.filename = self.filename_sw_off

    def create_connectors(self):  # Added new method
        """Create connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 1 connector: out1
        self.out1_id = Connector(self.canvas, "out", center.x + w / 2, center.y)
        self.conn_list = [self.out1_id]
        self.set_connector_visibility()

    def update_connectors(self):  # Added new method
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Update connector position based on angle
        if self.angle == 0:
            self.out1_id.x, self.out1_id.y = center.x + w / 2, center.y
        elif self.angle == 90:
            self.out1_id.x, self.out1_id.y = center.x, center.y - h / 2
        elif self.angle == 180:
            self.out1_id.x, self.out1_id.y = center.x - w / 2, center.y
        elif self.angle == 270:
            self.out1_id.x, self.out1_id.y = center.x, center.y + h / 2

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def toggle_state(self):
        self.out_state = not self.out_state
        self.toggle_switch()

        if self.wire_list:
            self.wire_list[0].wire_obj.state = self.out_state

    def __repr__(self):
        return "Switch: " + " x1: " + str(self.x1) + " y1: " + str(self.y1)

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
