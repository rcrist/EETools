from PIL import Image, ImageTk
import tkinter as tk

from Helper_Lib import Point
from Shape_Lib.shape import Shape
from Shape_Lib.selector import Selector
from Shape_Lib.connector import Connector


class Picture(Shape):
    def __init__(self, canvas, x1, y1, x2=0, y2=0):
        super().__init__(canvas, x1, y1, x2, y2)
        self.a_image = None
        self.ph_image = None
        self.filename = "D:/EETools/DiagramEditor/images/hamburger.png"
        self.angle = 0
        self.bbox = None
        self.type = "picture"

        self.s1_id, self.s2_id, self.s3_id, self.s4_id = None, None, None, None
        self.c1_id, self.c2_id, self.c3_id, self.c4_id = None, None, None, None

        self.create_shape()
        self.create_selectors()
        self.create_connectors()

    def create_shape(self):
        """Create the shape here"""
        self.a_image = Image.open(self.filename)
        self.a_image = self.a_image.rotate(self.angle)
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.id = self.canvas.create_image(self.x1, self.y1, anchor=tk.CENTER, image=self.ph_image, tags="pics")
        self.bbox = self.canvas.bbox(self.id)

    def update(self):
        """Update the shape here"""
        self.canvas.coords(self.id, self.x1, self.y1)

        self.a_image = Image.open(self.filename)
        self.a_image = self.a_image.rotate(self.angle)
        self.ph_image = ImageTk.PhotoImage(self.a_image)
        self.canvas.itemconfig(self.id, image=self.ph_image)

        self.bbox = self.canvas.bbox(self.id)

        self.update_selectors()
        if self.is_selected:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='normal')
        else:
            for s in self.sel_list:
                self.canvas.itemconfig(s.id, state='hidden')

        self.update_connectors()
        if self.is_drawing:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='normal')
        else:
            for c in self.conn_list:
                self.canvas.itemconfig(c.id, state='hidden')

        self.move_connected_lines()

    def create_selectors(self):
        # Calculate position of selectors from current shape position
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]

        """Create four selectors at the corners here"""
        self.s1_id = Selector(self.canvas, "s1", x1, y1)
        self.s2_id = Selector(self.canvas, "s2", x2, y1)
        self.s3_id = Selector(self.canvas, "s3", x2, y2)
        self.s4_id = Selector(self.canvas, "s4", x1, y2)

        self.sel_list = [self.s1_id, self.s2_id, self.s3_id, self.s4_id]
        for s in self.sel_list:
            self.canvas.itemconfig(s.id, state='hidden')

    def update_selectors(self):
        # Recalculate position of selectors from current shape position
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]

        """Update the position of all selectors here"""
        self.s1_id.x, self.s1_id.y = x1, y1
        self.s1_id.update()

        self.s2_id.x, self.s2_id.y = x2, y1
        self.s2_id.update()

        self.s3_id.x, self.s3_id.y = x2, y2
        self.s3_id.update()

        self.s4_id.x, self.s4_id.y = x1, y2
        self.s4_id.update()

    def create_connectors(self):
        """Create connectors here"""
        # Calculate the shape geometry
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1+w/2, y1+h/2)

        self.c1_id = Connector(self.canvas, "c2", center.x, center.y - h/2)    # Top Center
        self.c2_id = Connector(self.canvas, "c3", center.x + w/2, center.y)    # Right Center
        self.c3_id = Connector(self.canvas, "c4", center.x, center.y + h/2)    # Bottom Center
        self.c4_id = Connector(self.canvas, "c5", center.x - w/2, center.y)    # Left Center

        self.conn_list = [self.c1_id, self.c2_id, self.c3_id, self.c4_id]
        for c in self.conn_list:
            self.canvas.itemconfig(c.id, state='hidden')

    def update_connectors(self):
        """Update the position of all connectors here"""
        x1, y1, x2, y2 = self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]
        w = x2 - x1
        h = y2 - y1
        center = Point(x1+w/2, y1+h/2)

        self.c1_id.x, self.c1_id.y = center.x, center.y - h/2
        self.c1_id.update()

        self.c2_id.x, self.c2_id.y = center.x + w/2, center.y
        self.c2_id.update()

        self.c3_id.x, self.c3_id.y = center.x, center.y + h/2
        self.c3_id.update()

        self.c4_id.x, self.c4_id.y = center.x - w/2, center.y
        self.c4_id.update()

    def rotate(self):
        """Calculate rotation angle"""
        self.angle += 90
        if self.angle > 270:
            self.angle = 0
        self.update()

    def resize(self, offsets, event):
        pass

    def __repr__(self):
        return ("Picture: x, y = " + "(" + str(self.x1) + ", " + str(self.y1) +
                "\nimage filename = " + self.filename)
