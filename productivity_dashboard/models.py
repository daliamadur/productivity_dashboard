from dataclasses import dataclass
from enum import Enum, auto
from datetime import timedelta, datetime
from typing import Optional, Sequence

class PomodoroMode(Enum):
    WORK = ("work", 25)
    SHORT_BREAK = ("short break", 5)
    LONG_BREAK = ("long break", 10)

    @property
    def duration(self):
        return self.value[1] * 60

    @property
    def label(self):
        return self.value[0]

    @classmethod
    def get_time(cls, value):
        for member in cls:
            if member == value:
                return value.duration * 60
        raise ValueError(f"No matching value for {value}")
    
    @classmethod
    def get_label(cls, value):
        for member in cls:
            if member == value:
                return value['label']
            raise ValueError(f"No matching value for {value}")
            
class PomodoroStatus(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()

class Period(Enum):
    MINUTES = 1
    HOURS = 60

    @classmethod
    def get_label(cls, period, value=0):
        for member in cls:
            if member == period:
                name = member.name.lower()
                return name if value != 1 else name[:-1]
        raise ValueError(f"No matching value for {period}")

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
    next: Optional[datetime] #how much time until the next reminder (should update every minute?)
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

@dataclass
class Layout():
    rows: Sequence[int] = (1, 3)
    body_rows: Optional[Sequence[int]] = None
    body_columns: Optional[Sequence[int]] = None