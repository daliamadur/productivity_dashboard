import customtkinter as ctk
from ..utils import create_grid, format_pomodoro, build_top_panel, build_bottom_panel
from ..appstate import AppState

class PomodoroTab(ctk.CTkFrame):
    def __init__(self, parent, name, appstate: AppState):
        super().__init__(parent)

        self.appstate = appstate.pomodoro
        create_grid(self, rows=[1, 3])

        self.head = build_top_panel(name, self)
        self.body = build_bottom_panel(self, columns=[3,2])

        self._build_pomodoro_column()
        self._build_settings_column()

    def _build_pomodoro_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nesw")
        create_grid(frame, rows=[1, 1, 3, 1], columns=[1, 1, 1, 3, 1, 1, 1])

        #dummy variables
        total_sessions = 3
        target_sessions = 8

        #real variables
        mode = self.appstate.mode.label
        remaining_time = self.appstate.time_remaining
        
        total_time = self.appstate.mode.duration

        #session count
        session_count = ctk.CTkLabel(frame, text=total_sessions)
        session_count.grid(row=0, column=0)

        #progress bar
        progress = ctk.CTkProgressBar(frame)
        progress.set(remaining_time / total_time)
        progress.grid(row=0, column=1, columnspan=5, sticky="ew")

        #total sessions (goal)
        target_sessions = ctk.CTkLabel(frame, text=target_sessions)
        target_sessions.grid(row=0, column=6)

        #pomodoro mode
        mode_label = ctk.CTkLabel(frame, text=mode)
        mode_label.grid(row=1, column=0, columnspan=7, sticky="nesw")

        #duration
        duration_label = ctk.CTkLabel(frame, text=format_pomodoro(remaining_time))
        duration_label.grid(row=2, column=0, columnspan=7, sticky="nesw")

        #buttons
        start_button = ctk.CTkButton(frame, text="Start")
        start_button.grid(row=3, column=0, columnspan=3)

        pause_button = ctk.CTkButton(frame, text="Pause")
        pause_button.grid(row=3, column=3)
        
        reset_button = ctk.CTkButton(frame, text="Reset")
        reset_button.grid(row=3, column=4, columnspan=3)
           
    def _build_settings_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(row=0, column=1, sticky="nesw")
        create_grid(frame, rows=5, columns=[3, 1, 2])

        label = ctk.CTkLabel(frame, text="Settings")
        label.grid(row=0, column=0, columnspan=3)

        #duration
        duration_config_label = ctk.CTkLabel(frame, text="Work Duration")
        duration_config_value = ctk.CTkEntry(frame, width=50)
        duration_config_units_label = ctk.CTkLabel(frame, text="minutes")

        duration_config_label.grid(row=1, column=0, sticky="nsw")
        duration_config_value.grid(row=1, column=1)
        duration_config_units_label.grid(row=1, column=2, sticky="nsw")

        #break
        break_config_label = ctk.CTkLabel(frame, text="Break duration")
        break_config_value = ctk.CTkEntry(frame, width=50)
        break_config_units_label = ctk.CTkLabel(frame, text="minutes")

        break_config_label.grid(row=2, column=0, sticky="nsw")
        break_config_value.grid(row=2, column=1)
        break_config_units_label.grid(row=2, column=2, sticky="nsw")

        #target sessions
        target_config_label = ctk.CTkLabel(frame, text="Number of target sessions")
        target_config_value = ctk.CTkEntry(frame, width=50)
        target_config_units_label = ctk.CTkLabel(frame, text="sessions")

        target_config_label.grid(row=3, column=0, sticky="nsw")
        target_config_value.grid(row=3, column=1)
        target_config_units_label.grid(row=3, column=2, sticky="nsw")

        #auto cycle
        auto_cycle_label = ctk.CTkLabel(frame, text="Auto Cycle")
        auto_cycle_toggle = ctk.CTkSwitch(frame, text="")

        auto_cycle_label.grid(row=4, column=0, columnspan=2, sticky="nsw")
        auto_cycle_toggle.grid(row=4, column=2, sticky="nsw")