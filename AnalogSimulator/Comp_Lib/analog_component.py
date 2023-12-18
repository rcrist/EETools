from Comp_Lib.component import Component
from Comp_Lib.connector import Connector
from Helper_Lib import Point


class AnalogComponent(Component):
    """Universal model for analog components"""
    def __init__(self, canvas, comp_type, x1, y1, value=0):
        super().__init__(canvas, comp_type, x1, y1, value)

        self.conn_params = {
            'ports': {
                'resistor': 2,
                'capacitor': 2,
                'inductor': 2,
                'ground': 1,
                'dc_source': 2,
                'isource': 2,
                'ac_source': 2,
                'npn_transistor': 3
            },
            'conn_loc': {
                'resistor': 'ew',
                'capacitor': 'ew',
                'inductor': 'ew',
                'ground': 'n',
                'dc_source': 'ns',
                'isource': 'ns',
                'ac_source': 'ns',
                'npn_transistor': 'nsw'
            }
        }

        self.create()

    def create(self):
        self.set_image_filename()
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

    def create_connectors(self):
        # Calculate position of connectors from current comp position and size
        center, e, w, n, s = self.get_geometry()

        num_ports = self.conn_params['ports'][self.comp_type]
        if num_ports == 1:
            self.out = Connector(self.canvas, "in1", center.x, center.y)
            self.conn_list = [self.out]
        elif num_ports == 2:
            self.out = Connector(self.canvas, "out", center.x, center.y)
            self.in1 = Connector(self.canvas, "in1", center.x, center.y)
            self.conn_list = [self.in1, self.out]
        elif num_ports == 3:
            self.ba = Connector(self.canvas, "base", center.x, center.y)
            self.em = Connector(self.canvas, "emitter", center.x, center.y)
            self.co = Connector(self.canvas, "collector", center.x, center.y)
            self.conn_list = [self.ba, self.em, self.co]

    def update_connectors(self):
        """Update the position of connectors here"""
        center, e, w, n, s = self.get_geometry()

        conn_loc = self.conn_params['conn_loc'][self.comp_type]
        if conn_loc == 'ew':  # 2-port with ew ports
            self.calc_ew_conn_rotation(n, s, e, w)
        elif conn_loc == 'ns':  # 2-port with ns ports
            self.calc_ns_conn_rotation(n, s, e, w)
        elif conn_loc == 'n':  # 1-port with n port
            self.calc_n_conn_rotation(n, w)
        elif conn_loc == 'nsw':  # 3-port with nsw ports
            self.calc_nsw_conn_rotation(n, s, e, w)

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def calc_ew_conn_rotation(self, n, s, e, w):
        if self.angle == 0 or self.angle == 180:
            self.out.x, self.out.y = w.x, w.y
            self.in1.x, self.in1.y = e.x, e.y
        elif self.angle == 90 or self.angle == 270:
            self.out.x, self.out.y = n.x, n.y
            self.in1.x, self.in1.y = s.x, s.y

    def calc_ns_conn_rotation(self, n, s, e, w):
        if self.angle == 0 or self.angle == 180:
            self.out.x, self.out.y = n.x, n.y
            self.in1.x, self.in1.y = s.x, s.y
        elif self.angle == 90 or self.angle == 270:
            self.out.x, self.out.y = w.x, w.y
            self.in1.x, self.in1.y = e.x, e.y

    def calc_n_conn_rotation(self, n, w):
        if self.angle == 0 or self.angle == 180:
            self.out.x, self.out.y = n.x, n.y
        elif self.angle == 90 or self.angle == 270:
            self.out.x, self.out.y = w.x, w.y

    def calc_nsw_conn_rotation(self, n, s, e, w):
        if self.angle == 0 or self.angle == 180:
            self.em.x, self.em.y = n.x, n.y
            self.co.x, self.co.y = s.x, s.y
            self.ba.x, self.ba.y = w.x, w.y
        elif self.angle == 90 or self.angle == 270:
            self.em.x, self.em.y = w.x, w.y
            self.co.x, self.co.y = e.x, e.y
            self.ba.x, self.ba.y = s.x, s.y

    def get_geometry(self):
        sign = lambda angle: 1 if angle == 0 or angle == 180 else -1

        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        if self.comp_type == 'npn_transistor':
            e = Point(center.x + sign(self.angle) * w / 2, center.y)
            w = Point(center.x - sign(self.angle) * w / 2, center.y)
            n = Point(center.x + 20, center.y - sign(self.angle) * h / 2)
            s = Point(center.x + 20, center.y + sign(self.angle) * h / 2)
        else:
            e = Point(center.x - sign(self.angle) * w / 2, center.y)
            w = Point(center.x + sign(self.angle) * w / 2, center.y)
            n = Point(center.x, center.y - sign(self.angle) * h / 2)
            s = Point(center.x, center.y + sign(self.angle) * h / 2)

        return center, e, w, n, s

    def __repr__(self):
        if self.comp_type == "npn_transistor":
            return ("Type: " + self.comp_type + " Comp Text: " + self.comp_text + " x1: " + str(self.x1) +
                    " y1: " + str(self.y1) + " bf: " + str(self.bf) + " cjc: " + str(self.cjc) + " cjc_units: " +
                    self.cjc_units + " rb: " + str(self.rb) + " wire list: " + str(self.wire_list.__repr__()))
        else:
            return ("Type: " + self.comp_type + " Comp Text: " + self.comp_text + " x1: " + str(self.x1) + " y1: "
                    + str(self.y1) + " value: " + str(self.value) + " wire list: " + str(self.wire_list.__repr__()))

    def reprJson(self):
        if self.comp_type == "npn_transistor":
            return dict(type=self.comp_type, text=self.text, x1=self.x1, y1=self.y1, angle=self.angle,
                        bf=self.bf, cjc=self.cjc, cjc_units=self.cjc_units, rb=self.rb, wire_list=self.wire_list)
        else:
            return dict(type=self.comp_type, text=self.text, x1=self.x1, y1=self.y1, angle=self.angle,
                        value=self.value, units=self.units, wire_list=self.wire_list)
