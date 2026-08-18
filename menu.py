import csv


# ============================================================
# DISPLAY FULL CUSTOMER RECORD
# ============================================================

def show_customer(row):
    print("\n" + "=" * 60)
    print("CUSTOMER RECORD FOUND")
    print("=" * 60)

    print("Date / Time:", row[0])

    # --------------------------------------------------------
    # Store Details
    # --------------------------------------------------------

    print("\n--- Store Details ---")
    print("Store Name:", row[1])
    print("Store City:", row[2])

    if row[3]:
        print("Store Phone:", row[3])

    if row[4]:
        print("Store Logo:", row[4])

    # --------------------------------------------------------
    # Customer Details
    # --------------------------------------------------------

    print("\n--- Customer Details ---")
    print("Customer Name:", row[5])
    print("Age:", row[6])
    print("Phone:", row[7])
    print("Address:", row[8])
    print("Spectacle History:", row[9])

    if row[10]:
        print("Years Using Glasses:", row[10])

    # --------------------------------------------------------
    # Previous Prescription
    # --------------------------------------------------------

    print("\n--- Previous Prescription ---")

    print(
        "Right Eye (OD):",
        "SPH =", row[11],
        "CYL =", row[12],
        "AXIS =", row[13],
        "ADD =", row[14] if row[14] else "Not Required"
    )

    print(
        "Left Eye (OS):",
        "SPH =", row[15],
        "CYL =", row[16],
        "AXIS =", row[17],
        "ADD =", row[18] if row[18] else "Not Required"
    )

    # --------------------------------------------------------
    # Frame / Lens Details
    # --------------------------------------------------------

    print("\n--- Frame / Lens ---")
    print("Frame Details:", row[19])
    print("Lens Type:", row[20])

    # --------------------------------------------------------
    # Current Prescription
    # --------------------------------------------------------

    print("\n--- Current Prescription ---")

    print(
        "Right Eye (OD):",
        "SPH =", row[21],
        "CYL =", row[22],
        "AXIS =", row[23],
        "ADD =", row[24] if row[24] else "Not Required"
    )

    print(
        "Left Eye (OS):",
        "SPH =", row[25],
        "CYL =", row[26],
        "AXIS =", row[27],
        "ADD =", row[28] if row[28] else "Not Required"
    )

    # --------------------------------------------------------
    # Payment Details
    # --------------------------------------------------------

    print("\n--- Payment ---")
    print("Total Amount:", row[29])
    print("Advance Amount:", row[30])
    print("Balance Amount:", row[31])

    print("=" * 60)


# ============================================================
# PREPARE PRESCRIPTION MESSAGE
# ============================================================

def prepare_prescription_message(row):

    prescription_message = f"""
{row[1]}

Customer: {row[5]}

Spectacle Prescription

Right Eye (OD):
SPH: {row[21]}
CYL: {row[22]}
AXIS: {row[23]}
ADD: {row[24] if row[24] else "Not Required"}

Left Eye (OS):
SPH: {row[25]}
CYL: {row[26]}
AXIS: {row[27]}
ADD: {row[28] if row[28] else "Not Required"}

Please keep this prescription for your reference.
"""

    print("\n--- PRESCRIPTION MESSAGE ---")
    print(prescription_message)


# ============================================================
# SEARCH CUSTOMER
# ============================================================

def search_customer():

    print("\n--- SEARCH CUSTOMER ---")

    search_value = input(
        "Enter Customer Name or Phone Number: "
    ).strip().lower()

    found = False

    try:

        with open(
            "customers.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                # Old/incomplete CSV rows are ignored safely
                if len(row) < 32:
                    continue

                customer_name = row[5].strip().lower()
                phone = row[7].strip().lower()

                if (
                    search_value in customer_name
                    or search_value in phone
                ):

                    show_customer(row)

                    found = True

                    send_choice = input(
                        "\nPrepare prescription message "
                        "for this customer? (yes/no): "
                    ).strip().lower()

                    if send_choice in ["yes", "y"]:
                        prepare_prescription_message(row)

        if not found:
            print("\nCustomer not found.")

    except FileNotFoundError:
        print("\nNo customer records found yet.")


# ============================================================
# VIEW ALL CUSTOMERS
# ============================================================
def print_bill():
    print("\n--- PRINT BILL ---")

    search_value = input(
        "Enter Customer Name or Phone Number: "
    ).strip().lower()

    found = False

    try:
        with open(
            "customers.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) < 32:
                    continue

                customer_name = row[5].strip().lower()
                phone = row[7].strip().lower()

                if (
                    search_value in customer_name
                    or search_value in phone
                ):
                    print("\n" + "=" * 50)
                    print("              CUSTOMER BILL")
                    print("=" * 50)

                    print("Store Name:", row[1])
                    print("Store City:", row[2])

                    print("\nCustomer Name:", row[5])
                    print("Phone:", row[7])

                    print("\n--- Spectacle Details ---")
                    print("Frame Details:", row[19])
                    print("Lens Type:", row[20])

                    print("\n--- Payment Details ---")
                    print("Total Amount:", row[29])
                    print("Advance Amount:", row[30])
                    print("Balance Amount:", row[31])

                    print("=" * 50)

                    found = True

        if not found:
            print("\nCustomer not found.")

    except FileNotFoundError:
        print("\nNo customer records found yet.")

# ============================================================
# PRINT PRESCRIPTION
# ============================================================

def print_prescription():
    print("\n--- PRINT PRESCRIPTION ---")

    search_value = input(
        "Enter Customer Name or Phone Number: "
    ).strip().lower()

    found = False

    try:
        with open(
            "customers.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) < 32:
                    continue

                customer_name = row[5].strip().lower()
                phone = row[7].strip().lower()

                if (
                    search_value in customer_name
                    or search_value in phone
                ):

                    print("\n" + "=" * 60)
                    print("              SPECTACLE PRESCRIPTION")
                    print("=" * 60)

                    print("Store Name:", row[1])
                    print("Store City:", row[2])

                    print("\nCustomer Name:", row[5])
                    print("Phone:", row[7])

                    print("\n" + "-" * 60)
                    print("Eye        SPH        CYL        AXIS        ADD")
                    print("-" * 60)

                    print(
                        "RIGHT      ",
                        row[21],
                        "     ",
                        row[22],
                        "     ",
                        row[23],
                        "     ",
                        row[24] if row[24] else "Not Required"
                    )

                    print(
                        "LEFT       ",
                        row[25],
                        "     ",
                        row[26],
                        "     ",
                        row[27],
                        "     ",
                        row[28] if row[28] else "Not Required"
                    )

                    print("-" * 60)

                    found = True

            if not found:
                print("\nCustomer not found.")

    except FileNotFoundError:
        print("\nNo customer records found yet.")



def view_all_customers():

    print("\n--- ALL CUSTOMERS ---")

    found = False

    try:

        with open(
            "customers.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) < 32:
                    continue

                print(
                    "\nName:",
                    row[5],
                    "| Phone:",
                    row[7],
                    "| Balance:",
                    row[31]
                )

                found = True

        if not found:
            print("\nNo customer records found yet.")

    except FileNotFoundError:
        print("\nNo customer records found yet.")


# ============================================================
# MAIN MENU
# ============================================================

print("=" * 60)
print("          OPTICAL STORE CUSTOMER MANAGER")
print("=" * 60)

print("\nMAIN MENU")
print("1. Add New Customer")
print("2. Search Customer")
print("3. View All Customers")
print("4. Print Bill")
print("5. Print Prescription")
print("6. Exit")

choice = input("\nEnter your choice (1-6): ").strip()

# ============================================================
# MENU ACTIONS
# ============================================================

if choice == "1":

    print("\nOpening Add New Customer...")
    import app


elif choice == "2":

    search_customer()


elif choice == "3":

    view_all_customers()


elif choice == "4":

    print("\nOpening Print Bill...")
    print_bill()


elif choice == "5":

    print("\nOpening Print Prescription...")
    print_prescription()


elif choice == "6":

    print(
        "\nThank you for using "
        "Optical Store Customer Manager."
    )


else:

    print(
        "\nInvalid choice. "
        "Please enter 1, 2, 3, 4, 5 or 6."
    )