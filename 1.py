name = input("Enter student name: ")
score = float(input("Enter exam score (0-100): "))

if 90 <= score <= 100:
    grade = "A"
    remark = "Excellent"
elif score >= 75:
    grade = "B"
    remark = "Very Good"
elif score >= 60:
    grade = "C"
    remark = "Good"
elif score >= 40:
    grade = "D"
    remark = "Average"
else:
    grade = "F"
    remark = "Needs Improvement"

print("\n--- Student Report ---")
print("Name:", name)
print("Score:", score)
print("Grade:", grade)
print("Remark:", remark)
