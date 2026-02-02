from dataclasses import dataclass
from .models import PomodoroState, Link, Task, Reminder
from datetime import datetime

@dataclass
class AppState():
    date_time: datetime
    #quick acess links (top n (however many fit))
    links: list[Link]
    #pomodoro time -> time left, whether it's a break or work, pomodoro status (running or paused)
    pomodoro: PomodoroState
    #next reminder -> name, when it's due maybe?
    next_reminder: Reminder
    #top tasks -> (again top n highest priority)
    top_tasks: list[Task]