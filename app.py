import csv
from datetime import datetime
from store_config import store_name, store_city, store_phone, store_email, store_website, store_logo
print("==================================================")
print("          OPTICAL STORE CUSTOMER MANAGER")
print("==================================================")





# ==================================================
# 2. CUSTOMER / PATIENT DETAILS
# ==================================================

print("\n--- Customer Details ---")

customer_name = input("Enter Customer Name: ")

# Age validation
while True:
    try:
        age = int(input("Enter Patient Age: "))

        if age > 0:
            break
        else:
            print("Please enter a valid age.")

    except ValueError:
        print("Please enter age using numbers only.")

phone = input("Enter Customer Phone Number: ")
address = input("Enter Customer Address: ")


# ==================================================
# 3. SPECTACLE HISTORY
# ==================================================

print("\n--- Spectacle History ---")

while True:

    spectacle_history = input(
        "Enter Spectacle History "
        "(First-time / Existing): "
    ).strip().lower()

    if spectacle_history in ["first-time", "first time", "first"]:
        spectacle_history = "First-time"
        break

    elif spectacle_history in ["existing", "old"]:
        spectacle_history = "Existing"
        break

    else:
        print(
            "Please type First-time or Existing."
        )


# ==================================================
# 4. DEFAULT PREVIOUS PRESCRIPTION VALUES
# ==================================================

years_using_glasses = ""

previous_right_sph = ""
previous_right_cyl = ""
previous_right_axis = ""
previous_right_add = ""

previous_left_sph = ""
previous_left_cyl = ""
previous_left_axis = ""
previous_left_add = ""


# ==================================================
# 5. PREVIOUS PRESCRIPTION
#    ONLY FOR EXISTING SPECTACLE USERS
# ==================================================

if spectacle_history == "Existing":

    years_using_glasses = input(
        "How long have you been using glasses?: "
    )

    print("\n--- Previous Prescription ---")
    print(
        "Enter power with + or - sign."
    )
    print(
        "Example: -1.00, +2.00"
    )
    print(
        "Leave ADD blank if not required."
    )

    # ---------------- RIGHT EYE ----------------

    print("\nPrevious Right Eye (OD)")

    previous_right_sph = input(
        "Previous Right Eye SPH: "
    )

    previous_right_cyl = input(
        "Previous Right Eye CYL: "
    )

    previous_right_axis = input(
        "Previous Right Eye AXIS (0-180): "
    )

    previous_right_add = input(
        "Previous Right Eye ADD / Near Power: "
    )


    # ---------------- LEFT EYE ----------------

    print("\nPrevious Left Eye (OS)")

    previous_left_sph = input(
        "Previous Left Eye SPH: "
    )

    previous_left_cyl = input(
        "Previous Left Eye CYL: "
    )

    previous_left_axis = input(
        "Previous Left Eye AXIS (0-180): "
    )

    previous_left_add = input(
        "Previous Left Eye ADD / Near Power: "
    )

else:

    print(
        "First-time spectacle user - "
        "Previous prescription not required."
    )


# ==================================================
# 6. FRAME DETAILS
# ==================================================

print("\n--- Frame Details ---")

frame_details = input(
    "Enter Frame Details: "
)


# ==================================================
# 7. LENS TYPE
# ==================================================

print("\n--- Lens Details ---")

lens_type = input(
    "Enter Lens Type "
    "(Single Vision / Bifocal / Progressive / Other): "
)


# ==================================================
# 8. CURRENT PRESCRIPTION
# ==================================================

print("\n--- Current Prescription ---")

print(
    "Enter power with + or - sign "
    "(Example: -2.00 or +1.50)"
)

print(
    "Leave ADD blank when near/add power "
    "is not required."
)


# ==================================================
# 9. CURRENT RIGHT EYE
# ==================================================

print("\nRight Eye (OD)")

right_sph = input(
    "Enter Right Eye SPH: "
)

right_cyl = input(
    "Enter Right Eye CYL: "
)

right_axis = input(
    "Enter Right Eye AXIS (0-180): "
)

right_add = input(
    "Enter Right Eye ADD / Near Power: "
)


# ==================================================
# 10. CURRENT LEFT EYE
# ==================================================

print("\nLeft Eye (OS)")

left_sph = input(
    "Enter Left Eye SPH: "
)

left_cyl = input(
    "Enter Left Eye CYL: "
)

left_axis = input(
    "Enter Left Eye AXIS (0-180): "
)

left_add = input(
    "Enter Left Eye ADD / Near Power: "
)


# ==================================================
# 11. PAYMENT DETAILS
# ==================================================

print("\n--- Payment Details ---")


# Total Amount Validation
while True:

    try:

        total_amount = float(
            input("Enter Total Amount: ")
        )

        if total_amount >= 0:
            break

        else:
            print(
                "Total amount cannot be negative."
            )

    except ValueError:

        print(
            "Please enter amount using numbers only."
        )


# Advance Amount Validation
while True:

    try:

        advance_amount = float(
            input("Enter Advance Amount: ")
        )

        if advance_amount < 0:

            print(
                "Advance amount cannot be negative."
            )

        elif advance_amount > total_amount:

            print(
                "Advance amount cannot be greater "
                "than Total Amount."
            )

        else:

            break

    except ValueError:

        print(
            "Please enter amount using numbers only."
        )


# ==================================================
# 12. AUTOMATIC BALANCE CALCULATION
# ==================================================

balance = total_amount - advance_amount


# ==================================================
# 13. FINAL CUSTOMER SUMMARY
# ==================================================

print("\n")
print("==================================================")
print("                 CUSTOMER SUMMARY")
print("==================================================")


# ---------------- STORE ----------------

print("\n--- Store Details ---")

print(
    "Store Name:",
    store_name
)

print(
    "Town / City:",
    store_city
)

print(
    "Store Phone:",
    store_phone
)
if store_email:
    print("Store Email:", store_email)

if store_website:
    print("Store Website:", store_website)
if store_logo:

    print(
        "Store Logo:",
        store_logo
    )

else:

    print(
        "Store Logo: Not Added"
    )


# ---------------- CUSTOMER ----------------

print("\n--- Customer Details ---")

print(
    "Customer Name:",
    customer_name
)

print(
    "Patient Age:",
    age
)

print(
    "Phone Number:",
    phone
)

print(
    "Address:",
    address
)

print(
    "Spectacle History:",
    spectacle_history
)


# ---------------- PREVIOUS PRESCRIPTION ----------------

if spectacle_history == "Existing":

    print("\n--- Previous Prescription ---")

    print(
        "Using Glasses Since:",
        years_using_glasses
    )

    print(
        "Previous Right Eye (OD):",
        "SPH =", previous_right_sph,
        "CYL =", previous_right_cyl,
        "AXIS =", previous_right_axis,
        "ADD =",
        previous_right_add
        if previous_right_add
        else "Not Required"
    )

    print(
        "Previous Left Eye (OS):",
        "SPH =", previous_left_sph,
        "CYL =", previous_left_cyl,
        "AXIS =", previous_left_axis,
        "ADD =",
        previous_left_add
        if previous_left_add
        else "Not Required"
    )

else:

    print(
        "\nPrevious Prescription: "
        "Not Applicable"
    )


# ---------------- FRAME / LENS ----------------

print("\n--- Frame / Lens Details ---")

print(
    "Frame Details:",
    frame_details
)

print(
    "Lens Type:",
    lens_type
)


# ---------------- CURRENT PRESCRIPTION ----------------

print("\n--- Current Prescription ---")

print(
    "Right Eye (OD):",
    "SPH =", right_sph,
    "CYL =", right_cyl,
    "AXIS =", right_axis,
    "ADD =",
    right_add
    if right_add
    else "Not Required"
)

print(
    "Left Eye (OS):",
    "SPH =", left_sph,
    "CYL =", left_cyl,
    "AXIS =", left_axis,
    "ADD =",
    left_add
    if left_add
    else "Not Required"
)


# ---------------- PAYMENT ----------------

print("\n--- Payment ---")

print(
    "Total Amount:",
    total_amount
)

print(
    "Advance Amount:",
    advance_amount
)

print(
    "Balance Amount:",
    balance
)

# Save customer record to CSV
with open("customers.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        store_name,
        store_city,
        store_phone,
        store_logo,
        customer_name,
        age,
        phone,
        address,
        spectacle_history,
        years_using_glasses,
        previous_right_sph,
        previous_right_cyl,
        previous_right_axis,
        previous_right_add,
        previous_left_sph,
        previous_left_cyl,
        previous_left_axis,
        previous_left_add,
        frame_details,
        lens_type,
        right_sph,
        right_cyl,
        right_axis,
        right_add,
        left_sph,
        left_cyl,
        left_axis,
        left_add,
        total_amount,
        advance_amount,
        balance
    ])
print("\n==================================================")
print("        CUSTOMER RECORD COMPLETED SUCCESSFULLY")
print("==================================================")
print("\n--- PRESCRIPTION MESSAGE ---")

prescription_message = f"""
{store_name}

Spectacle Prescription

Right Eye (OD):
SPH: {right_sph}
CYL: {right_cyl}
AXIS: {right_axis}
ADD: {right_add if right_add else "Not Required"}

Left Eye (OS):
SPH: {left_sph}
CYL: {left_cyl}
AXIS: {left_axis}
ADD: {left_add if left_add else "Not Required"}

Please keep this prescription for your reference.
"""

print(prescription_message)