# Course Enrollment Management

courses = []
max_courses = 5

while True:
    if len(courses) >= max_courses:
        print("Maximum course limit reached!")
        break

    course_name = input("Enter course name (or done): ")

    if course_name.lower() == "done":
        break

    credits = input("Enter credits: ")

    if not credits.isdigit():
        print("Invalid credits!")
        continue

    credits = int(credits)

    if credits <= 0:
        print("Credits must be positive!")
        continue

    courses.append((course_name, credits))

print("\n--- Enrollment Report ---")
for course, credit in courses:
    print(course, "-", credit)

print("Total Courses:", len(courses))
