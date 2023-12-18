from pathlib import Path

from Wire_Lib.connector import Connector
from Comp_Lib.component import Comp
from Helper_Lib.point import Point


class LED(Comp):
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "led"
        self.state = False
        self.angle = 180

        self.led_color = self.canvas.led_color  # red, green, yellow, blue
        self.led_size = self.canvas.led_size  # small, large

        if self.led_size == "large":
            self.w = 40
            self.h = 40
            color_led_str = "../images/led/led_on_" + self.led_color + "_large.png"
            self.filename_led_on = Path(__file__).parent / color_led_str
            self.filename_led_off = Path(__file__).parent / "../images/led/led_off_large.png"
        elif self.led_size == "small":
            self.w = 20
            self.h = 20
            color_led_str = "../images/led/led_on_" + self.led_color + "_small.png"
            self.filename_led_on = Path(__file__).parent / color_led_str
            self.filename_led_off = Path(__file__).parent / "../images/led/led_off_small.png"
        self.filename = self.filename_led_off

        self.create_image(self.filename)
        self.update_bbox()
        self.create_selector()

        # Create 2 connectors
        self.in1_id = None
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.set_logic_level()
        self.update_led_color()
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def update_led_color(self):
        if self.state:
            self.filename = self.filename_led_on
        else:
            self.filename = self.filename_led_off

    def create_connectors(self):  # Added new method
        """Create connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 1 connector: out
        self.in1_id = Connector(self.canvas, "in", center.x - w / 2, center.y)
        self.conn_list = [self.in1_id]
        self.set_connector_visibility()

    def update_connectors(self):  # Added new method
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Update connector position based on angle
        if self.angle == 0:
            self.in1_id.x, self.in1_id.y = center.x + w / 2, center.y
        elif self.angle == 90:
            self.in1_id.x, self.in1_id.y = center.x, center.y - h / 2
        elif self.angle == 180:
            self.in1_id.x, self.in1_id.y = center.x - w / 2, center.y
        elif self.angle == 270:
            self.in1_id.x, self.in1_id.y = center.x, center.y + h / 2

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_logic_level(self):
        if self.wire_list:
            self.state = self.wire_list[0].wire_obj.state

    def __repr__(self):
        return "LED: " + " x1: " + str(self.x1) + " y1: " + str(self.y1)

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
