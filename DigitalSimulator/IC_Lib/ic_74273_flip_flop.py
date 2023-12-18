from pathlib import Path

from IC_Lib.ic import IC
from Helper_Lib.point import Point
from Wire_Lib.connector import Connector


class DFlipFlop:
    """Logical model for D Flip-Flop"""
    def __init__(self):
        self.R = False  # Clear
        self.C1 = False  # Clock
        self.D1 = False  # D Input
        self.Q1 = False  # Q Output

    def clear_ic(self):
        self.Q1 = False

    def clock_high(self):
        self.Q1 = self.D1

    def __repr__(self):
        return ("D Flip-Flop: " + "R: " + str(self.R) + " C1: " + str(self.C1) +
                " D1: " + str(self.D1) + " Q1: " + str(self.Q1))


class IC74273(IC):
    """Model for 74ls273 Quad D Flip-Flop IC - 20-pin package"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "ic74273"

        self.logic_dict = {}
        self.count_int = 0
        self.conn_inc = 15
        self.offset = -5

        # Initialize 8 x D-flip flops
        self.d1 = DFlipFlop()
        self.d2 = DFlipFlop()
        self.d3 = DFlipFlop()
        self.d4 = DFlipFlop()
        self.d5 = DFlipFlop()
        self.d6 = DFlipFlop()
        self.d7 = DFlipFlop()
        self.d8 = DFlipFlop()
        self.ff_list = [self.d1, self.d2, self.d3, self.d4, self.d5, self.d6, self.d7, self.d8]

        # Set initial logic states
        for i in range(1, 21):  # 20 pin IC
            self.logic_dict['c' + str(i)] = False

        self.filename = Path(__file__).parent / "../images/ics/74273_easy_100x155.png"
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
        conn_inc = self.conn_inc
        offset = self.offset

        # Note: Connector names correspond to pin-numbers, c1 = pin 1
        # Left side connectors
        self.conn_list.append(Connector(self.canvas, "c1", center.x - w / 2, center.y - h / 2 +
                                        offset + conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "c3", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "c4", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "c7", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 4))
        self.conn_list.append(Connector(self.canvas, "c8", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 5))
        self.conn_list.append(Connector(self.canvas, "c13", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 6))
        self.conn_list.append(Connector(self.canvas, "c14", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 7))
        self.conn_list.append(Connector(self.canvas, "c17", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 8))
        self.conn_list.append(Connector(self.canvas, "c18", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 9))
        self.conn_list.append(Connector(self.canvas, "c10", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 10))

        # Right side connectors
        self.conn_list.append(Connector(self.canvas, "c20", center.x + w / 2, center.y - h/2 + offset +
                                        conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "c2", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "c5", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "c6", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 4))
        self.conn_list.append(Connector(self.canvas, "c9", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 5))
        self.conn_list.append(Connector(self.canvas, "c12", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 6))
        self.conn_list.append(Connector(self.canvas, "c15", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 7))
        self.conn_list.append(Connector(self.canvas, "c16", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 8))
        self.conn_list.append(Connector(self.canvas, "c19", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 9))
        self.conn_list.append(Connector(self.canvas, "c11", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 10))

    def update_connectors(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc
        offset = self.offset

        # Update left side pins
        for i in range(0, 10):
            self.conn_list[i].x, self.conn_list[i].y = (center.x - w / 2, center.y - h / 2 +
                                                        offset + conn_inc * (i+1))

        # Update right side pins
        for j in range(0, 10):
            self.conn_list[j+10].x, self.conn_list[j+10].y = (center.x + w / 2, center.y - h / 2 +
                                                              offset + conn_inc * (j+1))

        # Draw the connectors
        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_logic_level(self):
        for wire in self.wire_list:
            # print(wire.connector_obj.name)
            if wire.connector_obj.name == "c1":  # CLR input
                self.logic_dict['c1'] = wire.wire_obj.state
                if not wire.wire_obj.state:
                    for ff in self.ff_list:
                        ff.clear_ic()
                    self.set_q_outputs()
            elif wire.connector_obj.name == "c11":  # CLK input
                self.logic_dict['c9'] = wire.wire_obj.state
                if wire.wire_obj.state:
                    for ff in self.ff_list:
                        ff.Q1 = ff.D1
                    self.set_q_outputs()
            elif wire.connector_obj.name == "c2":  # 1Q output
                wire.wire_obj.state = self.logic_dict['c2']
            elif wire.connector_obj.name == "c3":  # 1D input
                self.d1.D1 = wire.wire_obj.state
                self.logic_dict['c3'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c4":  # 2D input
                self.d2.D1 = wire.wire_obj.state
                self.logic_dict['c4'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c5":  # 2Q Output
                wire.wire_obj.state = self.logic_dict['c5']
            elif wire.connector_obj.name == "c6":  # 3Q Output
                wire.wire_obj.state = self.logic_dict['c6']
            elif wire.connector_obj.name == "c7":  # 3D input
                self.d3.D1 = wire.wire_obj.state
                self.logic_dict['c7'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c8":  # 4D input
                self.d4.D1 = wire.wire_obj.state
                self.logic_dict['c8'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c9":  # 4Q output
                wire.wire_obj.state = self.logic_dict['c9']
            elif wire.connector_obj.name == "c10":  # GND - input
                self.logic_dict['c10'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c12":  # 5Q output
                wire.wire_obj.state = self.logic_dict['c12']
            elif wire.connector_obj.name == "c13":  # 5D input
                self.d5.D1 = wire.wire_obj.state
                self.logic_dict['c13'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c14":  # 6D input
                self.d6.D1 = wire.wire_obj.state
                self.logic_dict['c14'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c15":  # 6Q output
                wire.wire_obj.state = self.logic_dict['c15']
            elif wire.connector_obj.name == "c16":  # 7Q output
                wire.wire_obj.state = self.logic_dict['c16']
            elif wire.connector_obj.name == "c17":  # 7D input
                self.d7.D1 = wire.wire_obj.state
                self.logic_dict['c17'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c18":  # 8D input
                self.d8.D1 = wire.wire_obj.state
                self.logic_dict['c18'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c19":  # 8Q output
                wire.wire_obj.state = self.logic_dict['c19']
            elif wire.connector_obj.name == "c20":  # VCC input
                self.logic_dict['c20'] = wire.wire_obj.state

    def set_q_outputs(self):
        self.logic_dict['c2'] = self.d1.Q1  # 1Q
        self.logic_dict['c5'] = self.d2.Q1  # 2Q
        self.logic_dict['c6'] = self.d3.Q1  # 3Q
        self.logic_dict['c9'] = self.d4.Q1  # 4Q
        self.logic_dict['c12'] = self.d1.Q1  # 5Q
        self.logic_dict['c15'] = self.d2.Q1  # 6Q
        self.logic_dict['c16'] = self.d3.Q1  # 7Q
        self.logic_dict['c19'] = self.d4.Q1  # 8Q
