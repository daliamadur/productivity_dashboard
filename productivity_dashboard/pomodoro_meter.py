import customtkinter as ctk
from .utils import format_pomodoro, pulse

class PomodoroWheel(ctk.CTkFrame):
    def __init__(self, parent, color, time, mode, size=160, thickness=12):
        super().__init__(parent)
        self.appearance_mode = ctk.get_appearance_mode()

        #for thickness and font size
        scale = size / 160

        self.size = size
        self.thickness = thickness
        #as a %
        self.progress = 0.0
        self.color = color
        self.time = time
        self.mode = mode

        self.canvas = ctk.CTkCanvas(
            self,
            width = size,
            height = size,
            bg = self.bg_color(),
            #border
            highlightthickness = 0
        )
        self.canvas.pack()

        pad = self.thickness // 2

        #oval - background
        self.bg_circle = self.canvas.create_oval(
            pad, pad,
            size - pad, size - pad,
            outline = "#3D3D3D" if self.appearance_mode == "Dark" else "#A9A9A9",
            width = self.thickness
        )

        #arc - progress
        self.arc = self.canvas.create_arc(
            pad, pad,
            size - pad, size - pad,
            start = 90,
            extent = 0,
            style = 'arc',
            outline = self.color,
            width = thickness
        )

        offset = pad * 2.4

        #text - pomodoro mode
        self.pomodoro_mode = self.canvas.create_text(
            (size - pad) / 2, ((size - pad) / 2) - offset,
            fill = '#DCE4EE' if self.appearance_mode == 'Dark' else '#1A1A1A',
            font = ('Ubuntu', int(12 * scale)),
            text = self.mode
        )

        #text - remaining time
        self.time_remaining = self.canvas.create_text(
            (size - pad) / 2, ((size - pad) / 2) + offset,
            fill = '#DCE4EE' if self.appearance_mode == 'Dark' else '#1A1A1A',
            font = ("Ubuntu", int(20 * scale), "bold"),
            text = format_pomodoro(self.time)
        )

    def set_progress(self, value: float):
        if value < 1:
            #ensure value is between 0 and 1
            self.progress = max(0.0, min(1.0, value))
        else:
            self.progress = 0
            self.canvas.itemconfigure(
                self.bg_circle,
                outline = pulse(self.color)
            )

        self.canvas.itemconfigure(
            self.arc,
            extent = -360 * self.progress
        )

    def bg_color(self):
        transparent = True
        parent = self.master
        color = None

        while transparent:
            color = parent.cget("fg_color")
            transparent = color == 'transparent'
            parent = parent.master

        print(self.appearance_mode)

        return color[0] if self.appearance_mode == 'Light' else color[1]
        
    def set_time(self, s_remaining: int):
        self.time = s_remaining

        self.canvas.itemconfigure(
            self.time_remaining,
            text = format_pomodoro(self.time)
        )

    def set_mode(self, pomodoro_mode: str):
        self.mode = pomodoro_mode

        self.canvas.itemconfigure(
            self.pomodoro_mode,
            text = self.mode
        )