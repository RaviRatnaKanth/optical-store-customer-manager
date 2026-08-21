import csv
import webbrowser
from urllib.parse import quote

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
    print("\n--- Frame / Lens Details ---")

    print("Frame Details:", row[19])

    if row[20]:
        print("Frame Brand:", row[20])

    if row[21]:
        print("Frame Offer:", row[21])

    print("Lens Type:", row[22])

    if row[23]:
        print("Lens Brand:", row[23])

    if row[24]:
        print("Lens Offer:", row[24])
    # --------------------------------------------------------
    # Current Prescription
    # --------------------------------------------------------

        print("\n--- Current Prescription ---")

    print(
        "Right Eye (OD):",
        "SPH =", row[25],
        "CYL =", row[26],
        "AXIS =", row[27],
        "ADD =", row[28] if row[28] else "Not Required"
    )

    print(
        "Left Eye (OS):",
        "SPH =", row[29],
        "CYL =", row[30],
        "AXIS =", row[31],
        "ADD =", row[32] if row[32] else "Not Required"
    )

    # --------------------------------------------------------
    # Payment Details
    # --------------------------------------------------------

    print("\n--- Payment ---")
    print("Total Amount:", row[37])
    print("Advance Amount:", row[38])
    print("Balance Amount:", row[39])

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
SPH: {row[25]}
CYL: {row[26]}
AXIS: {row[27]}
ADD: {row[28] if row[28] else "Not Required"}

Left Eye (OS):
SPH: {row[29]}
CYL: {row[30]}
AXIS: {row[31]}
ADD: {row[32] if row[32] else "Not Required"}

Please keep this prescription for your reference.
"""

    print("\n--- PRESCRIPTION MESSAGE ---")
    print(prescription_message)

    return prescription_message

def open_whatsapp(phone, message):
    clean_phone = phone.strip()

    if clean_phone.startswith("+"):
        clean_phone = clean_phone[1:]

    if len(clean_phone) == 10:
        clean_phone = "91" + clean_phone

    encoded_message = quote(message)

    whatsapp_url = (
        f"https://wa.me/{clean_phone}"
        f"?text={encoded_message}"
    )

    webbrowser.open(whatsapp_url)
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
                if len(row) < 40:
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
                        message = prepare_prescription_message(row)
                        open_whatsapp(row[7], message)

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

                if len(row) < 40:
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
                    print("Lens Type:", row[22])

                    print("\n--- Payment Details ---")
                    print("Total Amount:", row[37])
                    print("Advance Amount:", row[38])
                    print("Balance Amount:", row[39])

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

                # Ignore old/incomplete CSV records
                if len(row) < 40:
                    continue

                customer_name = row[5].strip().lower()
                phone = row[7].strip().lower()

                if (
                    search_value in customer_name
                    or search_value in phone
                ):

                    print("\n" + "=" * 65)
                    print("              SPECTACLE PRESCRIPTION")
                    print("=" * 65)

                    print("Store Name:", row[1])
                    print("Store City:", row[2])

                    print("\nCustomer Name:", row[5])
                    print("Phone:", row[7])

                    print("\n" + "-" * 65)

                    print(
                        f"{'Eye':<10}"
                        f"{'SPH':<12}"
                        f"{'CYL':<12}"
                        f"{'AXIS':<12}"
                        f"{'ADD':<15}"
                    )

                    print("-" * 65)

                    right_add = (
                        row[28]
                        if row[28]
                        else "Not Required"
                    )

                    left_add = (
                        row[32]
                        if row[32]
                        else "Not Required"
                    )

                    print(
                        f"{'RIGHT':<10}"
                        f"{row[25]:<12}"
                        f"{row[26]:<12}"
                        f"{row[27]:<12}"
                        f"{right_add:<15}"
                    )

                    print(
                        f"{'LEFT':<10}"
                        f"{row[29]:<12}"
                        f"{row[30]:<12}"
                        f"{row[31]:<12}"
                        f"{left_add:<15}"
                    )

                    print("-" * 65)

                    found = True
                    break

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

                # Ignore old/incomplete records
                if len(row) < 40:
                    continue

                print("\n" + "-" * 60)

                print("Customer Name:", row[5])
                print("Age:", row[6])
                print("Phone:", row[7])
                print("Address:", row[8])
                print("Spectacle History:", row[9])
                print("Years Using Glasses:", row[10])

                print("\n--- Frame / Lens Details ---")
                print("Frame Details:", row[19])
                print("Frame Brand:", row[20])
                print("Frame Offer:", row[21])
                print("Lens Type:", row[22])
                print("Lens Brand:", row[23])
                print("Lens Offer:", row[24])

                print("\n--- Current Prescription ---")

                print(
                    "Right Eye (OD):",
                    "SPH =", row[25],
                    "CYL =", row[26],
                    "AXIS =", row[27],
                    "ADD =", row[28] if row[28] else "Not Required"
                )

                print(
                    "Left Eye (OS):",
                    "SPH =", row[29],
                    "CYL =", row[30],
                    "AXIS =", row[31],
                    "ADD =", row[32] if row[32] else "Not Required"
                )
                print("\n--- Pupillary Distance (PD) ---")
                print("Distance PD:", row[33])
                print("Near PD:", row[34])

                print("\n--- Visual Acuity / Pinhole ---")
                print("Right Eye Visual Acuity:", row[35])
                print("Left Eye Visual Acuity:", row[36])
                print("Right Eye Pinhole:", row[37])
                print("Left Eye Pinhole:", row[38])

                print("\n--- Payment Details ---")
                print("Total Amount:", row[39])
                print("Advance Amount:", row[40])
                print("Balance Amount:", row[41])
 

            found = True

        if not found:
            print("\nNo complete customer records found.")

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