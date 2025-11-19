from models import Student, Course, Professor
from storage import CsvTable
from services import StudentService, CourseService, ProfessorService, AuthService

def bootstrap_tables():
    students = CsvTable("data/students.csv", ["Email_address", "First_name", "Last_name", "Course.id", "grades", "Marks"])
    course   = CsvTable("data/course.csv",   ["Course_id", "Course_name", "Description"])
    profs    = CsvTable("data/professors.csv", ["Professor_id", "Name", "Rank", "Course.id"])
    login    = CsvTable("data/login.csv",    ["User_id", "Password", "Role"])
    return students, course, profs, login

def main():
    students_tbl, course_tbl, prof_tbl, login_tbl = bootstrap_tables()
    student_svc = StudentService(students_tbl)
    course_svc  = CourseService(course_tbl)
    prof_svc    = ProfessorService(prof_tbl)
    auth_svc    = AuthService(login_tbl)

    print("=== CheckMyGrade (Lab 1) ===")
    print("1) Register  2) Login  3) Demo  0) Exit")
    choice = input("> ").strip()

    if choice == "1":
        uid = input("Email/User ID: ").strip()
        pw  = input("Password: ").strip()
        role = input("Role (professor/student): ").strip() or "student"
        auth_svc.register(uid, pw, role)
        print("Registered. Now login.")
    if choice in ("1","2"):
        uid = input("Email/User ID: ").strip()
        pw  = input("Password: ").strip()
        if auth_svc.login(uid, pw):
            print("Login success.")
        else:
            print("Login failed.")
            return
    elif choice == "3":
        print("Running a quick demo with search/sort/stats...")

    while True:
        print("\nMenu:")
        print(" 1) Add student")
        print(" 2) Search student by email")
        print(" 3) Sort students by marks (desc)")
        print(" 4) Course stats")
        print(" 5) Add course")
        print(" 6) Add professor")
        print(" 7) Course report")
        print(" 0) Exit")
        c = input("> ").strip()
        if c == "0":
            print("Bye.")
            break
        elif c == "1":
            email = input("Email: ").strip()
            fn = input("First name: ").strip()
            ln = input("Last name: ").strip()
            cid = input("Course id: ").strip()
            grade = input("Grade letter (A/B/C...): ").strip() or "A"
            marks = int(input("Marks (0-100): ").strip())
            student_svc.add_student(Student(email, fn, ln, cid, grade, marks))
            print("Added.")
        elif c == "2":
            email = input("Email to search: ").strip()
            result, ms = student_svc.search(email_address=email)
            print(f"Search took {ms:.2f} ms. Found:")
            for s in result:
                print(f" {s.email_address} {s.first_name} {s.last_name} {s.course_id} {s.grade_letter} {s.marks}")
        elif c == "3":
            result, ms = student_svc.sort("marks", reverse=True)
            print(f"Sort took {ms:.2f} ms. Top 5:")
            for s in result[:5]:
                print(f" {s.email_address} {s.first_name} {s.last_name} {s.marks}")
        elif c == "4":
            cid = input("Course id: ").strip()
            stats = student_svc.course_stats(cid)
            if not stats:
                print("No data for course.")
            else:
                print(f"Avg: {stats['average']:.2f}  Median: {stats['median']:.2f}  Count: {stats['count']}")
        elif c == "5":
            cid = input("Course id: ").strip()
            name = input("Course name: ").strip()
            desc = input("Description: ").strip()
            course_svc.add_course(Course(cid, name, desc))
            print("Course added.")
        elif c == "6":
            pid = input("Professor id (email): ").strip()
            name = input("Name: ").strip()
            rank = input("Rank: ").strip()
            cid = input("Course id: ").strip()
            prof_svc.add_professor(Professor(pid, name, rank, cid))
            print("Professor added.")
        elif c == "7":
            cid = input("Course id: ").strip()
            rows = student_svc.course_report(cid)
            print(f"{len(rows)} students in {cid}:")
            for s in rows:
                print(f" {s.email_address} {s.first_name} {s.last_name} {s.marks}")
        else:
            print("Unknown choice.")

if __name__ == "__main__":
    main()
