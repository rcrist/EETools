import customtkinter as ctk
from tktooltip import ToolTip
from pathlib import Path
from PIL import Image

import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit

from UI_Lib.file_menu_frame import FileMenuFrame
from UI_Lib.settings_frame import SettingsFrame
from UI_Lib.help_frame import HelpFrame
from Wire_Lib import AnalogWire


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
        libraries_path = find_libraries()
        _spice_library = SpiceLibrary(libraries_path)

        units = {
            'u_V': 1,
            'u_kΩ': 1000,
            'u_kHz': 1000,
            'u_uF': 1e-6,
            'u_MΩ': 1e6,
            'u_pF': 1e-12
        }

        freq_amplitude = 1
        freq_units = units['u_kHz']

        source = None

        circuit = Circuit('Transistor')

        for comp in self.canvas.comp_list:
            if not isinstance(comp, AnalogWire):
                if comp.comp_type == 'dc_source':
                    node_list = self.get_nodes(comp)
                    circuit.V('power', node_list[0], circuit.gnd, comp.value * units[comp.units])
                elif comp.comp_type == 'ac_source':
                    node_list = self.get_nodes(comp)
                    source = circuit.SinusoidalVoltageSource('in', node_list[0], circuit.gnd,
                             amplitude=comp.value*units[comp.units], frequency=freq_amplitude*freq_units)
                elif comp.comp_type == 'resistor':
                    comp_num = self.get_comp_num(comp.text)
                    node_list = self.get_nodes(comp)
                    circuit.R(comp_num, node_list[0], node_list[1], comp.value*units[comp.units])
                elif comp.comp_type == 'capacitor':
                    comp_num = self.get_comp_num(comp.text)
                    node_list = self.get_nodes(comp)
                    circuit.C(comp_num, node_list[0], node_list[1], comp.value * units[comp.units])
                elif comp.comp_type == 'inductor':
                    comp_num = self.get_comp_num(comp.text)
                    node_list = self.get_nodes(comp)
                    circuit.L(comp_num, node_list[0], node_list[1], comp.value * units[comp.units])
                elif comp.comp_type == 'npn_transistor':
                    comp_num = self.get_comp_num(comp.text)
                    node_list = self.get_nodes(comp)
                    circuit.BJT(comp_num, node_list[1], node_list[0], node_list[2], model='bjt')
                    circuit.model('bjt', 'npn', bf=comp.bf, cjc=comp.cjc*units[comp.cjc_units], rb=comp.rb)

        print(circuit)
        # Create circuit plots
        figure, ax = plt.subplots(figsize=(20, 10))

        # .ac dec 5 10m 1G

        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=source.period / 200, end_time=source.period * 2)

        ax.set_title('')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Voltage [V]')
        ax.grid()
        ax.plot(analysis['in'])
        ax.plot(analysis.out)
        ax.legend(('input', 'output'), loc=(.05, .1))

        plt.tight_layout()
        plt.show()

    @staticmethod
    def get_comp_num(comp_text):
        comp_num = comp_text[1:]
        return comp_num

    def get_nodes(self, in_comp):
        node_list = []
        for conn in in_comp.wire_list:
            for comp in self.canvas.comp_list:
                if isinstance(comp, AnalogWire) and comp.name == conn.wire_name:
                    node_list.append(comp.node_num)
        return node_list
