from ..utils import HyperLink, create_grid, format_date, format_time, load_icon, load_favicon
from ..appstate import AppState
from ..pomodoro_meter import PomodoroWheel
import customtkinter as ctk
from datetime import datetime
import webbrowser

#row=0, column=0, sticky="ew", padx=8, pady=4, columnspan=2

class HomeTab(ctk.CTkFrame):
    def __init__(self, parent, name, appstate: AppState):
        super().__init__(parent)

        create_grid(self, columns=3, rows=[1, 3])

        self.heading = ctk.CTkFrame(self, fg_color="transparent")

        #icon_image = ctk.CTkLabel(self.heading, text="", image = load_icon(icon, size=36, category="tabs"))
        label = ctk.CTkLabel(self.heading, text=name, font=("Ubuntu", 36, "bold"), justify=ctk.CENTER)

        #icon_image.pack(side=ctk.LEFT, fill="both")
        label.pack(side=ctk.LEFT, fill="both", padx=48)

        self.heading.grid(row = 0, column=0, columnspan = 3, sticky="nesw")

        #COLUMN 1 DATE-TIME
        self.date_time = ctk.CTkFrame(self, fg_color="transparent")
        self.date_time.grid(row=1, column=0, sticky="nesw")
        
        create_grid(self.date_time, rows=[1, 3, 2])

        self.date = ctk.CTkLabel(self.date_time, text=format_date(datetime.now()), font=("Ubuntu", 20), fg_color="transparent" )
        self.date.grid(row=0, sticky="nesw")

        self.time = ctk.CTkLabel(self.date_time, text=format_time(datetime.now()), font=("Ubuntu", 72), fg_color="transparent")
        self.time.grid(row=1, sticky="nesw")

        self.quick_links = ctk.CTkFrame(self.date_time, fg_color="transparent")

        self.quick_links.grid(row=2, sticky="nesw")
        for link in appstate.links:
            link_frame = ctk.CTkFrame(self.quick_links, fg_color="transparent", height=24)
            create_grid(link_frame, columns=[1, 7])
            
            icon = load_favicon(link.url, 20) if load_favicon(link.url, 20) else load_icon(link.icon, size=20, hover_image=False)
            image = ctk.CTkLabel(link_frame, text="", image=icon)
            label = HyperLink(link_frame, text=link.name, cursor="hand2")
            
            label.bind(f"<Button-1>", lambda _: self.callback(link.url))
            image.grid(row=0, column=0, sticky="nesw")
            label.grid(row=0, column=1, sticky="w")

            link_frame.pack(expand=True, fill="both")

        #COLUMN 2 - POMODORO TIMER
        self.pomodoro = ctk.CTkFrame(self, fg_color="transparent")
        self.pomodoro_wheel = PomodoroWheel(
            self.pomodoro, 
            color = '#5B7DB1',
            time = appstate.pomodoro.time_remaining,
            mode = appstate.pomodoro.mode.label,
            size=self.pomodoro.cget('width')
            )
        self.pomodoro_wheel.set_progress(appstate.pomodoro.time_remaining / appstate.pomodoro.mode.duration)

        self.pomodoro_wheel.pack()
        self.pomodoro.grid(row=1, column=1, sticky="nesw")

        #COLUMN 3 - TASKS + REMINDERS
        self.tasks_reminder = ctk.CTkFrame(self, fg_color="#00FF11")
        self.tasks_reminder.grid(row=1, column=2, sticky="nesw")
        
    def callback(self, url):
        webbrowser.open_new(url)

    #MOVE TO TIME CONTROLLER OBJECT
    def update_time(self):
        self.date.configure(text=format_date(datetime.now()))
        self.time.configure(text=format_time(datetime.now()))
        self.after(1, self.update_time)