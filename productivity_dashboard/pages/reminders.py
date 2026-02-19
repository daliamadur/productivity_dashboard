import customtkinter as ctk
from .page import Tab
from ..models import Reminder, Layout
from ..utils import create_grid, load_icon
from ..CTkScrollableDropdown import ctk_scrollable_dropdown as ctk_sd

class RemindersTab(Tab):
    def __init__(self, parent, name, reminders):
        super().__init__(
            parent=parent,
            name=name,
            state=reminders,
            layout=Layout(
                body_columns=[3, 2]
            )   
        )

        self.state: list[Reminder]

    def _build(self):
        self._build_reminders_column()
        self._build_settings_column()

    def _build_reminders_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(column=0, row=0, sticky="nesw")
        create_grid(frame, rows=len(self.state), columns=[3, 2])

        for i, reminder in enumerate(self.state):
            reminder_label = ctk.CTkFrame(frame, fg_color="transparent")
            create_grid(reminder_label, columns=[1, 5])

            reminder_icon = ctk.CTkLabel(reminder_label, text="", image=load_icon(reminder.icon))
            reminder_text = ctk.CTkLabel(reminder_label, text=reminder.name)
            reminder_icon.grid(row=0, column=0, padx=12, sticky="nse")
            reminder_text.grid(row=0, column=1, sticky="nsw")
            
            reminder_frequency = ctk.CTkLabel(frame, text=f"Every {reminder.frequency} {reminder.period.get_label(reminder.period, reminder.frequency)}", fg_color="transparent")
            reminder_frequency.grid()

            reminder_label.grid(row=i, column=0, sticky="nsew")
            reminder_frequency.grid(row=i, column=1, sticky="nsw", padx=16)

    def _build_add_reminder_column(self, frame, start):
        label = ctk.CTkLabel(frame, text="Add Reminder")
        frequency_label = ctk.CTkLabel(frame, text="Every")
        frequency_value = ctk.CTkEntry(frame)
        frequency_period = ctk.CTkOptionMenu(frame, values=["minutes", "hours"])

        alert = ctk.CTkFrame(frame, fg_color="transparent")
        create_grid(alert, columns=[5, 1])
        alert_label = ctk.CTkLabel(alert, text="Alert Sound")
        alert_toggle = ctk.CTkSwitch(alert, text="")
        alert_label.grid(row=0, column=0)
        alert_toggle.grid(row=0, column=1)

        toast = ctk.CTkFrame(frame, fg_color="transparent")
        create_grid(toast, columns=[5, 1])
        toast_label = ctk.CTkLabel(toast, text="Push Notification")
        toast_toggle = ctk.CTkSwitch(toast, text="")
        toast_label.grid(row=0, column=0)
        toast_toggle.grid(row=0, column=1)

        add_button = ctk.CTkButton(frame, text="Add new reminder")

        label.grid(row=start, column=0, columnspan=3)
        frequency_label.grid(row=start+1, column=0)
        frequency_value.grid(row=start+1, column=1)
        frequency_period.grid(row=start+1, column=2)
        alert.grid(row=start+2, column=0, columnspan=2, sticky="nesw")
        toast.grid(row=start+2, column=2, sticky="nesw")
        add_button.grid(row=start+3, column=0, columnspan=3, sticky="e", padx=16)

    def _build_edit_reminder_column(self, frame, start):
        label = ctk.CTkLabel(frame, text="Edit Reminder")

        edit_reminder_select = ctk.CTkComboBox(frame)
        ctk_sd.CTkScrollableDropdown(edit_reminder_select, values=[reminder.name for reminder in self.state])
        edit_reminder_select.set(self.state[0].name)

        frequency_label = ctk.CTkLabel(frame, text="Every")
        frequency_value = ctk.CTkEntry(frame)
        frequency_period = ctk.CTkOptionMenu(frame, values=["minutes", "hours"])

        alert = ctk.CTkFrame(frame, fg_color="transparent")
        create_grid(alert, columns=[5, 1])
        alert_label = ctk.CTkLabel(alert, text="Alert Sound")
        alert_toggle = ctk.CTkSwitch(alert, text="")
        alert_label.grid(row=0, column=0)
        alert_toggle.grid(row=0, column=1)

        toast = ctk.CTkFrame(frame, fg_color="transparent")
        create_grid(toast, columns=[5, 1])
        toast_label = ctk.CTkLabel(toast, text="Push Notification")
        toast_toggle = ctk.CTkSwitch(toast, text="")
        toast_label.grid(row=0, column=0)
        toast_toggle.grid(row=0, column=1)

        edit_button = ctk.CTkButton(frame, text="Save edited reminder")

        label.grid(row=start, column=0, columnspan=3)
        edit_reminder_select.grid(row=start+1, column=0, columnspan=3)
        frequency_label.grid(row=start+2, column=0)
        frequency_value.grid(row=start+2, column=1)
        frequency_period.grid(row=start+2, column=2)
        alert.grid(row=start+3, column=0, columnspan=2, sticky="nesw")
        toast.grid(row=start+3, column=2, sticky="nesw")
        edit_button.grid(row=start+4, column=0, columnspan=3, sticky="e", padx=16)

    def _build_delete_reminder_column(self, frame, start):
        label = ctk.CTkLabel(frame, text="Delete Reminder")

        edit_reminder_select = ctk.CTkComboBox(frame)
        ctk_sd.CTkScrollableDropdown(edit_reminder_select, values=[reminder.name for reminder in self.state])
        edit_reminder_select.set(self.state[0].name)

        delete_button = ctk.CTkButton(frame, text="Delete Reminder")

        label.grid(row=start, column=0, columnspan=3)
        edit_reminder_select.grid(row=start+1, column=0, columnspan=3)
        delete_button.grid(row=start+2, column=0, columnspan=3, sticky="e", padx=16)

    def _build_settings_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(column=1, row=0, sticky="nesw", pady=16)
        
        create_grid(frame, rows=14, columns=[2, 1, 3])
        self._build_add_reminder_column(frame, 0)
        self._build_edit_reminder_column(frame, 5)
        self._build_delete_reminder_column(frame, 11)