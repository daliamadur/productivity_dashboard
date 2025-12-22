import customtkinter as ctk
from datetime import datetime
from productivity_dashboard import create_grid, format_date, format_time

#row=0, column=0, sticky="ew", padx=8, pady=4, columnspan=2

class HomeTab(ctk.CTkFrame):
    def __init__(self, parent, name, appstate):
        super().__init__(parent)

        create_grid(self, columns=3, rows=[1, 3])

        self.heading = ctk.CTkFrame(self, fg_color="#FF0000")

        #icon_image = ctk.CTkLabel(self.heading, text="", image = load_icon(icon, size=36, category="tabs"))
        label = ctk.CTkLabel(self.heading, text=name, font=("Ubuntu", 36, "bold"), justify=ctk.CENTER)

        #icon_image.pack(side=ctk.LEFT, fill="both")
        label.pack(side=ctk.LEFT, fill="both", padx=48)

        self.heading.grid(row = 0, column=0, columnspan = 3, sticky="nesw")

        #COLUMN 1 DATE-TIME
        self.date_time = ctk.CTkFrame(self, fg_color="transparent")
        self.date_time.grid(row=1, column=0, sticky="nesw")
        
        create_grid(self.date_time, rows=[1, 3, 1])

        self.date = ctk.CTkLabel(self.date_time, text=format_date(datetime.now()), font=("Ubuntu", 20), fg_color="transparent" )
        self.date.grid(row=0, sticky="nesw")

        self.time = ctk.CTkLabel(self.date_time, text=format_time(datetime.now()), font=("Ubuntu", 72), fg_color="transparent")
        self.time.grid(row=1, sticky="nesw")

        self.quick_links = ctk.CTkFrame(self.date_time, fg_color="#FFFF00")

        self.quick_links.grid(row=2, sticky="nesw")

        #COLUMN 2 - POMODORO TIMER
        self.pomodoro = ctk.CTkFrame(self, fg_color="#00A6FF")
        self.pomodoro.grid(row=1, column=1, sticky="nesw")

        #COLUMN 3 - TASKS + REMINDERS
        self.tasks_reminder = ctk.CTkFrame(self, fg_color="#00FF11")
        self.tasks_reminder.grid(row=1, column=2, sticky="nesw")
        
    def update_time(self):
        self.date.configure(text=format_date(datetime.now()))
        self.time.configure(text=format_time(datetime.now()))
        self.after(1, self.update_time)