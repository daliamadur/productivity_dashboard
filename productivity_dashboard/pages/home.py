from ..utils import HyperLink, create_grid, format_date, format_time, format_duration, load_icon, load_favicon, callback, build_top_panel, build_bottom_panel
from ..appstate import AppState
from ..pomodoro_meter import PomodoroWheel
import customtkinter as ctk

class HomeTab(ctk.CTkFrame):
    def __init__(self, parent, name, appstate: AppState):
        super().__init__(parent)
        self.appstate = appstate

        create_grid(self, rows=[1, 3])

        self.head = build_top_panel(name, self)
        self.body = build_bottom_panel(self, rows=[1, 3, 2], columns=[1,3,1])

        self._build_date_time_column()
        self._build_pomodoro_column()
        self._build_reminder_tasks_column()

    def _build_date_time_column(self):
        date = ctk.CTkLabel(self.body, text=format_date(self.appstate.date_time), fg_color="transparent")
        date.grid(row=0, column=0, sticky="nesw")

        time = ctk.CTkLabel(self.body, text=format_time(self.appstate.date_time), fg_color="transparent")
        time.grid(row=1, column=0, sticky="nesw")

        quick_links = ctk.CTkFrame(self.body, fg_color="transparent")
        create_grid(quick_links, rows=2, columns=2, propagate=True)

        quick_links.grid(row=2, column=0, sticky="nesw")

        for i, link in enumerate(self.appstate.links):
            link_frame = ctk.CTkFrame(quick_links, fg_color="transparent", height=24)
            create_grid(link_frame, columns=2, propagate=True)
            
            icon = load_favicon(link.url, 20) if load_favicon(link.url, 20) else load_icon(link.icon, size=20, hover_image=False)
            image = ctk.CTkLabel(link_frame, text="", image=icon)
            label = HyperLink(link_frame, text=link.name, cursor="hand2")
            
            label.bind(f"<Button-1>", lambda _: callback(link.url))
            image.grid(row=0, column=0, sticky="e", padx=2)
            label.grid(row=0, column=1, sticky="w", padx=2)

            link_frame.grid(row=0 if i < 2 else 1, column=i%2, sticky="nsew")

    def _build_pomodoro_column(self):
        pomodoro = ctk.CTkFrame(self.body, fg_color="transparent")
        pomodoro_wheel = PomodoroWheel(
            pomodoro, 
            color = '#5B7DB1',
            time = self.appstate.pomodoro.time_remaining,
            mode = self.appstate.pomodoro.mode.label,
            size=pomodoro.cget('width')
            )
        pomodoro_wheel.set_progress(self.appstate.pomodoro.time_remaining / self.appstate.pomodoro.mode.duration)
        pomodoro_wheel.pack()
        pomodoro.grid(row=0, column=1, rowspan=3, sticky="nesw")

    def _next_reminder(self, parent):
        next_reminder = self.appstate.next_reminder
        
        #create frame for next reminder, place in section and split for icon + text
        upcoming_reminder = ctk.CTkFrame(parent, fg_color="transparent")
        upcoming_reminder.grid(row=0, column=2, sticky="nesw")
        create_grid(upcoming_reminder, columns=2)
        
        #get attrs
        reminder_icon = load_icon("reminders", category="tabs")
        reminder_text = f"{next_reminder.name} in {format_duration(next_reminder.time_until())}"
        #put in frame
        reminder_ctk_icon = ctk.CTkLabel(upcoming_reminder, text="", image=reminder_icon)
        reminder_ctk_text = ctk.CTkLabel(upcoming_reminder, text=reminder_text)
        reminder_ctk_icon.grid(row=0, column=0, sticky="e", padx=2)
        reminder_ctk_text.grid(row=0, column=1, sticky="w", padx=2)
    
    def _task_list(self, parent):
        task_list = ctk.CTkFrame(parent, fg_color="transparent")
        task_list.grid(row=1, column=2, rowspan=2, sticky="nsw", padx=8)
        create_grid(task_list, rows=5)
        
        for i, task in enumerate(self.appstate.top_tasks):
            checkbox = ctk.CTkCheckBox(task_list,
                                       text=task.name,
                                       border_width=2,
                                       border_color="white",
                                       corner_radius=24,
                                       checkbox_height=20,
                                       checkbox_width=20,
                                       hover_color="#808080",
                                       )
            checkbox.grid(row=i, column=0, padx=4)

    def _build_reminder_tasks_column(self):      
        #info for upcoming reminder
        self._next_reminder(self.body)
        self._task_list(self.body)