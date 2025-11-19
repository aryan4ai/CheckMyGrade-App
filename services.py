from __future__ import annotations
from typing import List, Dict, Optional, Tuple
import time, statistics

from models import Student, Course, Professor, LoginUser
from storage import CsvTable
from security import encrypt_password, decrypt_password

class StudentService:
    def __init__(self, table: CsvTable):
        self.table = table
        self._students = [self._row_to_student(r) for r in self.table.read_all()]
        self._index = {s.email_address: s for s in self._students}

    # --- Conversion helpers
    def _row_to_student(self, r):
        return Student(
            email_address=r["Email_address"].strip(),
            first_name=r["First_name"].strip(),
            last_name=r["Last_name"].strip(),
            course_id=r["Course.id"].strip(),
            grade_letter=r["grades"].strip(),
            marks=int(r["Marks"]),
        )

    def _student_to_row(self, s: Student):
        return {
            "Email_address": s.email_address,
            "First_name": s.first_name,
            "Last_name": s.last_name,
            "Course.id": s.course_id,
            "grades": s.grade_letter,
            "Marks": str(s.marks),
        }

    # --- CRUD
    def add_student(self, s: Student) -> None:
        if not s.email_address:
            raise ValueError("student_id (email_address) cannot be empty")
        if s.email_address in self._index:
            raise ValueError(f"Duplicate student_id: {s.email_address}")
        self._students.append(s)
        self._index[s.email_address] = s
        self.table.append(self._student_to_row(s))

    def delete_student(self, email_address: str) -> bool:
        s = self._index.pop(email_address, None)
        if not s:
            return False
        self._students = [x for x in self._students if x.email_address != email_address]
        self._flush()
        return True

    def update_student(self, email_address: str, **updates) -> bool:
        s = self._index.get(email_address)
        if not s:
            return False
        for k, v in updates.items():
            if hasattr(s, k):
                setattr(s, k, v)
        self._flush()
        return True

    def _flush(self) -> None:
        rows = [self._student_to_row(s) for s in self._students]
        self.table.write_all(rows)

    # --- Search & Sort with timing
    def search(self, **criteria):
        t0 = time.perf_counter()
        result = self._students
        for k, v in criteria.items():
            result = [s for s in result if str(getattr(s, k)).lower() == str(v).lower()]
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return result, elapsed_ms

    def sort(self, key: str, reverse: bool = False):
        t0 = time.perf_counter()
        if key == "email_address":
            result = sorted(self._students, key=lambda s: s.email_address.lower(), reverse=reverse)
        elif key == "marks":
            result = sorted(self._students, key=lambda s: s.marks, reverse=reverse)
        elif key == "name":
            result = sorted(self._students, key=lambda s: (s.last_name.lower(), s.first_name.lower()), reverse=reverse)
        else:
            raise ValueError("Unsupported sort key")
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return result, elapsed_ms

    # --- Stats & Reports
    def course_stats(self, course_id: str):
        course_marks = [s.marks for s in self._students if s.course_id == course_id]
        if not course_marks:
            return None
        avg = sum(course_marks) / len(course_marks)
        med = statistics.median(course_marks)
        return {"average": avg, "median": med, "count": len(course_marks)}

    def course_report(self, course_id: str):
        return [s for s in self._students if s.course_id == course_id]

    def student_report(self, email_address: str):
        return self._index.get(email_address)

class CourseService:
    def __init__(self, table: CsvTable):
        self.table = table
        self._courses = {}
        for r in self.table.read_all():
            self._courses[r["Course_id"]] = Course(r["Course_id"], r["Course_name"], r.get("Description",""))

    def add_course(self, c: Course) -> None:
        if not c.course_id:
            raise ValueError("course_id cannot be empty")
        if c.course_id in self._courses:
            raise ValueError(f"Duplicate course_id: {c.course_id}")
        self._courses[c.course_id] = c
        self.table.append({"Course_id": c.course_id, "Course_name": c.course_name, "Description": c.description})

    def delete_course(self, course_id: str) -> bool:
        if course_id not in self._courses:
            return False
        del self._courses[course_id]
        self._flush()
        return True

    def update_course(self, course_id: str, **updates) -> bool:
        c = self._courses.get(course_id)
        if not c: return False
        for k, v in updates.items():
            if hasattr(c, k): setattr(c, k, v)
        self._flush(); return True

    def _flush(self) -> None:
        rows = [{"Course_id": c.course_id, "Course_name": c.course_name, "Description": c.description} for c in self._courses.values()]
        self.table.write_all(rows)

class ProfessorService:
    def __init__(self, table: CsvTable):
        self.table = table
        self._professors = {}
        for r in self.table.read_all():
            self._professors[r["Professor_id"]] = Professor(r["Professor_id"], r["Name"], r["Rank"], r["Course.id"])

    def add_professor(self, p: Professor) -> None:
        if not p.professor_id:
            raise ValueError("professor_id cannot be empty")
        if p.professor_id in self._professors:
            raise ValueError(f"Duplicate professor_id: {p.professor_id}")
        self._professors[p.professor_id] = p
        self.table.append({"Professor_id": p.professor_id, "Name": p.name, "Rank": p.rank, "Course.id": p.course_id})

    def delete_professor(self, professor_id: str) -> bool:
        if professor_id not in self._professors:
            return False
        del self._professors[professor_id]
        self._flush(); return True

    def update_professor(self, professor_id: str, **updates) -> bool:
        p = self._professors.get(professor_id)
        if not p: return False
        for k, v in updates.items():
            if hasattr(p, k): setattr(p, k, v)
        self._flush(); return True

    def _flush(self) -> None:
        rows = [{"Professor_id": p.professor_id, "Name": p.name, "Rank": p.rank, "Course.id": p.course_id} for p in self._professors.values()]
        self.table.write_all(rows)

class AuthService:
    def __init__(self, table: CsvTable):
        self.table = table
        self._users = {}
        for r in self.table.read_all():
            self._users[r["User_id"]] = LoginUser(r["User_id"], r["Password"], r["Role"])

    def register(self, user_id: str, plain_password: str, role: str) -> None:
        if user_id in self._users:
            raise ValueError("User already exists")
        enc = encrypt_password(plain_password)
        self._users[user_id] = LoginUser(user_id, enc, role)
        self.table.append({"User_id": user_id, "Password": enc, "Role": role})

    def login(self, user_id: str, plain_password: str) -> bool:
        u = self._users.get(user_id)
        if not u: return False
        return decrypt_password(u.password_enc) == plain_password
