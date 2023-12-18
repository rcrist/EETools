import customtkinter as ctk
from tktooltip import ToolTip
from pathlib import Path
from PIL import Image

import skrf as rf
import matplotlib.pyplot as plt
rf.stylely()

from UI_Lib.file_menu_frame import FileMenuFrame
from UI_Lib.settings_frame import SettingsFrame
from UI_Lib.help_frame import HelpFrame

from Comp_Lib import Resistor, Inductor, Capacitor, Inport, Outport


class TopFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        # Add Top Frame widget here
        file_frame = FileMenuFrame(self.parent, self, self.canvas)
        file_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        settings_frame = SettingsFrame(self.parent, self, self.canvas)
        settings_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        help_frame = HelpFrame(self.parent, self, self.canvas)
        help_frame.pack(side=ctk.RIGHT, padx=5, pady=5)

        a_image = ctk.CTkImage(light_image=Image.open(Path(__file__).parent / "../icons/angle.png"),
                               dark_image=Image.open(Path(__file__).parent / "../icons/angle.png"),
                               size=(24, 24))
        self.button_id = ctk.CTkButton(self, text="", image=a_image, width=30, command=self.rotate_comp)
        self.button_id.pack(side=ctk.LEFT, padx=5, pady=5)
        ToolTip(self.button_id, msg="Rotate selected component")

        a_image = ctk.CTkImage(light_image=Image.open(Path(__file__).parent / "../icons/analyze.png"),
                               dark_image=Image.open(Path(__file__).parent / "../icons/analyze.png"),
                               size=(24, 24))
        self.button_id = ctk.CTkButton(self, text="", image=a_image, width=30, command=self.analyze_circuit)
        self.button_id.pack(side=ctk.LEFT, padx=5, pady=5)
        ToolTip(self.button_id, msg="Analyze circuit")

    def rotate_comp(self):
        self.parent.rotate_comp(_event=None)

    def analyze_circuit(self):
        ctx = []
        res, ind, cap, inport, outport = None, None, None, None, None
        freq = rf.Frequency(start=1.0, stop=10.0, unit='GHz', npoints=19)

        # Convert graphical components to microwave components
        for comp in self.canvas.comp_list:
            if isinstance(comp, Resistor):
                res = rf.Circuit.SeriesImpedance(frequency=freq, name='res', z0=50, Z=comp.resistance)
            elif isinstance(comp, Inductor):
                ind = rf.Circuit.SeriesImpedance(frequency=freq, name='ind', z0=50,
                                                 Z=1j * freq.w * comp.inductance * 1e-9)
            elif isinstance(comp, Capacitor):
                cap = rf.Circuit.SeriesImpedance(frequency=freq, name='cap', z0=50,
                                                 Z=1 / (1j * freq.w * comp.capacitance * 1e-12))
            elif isinstance(comp, Inport):
                inport = rf.Circuit.Port(freq, name='inport', z0=50)
            elif isinstance(comp, Outport):
                outport = rf.Circuit.Port(freq, name='outport', z0=50)

        comp_dict = {
            'resistor': res,
            'inductor': ind,
            'capacitor': cap,
            'inport': inport,
            'outport': outport,
            'wire': None
        }

        for conn in self.canvas.conn_list:
            ctx_conn = [(comp_dict[conn[0][0]], conn[0][1]), (comp_dict[conn[1][0]], conn[1][1])]
            ctx.append(ctx_conn)

        ckt = rf.Circuit(ctx)
        ntw = ckt.network

        print(ntw.s_mag)  # Print S-parameters to console

        ntw.plot_s_mag(m=0, n=0, lw=2, logx=False)
        ntw.plot_s_mag(m=1, n=0, lw=2, logx=False)
        plt.show()  # Display S-parameter plot

        ntw.plot_s_smith()
        plt.show()
