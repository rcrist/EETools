import tkinter as tk
from PIL import Image, ImageTk

from Helper_Lib import Point
from Comp_Lib.connector import Connector


class Component:
    def __init__(self, canvas, x1, y1):
        """Base class for component classes"""
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1

        self.id = None
        self.sel_id = None
        self.is_selected = False
        self.is_drawing = False
        self.selector = None
        self.angle = 0

        self.a_image = None
        self.ph_image = None
        self.bbox = None

        self.out = None
        self.in1 = None

        self.conn_list = []
        self.wire_list = []

    def create_image(self, filename):
        """Initial component image creation"""
        self.a_image = Image.open(filename)
        self.a_image = self.a_image.rotate(self.angle, expand=True)
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.id = self.canvas.create_image(self.x1, self.y1, anchor=tk.CENTER, image=self.ph_image, tags='gate')

    def update_position(self):
        """Update the position when the gate object is moved"""
        self.canvas.coords(self.id, self.x1, self.y1)  # Update position

    def update_image(self, filename):
        """Update the image for gate symbol rotation"""
        self.a_image = Image.open(filename)
        self.a_image = self.a_image.rotate(self.angle, expand=True)  # Update image rotation
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.canvas.itemconfig(self.id, image=self.ph_image)  # Update image

    def update_bbox(self):
        """Update the bounding box to get current gate coordinates"""
        self.bbox = self.canvas.bbox(self.id)

    def create_selector(self):
        """Create the red rectangle selector and check to see if the gate is selected"""
        x1, y1, x2, y2 = self.bbox[0] - 5, self.bbox[1] - 5, self.bbox[2] + 5, self.bbox[3] + 5
        self.sel_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=None, outline="red", width=2)
        self.set_selector_visibility()

    def update_selector(self):
        """Update the red rectangle selector coordinates and check to see if the gate is selected"""
        x1, y1, x2, y2 = self.bbox[0] - 5, self.bbox[1] - 5, self.bbox[2] + 5, self.bbox[3] + 5
        self.canvas.coords(self.sel_id, x1, y1, x2, y2)
        self.set_selector_visibility()

    def set_selector_visibility(self):
        """Set the selector visibility state"""
        if self.is_selected:
            self.canvas.itemconfig(self.sel_id, state='normal')
        else:
            self.canvas.itemconfig(self.sel_id, state='hidden')

    def create_connectors(self):
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define 3 connectors: in1, in2, out
        self.out = Connector(self.canvas, "out", center.x + w / 2, center.y)
        self.in1 = Connector(self.canvas, "in1", center.x - w / 2, center.y)

        # Update the connector list
        self.conn_list = [self.out, self.in1]

    def update_connectors(self):
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        if self.angle == 0:
            self.out.x, self.out.y = center.x + w / 2, center.y
            self.in1.x, self.in1.y = center.x - w / 2, center.y
        elif self.angle == 90:
            self.out.x, self.out.y = center.x, center.y - h / 2
            self.in1.x, self.in1.y = center.x, center.y + h / 2
        elif self.angle == 180:
            self.out.x, self.out.y = center.x - w / 2, center.y
            self.in1.x, self.in1.y = center.x + w / 2, center.y
        elif self.angle == 270:
            self.out.x, self.out.y = center.x, center.y + h / 2
            self.in1.x, self.in1.y = center.x, center.y - h / 2

        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def set_connector_visibility(self):
        """Set the connector visibility state"""
        if self.is_drawing:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='normal')
        else:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='hidden')

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
