# File Handling for Student Academic Records

with open("student_records.txt", "w") as file:
    file.write("ID,Name,Marks\n")
    file.write("101,Arjun,85\n")
    file.write("102,Meera,92\n")
    file.write("103,Ravi,76\n")
    file.write("104,Anita,89\n")

print("Records written successfully.")

with open("student_records.txt", "r") as file:
    records = file.readlines()

print("\nStored Records:")
for record in records:
    print(record.strip())

total_students = 0
total_marks = 0
highest_marks = -1
top_student = ""

for record in records[1:]:
    data = record.strip().split(",")

    name = data[1]
    marks = int(data[2])

    total_students += 1
    total_marks += marks

    if marks > highest_marks:
        highest_marks = marks
        top_student = name

average = total_marks / total_students

print("\n--- Report ---")
print("Total Students:", total_students)
print("Average Marks:", average)
print("Top Student:", top_student)
