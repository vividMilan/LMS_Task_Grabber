from enum import Enum

class ChipType(str, Enum):
    COURSE = "course"
    DATE = "date"
    TIME = "time"
    FILE = "file"