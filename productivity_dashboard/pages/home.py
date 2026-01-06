from ..utils import HyperLink, create_grid, format_date, format_time, format_duration, load_icon, load_favicon, callback
from ..appstate import AppState
from ..pomodoro_meter import PomodoroWheel
import customtkinter as ctk
from datetime import datetime

class HomeTab(ctk.CTkFrame):
    def __init__(self, parent, name, appstate: AppState):
        super().__init__(parent)
        self.appstate = appstate

        create_grid(self, columns=3, rows=[1, 3])

        self._build_top_panel(name)
        self._build_date_time_column()
        self._build_pomodoro_column()
        self._build_reminder_tasks_column()

    def _build_top_panel(self, name):
        heading = ctk.CTkFrame(self, fg_color="transparent")
        label = ctk.CTkLabel(heading, text=name, font=("Ubuntu", 36, "bold"), justify=ctk.CENTER)
        label.pack(side=ctk.LEFT, fill="both", padx=48)
        heading.grid(row = 0, column=0, columnspan = 3, sticky="nesw")

    def _build_date_time_column(self):
        date_time = ctk.CTkFrame(self, fg_color="transparent")
        date_time.grid(row=1, column=0, sticky="nesw")

        create_grid(date_time, rows=[1, 3, 2])

        date = ctk.CTkLabel(date_time, text=format_date(datetime.now()), font=("Ubuntu", 20), fg_color="transparent" )
        date.grid(row=0, sticky="nesw")

        time = ctk.CTkLabel(date_time, text=format_time(datetime.now()), font=("Ubuntu", 72), fg_color="transparent")
        time.grid(row=1, sticky="nesw")

        quick_links = ctk.CTkFrame(date_time, fg_color="transparent")

        quick_links.grid(row=2, sticky="nesw")

        for link in self.appstate.links:
            link_frame = ctk.CTkFrame(quick_links, fg_color="transparent", height=24)
            create_grid(link_frame, columns=[1, 7])
            
            icon = load_favicon(link.url, 20) if load_favicon(link.url, 20) else load_icon(link.icon, size=20, hover_image=False)
            image = ctk.CTkLabel(link_frame, text="", image=icon)
            label = HyperLink(link_frame, text=link.name, cursor="hand2")
            
            label.bind(f"<Button-1>", lambda _: callback(link.url))
            image.grid(row=0, column=0, sticky="nesw")
            label.grid(row=0, column=1, sticky="w")

            link_frame.pack(expand=True, fill="both")

    def _build_pomodoro_column(self):
        pomodoro = ctk.CTkFrame(self, fg_color="transparent")
        pomodoro_wheel = PomodoroWheel(
            pomodoro, 
            color = '#5B7DB1',
            time = self.appstate.pomodoro.time_remaining,
            mode = self.appstate.pomodoro.mode.label,
            size=pomodoro.cget('width')
            )
        pomodoro_wheel.set_progress(self.appstate.pomodoro.time_remaining / self.appstate.pomodoro.mode.duration)
        pomodoro_wheel.pack()
        pomodoro.grid(row=1, column=1, sticky="nesw")

    def _build_reminder_tasks_column(self):
        tasks_reminder = ctk.CTkFrame(self, fg_color="#00FF11")
        tasks_reminder.grid(row=1, column=2, sticky="nesw")

        create_grid(tasks_reminder, rows=[1, 5])
        
        #info for upcoming reminder
        next_reminder = self.appstate.next_reminder
        
        #create frame for next reminder, place in section and split for icon + text
        upcoming_reminder = ctk.CTkFrame(tasks_reminder, fg_color="#E6CD44")
        upcoming_reminder.grid(row=0, column=0, sticky="new", pady=8)
        create_grid(upcoming_reminder, columns=2)
        
        #get attrs
        reminder_icon = load_icon("reminders", category="tabs")
        reminder_text = f"{next_reminder.name} in {format_duration(next_reminder.time_until())}"
        #put in frame
        reminder_ctk_icon = ctk.CTkLabel(upcoming_reminder, text="", image=reminder_icon)
        reminder_ctk_text = ctk.CTkLabel(upcoming_reminder, text=reminder_text)
        reminder_ctk_icon.grid(row=0, column=0, sticky="ne", padx="2")
        reminder_ctk_text.grid(row=0, column=1, sticky="nw", padx="2")