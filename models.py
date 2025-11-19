from dataclasses import dataclass
from typing import Optional

@dataclass
class Student:
    email_address: str  # acts as unique student_id in this starter
    first_name: str
    last_name: str
    course_id: str
    grade_letter: str
    marks: int

@dataclass
class Course:
    course_id: str
    course_name: str
    description: str = ""

@dataclass
class Professor:
    professor_id: str  # we use email for id per sample
    name: str
    rank: str
    course_id: str

@dataclass
class LoginUser:
    user_id: str      # email/username
    password_enc: str # encrypted in file
    role: str         # e.g., "professor" or "student"
