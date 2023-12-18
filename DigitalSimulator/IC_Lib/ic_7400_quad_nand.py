from PIL import Image, ImageTk
import tkinter as tk
from pathlib import Path

from IC_Lib.ic import IC
from Wire_Lib.connector import Connector
from Helper_Lib.point import Point


class IC7400(IC):
    def __init__(self, canvas, x1, y1):
        super().__init__(canvas, x1, y1)
        self.type = "ic7400"

        self.logic_dict = {}

        # Set initial logic states
        for i in range(1, 15):
            self.logic_dict['c' + str(i)] = False
        self.logic_dict['c14'] = True

        self.filename = Path(__file__).parent / "../images/ics/ic_7400_80x60.png"
        self.a_image = Image.open(self.filename)
        self.a_image = self.a_image.rotate(self.angle, expand=True)
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.id = self.canvas.create_image(self.x1, self.y1, anchor=tk.CENTER, image=self.ph_image, tags="ics")
        self.bbox = self.canvas.bbox(self.id)

        # Create 14 connectors
        self.create_connectors()

        # Create selector
        x1, y1, x2, y2 = self.bbox[0] - 3, self.bbox[1] - 3, self.bbox[2] + 3, self.bbox[3] + 3
        self.sel_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=None, outline="red", width=2, tags="sel")
        self.canvas.itemconfig(self.sel_id, state='hidden')

    def update(self):
        self.set_logic_level()
        self.canvas.coords(self.id, self.x1, self.y1)  # Update position
        self.a_image = Image.open(self.filename)
        self.a_image = self.a_image.rotate(self.angle, expand=True)  # Update image rotation
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.canvas.itemconfig(self.id, image=self.ph_image)  # Update image
        self.bbox = self.canvas.bbox(self.id)

        if self.is_selected:
            x1, y1, x2, y2 = self.bbox[0] - 3, self.bbox[1] - 3, self.bbox[2] + 3, self.bbox[3] + 3
            self.canvas.coords(self.sel_id, x1, y1, x2, y2)
            self.canvas.itemconfig(self.sel_id, state='normal')
        else:
            self.canvas.itemconfig(self.sel_id, state='hidden')

        self.update_connectors()
        self.set_connector_visibility()

    def create_connectors(self):
        # Calculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        for i in range(1, 15):
            if i <= 7:
                self.conn_list.append(Connector(self.canvas, "c" + str(i), center.x - w/2 + i * 10, center.y + h / 2))
            else:
                self.conn_list.append(Connector(self.canvas, "c" + str(i), center.x + w/2 - (i-7) * 10,
                                                center.y - h / 2))

    def set_connector_visibility(self):
        if self.is_drawing:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='normal')
        else:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='hidden')

    def update_connectors(self):
        # Recalculate position of connectors from current shape position and size
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w, h = x2 - x1, y2 - y1
        center = Point(x1 + w / 2, y1 + h / 2)

        # Define the positions for a 14-pin IC based on the angle
        if self.angle == 0:
            for i in range(1, 15):
                if i <= 7:
                    self.conn_list[i-1].x, self.conn_list[i-1].y = center.x - w/2 + i * 10, center.y + h / 2
                else:
                    self.conn_list[i-1].x, self.conn_list[i-1].y = center.x + w/2 - (i-7) * 10, center.y - h / 2
        elif self.angle == 90:
            for i in range(1, 15):
                if i <= 7:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x + w / 2, center.y + h/2 - i * 10
                else:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x - w/2, center.y - h/2  + (i - 7) * 10
        elif self.angle == 180:
            for i in range(1, 15):
                if i <= 7:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x + w / 2 - i * 10, center.y + h / 2
                else:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x - w / 2 + (i - 7) * 10, center.y - h / 2
        elif self.angle == 270:
            for i in range(1, 15):
                if i <= 7:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x - w / 2, center.y - h/2 + i * 10
                else:
                    self.conn_list[i - 1].x, self.conn_list[i - 1].y = center.x + w/2, center.y + h/2  - (i - 7) * 10

        # Draw the connectors
        for c in self.conn_list:
            c.update()

        self.move_connected_wires()

    def rotate(self):
        # Calculate rotation angle
        self.angle += 90
        if self.angle > 270:
            self.angle = 0

    def resize(self, offsets, event):
        pass

    def check_selector_hit(self, x, y):
        pass

    def set_logic_level(self):
        # c1 = in1_1
        # c2 = in2_1
        # c3 = out_1
        # c4 = in1_2
        # c5 = in2_2
        # c6 = out_2
        # c7 = gnd
        # c8 = out_3
        # c9 = in2_3
        # c10 = in1_3
        # c11 = out_4
        # c12 = in2_4
        # c13 = in1_4
        # c14 = vcc

        for wire in self.wire_list:
            # NAND Gate #1
            if wire.connector_obj.name == "c1":
                self.logic_dict['c1'] = wire.line_obj.state
                self.logic_dict['c3'] = not(self.logic_dict['c1'] and self.logic_dict['c2'])
            elif wire.connector_obj.name == "c2":
                self.logic_dict['c2'] = wire.line_obj.state
                self.logic_dict['c3'] = not(self.logic_dict['c1'] and self.logic_dict['c2'])
            elif wire.connector_obj.name == "c3":
                wire.line_obj.state = self.logic_dict['c3']

            # NAND Gate #2
            elif wire.connector_obj.name == "c4":
                self.logic_dict['c4'] = wire.line_obj.state
                self.logic_dict['c6'] = not(self.logic_dict['c4'] and self.logic_dict['c5'])
            elif wire.connector_obj.name == "c5":
                self.logic_dict['c5'] = wire.line_obj.state
                self.logic_dict['c6'] = not(self.logic_dict['c4'] and self.logic_dict['c5'])
            elif wire.connector_obj.name == "c6":
                wire.line_obj.state = self.logic_dict['c6']

            # NAND Gate #3
            elif wire.connector_obj.name == "c10":
                self.logic_dict['c10'] = wire.line_obj.state
                self.logic_dict['c8'] = not(self.logic_dict['c10'] and self.logic_dict['c9'])
            elif wire.connector_obj.name == "c9":
                self.logic_dict['c9'] = wire.line_obj.state
                self.logic_dict['c8'] = not(self.logic_dict['c10'] and self.logic_dict['c9'])
            elif wire.connector_obj.name == "c8":
                wire.line_obj.state = self.logic_dict['c8']

            # NAND Gate #4
            elif wire.connector_obj.name == "c13":
                self.logic_dict['c13'] = wire.line_obj.state
                self.logic_dict['c11'] = not(self.logic_dict['c13'] and self.logic_dict['c12'])
            elif wire.connector_obj.name == "c12":
                self.logic_dict['c12'] = wire.line_obj.state
                self.logic_dict['c11'] = not(self.logic_dict['c13'] and self.logic_dict['c12'])
            elif wire.connector_obj.name == "c11":
                wire.line_obj.state = self.logic_dict['c11']
