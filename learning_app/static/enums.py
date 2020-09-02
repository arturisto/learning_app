from enum import Enum


class QuestionType(Enum):
    MULTI = "Multiple Choice Question"
    SINGLE = "Single Answer Question"


class QuestionComplexity(Enum):
    HARD = "Hard"
    ADVANCED = "Advanced"
    EASY = "Easy"


class ExamType(Enum):
    PRACTICE = "Practice Exam"
    REAL = "Real Exam"


class UserType(str, Enum):
    STUDENT = "Student"
    TEACHER = "Teacher"
    ADMIN = "Admin"
