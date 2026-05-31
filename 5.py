# Fee Calculation using Functions
def calculate_fee(tuition_fee, hostel_fee=0, transportation_fee=0):
    return tuition_fee + hostel_fee + transportation_fee

tuition = float(input("Enter Tuition Fee: "))
hostel = float(input("Enter Hostel Fee: "))
transport = float(input("Enter Transport Fee: "))

total = calculate_fee(tuition, hostel, transport)

print("Total Fee =", total)
