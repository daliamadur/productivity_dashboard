from dataclasses import dataclass
from enum import Enum, auto
from datetime import timedelta, datetime
from typing import Optional

class PomodoroMode(Enum):
    WORK = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()

class PomodoroStatus(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()

class Period(Enum):
    MINUTES = 1
    HOURS = 60

class Category(Enum):
    ADMIN_SETUP = auto()
    CAREER_PRESENCE = auto()
    SKILL_BUILDING = auto()
    DEEP_WORK = auto()
    CREATIVE_EXPANSION = auto()
    OTHER_WORK = auto()

class Energy(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

@dataclass
class Link():
    name: str
    icon: str
    url: str

@dataclass
class Reminder():
    name: str
    frequency: int
    period: Period
    next: Optional[datetime]
    icon: str
    alert: bool
    toast: bool
    
    def time_until(self) -> timedelta:
        return self.next - datetime.now()

@dataclass
class Task():
    name: str
    category: Category
    energy: Energy
    priority: Priority
    steps: list[str]

@dataclass
class PomodoroState():
    time_remaining: int
    mode: PomodoroMode
    status: PomodoroStatus