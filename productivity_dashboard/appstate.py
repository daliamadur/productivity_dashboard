from dataclasses import dataclass
from productivity_dashboard import PomodoroState, Link, Task, Reminder

@dataclass
class AppState():
    #quick acess links (top n (however many fit))
    links: list[Link]
    #pomodoro time -> time left, whether it's a break or work, pomodoro status (running or paused)
    pomodoro: PomodoroState
    #next reminder -> name, when it's due maybe?
    next_reminder: Reminder
    #top tasks -> (again top n highest priority)
    top_tasks = list[Task]