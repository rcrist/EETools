import customtkinter as ctk

from UI_Lib.mouse import Mouse
from UI_Lib.grid import Grid
from Wire_Lib import Node


class CompDialog(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Component Dialog")

        self.text = ""
        self.value = 0
        self.units = ""

        self.text_entry = None
        self.value_entry = None
        self.units_entry = None

        self.initDialog()

    def initDialog(self):
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill=ctk.X)

        text_lbl = ctk.CTkLabel(text_frame, text="Text", width=6)
        text_lbl.pack(side=ctk.LEFT, padx=5, pady=10)

        self.text_entry = ctk.CTkEntry(text_frame, placeholder_text="CTkEntry")
        self.text_entry.pack(fill=ctk.X, padx=5, expand=True)

        value_frame = ctk.CTkFrame(self)
        value_frame.pack(fill=ctk.X)

        value_lbl = ctk.CTkLabel(value_frame, text="Value", width=6)
        value_lbl.pack(side=ctk.LEFT, padx=5, pady=10)

        self.value_entry = ctk.CTkEntry(value_frame, placeholder_text="CTkEntry")
        self.value_entry.pack(fill=ctk.X, padx=5, expand=True)

        units_frame = ctk.CTkFrame(self)
        units_frame.pack(fill=ctk.X)

        units_lbl = ctk.CTkLabel(units_frame, text="Units (Ω,nF,pF, etc.)", width=6)
        units_lbl.pack(side=ctk.LEFT, padx=5, pady=10)

        self.units_entry = ctk.CTkEntry(units_frame, placeholder_text="CTkEntry")
        self.units_entry.pack(fill=ctk.X, padx=5, expand=True)

        frame9 = ctk.CTkFrame(self)
        frame9.pack(fill=ctk.X)

        btn = ctk.CTkButton(frame9, text="Cancel", command=self.cancel, width=60)
        btn.pack(side=ctk.RIGHT, padx=5, pady=5)

        btn = ctk.CTkButton(frame9, text="OK", command=self.onSubmit, width=60)
        btn.pack(side=ctk.RIGHT, padx=5, pady=5)

    def onSubmit(self):
        self.text = self.text_entry.get()
        self.value = self.value_entry.get()
        self.units = self.units_entry.get()
        self.destroy()

    def cancel(self):
        self.destroy()


class TransistorDialog(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Transistor Dialog")

        self.text = ""
        self.output1 = ""
        self.output2 = ""
        self.output3 = ""
        self.output4 = ""

        self.text_entry = None
        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.entry4 = None

        self.initDialog()

    def initDialog(self):
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill=ctk.X)

        text_lbl = ctk.CTkLabel(text_frame, text="Text", width=6)
        text_lbl.pack(side=ctk.LEFT, padx=5, pady=10)

        self.text_entry = ctk.CTkEntry(text_frame, placeholder_text="CTkEntry")
        self.text_entry.pack(fill=ctk.X, padx=5, expand=True)

        frame1 = ctk.CTkFrame(self)
        frame1.pack(fill=ctk.X)

        lbl1 = ctk.CTkLabel(frame1, text="bf", width=6)
        lbl1.pack(side=ctk.LEFT, padx=5, pady=10)

        self.entry1 = ctk.CTkEntry(frame1, placeholder_text="CTkEntry")
        self.entry1.pack(fill=ctk.X, padx=5, expand=True)

        frame2 = ctk.CTkFrame(self)
        frame2.pack(fill=ctk.X)

        lbl2 = ctk.CTkLabel(frame2, text="cjc", width=6)
        lbl2.pack(side=ctk.LEFT, padx=5, pady=10)

        self.entry2 = ctk.CTkEntry(frame2, placeholder_text="CTkEntry")
        self.entry2.pack(fill=ctk.X, padx=5, expand=True)

        frame3 = ctk.CTkFrame(self)
        frame3.pack(fill=ctk.X)

        lbl3 = ctk.CTkLabel(frame3, text="cjc_units", width=6)
        lbl3.pack(side=ctk.LEFT, padx=5, pady=10)

        self.entry3 = ctk.CTkEntry(frame3, placeholder_text="CTkEntry")
        self.entry3.pack(fill=ctk.X, padx=5, expand=True)

        frame4 = ctk.CTkFrame(self)
        frame4.pack(fill=ctk.X)

        lbl4 = ctk.CTkLabel(frame4, text="rb", width=6)
        lbl4.pack(side=ctk.LEFT, padx=5, pady=10)

        self.entry4 = ctk.CTkEntry(frame4, placeholder_text="CTkEntry")
        self.entry4.pack(fill=ctk.X, padx=5, expand=True)

        frame9 = ctk.CTkFrame(self)
        frame9.pack(fill=ctk.X)

        btn = ctk.CTkButton(frame9, text="Cancel", command=self.cancel, width=60)
        btn.pack(side=ctk.RIGHT, padx=5, pady=5)

        # Command tells the form what to do when the button is clicked
        btn = ctk.CTkButton(frame9, text="OK", command=self.onSubmit, width=60)
        btn.pack(side=ctk.RIGHT, padx=5, pady=5)

    def onSubmit(self):
        self.text = self.text_entry.get()
        self.output1 = self.entry1.get()
        self.output2 = self.entry2.get()
        self.output3 = self.entry3.get()
        self.output4 = self.entry4.get()
        self.destroy()

    def cancel(self):
        self.destroy()


class Canvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.led_color = "red"
        self.led_size = "large"
        self.grid = Grid(self, 10)
        self.wire_dir = "H"
        self.mouse = Mouse(self)
        self.comp_list = []
        self.wire_list = []
        self.wire_dict = {}

        self.mouse.move_mouse_bind_events()

    def redraw(self):
        self.delete('grid_line')
        self.grid.draw()
        self.tag_lower("grid_line")
        for c in self.comp_list:
            c.update()

    def show_connectors(self):
        for s in self.comp_list:
            s.is_drawing = True
        self.redraw()

    def hide_connectors(self):
        for s in self.comp_list:
            s.is_drawing = False
        self.redraw()

    def edit_shape(self, _event=None):
        if self.mouse.selected_comp:
            comp = self.mouse.selected_comp
            if isinstance(comp, Node):
                dialog = ctk.CTkInputDialog(text="Enter new text", title="Edit Node Text")
                comp.text = dialog.get_input()
                self.redraw()
            elif (comp.comp_type == 'resistor' or comp.comp_type == 'inductor' or comp.comp_type == 'capacitor' or
                  comp.comp_type == 'dc_source' or comp.comp_type == 'ac_source' or
                  comp.comp_type == 'isource'):
                dialog = CompDialog(self)
                dialog.wm_attributes('-topmost', True)
                dialog.wait_window()
                comp.text = dialog.text
                comp.value = dialog.value
                comp.units = dialog.units
                comp.comp_text = comp.text + "=" + str(comp.value) + comp.units
                self.redraw()
            elif comp.comp_type == 'npn_transistor':
                dialog = TransistorDialog(self)
                dialog.wm_attributes('-topmost', True)
                dialog.wait_window()
                comp.text = dialog.text
                comp.bf = dialog.output1
                comp.cjc = dialog.output2
                comp.cjc_units = dialog.output3
                comp.rb = dialog.output4
                self.redraw()

    def set_horiz_dir(self, _event):
        self.wire_dir = "H"

    def set_vert_dir(self, _event):
        self.wire_dir = "V"
