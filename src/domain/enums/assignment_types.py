from enum import Enum

class AssignmentType(str, Enum):
    MINI_PROJECT = "mini_project"
    VIVA_SLOT = "viva_slot"
    QUIZ = "quiz"
    TMA = "tma"
    EXAM = "exam"