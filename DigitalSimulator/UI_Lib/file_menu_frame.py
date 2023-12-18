import customtkinter as ctk
from tkinter import filedialog as fd
from pathlib import Path
import json
from PIL import Image

from Comp_Lib import AndGate, OrGate, NandGate, NorGate, XorGate, XnorGate, Switch, LED, Text, Clock
from IC_Lib import IC74161, IC28C16, SevenSegment
from Wire_Lib import Wire, SegmentWire, Connection


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "reprJson"):
            return o.reprJson()
        else:
            return super().default(o)


class JSONDCoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=JSONDCoder.from_dict)

    @staticmethod
    def from_dict(_d):
        return _d


class FileMenuFrame(ctk.CTkFrame):
    def __init__(self, window, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.obj_type_dict = {'and': AndGate,
                              'nand': NandGate,
                              'or': OrGate,
                              'nor': NorGate,
                              'xor': XorGate,
                              'xnor': XnorGate,
                              'switch': Switch,
                              'wire': Wire,
                              'led': LED,
                              'text': Text,
                              'clock': Clock,
                              '7_segment': SevenSegment,
                              'ic74161': IC74161,
                              'ic28C16': IC28C16}

        self.menu_on = False

        self.menu_frame = ctk.CTkFrame(window, height=100, bg_color="white")

        new_btn = ctk.CTkButton(self.menu_frame, text="New", width=150, command=self.new_diagram)
        new_btn.pack(pady=5)

        open_btn = ctk.CTkButton(self.menu_frame, text="Open", width=150, command=self.load_diagram)
        open_btn.pack(pady=5)

        save_btn = ctk.CTkButton(self.menu_frame, text="Save", width=150, command=self.save_diagram)
        save_btn.pack(pady=5)

        exit_btn = ctk.CTkButton(self.menu_frame, text="Exit", width=150, command=window.destroy)
        exit_btn.pack(pady=5)

        my_image = ctk.CTkImage(light_image=Image.open
                                (Path(__file__).parent / "../icons/hamburger_menu.png"),
                                dark_image=Image.open
                                (Path(__file__).parent / "../icons/hamburger_menu.png"),
                                size=(24, 24))

        button = ctk.CTkButton(self, text="", image=my_image, width=30, command=self.show_menu)
        button.pack(side=ctk.LEFT, padx=5, pady=10)

    def new_diagram(self):
        self.canvas.delete("all")
        self.canvas.comp_list = []

    def load_diagram(self):
        try:
            filetypes = (('json files', '*.json'), ('All files', '*.*'))
            f = fd.askopenfilename(filetypes=filetypes, initialdir="./")
            with open(f) as file:
                d = json.load(file)
                # print(d)

                for item in d:
                    if item['type'] == "wire":
                        wire = Wire(self.canvas, x1=item['x1'], y1=item['y1'], x2=item['x2'], y2=item['y2'])
                        self.canvas.comp_list.append(wire)
                    elif item['type'] == "segment_wire":
                        wire = SegmentWire(self.canvas, x1=item['x1'], y1=item['y1'], x2=item['x2'], y2=item['y2'])
                        self.canvas.comp_list.append(wire)
                    elif item['type'] == "switch":
                        switch = Switch(self.canvas, x1=item['x1'], y1=item['y1'])
                        switch.angle = item['angle']
                        self.canvas.comp_list.append(switch)
                    elif item['type'] == "led":
                        led = LED(self.canvas, x1=item['x1'], y1=item['y1'])
                        led.angle = item['angle']
                        self.canvas.comp_list.append(led)
                    elif item['type'] == "clock":
                        clock = Clock(self.canvas, x1=item['x1'], y1=item['y1'])
                        clock.angle = item['angle']
                        self.canvas.comp_list.append(clock)
                    elif item['type'] == "ic28C16":
                        ic28C16 = IC28C16(self.canvas, x1=item['x1'], y1=item['y1'])
                        ic28C16.angle = item['angle']
                        self.canvas.comp_list.append(ic28C16)
                    elif item['type'] == "ic74161":
                        ic74161 = IC74161(self.canvas, x1=item['x1'], y1=item['y1'])
                        ic74161.angle = item['angle']
                        self.canvas.comp_list.append(ic74161)
                    elif item['type'] == "7_segment":
                        seven_segment = SevenSegment(self.canvas, x1=item['x1'], y1=item['y1'])
                        seven_segment.angle = item['angle']
                        self.canvas.comp_list.append(seven_segment)

                # Add connections
                for item in d:
                    if item['type'] == "switch":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(switch, wire, wire_item['wire_end'])
                                switch.wire_list.append(conn)

                    elif item['type'] == "clock":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(clock, wire, wire_item['wire_end'])
                                clock.wire_list.append(conn)

                    elif item['type'] == "ic74161":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(ic74161, wire, wire_item['wire_end'])
                                ic74161.wire_list.append(conn)

                    elif item['type'] == "ic28C16":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(ic28C16, wire, wire_item['wire_end'])
                                ic28C16.wire_list.append(conn)

                    elif item['type'] == "7_segment":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(seven_segment, wire, wire_item['wire_end'])
                                seven_segment.wire_list.append(conn)

                    elif item['type'] == "led":
                        wire_list = item['wire_list']
                        for wire_item in wire_list:
                            x1 = wire_item['wire_obj']['x1']
                            y1 = wire_item['wire_obj']['y1']
                            x2 = wire_item['wire_obj']['x2']
                            y2 = wire_item['wire_obj']['y2']
                            # Test to see if wire obj matches wire coordinates
                            if x1 == wire.x1 and y1 == wire.y1 and x2 == wire.x2 and y2 == wire.y2:
                                conn = Connection(led, wire, wire_item['wire_end'])
                                led.wire_list.append(conn)

        except FileNotFoundError:
            with open('untitled.canvas', 'w') as _file:
                pass
            self.canvas.comp_list = []

    def save_diagram(self):
        filetypes = (('json files', '*.json'), ('All files', '*.*'))
        f = fd.asksaveasfilename(filetypes=filetypes, initialdir="./")
        with open(f, 'w') as file:
            file.write(json.dumps(self.canvas.comp_list, cls=MyEncoder, indent=4))

    def show_menu(self):
        if not self.menu_on:
            self.menu_frame.place(x=15, y=60)
            self.menu_frame.tkraise()
            self.menu_on = True
        else:
            self.menu_frame.place_forget()
            self.menu_on = False
