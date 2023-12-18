from pathlib import Path

from IC_Lib.ic import IC
from Helper_Lib.point import Point
from Wire_Lib.connector import Connector


class IC28C16(IC):
    """Model for 28C16 2K x 8-Bit EEPROM - 24-pin package"""
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "ic28C16"

        self.logic_dict = {}
        self.conn_inc = 15
        self.offset = -5

        # Set initial logic states
        for i in range(1, 25):  # 24 pin IC
            self.logic_dict['c' + str(i)] = False

        self.zero, self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight, self.nine = (
            None, None, None, None, None, None, None, None, None, None)
        self.set_display_data()

        self.filename = Path(__file__).parent / "../images/ics/28C16_easy_100x190.png"
        self.create_ic()

        # Define program for Display 0-1
        self.program1 = {
            '0000': self.zero,
            '0001': self.zero,
            '0010': self.zero,
            '0011': self.zero,
            '0100': self.zero,
            '0101': self.zero,
            '0110': self.zero,
            '0111': self.zero,
            '1000': self.zero,
            '1001': self.zero,
            '1010': self.one,
            '1011': self.one,
            '1100': self.one,
            '1101': self.one,
            '1110': self.one,
            '1111': self.one
        }

        # Define program for Display 0-9
        self.program2 = {
            '0000': self.zero,
            '0001': self.one,
            '0010': self.two,
            '0011': self.three,
            '0100': self.four,
            '0101': self.five,
            '0110': self.six,
            '0111': self.seven,
            '1000': self.eight,
            '1001': self.nine,
            '1010': self.zero,
            '1011': self.one,
            '1100': self.two,
            '1101': self.three,
            '1110': self.four,
            '1111': self.five
        }

    def set_display_data(self):
        # Set output for a, b, c, d, e, f, g on the display
        self.zero = [True, True, True, True, True, True, False]
        self.one = [False, True, True, False, False, False, False]
        self.two = [True, True, False, True, True, False, True]
        self.three = [True, True, True, True, False, False, True]
        self.four = [False, True, True, False, False, True, True]
        self.five = [True, False, True, True, False, True, True]
        self.six = [True, False, True, True, True, True, True]
        self.seven = [True, True, True, False, False, False, False]
        self.eight = [True, True, True, True, True, True, True]
        self.nine = [True, True, True, False, False, True, True]

    def create_ic(self):
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
        self.conn_list.append(Connector(self.canvas, "c8", center.x - w / 2, center.y - h / 2 +
                                        offset + conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "c7", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "c6", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "c5", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 4))
        self.conn_list.append(Connector(self.canvas, "c4", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 5))
        self.conn_list.append(Connector(self.canvas, "c3", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 6))
        self.conn_list.append(Connector(self.canvas, "c2", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 7))
        self.conn_list.append(Connector(self.canvas, "c1", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 8))
        self.conn_list.append(Connector(self.canvas, "c23", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 9))
        self.conn_list.append(Connector(self.canvas, "c22", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 10))
        self.conn_list.append(Connector(self.canvas, "c19", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 11))
        self.conn_list.append(Connector(self.canvas, "c12", center.x - w / 2, center.y - h / 2 + offset +
                                        conn_inc * 12))

        # Right side connectors
        self.conn_list.append(Connector(self.canvas, "c24", center.x + w / 2, center.y - h/2 + offset +
                                        conn_inc * 1))
        self.conn_list.append(Connector(self.canvas, "c9", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 2))
        self.conn_list.append(Connector(self.canvas, "c10", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 3))
        self.conn_list.append(Connector(self.canvas, "c11", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 4))
        self.conn_list.append(Connector(self.canvas, "c13", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 5))
        self.conn_list.append(Connector(self.canvas, "c14", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 6))
        self.conn_list.append(Connector(self.canvas, "c15", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 7))
        self.conn_list.append(Connector(self.canvas, "c16", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 8))
        self.conn_list.append(Connector(self.canvas, "c17", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 9))
        self.conn_list.append(Connector(self.canvas, "c18", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 10))
        self.conn_list.append(Connector(self.canvas, "c20", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 11))
        self.conn_list.append(Connector(self.canvas, "c21", center.x + w / 2, center.y - h / 2 + offset +
                                        conn_inc * 12))

    def update_connectors(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)
        conn_inc = self.conn_inc
        offset = self.offset

        # Update left side pins
        for i in range(0, 12):
            self.conn_list[i].x, self.conn_list[i].y = (center.x - w / 2, center.y - h / 2 +
                                                        offset + conn_inc * (i+1))

        # Update right side pins
        for j in range(0, 12):
            self.conn_list[j+12].x, self.conn_list[j+12].y = (center.x + w / 2, center.y - h / 2 +
                                                              offset + conn_inc * (j+1))

        # Draw the connectors
        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_logic_level(self):
        for wire in self.wire_list:
            if wire.connector_obj.name == "c1":
                self.logic_dict['c1'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c2":
                self.logic_dict['c2'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c3":
                self.logic_dict['c3'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c4":
                self.logic_dict['c4'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c5":
                self.logic_dict['c5'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c6":
                self.logic_dict['c6'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c7":
                self.logic_dict['c7'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c8":
                self.logic_dict['c8'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c9":  # I/O 0
                wire.wire_obj.state = self.logic_dict['c9']
            elif wire.connector_obj.name == "c10":  # I/O 1
                wire.wire_obj.state = self.logic_dict['c10']
            elif wire.connector_obj.name == "c11":  # I/O 2
                wire.wire_obj.state = self.logic_dict['c11']
            elif wire.connector_obj.name == "c12":  # VSS = GND
                self.logic_dict['c12'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c13":  # I/O 3
                wire.wire_obj.state = self.logic_dict['c13']
            elif wire.connector_obj.name == "c14":  # I/O 4
                wire.wire_obj.state = self.logic_dict['c14']
            elif wire.connector_obj.name == "c15":  # I/O 5
                wire.wire_obj.state = self.logic_dict['c15']
            elif wire.connector_obj.name == "c16":  # I/O 6
                wire.wire_obj.state = self.logic_dict['c16']
            elif wire.connector_obj.name == "c17":  # I/O 7
                wire.wire_obj.state = self.logic_dict['c17']
            elif wire.connector_obj.name == "c18":  # !CE
                self.logic_dict['c18'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c19":  # A10
                self.logic_dict['c19'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c20":  # !OE
                self.logic_dict['c20'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c21":  # !WE
                self.logic_dict['c21'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c22":  # A9
                self.logic_dict['c22'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c23":  # A8
                self.logic_dict['c23'] = wire.wire_obj.state
            elif wire.connector_obj.name == "c24":  # VCC
                self.logic_dict['c24'] = wire.wire_obj.state

            key, ps = self.convert_address_to_key()
            if ps is True:  # Select program #1
                io = self.program1[key]
            else:  # Select program #2
                io = self.program2[key]

            self.set_io_output(io)

    def convert_address_to_key(self):
        a0 = self.logic_dict['c8']  # Counter bit 0
        a1 = self.logic_dict['c7']  # Counter bit 1
        a2 = self.logic_dict['c6']  # Counter bit 2
        a3 = self.logic_dict['c5']  # Counter bit 3

        ps = self.logic_dict['c4']  # EEPROM Program Select

        result = lambda s: '1' if s is True else '0'
        k0 = result(a0)
        k1 = result(a1)
        k2 = result(a2)
        k3 = result(a3)
        key = k3 + k2 + k1 + k0
        return key, ps

    def set_io_output(self, io):
        self.logic_dict['c9']  = io[0]  # i/o 0 = a
        self.logic_dict['c10']  = io[1]  # i/o 1 = b
        self.logic_dict['c11']  = io[2]  # i/o 2 = c
        self.logic_dict['c13']  = io[3]  # i/o 3 = d
        self.logic_dict['c14']  = io[4]  # i/o 4 = e
        self.logic_dict['c15']  = io[5]  # i/o 5 = f
        self.logic_dict['c16']  = io[6]  # i/o 6 = g
        self.logic_dict['c17']  = False  # Not Used

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, wire_list=self.wire_list)
