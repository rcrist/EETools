import customtkinter as ctk


class BottomFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = "Diagram editor ready..."

        self.message = ctk.CTkLabel(self, text=self.text)
        self.message.pack(side=ctk.LEFT, padx=5, pady=5)

    def update(self):
        self.message.configure(text=self.text)
