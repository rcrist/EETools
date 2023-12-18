import customtkinter as ctk
from tkinter import filedialog as fd
from pathlib import Path
import json
from PIL import Image

from Comp_Lib import Resistor, Inductor, Capacitor, Connection
from Comp_Lib import Inport, Outport
from Wire_Lib import StraightWire, SegmentWire, ElbowWire


class Encoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "reprJson"):
            return o.reprJson()
        else:
            return super().default(o)


class Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=Decoder.from_dict)

    @staticmethod
    def from_dict(_d):
        return _d


class FileMenuFrame(ctk.CTkFrame):
    def __init__(self, window, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.obj_type_dict = {'resistor': Resistor,
                              'inductor': Inductor,
                              'capacitor': Capacitor,
                              'inport': Inport,
                              'outport': Outport,
                              'straight': StraightWire,
                              'segment': SegmentWire,
                              'elbow': ElbowWire}

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
        self.canvas.comp_list.clear()
        self.canvas.wire_list.clear()

    def load_diagram(self):
        try:
            filetypes = (('json files', '*.json'), ('All files', '*.*'))
            f = fd.askopenfilename(filetypes=filetypes, initialdir="./")
            with open(f) as file:
                d = json.load(file)
                self.convert_json_data(d)
        except FileNotFoundError:
            with open('untitled.canvas', 'w') as _file:
                pass

    def convert_json_data(self, data):
        """Convert json data to a circuit object"""
        # Get circuit list from json data
        json_comp_list = data[0]['comp_list']
        for json_comp in json_comp_list:
            if json_comp['type'] == 'resistor':
                res = Resistor(self.canvas, int(json_comp['x1']), int(json_comp['y1']), int(json_comp['resistance']))
                conn_dict = json_comp['wire_list'][0]
                res.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                conn_dict = json_comp['wire_list'][1]
                res.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                self.canvas.comp_list.append(res)
            elif json_comp['type'] == 'inductor':
                ind = Inductor(self.canvas, int(json_comp['x1']), int(json_comp['y1']), int(json_comp['inductance']))
                conn_dict = json_comp['wire_list'][0]
                ind.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                conn_dict = json_comp['wire_list'][1]
                ind.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                self.canvas.comp_list.append(ind)
            elif json_comp['type'] == 'capacitor':
                cap = Capacitor(self.canvas, int(json_comp['x1']), int(json_comp['y1']), int(json_comp['capacitance']))
                conn_dict = json_comp['wire_list'][0]
                cap.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                conn_dict = json_comp['wire_list'][1]
                cap.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                self.canvas.comp_list.append(cap)
            elif json_comp['type'] == 'inport':
                port1 = Inport(self.canvas, int(json_comp['x1']), int(json_comp['y1']))
                conn_dict = json_comp['wire_list'][0]
                port1.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                self.canvas.comp_list.append(port1)
            elif json_comp['type'] == 'outport':
                port2 = Outport(self.canvas, int(json_comp['x1']), int(json_comp['y1']))
                conn_dict = json_comp['wire_list'][0]
                port2.wire_list.append(Connection(conn_dict['comp_conn'], conn_dict['wire_name'],
                                                conn_dict['wire_end']))
                self.canvas.comp_list.append(port2)
            elif json_comp['type'] == 'straight':
                wire = StraightWire(self.canvas, int(json_comp['x1']), int(json_comp['y1']), int(json_comp['x2']),
                                    int(json_comp['y2']))
                wire.name = json_comp['name']
                self.canvas.comp_list.append(wire)
                self.canvas.wire_dict[wire.name] = wire

        # Get connection list from json data
        self.canvas.conn_list = data[1]['conn_list']

    def save_diagram(self):
        comp_dict = {'comp_list': self.canvas.comp_list}
        conn_dict = {'conn_list': self.canvas.conn_list}
        circuit = [comp_dict, conn_dict]

        filetypes = (('json files', '*.json'), ('All files', '*.*'))
        f = fd.asksaveasfilename(filetypes=filetypes, initialdir="./")
        with open(f, 'w') as file:
            file.write(json.dumps(circuit, cls=Encoder, indent=4))

    def show_menu(self):
        if not self.menu_on:
            self.menu_frame.place(x=5, y=60)
            self.menu_frame.tkraise()
            self.menu_on = True
        else:
            self.menu_frame.place_forget()
            self.menu_on = False
