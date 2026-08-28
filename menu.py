import csv
import subprocess
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
    print("Total Amount:", row[39])
    print("Advance Amount:", row[40])
    print("Balance Amount:", row[41])

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
    clean_phone = clean_phone.replace(" ", "").replace("-", "")
    if clean_phone.startswith("+"):
        clean_phone = clean_phone[1:]

    if not (len(clean_phone) == 10 and clean_phone.isdigit() and clean_phone[0] in "6789"):
     print("\nInvalid Indian mobile number. Please enter a valid 10-digit mobile number.")
     return

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
        "Enter Customer Name, Phone Number or Address: "
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
                address = row[8].strip().lower()
                if (
                    search_value in customer_name
                    or search_value in phone
                    or search_value in address
                ):
                    found = True

                    print("\nCUSTOMER RECORD FOUND")
                    show_customer(row)
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



def edit_customer():
    print("\n--- EDIT CUSTOMER ---")

    search_value = input(
        "Enter Customer Name or Phone Number: "
    ).strip().lower()

    rows = []
    found = False

    try:
        with open(
            "customers.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(file)
            rows = list(reader)

        for i, row in enumerate(rows):

            if len(row) < 40:
                continue

            customer_name = row[5].strip().lower()
            phone = row[7].strip().lower()

            if (
                search_value in customer_name
                or search_value in phone
        ):
                found = True

                print("\nCustomer Found:")
                show_customer(row)

                print("\nLeave blank to keep the old value.")

                new_name = input(
                    f"Customer Name [{row[5]}]: "
            ).strip()

                new_age = input(
                    f"Age [{row[6]}]: "
            ).strip()

                new_phone = input(
                    f"Phone Number [{row[7]}]: "
            ).strip()

                new_address = input(
                    f"Address [{row[8]}]: "
            ).strip()
                new_history = input(
                    f"Spectacle History [{row[9]}]: "
            ).strip()

                new_years = input(
                    f"Years Using Glasses [{row[10]}]: "
            ).strip()

                            
                if new_name:
                    row[5] = new_name

                if new_age:
                    row[6] = new_age

                if new_phone:
                    row[7] = new_phone

                if new_address:
                        row[8] = new_address
                if new_history:
                   row[9] = new_history

                if new_years:
                   row[10] = new_years
                print("\n--- Edit Frame / Lens Details ---")

            new_frame_details = input(
                f"Frame Details [{row[19]}]: "
            ).strip()
            if new_frame_details:
                row[19] = new_frame_details

            new_frame_brand = input(
                f"Frame Brand [{row[20]}]: "
            ).strip()
            if new_frame_brand:
                row[20] = new_frame_brand

            new_frame_offer = input(
                f"Frame Offer [{row[21]}]: "
            ).strip()
            if new_frame_offer:
                row[21] = new_frame_offer

            new_lens_type = input(
                f"Lens Type [{row[22]}]: "
            ).strip()
            if new_lens_type:
                row[22] = new_lens_type

            new_lens_brand = input(
                f"Lens Brand [{row[23]}]: "
            ).strip()
            if new_lens_brand:
                row[23] = new_lens_brand

            new_lens_offer = input(
                f"Lens Offer [{row[24]}]: "
            ).strip()
            if new_lens_offer:
                row[24] = new_lens_offer
            print("\n--- Edit Current Prescription ---")

            new_od_sph = input(
                f"Right Eye (OD) SPH [{row[25]}]: "
            ).strip()
            if new_od_sph:
                row[25] = new_od_sph

            new_od_cyl = input(
                f"Right Eye (OD) CYL [{row[26]}]: "
            ).strip()
            if new_od_cyl:
                row[26] = new_od_cyl

            new_od_axis = input(
                f"Right Eye (OD) AXIS [{row[27]}]: "
            ).strip()
            if new_od_axis:
                row[27] = new_od_axis

            new_od_add = input(
                f"Right Eye (OD) ADD [{row[28]}]: "
            ).strip()
            if new_od_add:
                row[28] = new_od_add

            new_os_sph = input(
                f"Left Eye (OS) SPH [{row[29]}]: "
            ).strip()
            if new_os_sph:
                row[29] = new_os_sph

            new_os_cyl = input(
                f"Left Eye (OS) CYL [{row[30]}]: "
            ).strip()
            if new_os_cyl:
                row[30] = new_os_cyl

            new_os_axis = input(
                f"Left Eye (OS) AXIS [{row[31]}]: "
            ).strip()
            if new_os_axis:
                row[31] = new_os_axis

            new_os_add = input(
                f"Left Eye (OS) ADD [{row[32]}]: "
            ).strip()
            if new_os_add:
                row[32] = new_os_add

            rows[i] = row
            with open(
                    "customers.csv",
                    "w",
                    newline="",
                    encoding="utf-8"
        ) as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                    print("\nCustomer updated successfully.")
                    break

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

                if len(row) < 42:
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
                    print("Total Amount:", row[39])
                    print("Advance Amount:", row[40])
                    print("Balance Amount:", row[41])

                    print("=" * 50)

                    found = True
                    break

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
                    print("\n--- PD Details ---")
                    print("Distance PD:", row[33])
                    print("Near PD:", row[34])

                    print("\n--- Visual Acuity ---")
                    print("Right Eye Distance VA:", row[35])
                    print("Left Eye Distance VA:", row[36])
                    print("Right Eye Near VA:", row[37])
                    print("Left Eye Near VA:", row[38])

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
while True:
    print("=" * 60)
    print("          OPTICAL STORE CUSTOMER MANAGER")
    print("=" * 60)

    print("\nMAIN MENU")
    print("1. Add New Customer")
    print("2. Search Customer")
    print("3. View All Customers")
    print("4. Print Bill")
    print("5. Print Prescription")
    print("6. Edit Customer")
    print("7. Exit")

    choice = input("\nEnter your choice (1-7): ").strip()

    # ============================================================
    # MENU ACTIONS
    # ============================================================

    if choice == "1":

        print("\nOpening Add New Customer...")
        subprocess.run(["python", "app.py"])


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
        edit_customer()


    elif choice == "7":

        print(
            "\nThank you for using "
            "Optical Store Customer Manager."
        )
        break

    else:

        print(
            "\nInvalid choice. "
            "Please enter 1, 2, 3, 4, 5 , 6. or 7"
        ) 
