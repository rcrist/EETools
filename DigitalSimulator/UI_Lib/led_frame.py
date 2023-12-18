import customtkinter as ctk
from tktooltip import ToolTip


class LedFrame(ctk.CTkFrame):
    def __init__(self, window, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.canvas = canvas

        self.led_color = "red"  # red, yellow, blue, green
        self.lec_size = "large"  # large, small

        self.init_led_color_control(self)
        self.init_led_size_control(self)

    def init_led_color_control(self, parent_frame):
        move_frame = ctk.CTkFrame(parent_frame, width=150)
        move_frame.configure(fg_color=("gray28", "gray28"))  # set frame color
        move_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        image_label = ctk.CTkLabel(move_frame, text="LED Color", corner_radius=10)
        image_label.pack(side=ctk.LEFT, padx=5, pady=5)

        # Add OptionMenu to top frame
        def option_menu_callback(choice):
            self.canvas.led_color = choice

        option_menu = ctk.CTkOptionMenu(move_frame, values=["red", "yellow", "blue", "green"], width=100,
                                        command=option_menu_callback)
        option_menu.pack(side=ctk.LEFT, padx=5, pady=5)
        option_menu.set("red")

        ToolTip(option_menu, msg="Set LED color")

    def init_led_size_control(self, parent_frame):
        move_frame = ctk.CTkFrame(parent_frame, width=150)
        move_frame.configure(fg_color=("gray28", "gray28"))  # set frame color
        move_frame.pack(side=ctk.LEFT, padx=5, pady=5)

        image_label = ctk.CTkLabel(move_frame, text="LED Size", corner_radius=10)
        image_label.pack(side=ctk.LEFT, padx=5, pady=5)

        # Add OptionMenu to top frame
        def option_menu_callback(choice):
            self.canvas.led_size = choice

        option_menu = ctk.CTkOptionMenu(move_frame, values=["large", "small"], width=100,
                                        command=option_menu_callback)
        option_menu.pack(side=ctk.LEFT, padx=5, pady=5)
        option_menu.set("large")

        ToolTip(option_menu, msg="Set LED size")
