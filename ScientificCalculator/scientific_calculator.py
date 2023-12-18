import customtkinter as ctk
from math import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1525x425x10x10")
        self.title("Scientific Calculator")

        self.expression = ""
        self.equation = ctk.StringVar()
        self.sel = ""
        self.memory = 0

        # Create a label to display results of the calculation
        label = ctk.CTkLabel(self, text="0.00", padx=10, anchor=ctk.SE, font=('arial',22), textvariable=self.equation,
                             fg_color="transparent", width=1500, height=60)
        label.grid(row=0, column=0, columnspan=10, rowspan=4, padx=10, pady=5)
        label.configure(bg_color="#555500")

        # Initialize a button array (list of lists)
        self.buttons = [[None]*10 for _ in range(5)]

        # Create buttons
        self.button_text = [
            ["sin", "cos", "tan", "\u03C0", "MC", "MR", "M+", "M-", "MS", "\u232B"],  # Row 5
            ["asin", "acos", "atan", "radians", "degrees", "CLR", "7", "8", "9", "\u00F7"],  # Row 6
            ["sec", "csc", "cot", "e", "exp", "%", "4", "5", "6", "*"],  # Row 7
            ["x^2", "1/x", "|x|", "n!", "(", ")", "1", "2", "3", "-"],  # Row 8
            ["log", "log10", "10^x", "2\u03C0", "\u221A", "+/-", "0", "=", ".", "+"],  # Row 9
        ]

        # Display button in a 5x10 array
        for x in range(5):
            for y in range(10):
                self.buttons[x][y] = ctk.CTkButton(self, text=self.button_text[x][y], height=60,
                                                   font=('arial',18),
                                                   command=lambda x1=x, y1=y: self.press(x1, y1))
                if 0 < x < 5 < y < 9:
                    self.buttons[x][y].configure(fg_color="#3b3b3b")
                else:
                    self.buttons[x][y].configure(fg_color="#7b7b7b")
                self.buttons[x][y].grid(row=x+4, column=y, padx=5, pady=5)

    def press(self, x, y):
        # Check for special cases where eval can't evaluate the button text
        self.sel = self.button_text[x][y]  # self.sel is a short alias for self.button_text[x][y]
        if self.sel == "CLR" or self.sel == "=" or self.sel == "\u00F7" or self.sel == "1/x" or \
                self.sel == "\u232B" or self.sel == "\u03C0" or self.sel == "x^2" or self.sel == "|x|" or \
                self.sel == "+/-" or self.sel == "n!" or self.sel == "10^x" or self.sel == "\u221A" or \
                self.sel == "2\u03C0":
            self.special_case(x, y)
        elif self.sel == "MC" or self.sel == "MR" or self.sel == "M+" or self.sel == "M-" or self.sel == "MS":
            self.memory_operation(x,y)
        else:
            self.expression += self.button_text[x][y]
            self.equation.set(self.expression)

    def special_case(self, x, y):
        if self.sel == "CLR":  # Clear button selected
            self.expression = ""
            self.equation.set("")
        elif self.sel == "=":  # Equal button pressed, evaluate the current expression
            total = str(eval(self.expression))
            self.equation.set(total)
            self.expression = ""
        elif self.sel == "\u00F7":  # Divide button pressed
            self.expression += "/"
            self.equation.set(self.expression)
        elif self.sel == "1/x":  # 1/x button pressed
            self.expression = "1 / " + self.expression
            self.equation.set(self.expression)
        elif self.sel == "\u232B":  # backspace button pressed
            self.expression = self.expression.rstrip(self.expression[-1])
            self.equation.set(self.expression)
        elif self.sel == "\u03C0":   # pi
            self.expression += "pi"
            self.equation.set(self.expression)
        elif self.sel == "2\u03C0":  # 2pi
            self.expression += "2*pi"
            self.equation.set(self.expression)
        elif self.sel == "x^2":  # x raised to the power of 2
            self.expression = pow(float(self.expression), 2)
            self.equation.set(str(self.expression))
        elif self.sel == "|x|":  # abs(x)
            self.expression = fabs(float(self.expression))
            self.equation.set(str(self.expression))
        elif self.sel == "+/-":  # invert sign
            self.expression = -float(self.expression)
            self.equation.set(str(self.expression))
        elif self.sel == "n!":  # factorial
            self.expression = factorial(int(self.expression))
            self.equation.set(str(self.expression))
        elif self.sel == "10^x":  # 10 to the power of x
            self.expression = pow(10, float(self.expression))
            self.equation.set(str(self.expression))
        elif self.sel == "\u221A":  # square root
            self.expression = sqrt(float(self.expression))
            self.equation.set(str(self.expression))

    def memory_operation(self, x, y):
        if self.sel == "MC":
            self.memory = 0
        elif self.sel == "MR":
            self.expression += str(self.memory)
            self.equation.set(str(self.expression))
        elif self.sel == "M+":
            self.memory += int(self.expression)
        elif self.sel == "M-":
            self.memory -= int(self.expression)
        elif self.sel == "MS":
            self.memory = int(self.expression)


if __name__ == "__main__":
    app = App()
    app.mainloop()
