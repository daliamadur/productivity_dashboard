from dataclasses import dataclass
from typing import Callable
from .pages.home import HomeTab
from .pages.links import LinksTab
from .pages.pomodoro import PomodoroTab
from .pages.reminders import RemindersTab
from .pages.tasks import TasksTab
from .pages.stats import StatsTab
from .pages.settings import SettingsTab

@dataclass
class TabMeta():
    name: str
    icon: str
    builder: Callable

MENU = TabMeta(
    name="Menu",
    icon="menu",
    builder=None
)

PAGES = {
    "HOME": TabMeta(
        name="Home",
        icon="home",
        builder=HomeTab,
    ),
    "TASKS": TabMeta(
        name="Task List",
        icon="tasks",
        builder=TasksTab,
    ),
    "POMODORO": TabMeta(
        name="Pomodoro",
        icon="pomodoro",
        builder=PomodoroTab,
    ),
    "LINKS": TabMeta(
        name="Quick Links",
        icon="links",
        builder=LinksTab,
    ),
    "REMINDERS": TabMeta(
        name="Reminders",
        icon="reminders",
        builder=RemindersTab,
    ),
    "STATS": TabMeta(
        name="Personal Stats",
        icon="stats",
        builder=StatsTab,
    ),
    "SETTINGS": TabMeta(
        name="Settings",
        icon="settings",
        builder=SettingsTab,
    )
}