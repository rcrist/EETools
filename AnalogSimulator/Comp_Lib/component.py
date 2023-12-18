import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from Helper_Lib import Point


class Component:
    def __init__(self, canvas, comp_type, x1, y1, value):
        """Base class for component classes"""
        self.canvas = canvas
        self.comp_type = comp_type
        self.x1 = x1
        self.y1 = y1
        self.value = value
        self.units = None

        if self.comp_type == 'npn_transistor':
            self.bf = None
            self.cjc = None
            self.cjc_units = None
            self.rb = None

        self.id = None
        self.sel_id = None

        self.is_selected = False
        self.is_drawing = False
        self.selector = None
        self.angle = 0
        self.text = None
        self.comp_text = None
        self.text_id = None

        self.filename = None
        self.a_image = None
        self.ph_image = None
        self.bbox = None

        self.out = None
        self.in1 = None
        self.ba = None
        self.em = None
        self.co = None

        self.conn_list = []
        self.wire_list = []

        # Define component parameters in a dictionary of dictionaries
        self.params = {
            'filename': {
                'resistor': "../images/lumped/resistor_60x30.png",
                'capacitor': "../images/lumped/capacitor_60x30.png",
                'inductor': "../images/lumped/inductor_60x30.png",
                'ground': "../images/sources/ground_50x40.png",
                'dc_source': "../images/sources/voltage_source_40x40.png",
                'isource': "../images/sources/current_source_40x40.png",
                'ac_source': "../images/sources/ac_voltage_source_40x40.png",
                'npn_transistor': "../images/transistors/npn_transistor_60x71.png"
            },
            'text': {
                'resistor': 'R1',
                'capacitor': 'C1',
                'inductor': 'L1',
                'ground': "",
                'dc_source': "Vpwr",
                'isource': "I",
                'ac_source': "Vin",
                'npn_transistor': "Q1"
            }
        }

    def set_image_filename(self):
        self.filename = Path(__file__).parent / self.params['filename'][self.comp_type]

    def create_text(self):
        self.comp_text = self.params['text'][self.comp_type]
        if self.comp_type == 'isource' or self.comp_type == 'dc_source' or self.comp_type == 'ac_source':
            text_loc = Point(self.x1-40, self.y1)  # Put text on left side of symbol
        elif self.comp_type == 'npn_transistor':
            text_loc = Point(self.x1 - 10, self.y1 - 40)  # Put text above symbol
        else:
            text_loc = Point(self.x1, self.y1-30)  # Put text above symbol
        self.text_id = self.canvas.create_text(text_loc.x, text_loc.y,
                                text=self.comp_text, fill="black",
                                font='Helvetica 10 bold',
                                angle=self.angle, tags="text")

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

    def update_text(self):
        self.canvas.itemconfig(self.text_id, text=self.comp_text)
        if self.comp_type == 'isource' or self.comp_type == 'dc_source' or self.comp_type == 'ac_source':
            if self.angle == 0 or self.angle == 180:
                self.set_east_text()
            elif self.angle == 90 or self.angle == 270:
                self.set_north_text()
        elif self.comp_type == 'npn_transistor':
            self.set_transistor_text()
        else:
            if self.angle == 0 or self.angle == 180:
                self.set_north_text()
            elif self.angle == 90 or self.angle == 270:
                self.set_east_text()

    def set_east_text(self):
        self.canvas.coords(self.text_id, self.x1 - 70, self.y1)

    def set_north_text(self):
        self.canvas.coords(self.text_id, self.x1, self.y1 - 30)

    def set_transistor_text(self):
        self.canvas.itemconfig(self.text_id, text=self.text)
        self.canvas.coords(self.text_id, self.x1 - 10, self.y1 - 40)

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
