from pathlib import Path

from IC_Lib.ic import IC
from Helper_Lib.point import Point
from Wire_Lib.connector import Connector


class IC74161(IC):
    """Model for 74ls161 Counter IC - 16-pin package"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "ic74161"

        self.logic_dict = {}
        self.count_int = 0

        # Initialize 4 x D-flip flops
        self.d1, self.d2, self.d3, self.d4 = False, False, False, False

        # Set initial logic states
        for i in range(1, 17):  # 16 pin IC
            self.logic_dict['c' + str(i)] = False

        self.filename = Path(__file__).parent / "../images/ics/74161_easy_100x160.png"
        self.create_image(self.filename)
        self.update_bbox()
        self.create_selector()
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
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        self.conn_list.append(Connector(self.canvas, "c1", center.x + w/2, center.y - h/2 + 20))
        self.conn_list.append(Connector(self.canvas, "c2", center.x + w / 2, center.y - h / 2 + 30))
        self.conn_list.append(Connector(self.canvas, "c3", center.x + w / 2, center.y - h / 2 + 100))
        self.conn_list.append(Connector(self.canvas, "c4", center.x + w / 2, center.y - h / 2 + 110))
        self.conn_list.append(Connector(self.canvas, "c5", center.x + w / 2, center.y - h / 2 + 120))
        self.conn_list.append(Connector(self.canvas, "c6", center.x + w / 2, center.y - h / 2 + 130))
        self.conn_list.append(Connector(self.canvas, "c7", center.x + w / 2, center.y - h / 2 + 60))
        self.conn_list.append(Connector(self.canvas, "c10", center.x + w / 2, center.y - h / 2 + 70))

        self.conn_list.append(Connector(self.canvas, "c9", center.x - w / 2, center.y - h/2 + 20))
        self.conn_list.append(Connector(self.canvas, "c15", center.x - w / 2, center.y - h / 2 + 40))
        self.conn_list.append(Connector(self.canvas, "c11", center.x - w / 2, center.y - h / 2 + 70))
        self.conn_list.append(Connector(self.canvas, "c12", center.x - w / 2, center.y - h / 2 + 80))
        self.conn_list.append(Connector(self.canvas, "c13", center.x - w / 2, center.y - h / 2 + 90))
        self.conn_list.append(Connector(self.canvas, "c14", center.x - w / 2, center.y - h / 2 + 100))
        self.conn_list.append(Connector(self.canvas, "c8", center.x - w / 2, center.y - h / 2 + 130))
        self.conn_list.append(Connector(self.canvas, "c16", center.x - w / 2, center.y - h / 2 + 140))

    def update_connectors(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        self.conn_list[0].x, self.conn_list[0].y = center.x + w/2, center.y - h/2 + 20
        self.conn_list[1].x, self.conn_list[1].y = center.x + w / 2, center.y - h / 2 + 30
        self.conn_list[2].x, self.conn_list[2].y = center.x + w / 2, center.y - h / 2 + 100
        self.conn_list[3].x, self.conn_list[3].y = center.x + w / 2, center.y - h / 2 + 110
        self.conn_list[4].x, self.conn_list[4].y = center.x + w / 2, center.y - h / 2 + 120
        self.conn_list[5].x, self.conn_list[5].y = center.x + w / 2, center.y - h / 2 + 130
        self.conn_list[6].x, self.conn_list[6].y = center.x + w / 2, center.y - h / 2 + 60
        self.conn_list[7].x, self.conn_list[7].y = center.x + w / 2, center.y - h / 2 + 70

        self.conn_list[8].x, self.conn_list[8].y = center.x - w/2, center.y - h/2 + 20
        self.conn_list[9].x, self.conn_list[9].y = center.x - w / 2, center.y - h / 2 + 40
        self.conn_list[10].x, self.conn_list[10].y = center.x - w / 2, center.y - h / 2 + 70
        self.conn_list[11].x, self.conn_list[11].y = center.x - w / 2, center.y - h / 2 + 80
        self.conn_list[12].x, self.conn_list[12].y = center.x - w / 2, center.y - h / 2 + 90
        self.conn_list[13].x, self.conn_list[13].y = center.x - w / 2, center.y - h / 2 + 100
        self.conn_list[14].x, self.conn_list[14].y = center.x - w / 2, center.y - h / 2 + 130
        self.conn_list[15].x, self.conn_list[15].y = center.x - w / 2, center.y - h / 2 + 140

        # Draw the connectors
        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_logic_level(self):
        for wire in self.wire_list:
            print(wire, wire.connector_obj.name)
            if wire.connector_obj.name == "c1":  # CLR input
                self.logic_dict['c1'] = wire.wire_obj.state
                if not wire.wire_obj.state:
                    self.d1 = self.d2 = self.d3 = self.d4 = False
                    self.set_ABCD()
            elif wire.connector_obj.name == "c2":  # CLK input
                self.logic_dict['c2'] = wire.wire_obj.state
                if wire.wire_obj.state:
                    self.count_int = self.add_one(self.count_int)
                    binary = format(self.count_int, '04b')
                    self.parse_binary(binary)
                    self.set_ABCD()
            elif wire.connector_obj.name == "c3":  # Output A
                wire.wire_obj.state = self.logic_dict['c3']
            elif wire.connector_obj.name == "c4":  # Output B
                wire.wire_obj.state = self.logic_dict['c4']
            elif wire.connector_obj.name == "c5":  # Output C
                wire.wire_obj.state = self.logic_dict['c5']
            elif wire.connector_obj.name == "c6":  # Output D
                wire.wire_obj.state = self.logic_dict['c6']
            elif wire.connector_obj.name == "c7":  # ENP - enable input
                self.logic_dict['c7'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c10":  # ENT - enable input
                self.logic_dict['c10'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c8":  # GND - input
                self.logic_dict['c8'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c16":  # VCC - input
                self.logic_dict['c16'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c9":  # |LOAD - input
                self.logic_dict['c9'] = wire.wire_obj.state
                if not wire.wire_obj.state:
                    self.d1 = self.logic_dict["c14"]
                    self.d2 = self.logic_dict["c13"]
                    self.d3 = self.logic_dict["c12"]
                    self.d4 = self.logic_dict["c11"]
                    self.set_ABCD()
            elif wire.connector_obj.name == "c11":  # Qd - input
                self.logic_dict['c11'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c12":  # Qc - input
                self.logic_dict['c12'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c13":  # Qb - input
                self.logic_dict['c13'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c14":  # Qa - input
                self.logic_dict['c14'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c15":  # RCO - input
                self.logic_dict['c15'] = wire.wire_obj.state

    def set_ABCD(self):
        self.logic_dict['c3'] = self.d1
        self.logic_dict['c4'] = self.d2
        self.logic_dict['c5'] = self.d3
        self.logic_dict['c6'] = self.d4

    @staticmethod
    def add_one(num):
        num += 1
        if num > 15:
            num = 0
        # print("Count_int: ", num)
        return num

    def parse_binary(self, bin_num):
        result = lambda s: True if s == '1' else False
        self.d1 = result(bin_num[3])
        self.d2 = result(bin_num[2])
        self.d3 = result(bin_num[1])
        self.d4 = result(bin_num[0])

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
