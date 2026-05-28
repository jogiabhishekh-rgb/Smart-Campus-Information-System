from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STUDENTS_FILE = DATA_DIR / "students.csv"
ENROLLMENTS_FILE = DATA_DIR / "enrollments.json"
ACADEMIC_RECORDS_FILE = DATA_DIR / "academic_records.csv"
REPORTS_DIR = BASE_DIR / "reports"

COURSES = {
    "PY101": {"name": "Python Programming", "credits": 4, "fee": 4500},
    "DB102": {"name": "Database Management", "credits": 3, "fee": 3500},
    "WD103": {"name": "Web Development", "credits": 3, "fee": 4000},
    "AI104": {"name": "AI Fundamentals", "credits": 4, "fee": 5500},
}


@dataclass
class Student:
    student_id: str
    name: str
    department: str
    semester: int
    marks: float
    attendance: float

    @property
    def grade(self) -> str:
        return calculate_grade(self.marks)

    @property
    def result(self) -> str:
        return "Pass" if self.marks >= 40 and self.attendance >= 75 else "Needs Improvement"


def ensure_storage() -> None:
    """Ensure all required directories and files exist."""
    try:
        DATA_DIR.mkdir(exist_ok=True, parents=True)
        REPORTS_DIR.mkdir(exist_ok=True, parents=True)

        if not STUDENTS_FILE.exists():
            with STUDENTS_FILE.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=list(Student.__annotations__.keys()))
                writer.writeheader()

        if not ENROLLMENTS_FILE.exists():
            ENROLLMENTS_FILE.write_text("{}", encoding="utf-8")

        if not ACADEMIC_RECORDS_FILE.exists():
            with ACADEMIC_RECORDS_FILE.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["student_id", "course_code", "internal_marks", "external_marks", "total", "grade"])
    except OSError as error:
        print(f"Error ensuring storage: {error}")


def calculate_grade(marks: float) -> str:
    """Calculate grade based on marks. Marks should be between 0 and 100."""
    if marks < 0:
        return "Invalid"
    if marks >= 90:
        return "A+"
    if marks >= 80:
        return "A"
    if marks >= 70:
        return "B"
    if marks >= 60:
        return "C"
    if marks >= 50:
        return "D"
    if marks >= 40:
        return "E"
    return "F"


def calculate_fee(course_codes: list[str], scholarship_percent: float = 0) -> float:
    """Calculate total fee for given course codes with optional scholarship."""
    total = sum(COURSES[code]["fee"] for code in course_codes if code in COURSES)
    discount = total * (scholarship_percent / 100)
    return max(0, total - discount)


def load_students() -> list[Student]:
    """Load all students from CSV file."""
    ensure_storage()
    students: list[Student] = []
    try:
        with STUDENTS_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                return students
            for row in reader:
                if row and all(key in row for key in Student.__annotations__.keys()):
                    students.append(
                        Student(
                            student_id=row["student_id"],
                            name=row["name"],
                            department=row["department"],
                            semester=int(row["semester"]),
                            marks=float(row["marks"]),
                            attendance=float(row["attendance"]),
                        )
                    )
    except (ValueError, KeyError, OSError) as error:
        print(f"Error loading students: {error}")
    return students


def save_students(students: list[Student]) -> None:
    """Save students to CSV file."""
    try:
        with STUDENTS_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(Student.__annotations__.keys()))
            writer.writeheader()
            writer.writerows(asdict(student) for student in students)
    except OSError as error:
        print(f"Error saving students: {error}")


def load_enrollments() -> dict[str, list[str]]:
    """Load enrollments from JSON file."""
    ensure_storage()
    try:
        return json.loads(ENROLLMENTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading enrollments: {error}")
        return {}


def save_enrollments(enrollments: dict[str, list[str]]) -> None:
    """Save enrollments to JSON file."""
    try:
        ENROLLMENTS_FILE.write_text(json.dumps(enrollments, indent=2), encoding="utf-8")
    except OSError as error:
        print(f"Error saving enrollments: {error}")


def input_float(prompt: str, minimum: float = 0, maximum: float = 100) -> float:
    """Get float input from user with validation."""
    while True:
        try:
            value = float(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Enter a valid number.")


def input_int(prompt: str, minimum: int = 1, maximum: int = 8) -> int:
    """Get integer input from user with validation."""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Enter a valid integer.")


def register_student() -> None:
    """Register a new student."""
    students = load_students()
    student_id = input("Student ID: ").strip().upper()
    if any(student.student_id == student_id for student in students):
        print("Student ID already exists.")
        return

    student = Student(
        student_id=student_id,
        name=input("Name: ").strip(),
        department=input("Department: ").strip(),
        semester=input_int("Semester: ", 1, 8),
        marks=input_float("Overall marks: "),
        attendance=input_float("Attendance percentage: "),
    )
    students.append(student)
    save_students(students)
    print(f"Registered {student.name}. Grade: {student.grade}, Result: {student.result}")


def show_courses() -> None:
    """Display all available courses."""
    print("\nAvailable Courses")
    print("-" * 68)
    for code, course in COURSES.items():
        print(f"{code:6} {course['name']:<25} Credits: {course['credits']} Fee: Rs.{course['fee']}")


def enroll_student() -> None:
    """Enroll a student in courses."""
    students = load_students()
    enrollments = load_enrollments()
    student_id = input("Student ID: ").strip().upper()
    if not any(student.student_id == student_id for student in students):
        print("Student not found. Register the student first.")
        return

    show_courses()
    selected = input("Enter course codes separated by comma: ").upper().replace(" ", "").split(",")
    valid_courses = [code for code in selected if code in COURSES]
    if not valid_courses:
        print("No valid course selected.")
        return

    current = set(enrollments.get(student_id, []))
    current.update(valid_courses)
    enrollments[student_id] = sorted(current)
    save_enrollments(enrollments)
    print(f"Enrollment updated. Courses: {', '.join(enrollments[student_id])}")


def list_students(students: list[Student] | None = None) -> None:
    """Display student records."""
    students = students if students is not None else load_students()
    if not students:
        print("No student records found.")
        return

    print("\nStudent Records")
    print("-" * 96)
    print(f"{'ID':<10} {'Name':<20} {'Dept':<15} {'Sem':<5} {'Marks':<8} {'Att%':<8} {'Grade':<7} Result")
    print("-" * 96)
    for student in students:
        print(
            f"{student.student_id:<10} {student.name:<20} {student.department:<15} "
            f"{student.semester:<5} {student.marks:<8.2f} {student.attendance:<8.2f} "
            f"{student.grade:<7} {student.result}"
        )


def search_students() -> None:
    """Search for students by ID, name, or department."""
    students = load_students()
    term = input("Search by ID, name, or department: ").strip().lower()
    if not term:
        print("Search term cannot be empty.")
        return
    results = [
        student
        for student in students
        if term in student.student_id.lower()
        or term in student.name.lower()
        or term in student.department.lower()
    ]
    list_students(results)


def sort_students() -> None:
    """Sort and display students by selected criteria."""
    students = load_students()
    print("Sort by: 1. Name  2. Marks  3. Attendance  4. Semester")
    choice = input("Choice: ").strip()
    sort_map = {
        "1": ("name", False),
        "2": ("marks", True),
        "3": ("attendance", True),
        "4": ("semester", False),
    }
    key_name, reverse = sort_map.get(choice, ("name", False))
    list_students(sorted(students, key=lambda student: getattr(student, key_name), reverse=reverse))


def fee_menu() -> None:
    """Calculate and display fees for a student."""
    enrollments = load_enrollments()
    student_id = input("Student ID: ").strip().upper()
    course_codes = enrollments.get(student_id, [])
    if not course_codes:
        print("No enrolled courses found for this student.")
        return

    scholarship = input_float("Scholarship percentage (0 if none): ")
    payable = calculate_fee(course_codes, scholarship)
    print(f"Courses: {', '.join(course_codes)}")
    print(f"Total payable fee after scholarship: Rs.{payable:.2f}")


def add_academic_record() -> None:
    """Add academic record for a student in a course."""
    students = load_students()
    student_id = input("Student ID: ").strip().upper()
    if not any(student.student_id == student_id for student in students):
        print("Student not found.")
        return

    show_courses()
    course_code = input("Course code: ").strip().upper()
    if course_code not in COURSES:
        print("Invalid course code.")
        return

    internal = input_float("Internal marks out of 40: ", 0, 40)
    external = input_float("External marks out of 60: ", 0, 60)
    total = internal + external

    try:
        with ACADEMIC_RECORDS_FILE.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([student_id, course_code, internal, external, total, calculate_grade(total)])
        print(f"Academic record saved. Total: {total:.2f}, Grade: {calculate_grade(total)}")
    except OSError as error:
        print(f"Error saving academic record: {error}")


def scan_directory() -> None:
    """Scan and display contents of a directory."""
    directory = input("Directory to scan (blank for project data folder): ").strip()
    target = Path(directory) if directory else DATA_DIR

    try:
        print(f"\nScanning: {target.resolve()}")
        if not target.exists():
            print("Directory not found.")
            return
        for path in sorted(target.iterdir()):
            kind = "Directory" if path.is_dir() else "File"
            size = "-" if path.is_dir() else f"{path.stat().st_size} bytes"
            print(f"{kind:<10} {path.name:<35} {size}")
    except PermissionError:
        print("Permission denied while scanning this directory.")
    except OSError as error:
        print(f"Could not scan directory: {error}")


def generate_analytics() -> None:
    """Generate and display performance analytics."""
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
    except ImportError:
        print("Analytics needs NumPy, Pandas, and Matplotlib.")
        print("Install them with: pip install -r requirements.txt")
        return

    students = load_students()
    if not students:
        seed_sample_data()
        students = load_students()

    if not students:
        print("No student data available for analytics.")
        return

    try:
        dataframe = pd.DataFrame([asdict(student) for student in students])
        marks = np.array(dataframe["marks"], dtype=float)
        attendance = np.array(dataframe["attendance"], dtype=float)

        print("\nPerformance Analytics")
        print("-" * 40)
        print(f"Average marks: {np.mean(marks):.2f}")
        print(f"Highest marks: {np.max(marks):.2f}")
        print(f"Lowest marks: {np.min(marks):.2f}")
        print(f"Average attendance: {np.mean(attendance):.2f}%")
        print("\nDepartment-wise average marks")
        print(dataframe.groupby("department")["marks"].mean().round(2).to_string())

        REPORTS_DIR.mkdir(exist_ok=True, parents=True)
        chart_path = REPORTS_DIR / "student_performance.png"
        plt.figure(figsize=(9, 5))
        plt.bar(dataframe["name"], dataframe["marks"], color="#2f6f6d")
        plt.axhline(float(np.mean(marks)), color="#c44e52", linestyle="--", label="Average")
        plt.title("Student Performance Analytics")
        plt.xlabel("Student")
        plt.ylabel("Marks")
        plt.ylim(0, 100)
        plt.xticks(rotation=30, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        print(f"\nChart saved to: {chart_path}")
    except (ValueError, KeyError, OSError) as error:
        print(f"Error generating analytics: {error}")


def seed_sample_data() -> None:
    """Create sample student and enrollment data."""
    students = [
        Student("SC001", "Aarav Sharma", "IT", 3, 88, 92),
        Student("SC002", "Diya Patel", "CSE", 3, 76, 84),
        Student("SC003", "Kabir Rao", "IT", 4, 91, 95),
        Student("SC004", "Meera Nair", "AIML", 2, 67, 78),
        Student("SC005", "Rohan Gupta", "CSE", 4, 39, 72),
    ]
    save_students(students)
    save_enrollments(
        {
            "SC001": ["PY101", "DB102"],
            "SC002": ["PY101", "WD103"],
            "SC003": ["AI104", "PY101"],
            "SC004": ["DB102", "WD103"],
            "SC005": ["PY101"],
        }
    )
    print("Sample student and enrollment data created.")


def show_summary() -> None:
    """Display campus-wide summary statistics."""
    students = load_students()
    enrollments = load_enrollments()
    print("\nSmart Campus Summary")
    print("-" * 40)
    print(f"Students registered: {len(students)}")
    print(f"Total enrollments: {sum(len(courses) for courses in enrollments.values())}")
    if students:
        print(f"Average marks: {mean(student.marks for student in students):.2f}")
        print(f"Average attendance: {mean(student.attendance for student in students):.2f}%")


def menu() -> None:
    """Display main menu and handle user choices."""
    ensure_storage()
    actions = {
        "1": register_student,
        "2": enroll_student,
        "3": list_students,
        "4": search_students,
        "5": sort_students,
        "6": fee_menu,
        "7": add_academic_record,
        "8": scan_directory,
        "9": generate_analytics,
        "10": seed_sample_data,
        "11": show_summary,
    }

    while True:
        print("\nSmart Campus Information System")
        print("=" * 40)
        print("1. Student registration and grade evaluation")
        print("2. Course enrollment management")
        print("3. Student record storage and management")
        print("4. Search student data")
        print("5. Sort student data")
        print("6. Fee calculation")
        print("7. File-based academic record management")
        print("8. Directory scanning with exception handling")
        print("9. Student performance analytics")
        print("10. Create sample data")
        print("11. Show campus summary")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Thank you for using Smart Campus Information System.")
            break

        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as error:
                print(f"An error occurred: {error}")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
