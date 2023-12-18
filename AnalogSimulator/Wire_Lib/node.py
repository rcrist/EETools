from Helper_Lib import Point
from Comp_Lib import Connector


class Node:
    def __init__(self, canvas, x1, y1):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1

        self.text = '0'
        self.comp_type = 'node'
        self.id = None
        self.text_id = None
        self.sel_id = None
        self.wire_list = []
        self.bbox = None
        self.angle = 0
        self.is_selected = False
        self.is_drawing = False
        self.conn = None
        self.conn_list = []

        self.create()

    def create(self):
        self.create_node()
        self.update_bbox()
        self.create_text()
        self.create_selector()
        self.create_connectors()
        self.set_connector_visibility()

    def create_node(self):
        self.id = self.canvas.create_oval(self.x1 - 5, self.y1 - 5, self.x1 + 5, self.y1 + 5, fill="black")

    def update_bbox(self):
        """Update the bounding box to get current gate coordinates"""
        self.bbox = self.canvas.bbox(self.id)

    def create_text(self):
        text_loc = Point(self.x1-10, self.y1-10)  # Put text above symbol
        self.text_id = self.canvas.create_text(text_loc.x, text_loc.y,
                                text=self.text, fill="black",
                                font='Helvetica 10 bold',
                                angle=self.angle, tags="text")

    def create_selector(self):
        """Create the red rectangle selector and check to see if the gate is selected"""
        x1, y1, x2, y2 = self.bbox[0] - 5, self.bbox[1] - 5, self.bbox[2] + 5, self.bbox[3] + 5
        self.sel_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=None, outline="red", width=2)
        self.set_selector_visibility()

    def set_selector_visibility(self):
        """Set the selector visibility state"""
        if self.is_selected:
            self.canvas.itemconfig(self.sel_id, state='normal')
        else:
            self.canvas.itemconfig(self.sel_id, state='hidden')

    def create_connectors(self):
        # Calculate position of connectors from current comp position and size
        center = self.get_geometry()

        self.conn = Connector(self.canvas, "conn", center.x, center.y)
        self.conn_list = [self.conn]

    def get_geometry(self):
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        return center

    def set_connector_visibility(self):
        """Set the connector visibility state"""
        if self.is_drawing:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='normal')
        else:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='hidden')

    def update(self):
        self.update_position()
        self.update_bbox()
        self.update_text()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def update_position(self):
        self.canvas.coords(self.id, self.x1 - 5, self.y1 - 5, self.x1 + 5, self.y1 + 5)  # Update position

    def update_text(self):
        self.canvas.itemconfig(self.text_id, text=self.text)
        self.canvas.coords(self.text_id, self.x1 - 10, self.y1 - 10)

    def update_selector(self):
        """Update the red rectangle selector coordinates and check to see if the gate is selected"""
        x1, y1, x2, y2 = self.bbox[0] - 5, self.bbox[1] - 5, self.bbox[2] + 5, self.bbox[3] + 5
        self.canvas.coords(self.sel_id, x1, y1, x2, y2)
        self.set_selector_visibility()

    def update_connectors(self):
        """Update the position of connectors here"""
        center = self.get_geometry()

        self.conn.x, self.conn.y = center.x, center.y

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def check_connector_hit(self, x, y):
        """Hit test to see if a connector is at the provided x, y coordinates"""
        for conn in self.conn_list:
            if conn.connector_hit_test(x, y):
                return conn
        return None

    def move_connected_wires(self):
        """Resize connected wires if the shape is moved"""
        for connection in self.wire_list:  # comp_conn, wire_name, wire_end
            for connector in self.conn_list:
                if connector.name == connection.comp_conn:
                    wire_obj = self.canvas.wire_dict[connection.wire_name]
                    if connection.wire_end == "begin":
                        wire_obj.x1 = connector.x
                        wire_obj.y1 = connector.y
                    elif connection.wire_end == "end":
                        wire_obj.x2 = connector.x
                        wire_obj.y2 = connector.y

    def rotate(self):
        """Set the rotation angle to the current angle + 90 deg, reset to 0 deg if angle > 270 deg"""
        self.angle += 90
        if self.angle > 270:
            self.angle = 0

    def hit_test(self, x, y):
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.is_selected = True
        else:
            self.is_selected = False

    def __repr__(self):
        return ("Type: " + self.comp_type + " Text: " + self.text + " x1: " + str(self.x1) + " y1: " +
                str(self.y1) + " wire list: " + str(self.wire_list.__repr__()))

    def reprJson(self):
        return dict(type=self.comp_type, text=self.text, x1=self.x1, y1=self.y1, angle=self.angle,
                    wire_list=self.wire_list)
