# Student Record Management

students = []

students.append({"name": "Priya", "age": 20, "grades": [85, 90, 78]})
students.append({"name": "Rahul", "age": 21, "grades": [72, 88, 91]})
students.append({"name": "Anita", "age": 19, "grades": [95, 89, 92]})

print("=== Student Records ===")

for student in students:
    print("Name:", student["name"])
    print("Age:", student["age"])
    print("Grades:", student["grades"])
    print("------------------")

event_A = {"Priya", "Rahul", "Anita", "Kiran"}
event_B = {"Rahul", "Anita", "Sneha"}

print("\n=== Event Analysis ===")
print("Common:", event_A & event_B)
print("All:", event_A | event_B)
print("Only Event A:", event_A - event_B)
