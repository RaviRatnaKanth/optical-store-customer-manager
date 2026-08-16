print("======================================")
print("      Optical Store Customer Manager")
print("======================================")

# Customer Details
customer_name = input("Enter Customer Name: ")
phone = input("Enter Phone Number: ")
address = input("Enter Address: ")

# Frame Details
frame_details = input("Enter Frame Details: ")

# Prescription Details
print("\n--- Prescription Details ---")
print("Enter power with + or - sign (Example: -2.00 or +1.50)")

# Right Eye
print("\nRight Eye (OD)")
right_sph = input("Enter Right Eye SPH: ")
right_cyl = input("Enter Right Eye CYL: ")
right_axis = input("Enter Right Eye Axis (0-180): ")

# Left Eye
print("\nLeft Eye (OS)")
left_sph = input("Enter Left Eye SPH: ")
left_cyl = input("Enter Left Eye CYL: ")
left_axis = input("Enter Left Eye Axis (0-180): ")

# Addition Power
print("\nAddition / Near Power")
addition = input(
    "Enter ADD Power for Bifocal/Progressive "
    "(Example: +2.00, leave blank if not required): "
)

# Amount Details
print("\n--- Payment Details ---")

total_amount = float(input("Enter Total Amount: "))
advance_amount = float(input("Enter Advance Amount: "))

balance = total_amount - advance_amount

# Final Customer Summary
print("\n======================================")
print("           CUSTOMER SUMMARY")
print("======================================")

print("Customer Name:", customer_name)
print("Phone Number:", phone)
print("Address:", address)
print("Frame Details:", frame_details)

print("\n--- Prescription ---")

print(
    "Right Eye (OD):",
    "SPH =", right_sph,
    "CYL =", right_cyl,
    "AXIS =", right_axis
)

print(
    "Left Eye (OS):",
    "SPH =", left_sph,
    "CYL =", left_cyl,
    "AXIS =", left_axis
)

if addition:
    print("ADD Power:", addition)
else:
    print("ADD Power: Not Required")

print("\n--- Payment ---")
print("Total Amount:", total_amount)
print("Advance Amount:", advance_amount)
print("Balance Amount:", balance)

print("======================================")