import customtkinter as ctk

class PomodoroTab(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text=name)
        self.label.pack()