import csv
import os
import webbrowser
import urllib.parse
from datetime import datetime
from store_config import store_name, store_city, store_phone, store_email, store_website, store_logo
record_date = datetime.now().strftime("%d-%m-%Y")
record_time = datetime.now().strftime("%I:%M %p")

print("==================================================")
print("          OPTICAL STORE CUSTOMER MANAGER")
print("==================================================")





# ==================================================
# 2. CUSTOMER / PATIENT DETAILS
# ==================================================

print("\n--- Customer Type ---")
print("1. New Customer")
print("2. Existing Customer")
print("3. Pending Balance Customers")

while True:
    customer_type = input(
        "Select Customer Type (1/2/3): "
    ).strip()

    if customer_type in ["1", "2", "3"]:
        break

    print(
        "Please select 1 for New Customer, "
        "2 for Existing Customer, "
        "or 3 for Pending Balance Customers."
    )

# --------------------------------------------------
# PHONE NORMALIZATION HELPER
# --------------------------------------------------

def normalize_indian_phone(value):
    clean_phone = (
        value.strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if clean_phone.startswith("+91"):
        clean_phone = clean_phone[3:]

    elif clean_phone.startswith("0091"):
        clean_phone = clean_phone[4:]

    elif (
        clean_phone.startswith("91")
        and len(clean_phone) == 12
    ):
        clean_phone = clean_phone[2:]

    return clean_phone
# ==================================================
# PENDING BALANCE CUSTOMERS
# ==================================================

if customer_type == "3":

    print("\n--- Pending Balance Customers ---")

    latest_payment_orders = {}

    with open(
        "payments.csv",
        "r",
        encoding="utf-8"
    ) as payment_file:

        payment_reader = csv.reader(
            payment_file
        )

        next(payment_reader, None)

        for payment_row in payment_reader:

            if len(payment_row) < 13:
                continue

            order_key = (
                payment_row[1].strip().lower(),
                normalize_indian_phone(payment_row[2]),
                payment_row[3].strip().lower(),
                payment_row[4],
                payment_row[5],
                payment_row[6]
            )

            latest_payment_orders[
                order_key
            ] = payment_row

    pending_balance_orders = []

    for payment_row in latest_payment_orders.values():

        try:
            remaining_balance = float(
                payment_row[9]
            )
        except ValueError:
            continue

        if remaining_balance > 0:
            pending_balance_orders.append(
                payment_row
            )

    if not pending_balance_orders:

        print(
            "No pending balance customers found."
        )

        raise SystemExit

    pending_balance_orders.sort(
        key=lambda row: row[4],
        reverse=True
    )

    for number, payment_row in enumerate(
        pending_balance_orders,
        start=1
    ):

        total_amount_value = float(
            payment_row[6]
        )

        remaining_balance = float(
            payment_row[9]
        )

        paid_amount = (
            total_amount_value
            - remaining_balance
        )

        phone_display = (
            payment_row[2]
            if payment_row[2].strip()
            else "No Phone"
        )

        print(
            f"\n{number}. "
            f"{payment_row[1]} | "
            f"{phone_display}"
        )

        print(
            f"   Order: {payment_row[5]} | "
            f"Date: {payment_row[4]}"
        )

        print(
            f"   Total: ₹{total_amount_value:.2f} | "
            f"Paid: ₹{paid_amount:.2f} | "
            f"Balance: ₹{remaining_balance:.2f}"
        )

        print(
            f"   Delivery: {payment_row[12]}"
        )

        if (
            len(payment_row) > 13
            and payment_row[13].strip()
        ):
            print(
                f"   Delivered On: {payment_row[13]}"
            )
    while True:
        pending_choice_input = input(
            "\nSelect Pending Order Number: "
        ).strip()

        if not pending_choice_input.isdigit():
            print(
                "Please enter a valid order number."
            )
            continue

        pending_choice = int(
            pending_choice_input
        )

        if (
            1
            <= pending_choice
            <= len(pending_balance_orders)
        ):
            break

        print(
            "Please select an order number "
            "from the list."
        )

    selected_pending_order = (
        pending_balance_orders[
            pending_choice - 1
        ]
    )

    print(
        "\n--- Selected Pending Order ---"
    )

    print(
        "Customer:",
        selected_pending_order[1]
    )

    print(
        "Phone:",
        selected_pending_order[2]
        if selected_pending_order[2].strip()
        else "No Phone"
    )

    print(
        "Order:",
        selected_pending_order[5]
    )

    print(
        "Order Date / Time:",
        selected_pending_order[4]
    )

    print(
        "Balance Due: ₹"
        f"{float(selected_pending_order[9]):.2f}"
    )

    total_amount_value = float(
        selected_pending_order[6]
    )

    current_balance = float(
        selected_pending_order[9]
    )

    previous_paid = (
        total_amount_value
        - current_balance
    )

    print("\n--- Current Payment Status ---")
    print(
        f"Total Amount: ₹{total_amount_value:.2f}"
    )
    print(
        f"Already Paid: ₹{previous_paid:.2f}"
    )
    print(
        f"Balance Due: ₹{current_balance:.2f}"
    )

    while True:
        try:
            amount_paid_now = float(
                input(
                    "Enter Amount Paid Now "
                    "(0 if no payment): "
                )
            )

            if amount_paid_now < 0:
                print(
                    "Payment amount cannot be negative."
                )
                continue

            if amount_paid_now > current_balance:
                print(
                    "Payment cannot be greater "
                    "than the Balance Due."
                )
                continue

            break

        except ValueError:
            print(
                "Please enter amount using numbers only."
            )

    new_balance = round(
        current_balance - amount_paid_now,
        2
    )

    print("\n--- Delivery Status ---")
    print("1. Pending")
    print("2. Delivered")

    while True:
        delivery_choice = input(
            "Select Delivery Status (1/2): "
        ).strip()

        if delivery_choice == "1":
            delivery_status = "Pending"
            break

        if delivery_choice == "2":
            delivery_status = "Delivered"
            break

        print("Please select 1 or 2.")

    if new_balance == 0:
        payment_status = "Paid"
    else:
        payment_status = "Pending"

    if amount_paid_now == 0:
        payment_type = "Delivery Update"
    elif new_balance == 0:
        payment_type = "Balance Payment"
    else:
        payment_type = "Part Payment"

    payment_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "payments.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as payment_file:

        payment_writer = csv.writer(
            payment_file
        )

        payment_writer.writerow([
            payment_datetime,
            selected_pending_order[1],
            selected_pending_order[2],
            selected_pending_order[3],
            selected_pending_order[4],
            selected_pending_order[5],
            total_amount_value,
            previous_paid,
            amount_paid_now,
            new_balance,
            payment_type,
            payment_status,
delivery_status,
(
    selected_pending_order[13]
    if len(selected_pending_order) > 13
    and selected_pending_order[13].strip()
    else (
        payment_datetime
        if delivery_status == "Delivered"
        else ""
    )
)
])
    print("\n--- Payment Update Completed ---")
    print(
        f"Previous Paid: ₹{previous_paid:.2f}"
    )
    print(
        f"Paid Now: ₹{amount_paid_now:.2f}"
    )
    print(
        f"Remaining Balance: ₹{new_balance:.2f}"
    )
    print(
        f"Payment Status: {payment_status}"
    )
    print(
        f"Delivery Status: {delivery_status}"
    )

    pending_phone = normalize_indian_phone(
        selected_pending_order[2]
    )

    if pending_phone:

        while True:
            send_payment_update = input(
                "Send Payment Update on WhatsApp? (y/n): "
            ).strip().lower()

            if send_payment_update in ["y", "n"]:
                break

            print(
                "Please enter y for Yes or n for No."
            )

        if send_payment_update == "y":

            if amount_paid_now > 0 and new_balance == 0:
                update_title = "Final Payment Update"
            elif amount_paid_now > 0:
                update_title = "Payment Update"
            else:
                update_title = "Delivery Update"

            delivery_date_for_message = (
                selected_pending_order[13]
                if len(selected_pending_order) > 13
                and selected_pending_order[13].strip()
                else (
                    payment_datetime
                    if delivery_status == "Delivered"
                    else ""
                )
            )

            payment_update_message = f"""
{store_name}
Customer Name: {selected_pending_order[1]}

{update_title}

Order Type: {selected_pending_order[5]}
Order Date / Time: {selected_pending_order[4]}

Total Amount: ₹{total_amount_value:.2f}
Previously Paid: ₹{previous_paid:.2f}
Paid Now: ₹{amount_paid_now:.2f}
Remaining Balance: ₹{new_balance:.2f}

Payment Status: {payment_status}
Delivery Status: {delivery_status}
{f"Delivered On: {delivery_date_for_message}" if delivery_date_for_message else ""}

Thank you for choosing {store_name}.
"""
            whatsapp_message = urllib.parse.quote(
                payment_update_message
            )

            whatsapp_url = (
                f"https://wa.me/91{pending_phone}"
                f"?text={whatsapp_message}"
            )

            webbrowser.open(
                whatsapp_url
            )

            print(
                "Opening WhatsApp Payment Update..."
            )

    else:
        print(
            "WhatsApp Payment Update cannot be sent - "
            "Customer phone number is not available."
        )

    raise SystemExit
# --------------------------------------------------
# EXISTING CUSTOMER SEARCH
# --------------------------------------------------

if customer_type == "2":

    search_value = input(
        "Enter Existing Customer Name or Phone: "
    ).strip()

    search_name = search_value.lower()

    search_phone = normalize_indian_phone(
        search_value
    )

    searching_by_phone = (
        search_phone.isdigit()
        and len(search_phone) == 10
    )

    matching_customers = []

    with open(
        "customers.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        next(reader, None)

        for row in reader:

            if len(row) <= 9:
                continue

            row_name = row[5].strip().lower()

            row_phone = normalize_indian_phone(
                row[8]
            )

            if searching_by_phone:

                if row_phone == search_phone:
                    matching_customers.append(
                        row
                    )

            else:

                if row_name == search_name:
                    matching_customers.append(
                        row
                    )

    customer_history_rows = matching_customers.copy()

    # ----------------------------------------------
    # REMOVE DUPLICATE CUSTOMER RESULTS
    # ----------------------------------------------

    unique_customers = {}

    for customer in matching_customers:

        customer_name_key = (
            customer[5]
            .strip()
            .lower()
        )

        customer_phone_key = (
            normalize_indian_phone(
                customer[8]
            )
        )

        if customer_phone_key:

            customer_key = (
                customer_name_key,
                customer_phone_key
            )

        else:

            customer_address_key = (
                customer[9]
                .strip()
                .lower()
            )

            customer_key = (
                customer_name_key,
                customer_address_key
            )

        # Keeps latest matching record
        unique_customers[
            customer_key
        ] = customer


    matching_customers = list(
        unique_customers.values()
    )


    # ----------------------------------------------
    # ONE CUSTOMER FOUND
    # ----------------------------------------------

    if len(matching_customers) == 1:

        selected_customer = (
            matching_customers[0]
        )

        customer_name = (
            selected_customer[5]
        )

        phone = (
            selected_customer[8]
        )

        print("\nSelected Customer:")

        print(
            f"Name: {customer_name} | "
            f"Phone: {phone}"
        )

        while True:

            confirm = input(
                "Is this the correct customer? (y/n): "
            ).strip().lower()

            if confirm == "y":

                print(
                    "Customer confirmed."
                )

                print(
                    "Customer selection successful."
                )

                break

            elif confirm == "n":

                print(
                    "Customer not confirmed."
                )

                raise SystemExit

            else:

                print(
                    "Please enter y for Yes or n for No."
                )


    # ----------------------------------------------
    # MULTIPLE CUSTOMERS FOUND
    # ----------------------------------------------

    elif len(matching_customers) > 1:

        print(
            "\nMultiple customers found:"
        )

        for number, customer in enumerate(
            matching_customers,
            start=1
        ):

            print(
                f"{number}. "
                f"Name: {customer[5]} | "
                f"Phone: {customer[8]} | "
                f"Address: {customer[9]}"
            )


        while True:

            choice = input(
                "Select Customer Number: "
            ).strip()


            # Customer number must contain digits
            if not choice.isdigit():

                print(
                    "Please enter a valid customer number."
                )

                continue


            choice = int(choice)


            # Customer number must be in displayed range
            if not (
                1
                <= choice
                <= len(matching_customers)
            ):

                print(
                    "Invalid customer number. Please try again."
                )

                continue


            selected_customer = (
                matching_customers[
                    choice - 1
                ]
            )

            customer_name = (
                selected_customer[5]
            )

            phone = (
                selected_customer[8]
            )


            print(
                "\nSelected Customer:"
            )

            print(
                f"Name: {customer_name} | "
                f"Phone: {phone}"
            )


            # --------------------------------------
            # CUSTOMER CONFIRMATION
            # --------------------------------------

            while True:

                confirm = input(
                    "Is this the correct customer? (y/n): "
                ).strip().lower()

                if confirm == "y":

                    print(
                        "Customer confirmed."
                    )

                    print(
                        "Customer selection successful."
                    )

                    break

                elif confirm == "n":

                    print(
                        "Customer not confirmed."
                    )

                    raise SystemExit

                else:

                    print(
                        "Please enter y for Yes or n for No."
                    )


            # Leave customer-number selection loop
            break


    # ----------------------------------------------
    # NO CUSTOMER FOUND
    # ----------------------------------------------

    else:

        print(
            "Customer not found."
        )

        raise SystemExit
        # ----------------------------------------------
    # LOAD LATEST AVAILABLE PRESCRIPTION
    # ----------------------------------------------

    selected_customer = selected_customer.copy()

    selected_name = selected_customer[5].strip().lower()
    selected_phone = normalize_indian_phone(
        selected_customer[8]
    )
    selected_address = selected_customer[9].strip().lower()

    for history_row in reversed(customer_history_rows):

        if len(history_row) < 36:
            continue

        same_name = (
            history_row[5].strip().lower()
            == selected_name
        )

        history_phone = normalize_indian_phone(
            history_row[8]
        )

        history_address = (
            history_row[9].strip().lower()
        )

        if selected_phone:
            same_customer = (
                same_name
                and history_phone == selected_phone
            )
        else:
            same_customer = (
                same_name
                and history_address == selected_address
            )

        if not same_customer:
            continue

        if any(
            value.strip()
            for value in history_row[28:36]
        ):
            selected_customer[12:20] = history_row[28:36]
            break

        if any(
            value.strip()
            for value in history_row[12:20]
        ):
            selected_customer[12:20] = history_row[12:20]
            break


# ==================================================
# CUSTOMER DETAILS
# ==================================================

print(
    "\n--- Customer Details ---"
)


# --------------------------------------------------
# CUSTOMER NAME
# --------------------------------------------------

if customer_type == "1":

    while True:

        customer_name = input(
            "Enter Customer Name: "
        ).strip().title()

        if (
            customer_name
            and any(
                char.isalpha()
                for char in customer_name
            )
            and all(
                char.isalpha()
                or char.isspace()
                or char in [
                    ".",
                    "'",
                    "-"
                ]
                for char in customer_name
            )
        ):

            break

        print(
            "Invalid customer name. "
            "Please enter a valid name using letters."
        )

else:

    customer_name = (
        selected_customer[5]
    )


# --------------------------------------------------
# GENDER
# --------------------------------------------------

if customer_type == "1":

    print(
        "\n--- Gender ---"
    )

    print(
        "1. Male"
    )

    print(
        "2. Female"
    )


    while True:

        gender_choice = input(
            "Select Gender (1/2): "
        ).strip()

        if gender_choice == "1":

            gender = "Male"
            break

        elif gender_choice == "2":

            gender = "Female"
            break

        else:

            print(
                "Please select 1 for Male or 2 for Female."
            )

else:

    gender = (
        selected_customer[6]
    )


# --------------------------------------------------
# AGE
# --------------------------------------------------

if customer_type == "1":

    while True:

        try:

            age = int(
                input(
                    "Enter Patient Age: "
                )
            )

            if age > 0:

                break

            print(
                "Please enter a valid age."
            )

        except ValueError:

            print(
                "Please enter age using numbers only."
            )

else:

    age = (
        selected_customer[7]
    )


# --------------------------------------------------
# PHONE NUMBER
# --------------------------------------------------

if customer_type == "1":

    while True:

        raw_phone = input(
            "Enter Customer Phone Number "
            "(Optional - press Enter if unavailable): "
        ).strip()


        # Phone is optional
        if raw_phone == "":

            phone = ""
            break


        clean_phone = (
            normalize_indian_phone(
                raw_phone
            )
        )


        if (
            clean_phone.isdigit()
            and len(clean_phone) == 10
            and clean_phone[0]
            in ["6", "7", "8", "9"]
        ):

            phone = clean_phone
            break


        print(
            "Invalid phone number. "
            "Enter a valid Indian 10-digit mobile "
            "number, optionally with +91, "
            "or leave blank."
        )

else:

    phone = (
        selected_customer[8]
    )


# --------------------------------------------------
# TOWN / VILLAGE
# --------------------------------------------------

if customer_type == "1":

    while True:

        address = input(
            "Enter Town / Village (Required): "
        ).strip().title()


        if (
            address
            and any(
                char.isalpha()
                for char in address
            )
            and all(
                char.isalpha()
                or char.isspace()
                or char in [
                    ".",
                    ",",
                    "-",
                    "'"
                ]
                for char in address
            )
        ):

            break


        print(
            "Town / Village is required. "
            "Please enter a valid place name."
        )


    # ----------------------------------------------
    # FULL ADDRESS - OPTIONAL
    # ----------------------------------------------

    full_address = input(
        "Enter Full Address "
        "(Optional - press Enter to skip): "
    ).strip().title()


else:

    address = (
        selected_customer[9]
    )

    full_address = (
        selected_customer[46]
        if len(selected_customer) > 46
        else ""
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
# 6. FRAME DETAILS
# ==================================================

print("\n--- Frame Details ---")

print("\n--- Order Type ---")
print("1. Frame Only")
print("2. Lenses Only")
print("3. Frame + Lenses")

if customer_type == "2":
    print("4. Previous Prescription")
    print("5. Old Order History")
    print("6. Payment / Delivery Update")


while True:
    if customer_type == "2":
        order_type = input(
            "Select Order Type (1/2/3/4/5/6): "
        ).strip()
        valid_options = ["1", "2", "3", "4", "5", "6"]
    else:
        order_type = input(
            "Select Order Type (1/2/3): "
        ).strip()
        valid_options = ["1", "2", "3"]
    if order_type in valid_options:
        break

    print("Please select a valid Order Type.")


# ==================================================
# PREVIOUS PRESCRIPTION
# ==================================================

if customer_type == "2" and order_type == "4":
    latest_prescription = None

    selected_name_key = selected_customer[5].strip().lower()
    selected_phone_key = normalize_indian_phone(
        selected_customer[8]
    )
    selected_address_key = selected_customer[9].strip().lower()

    with open(
        "customers.csv",
        "r",
        encoding="utf-8"
    ) as customer_file:

        customer_reader = csv.reader(customer_file)
        next(customer_reader, None)

        for customer in customer_reader:

            if len(customer) < 36:
                continue

            customer_name_key = customer[5].strip().lower()
            customer_phone_key = normalize_indian_phone(
                customer[8]
            )
            customer_address_key = customer[9].strip().lower()

            if selected_phone_key:
                same_customer = (
                    customer_name_key == selected_name_key
                    and customer_phone_key == selected_phone_key
                )
            else:
                same_customer = (
                    customer_name_key == selected_name_key
                    and customer_address_key == selected_address_key
                )

            has_prescription = any(
                value.strip()
                for value in customer[28:36]
            )

            if same_customer and has_prescription:
                if (
                    latest_prescription is None
                    or customer[0] > latest_prescription[0]
                ):
                    latest_prescription = customer

    print("\n--- Previous Prescription ---")

    if latest_prescription is not None:
        print(
            "Prescription Date / Time:",
            latest_prescription[0]
        )

        print("OD:")
        print(
            f"SPH: {latest_prescription[28]} | "
            f"CYL: {latest_prescription[29]} | "
            f"AXIS: {latest_prescription[30]} | "
            f"ADD: {latest_prescription[31]}"
        )

        print("OS:")
        print(
            f"SPH: {latest_prescription[32]} | "
            f"CYL: {latest_prescription[33]} | "
            f"AXIS: {latest_prescription[34]} | "
            f"ADD: {latest_prescription[35]}"
        )

    else:
        print("No previous prescription found.")

    raise SystemExit
# ==================================================
# OLD ORDER HISTORY
# ==================================================

if customer_type == "2" and order_type == "5":
    customer_orders = []

    selected_name_key = selected_customer[5].strip().lower()
    selected_phone_key = normalize_indian_phone(
        selected_customer[8]
    )
    selected_address_key = selected_customer[9].strip().lower()

    with open(
        "customers.csv",
        "r",
        encoding="utf-8"
    ) as customer_file:

        customer_reader = csv.reader(customer_file)
        next(customer_reader, None)

        for customer in customer_reader:

            if len(customer) < 28:
                continue

            customer_name_key = customer[5].strip().lower()
            customer_phone_key = normalize_indian_phone(
                customer[8]
            )
            customer_address_key = customer[9].strip().lower()

            if selected_phone_key:
                same_customer = (
                    customer_name_key == selected_name_key
                    and customer_phone_key == selected_phone_key
                )
            else:
                same_customer = (
                    customer_name_key == selected_name_key
                    and customer_address_key == selected_address_key
                )

            if same_customer:
                customer_orders.append(customer)

    customer_orders.sort(
        key=lambda row: row[0],
        reverse=True
    )
    print("\n--- Old Order History ---")
    print("Matching Orders Found:", len(customer_orders))

    for number, order in enumerate(customer_orders, start=1):
        print(
            f"{number}. Order Date / Time: {order[0]} | "
            f"Frame: {order[20]} | "
            f"Lens: {order[24]}"
        )

    order_choice_input = input("Select Order Number: ")

    if not order_choice_input.isdigit():
        print("Invalid input. Please enter an order number.")
        raise SystemExit

    order_choice = int(order_choice_input)

    if order_choice < 1 or order_choice > len(customer_orders):
        print("Invalid order number. Please select from the list.")
        raise SystemExit

    selected_order = customer_orders[order_choice - 1]

    print("\n==================================================")
    print("              OLD ORDER DETAILS")
    print("==================================================")
    print("Order Date / Time :", selected_order[0])
    print()
    if selected_order[20].strip():
        print("--- Frame Details ---")
        print("Frame      :", selected_order[20])
        if selected_order[21].strip():
            print("Brand      :", selected_order[21])
        if selected_order[22].strip() and selected_order[22].strip() not in ["0", "0.0"]:
            print("Offer      :", selected_order[22])
        if selected_order[23].strip() and selected_order[23].strip() not in ["0", "0.0"]:
            print("Price      : ₹", selected_order[23])
    if selected_order[24].strip():
        print("--- Lens Details ---")
        print("Lens Type  :", selected_order[24])
    if selected_order[25].strip():
        print("Brand      :", selected_order[25])
    if selected_order[26].strip() and selected_order[26].strip() not in ["0", "0.0"]:
        print("Offer      :", selected_order[26]) 
    if selected_order[27].strip() and selected_order[27].strip() not in ["0", "0.0"]:
        print("Price      : ₹", selected_order[27])  
    if len(selected_order) > 45 and selected_order[45].strip():
        print("Features   :", selected_order[45])
    raise SystemExit
# ==================================================
# PAYMENT / DELIVERY UPDATE
# ==================================================

if customer_type == "2" and order_type == "6":

    print("\n--- Payment / Delivery Update ---")

    selected_name_key = (
        selected_customer[5]
        .strip()
        .lower()
    )

    selected_phone_key = normalize_indian_phone(
        selected_customer[8]
    )

    selected_address_key = (
        selected_customer[9]
        .strip()
        .lower()
    )

    payment_rows = []

    with open(
        "payments.csv",
        "r",
        encoding="utf-8"
    ) as payment_file:

        payment_reader = csv.reader(
            payment_file
        )

        next(payment_reader, None)

        for payment_row in payment_reader:

            if len(payment_row) < 13:
                continue

            payment_name_key = (
                payment_row[1]
                .strip()
                .lower()
            )

            payment_phone_key = normalize_indian_phone(
                payment_row[2]
            )

            payment_address_key = (
                payment_row[3]
                .strip()
                .lower()
            )

            if selected_phone_key:

                same_customer = (
                    payment_name_key
                    == selected_name_key
                    and payment_phone_key
                    == selected_phone_key
                )

            else:

                same_customer = (
                    payment_name_key
                    == selected_name_key
                    and payment_address_key
                    == selected_address_key
                )

            if same_customer:
                payment_rows.append(
                    payment_row
                )

    if not payment_rows:

        print(
            "No payment records found "
            "for this customer."
        )

        raise SystemExit

    latest_orders = {}

    for payment_row in payment_rows:

        order_key = (
            payment_row[4],
            payment_row[5],
            payment_row[6]
        )

        latest_orders[
            order_key
        ] = payment_row

    active_orders = []

    for payment_row in latest_orders.values():

        try:
            remaining_balance = float(
                payment_row[9]
            )
        except ValueError:
            continue

        delivery_status = (
            payment_row[12]
            .strip()
            .lower()
        )

        if (
            remaining_balance > 0
            or delivery_status != "delivered"
        ):
            active_orders.append(
                payment_row
            )

    if not active_orders:

        print(
            "No pending payment or "
            "delivery updates found."
        )

        raise SystemExit

    active_orders.sort(
        key=lambda row: row[4],
        reverse=True
    )

    print("\nPending Orders:")

    for number, payment_row in enumerate(
        active_orders,
        start=1
    ):

        total_value = float(
            payment_row[6]
        )

        balance_value = float(
            payment_row[9]
        )

        paid_value = (
            total_value
            - balance_value
        )

        print(
            f"{number}. "
            f"{payment_row[4]} | "
            f"{payment_row[5]} | "
            f"Total: ₹{total_value:.2f} | "
            f"Paid: ₹{paid_value:.2f} | "
            f"Balance: ₹{balance_value:.2f} | "
            f"Delivery: {payment_row[12]}"
        )

        if (
            len(payment_row) > 13
            and payment_row[13].strip()
        ):
            print(
                f"   Delivered On: {payment_row[13]}"
            )
    while True:

        payment_choice = input(
            "Select Order Number: "
        ).strip()

        if not payment_choice.isdigit():

            print(
                "Please enter a valid "
                "order number."
            )

            continue

        payment_choice = int(
            payment_choice
        )

        if not (
            1
            <= payment_choice
            <= len(active_orders)
        ):

            print(
                "Invalid order number. "
                "Please try again."
            )

            continue

        break

    selected_payment = active_orders[
        payment_choice - 1
    ]

    order_datetime = selected_payment[4]
    order_type_name = selected_payment[5]

    total_amount_value = float(
        selected_payment[6]
    )

    current_balance = float(
        selected_payment[9]
    )

    previous_paid = (
        total_amount_value
        - current_balance
    )

    print("\n--- Current Payment Status ---")

    print(
        f"Total Amount: "
        f"₹{total_amount_value:.2f}"
    )

    print(
        f"Already Paid: "
        f"₹{previous_paid:.2f}"
    )

    print(
        f"Balance Due: "
        f"₹{current_balance:.2f}"
    )

    while True:

        try:

            amount_paid_now = float(
                input(
                    "Enter Amount Paid Now "
                    "(0 if no payment): "
                )
            )

            if amount_paid_now < 0:

                print(
                    "Payment amount cannot "
                    "be negative."
                )

                continue

            if amount_paid_now > current_balance:

                print(
                    "Payment cannot be greater "
                    "than the Balance Due."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter amount using "
                "numbers only."
            )

    new_balance = round(
        current_balance
        - amount_paid_now,
        2
    )

    print("\n--- Delivery Status ---")
    print("1. Pending")
    print("2. Delivered")

    while True:

        delivery_choice = input(
            "Select Delivery Status (1/2): "
        ).strip()

        if delivery_choice == "1":
            delivery_status = "Pending"
            break

        if delivery_choice == "2":
            delivery_status = "Delivered"
            break

        print(
            "Please select 1 or 2."
        )

    if new_balance == 0:
        payment_status = "Paid"
    else:
        payment_status = "Pending"

    if amount_paid_now == 0:
        payment_type = "Delivery Update"
    elif new_balance == 0:
        payment_type = "Balance Payment"
    else:
        payment_type = "Part Payment"

    from datetime import datetime

    payment_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "payments.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as payment_file:

        payment_writer = csv.writer(
            payment_file
        )

        payment_writer.writerow([
            payment_datetime,
            selected_customer[5],
            selected_customer[8],
            selected_customer[9],
            order_datetime,
            order_type_name,
            total_amount_value,
            previous_paid,
            amount_paid_now,
            new_balance,
            payment_type,
            payment_status,
delivery_status,
(
    selected_payment[13]
    if len(selected_payment) > 13
    and selected_payment[13].strip()
    else (
        payment_datetime
        if delivery_status == "Delivered"
        else ""
    )
)
])
    print("\n--- Payment Update Completed ---")

    print(
        f"Previous Paid: "
        f"₹{previous_paid:.2f}"
    )

    print(
        f"Paid Now: "
        f"₹{amount_paid_now:.2f}"
    )

    print(
        f"Remaining Balance: "
        f"₹{new_balance:.2f}"
    )

    print(
        f"Payment Status: "
        f"{payment_status}"
    )

    print(
        f"Delivery Status: "
        f"{delivery_status}"
    )

# ----------------------------------------------
# WHATSAPP PAYMENT / DELIVERY UPDATE
# ----------------------------------------------

if customer_type == "2" and order_type == "6":

    if phone:

        while True:
            send_payment_update = input(
                "Send Payment Update on WhatsApp? (y/n): "
            ).strip().lower()

            if send_payment_update in ["y", "n"]:
                break

            print(
                "Please enter y for Yes or n for No."
            )

        if send_payment_update == "y":

            if amount_paid_now > 0 and new_balance == 0:
                update_title = "Final Payment Update"

            elif amount_paid_now > 0:
                update_title = "Payment Update"

            else:
                update_title = "Delivery Update"

            delivery_date_for_message = (
                selected_payment[13]
                if len(selected_payment) > 13
                and selected_payment[13].strip()
                else (
                    payment_datetime
                    if delivery_status == "Delivered"
                    else ""
                )
            )

            payment_update_message = f"""
{store_name}
Customer Name: {selected_customer[5]}

{update_title}

Order Type: {order_type_name}
Order Date / Time: {order_datetime}

Total Amount: ₹{total_amount_value:.2f}
Previously Paid: ₹{previous_paid:.2f}
Paid Now: ₹{amount_paid_now:.2f}
Remaining Balance: ₹{new_balance:.2f}

Payment Status: {payment_status}
Delivery Status: {delivery_status}
{f"Delivered On: {delivery_date_for_message}" if delivery_date_for_message else ""}

Thank you for choosing {store_name}.
"""
            whatsapp_message = urllib.parse.quote(
                payment_update_message
            )

            whatsapp_url = (
                f"https://wa.me/91{phone}"
                f"?text={whatsapp_message}"
            )

            webbrowser.open(
                whatsapp_url
            )

            print(
                "Opening WhatsApp Payment Update..."
            )

    else:
        print(
            "WhatsApp Payment Update cannot be sent - "
            "Customer phone number is not available."
        )

    raise SystemExit
# ==================================================
# FRAME ENTRY
# ==================================================

if order_type in ["1", "3"]:
    frame_details = input(
        "Enter Frame Details: "
    ).strip()

    print("\n--- Frame Category ---")
    print("1. Brand")
    print("2. Non-Brand")

    while True:
        frame_category = input(
            "Select Frame Category (1/2): "
        ).strip()

        if frame_category in ["1", "2"]:
            break

        print("Please enter 1 or 2 only.")

    if frame_category == "1":
        frame_brand = input(
            "Enter Frame Brand: "
        ).strip()
    else:
        frame_brand = "Non-Brand"

    frame_offer = input(
        "Enter Frame Offer: "
    ).strip()

    while True:
        try:
            frame_price = float(
                input("Enter Frame Price: ").strip()
            )

            if frame_price < 0:
                print(
                    "Frame Price cannot be negative."
                )
                continue

            break

        except ValueError:
            print(
                "Please enter Frame Price using numbers only."
            )
else:
    frame_details = ""
    frame_category = ""
    frame_brand = ""
    frame_offer = ""
    frame_price = 0.0

# ==================================================
# 7. LENS TYPE
# ==================================================

if order_type in ["2", "3"]:
    print("\n--- Lens Details ---")

    print("\n--- Lens Type ---")
    print("1. Single Vision")
    print("2. Bifocal")

    add_requirement = ""

    while True:
        lens_type_choice = input("Select Lens Type (1/2): ").strip()

        if lens_type_choice == "1":
            lens_type = "Single Vision"
            break

        elif lens_type_choice == "2":
            print("\n--- Bifocal Type ---")
            print("1. Kryptok Bifocal")
            print("2. D Bifocal")
            print("3. Progressive Bifocal")
            print("4. Other")

            while True:
                bifocal_choice = input(
                    "Select Bifocal Type (1/2/3/4): "
                ).strip()

                if bifocal_choice == "1":
                    lens_type = "Kryptok Bifocal"
                    break

                elif bifocal_choice == "2":
                    lens_type = "D Bifocal"
                    break

                elif bifocal_choice == "3":
                    lens_type = "Progressive Bifocal"
                    break

                elif bifocal_choice == "4":
                    lens_type = "Other"
                    break

                else:
                    print(
                        "Invalid option. Please select 1, 2, 3 or 4."
                    )

            print("\n--- ADD Requirement ---")
            print("1. Both Eyes")
            print("2. Right Eye (OD) Only")
            print("3. Left Eye (OS) Only")

            while True:
                add_requirement = input(
                    "Select ADD Requirement (1/2/3): "
                ).strip()

                if add_requirement in ["1", "2", "3"]:
                    break

                print(
                    "Invalid option. Please select 1, 2 or 3."
                )

            break

        else:
            print(
                "Invalid option. Please select 1 or 2."
            )

    # ==================================================
    # LENS FEATURES / COATING VALIDATION
    # ==================================================

    while True:
        lens_features = input(
            "Enter Lens Features / Coating (Optional): "
        ).strip().title()

        normalized_features = (
            lens_features.lower()
            .replace(".", " ")
            .replace("-", " ")
            .replace("/", " ")
            .replace(",", " ")
            .replace("_", " ")
        )

        feature_words = normalized_features.split()

        has_kt = (
            "kt" in feature_words
            or "kryptok" in feature_words
        )

        has_progressive = (
            "progressive" in feature_words
        )

        has_d_bifocal = (
            "d bifocal" in normalized_features
            or "dbifocal" in normalized_features
        )

        # Single Vision cannot contain Bifocal design names
        if lens_type == "Single Vision":
            if has_kt:
                print(
                    "KT / Kryptok is a Bifocal type and "
                    "cannot be used with Single Vision."
                )
                continue

            if has_progressive:
                print(
                    "Progressive cannot be used with "
                    "Single Vision."
                )
                continue

            if has_d_bifocal:
                print(
                    "D Bifocal cannot be used with "
                    "Single Vision."
                )
                continue

        # Kryptok cannot conflict with other Bifocal designs
        elif lens_type == "Kryptok Bifocal":
            if has_progressive:
                print(
                    "Progressive cannot be used with "
                    "Kryptok Bifocal."
                )
                continue

            if has_d_bifocal:
                print(
                    "D Bifocal cannot be used with "
                    "Kryptok Bifocal."
                )
                continue

        # D Bifocal cannot conflict with Kryptok or Progressive
        elif lens_type == "D Bifocal":
            if has_kt:
                print(
                    "KT / Kryptok cannot be used with "
                    "D Bifocal."
                )
                continue

            if has_progressive:
                print(
                    "Progressive cannot be used with "
                    "D Bifocal."
                )
                continue

        # Progressive cannot contain Kryptok or D Bifocal
        elif lens_type == "Progressive Bifocal":
            if has_kt:
                print(
                    "KT / Kryptok cannot be used with "
                    "Progressive Bifocal."
                )
                continue

            if has_d_bifocal:
                print(
                    "D Bifocal cannot be used with "
                    "Progressive Bifocal."
                )
                continue

        break

    lens_brand = input(
        "Enter Lens Brand (Optional): "
    ).strip().title()

    lens_offer = input(
        "Enter Lens Offer: "
    ).strip()

    while True:
        lens_price_input = input("Enter Lens Price: ").strip()

        try:
            lens_price = float(lens_price_input)

            if lens_price < 0:
                print("Lens Price cannot be negative.")
                continue

            break

        except ValueError:
            print("Please enter Lens Price using numbers only.")
else:
    lens_type = ""
    add_requirement = ""
    lens_features = ""
    lens_brand = ""
    lens_offer = ""
    lens_price = 0.0
# ==================================================
# 3. SPECTACLE HISTORY
# ==================================================

print("\n--- Spectacle History ---")

if customer_type == "2":
    spectacle_history = "Existing"

    years_using_glasses = selected_customer[11]

    previous_right_sph = selected_customer[12]
    previous_right_cyl = selected_customer[13]
    previous_right_axis = selected_customer[14]
    previous_right_add = selected_customer[15]

    previous_left_sph = selected_customer[16]
    previous_left_cyl = selected_customer[17]
    previous_left_axis = selected_customer[18]
    previous_left_add = selected_customer[19]

    print(
        "Existing customer - "
        "previous prescription loaded automatically."
    )

    print("\n--- Previous Prescription ---")

    print("OD:")
    print(
        f"SPH: {previous_right_sph} | "
        f"CYL: {previous_right_cyl} | "
        f"AXIS: {previous_right_axis} | "
        f"ADD: {previous_right_add}"
    )

    print("OS:")
    print(
        f"SPH: {previous_left_sph} | "
        f"CYL: {previous_left_cyl} | "
        f"AXIS: {previous_left_axis} | "
        f"ADD: {previous_left_add}"
    )

elif order_type in ["2", "3"]:

    while True:
        spectacle_history = input(
            "Enter Spectacle History "
            "(First-time / Existing): "
        ).strip().lower()

        if spectacle_history in [
            "first-time",
            "first time",
            "first"
        ]:
            spectacle_history = "First-time"
            break

        elif spectacle_history in [
            "existing",
            "old"
        ]:
            spectacle_history = "Existing"
            break

        else:
            print(
                "Please type First-time or Existing."
            )

    if spectacle_history == "Existing":

        years_using_glasses = input(
            "How long have you been using glasses?: "
        )

        while True:
            has_previous_prescription = input(
                "Do you have previous prescription details? (y/n): "
            ).strip().lower()

            if has_previous_prescription in ["y", "yes"]:
                has_previous_prescription = "y"
                break

            elif has_previous_prescription in ["n", "no"]:
                has_previous_prescription = "n"
                break

            else:
                print("Please enter y for Yes or n for No.")

        if has_previous_prescription == "y":

            print("\n--- Previous Prescription ---")
            print("Enter power with + or - sign.")
            print("Example: -1.00, +2.00")
            print("Leave ADD blank if not required.")

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
            previous_right_sph = ""
            previous_right_cyl = ""
            previous_right_axis = ""
            previous_right_add = ""

            previous_left_sph = ""
            previous_left_cyl = ""
            previous_left_axis = ""
            previous_left_add = ""

            print("Previous prescription details skipped.")
    else:
        print(
            "First-time spectacle user - "
            "Previous prescription not required."
        )

else:
    spectacle_history = "Not Applicable"
# ==================================================
# 8. CURRENT PRESCRIPTION
# ==================================================

if order_type in ["2", "3"]:
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

    while True:
        right_sph = input("Enter Right Eye SPH (+/-): ").strip()

        if right_sph.lower() == "plano":
            right_sph = "Plano"
            break

        if right_sph == "0":
            break

        if right_sph.startswith(("+", "-")):
            number_part = right_sph[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 30
            ):
                break

        print("Invalid SPH. Enter like -1.00, +1.25, 0 or Plano.")

    while True:
        right_cyl = input("Enter Right Eye CYL (+/-): ").strip()

        if right_cyl == "":
            break

        if right_cyl == "0":
            break

        if right_cyl.startswith(("+", "-")):
            number_part = right_cyl[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 10
            ):
                break

        print("Invalid CYL. Enter like -0.50, +1.25, 0 or leave blank.")

    while True:
        right_axis = input("Enter Right Eye AXIS (0-180): ").strip()

        if right_axis == "":
            break

        if right_axis.isdigit():
            axis_value = int(right_axis)

            if 0 <= axis_value <= 180:
                break

        print("Invalid AXIS. Enter a number from 0 to 180 or leave blank.")

    if lens_type_choice == "1" or add_requirement == "3":
        right_add = ""
    else:
        while True:
            right_add = input(
                "Enter Right Eye ADD / Near Power (+): "
            ).strip()

            if right_add in ["", "0"]:
                print("ADD is required for Right Eye.")
                continue

            if right_add.startswith("+"):
                number_part = right_add[1:]
                parts = number_part.split(".")

                if (
                    len(parts) == 2
                    and parts[0].isdigit()
                    and len(parts[1]) == 2
                    and parts[1] in ["00", "25", "50", "75"]
                    and float(number_part) <= 5
                ):
                    break

            print(
                "Invalid ADD. Enter like +1.00, +1.25, +1.50 or +2.00."
            )
    # ==================================================
    # 10. CURRENT LEFT EYE
    # ==================================================

    print("\nLeft Eye (OS)")

    while True:
        left_sph = input("Enter Left Eye SPH (+/-): ").strip()

        if left_sph.lower() == "plano":
            left_sph = "Plano"
            break

        if left_sph == "0":
            break

        if left_sph.startswith(("+", "-")):
            number_part = left_sph[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 30
            ):
                break

        print("Invalid SPH. Enter like -1.00, +1.25, 0 or Plano.")

    while True:
        left_cyl = input("Enter Left Eye CYL (+/-): ").strip()

        if left_cyl == "":
            break

        if left_cyl == "0":
            break

        if left_cyl.startswith(("+", "-")):
            number_part = left_cyl[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 10
            ):
                break

        print("Invalid CYL. Enter like -1.00, +0.50, 0 or leave blank.")

    while True:
        left_axis = input("Enter Left Eye AXIS (0-180): ").strip()

        if left_axis == "":
            break

        if left_axis.isdigit():
            axis_value = int(left_axis)

            if 0 <= axis_value <= 180:
                break

        print("Invalid AXIS. Enter a number from 0 to 180 or leave blank.")

    # Left Eye ADD Logic
    if lens_type_choice == "1" or add_requirement == "2":
        left_add = ""
    else:
        while True:
            left_add = input(
                "Enter Left Eye ADD / Near Power (+): "
            ).strip()

            if left_add in ["", "0"]:
                print("ADD is required for Left Eye.")
                continue

            if left_add.startswith("+"):
                number_part = left_add[1:]
                parts = number_part.split(".")

                if (
                    len(parts) == 2
                    and parts[0].isdigit()
                    and len(parts[1]) == 2
                    and parts[1] in ["00", "25", "50", "75"]
                    and float(number_part) <= 5
                ):
                    break

            print(
                "Invalid ADD. Enter like +1.00, +1.25, +1.50 or +2.00."
            )

else:
    right_sph = ""
    right_cyl = ""
    right_axis = ""
    right_add = ""

    left_sph = ""
    left_cyl = ""
    left_axis = ""
    left_add = ""

    distance_pd = ""
    near_pd = ""

    right_va = ""
    left_va = ""
    right_pinhole = ""
    left_pinhole = ""

if order_type in ["2", "3"]:
    print("\n--- Pupillary Distance (PD) (Optional) ---")
    distance_pd = input(
        "Enter Distance PD in mm (Example: 62): "
    ).strip()

    near_pd = input(
        "Enter Near PD in mm (Example: 59): "
    ).strip()

    print("\n--- Visual Acuity Test (Optional) ---")

    right_va = input(
        "Right Eye Visual Acuity (Example: 6/6): "
    ).strip()

    left_va = input(
        "Left Eye Visual Acuity (Example: 6/6): "
    ).strip()

    right_pinhole = input(
        "Right Eye Pinhole (Example: 6/6): "
    ).strip()

    left_pinhole = input(
        "Left Eye Pinhole (Example: 6/6): "
    ).strip()
# ==================================================
# 11. PAYMENT DETAILS
# ==================================================

    print("\n--- Payment Details ---")


# Order Total
order_total = frame_price + lens_price
print(f"Order Total: ₹{order_total:.2f}")

# Less Amount Validation
while True:
    less_amount_input = input(
        "Enter Less Amount "
        "(Optional - press Enter for 0): "
    ).strip()

    if less_amount_input == "":
        less_amount = 0.0
        break

    try:
        less_amount = float(less_amount_input)

        if less_amount < 0:
            print("Less Amount cannot be negative.")

        elif less_amount > order_total:
            print(
                "Less Amount cannot be greater "
                "than Order Total."
            )

        else:
            break

    except ValueError:
        print(
            "Please enter Less Amount "
            "using numbers only."
        )

# Final Total After Less Amount
total_amount = order_total - less_amount
print(f"Final Total Amount: ₹{total_amount:.2f}")

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
                "than Final Total Amount."
            )

        else:
            break

    except ValueError:
        print(
            "Please enter amount using numbers only."
        )

# Automatic Balance Calculation
balance = total_amount - advance_amount
# ----------------------------------------------
# SAVE INITIAL PAYMENT RECORD
# ----------------------------------------------

if order_type in ["1", "2", "3"]:

    from datetime import datetime

    payment_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    order_type_name = {
        "1": "Frame Only",
        "2": "Lenses Only",
        "3": "Frame + Lenses"
    }[order_type]

    if balance == 0:
        payment_type = "Full Payment"
        payment_status = "Paid"
    elif advance_amount > 0:
        payment_type = "Advance"
        payment_status = "Pending"
    else:
        payment_type = "No Advance"
        payment_status = "Pending"

    with open(
        "payments.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as payment_file:

        payment_writer = csv.writer(
            payment_file
        )

        payment_writer.writerow([
            payment_datetime,
            customer_name,
            phone,
            address,
            payment_datetime,
            order_type_name,
            total_amount,
            0,
            advance_amount,
            balance,
            payment_type,
            payment_status,
            "Pending",
            ""
            ])


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
    "Gender:",
    gender
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

if full_address:
    print("Full Address:", full_address)
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

    if any([
        previous_right_sph,
        previous_right_cyl,
        previous_right_axis,
        previous_right_add,
        previous_left_sph,
        previous_left_cyl,
        previous_left_axis,
        previous_left_add
    ]):

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
        print("Previous Prescription: Not available")
else:

    print(
        "\nPrevious Prescription: "
        "Not Applicable"
    )


# ---------------- FRAME / LENS ----------------

print("\n--- Frame / Lens Details ---")

if order_type in ["1", "3"]:
    print("Frame Details:", frame_details)

    if frame_brand:
        print("Frame Brand:", frame_brand)

    if frame_offer:
        print("Frame Offer:", frame_offer)

    print("Frame Price:", frame_price)

if order_type in ["2", "3"]:
    print("Lens Type:", lens_type)

    if lens_features:
        print("Lens Features / Coating:", lens_features)

    if lens_brand:
        print("Lens Brand:", lens_brand)

    if lens_offer:
        print("Lens Offer:", lens_offer)

    print("Lens Price:", lens_price)
# ---------------- CURRENT PRESCRIPTION ----------------

if order_type in ["2", "3"]:

    print("\n--- Current Prescription ---")

    print(
        "Right Eye (OD):",
        "SPH =", right_sph,
        "CYL =", right_cyl,
        "AXIS =", right_axis,
        "ADD =",
        right_add if right_add else "Not Required"
    )

    print(
        "Left Eye (OS):",
        "SPH =", left_sph,
        "CYL =", left_cyl,
        "AXIS =", left_axis,
        "ADD =",
        left_add if left_add else "Not Required"
    )

    if distance_pd or near_pd:
        print(
            "Distance PD:",
            distance_pd if distance_pd else "Not Measured"
        )

        print(
            "Near PD:",
            near_pd if near_pd else "Not Measured"
        )

    # ---------------- VISUAL ACUITY / PINHOLE ----------------

    if right_va or left_va or right_pinhole or left_pinhole:

        if right_va:
            print("Right Eye Visual Acuity :", right_va)

        if left_va:
            print("Left Eye Visual Acuity  :", left_va)

        if right_pinhole:
            print("Right Eye Pinhole       :", right_pinhole)

        if left_pinhole:
            print("Left Eye Pinhole        :", left_pinhole)

# ---------------- PAYMENT ----------------

print("\n--- Payment ---")

print(
    "Order Total:",
    order_total
)

print(
    "Less Amount:",
    less_amount
)

print(
    "Final Total Amount:",
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
csv_file_exists = os.path.exists("customers.csv")
# Save customer record to CSV
with open("customers.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not csv_file_exists:
       writer.writerow([
    "Date/Time",
    "Store Name",
    "Store City",
    "Store Phone",
    "Store Logo",
    "Customer Name",
    "Gender",
    "Age",
    "Phone",
    "Address",
    "Spectacle History",
    "Years Using Glasses",
    "Previous Right SPH",
    "Previous Right CYL",
    "Previous Right AXIS",
    "Previous Right ADD",
    "Previous Left SPH",
    "Previous Left CYL",
    "Previous Left AXIS",
    "Previous Left ADD",
    "Frame Details",
    "Frame Brand",
    "Frame Offer",
    "Frame Price",
    "Lens Type",
    "Lens Brand",
    "Lens Offer",
    "Lens Price",
    "Right SPH",
    "Right CYL",
    "Right AXIS",
    "Right ADD",
    "Left SPH",
    "Left CYL",
    "Left AXIS",
    "Left ADD",
    "Distance PD",
    "Near PD",
    "Right VA",
    "Left VA",
    "Right Pinhole",
    "Left Pinhole",
    "Total Amount",
    "Advance Amount",
    "Balance",
    "Lens Features / Coating",
    "Full Address"
 ])   
    writer.writerow([  
            
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    store_name,
    store_city,
    store_phone,
    store_logo,
    customer_name,
    gender,
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
    frame_brand,
    frame_offer,
    frame_price,
    lens_type,
    lens_brand,
    
    lens_offer,
    lens_price,
    right_sph,
    right_cyl,
    right_axis,
    right_add,
    left_sph,
    left_cyl,
    left_axis,
    left_add,
    distance_pd,
    near_pd,
    right_va,
    left_va,
    right_pinhole,
    left_pinhole,
    total_amount,
    advance_amount,
    balance,
    lens_features,
    full_address,
 ])

print("\n==================================================")
print("        CUSTOMER RECORD COMPLETED SUCCESSFULLY")
print("==================================================")
if order_type == "1":
    print("\n--- ORDER MESSAGE ---")
else:
    print("\n--- PRESCRIPTION MESSAGE ---")
if order_type == "1":
    prescription_message = f"""
{store_name}
Customer Name: {customer_name}
Date: {record_date}
Time: {record_time}

Frame Order

Frame Details: {frame_details}
Frame Brand: {frame_brand}
{f"Frame Offer: {frame_offer}" if frame_offer else ""}
Frame Price: ₹{frame_price}

Thank you for choosing {store_name}.
"""

else:
    prescription_message = f"""
{store_name}
Customer Name: {customer_name}
Date: {record_date}
Time: {record_time}
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
{f"Pupillary Distance (PD):\nDistance PD: {distance_pd}\nNear PD: {near_pd}\n" if distance_pd or near_pd else ""}

{f"Visual Acuity / Pinhole Test:\nRight Eye Visual Acuity: {right_va}\nLeft Eye Visual Acuity: {left_va}\nRight Eye Pinhole: {right_pinhole}\nLeft Eye Pinhole: {left_pinhole}\n" if right_va or left_va or right_pinhole or left_pinhole else ""}
Please keep this prescription for your reference.
"""
print(prescription_message)
print("\n--- Send Message ---")
print("1. Normal SMS")

if order_type == "1":
    print("2. WhatsApp Order")
else:
    print("2. WhatsApp Prescription")

print("3. WhatsApp Payment Receipt")
print("4. WhatsApp Balance Reminder")

if order_type == "1":
    print("5. WhatsApp Order + Payment")
else:
    print("5. WhatsApp Prescription + Payment")

print("6. Skip")
while True:
    message_choice = input(
        "Select Message Option (1/2/3/4/5/6): "
    ).strip()

    if message_choice in ["1", "2", "3", "4", "5", "6"]:
        break

    print("Please select a valid Message Option (1-6).")
if message_choice == "1":
    if not phone:
        print("Normal SMS cannot be prepared - Customer phone number is not available.")
    else:
        sms_message = prescription_message

        print("\n--- NORMAL SMS TEXT ---")
        print(sms_message)
if message_choice == "2":
    if not phone:
        print("WhatsApp Prescription cannot be sent - Customer phone number is not available.")
    else:
        import urllib.parse
        import webbrowser

        whatsapp_message = urllib.parse.quote(prescription_message)
        whatsapp_url = f"https://wa.me/91{phone}?text={whatsapp_message}"

        webbrowser.open(whatsapp_url)
if message_choice == "2" and phone:
    if order_type == "1":
        print("Opening WhatsApp Order...")
    else:
        print("Opening WhatsApp Prescription...")
if message_choice == "3":
    if not phone:
        print("WhatsApp Payment Receipt cannot be sent - Customer phone number is not available.")
    else:
        import urllib.parse
        import webbrowser

        payment_message = f"""{store_name}
Customer Name: {customer_name}

Payment Receipt

Total Amount: ₹{total_amount}
Advance Amount: ₹{advance_amount}
Balance Amount: ₹{balance}

Thank you for choosing {store_name}.
"""

        whatsapp_message = urllib.parse.quote(payment_message)
        whatsapp_url = f"https://wa.me/91{phone}?text={whatsapp_message}"

        webbrowser.open(whatsapp_url)
        print("Opening WhatsApp Payment Receipt...")
if message_choice == "4":
    if not phone:
        print("WhatsApp Balance Reminder cannot be sent - Customer phone number is not available.")
    else:
        import urllib.parse
        import webbrowser

        balance_message = f"""{store_name}
Customer Name: {customer_name}

Balance Payment Reminder

Your pending balance amount is ₹{balance}.

Please make the balance payment at your convenience.

Thank you,
{store_name}
"""

        whatsapp_message = urllib.parse.quote(balance_message)
        whatsapp_url = f"https://wa.me/91{phone}?text={whatsapp_message}"

        webbrowser.open(whatsapp_url)
        print("Opening WhatsApp Balance Reminder...")
if message_choice == "5":
    if not phone:
        print("WhatsApp Prescription + Payment cannot be sent - Customer phone number is not available.")
    else:
        import urllib.parse
        import webbrowser

        combined_message = f"""{prescription_message}

Payment Details

Total Amount: ₹{total_amount}
Advance Amount: ₹{advance_amount}
Balance Amount: ₹{balance}

Thank you for choosing {store_name}.
"""

        whatsapp_message = urllib.parse.quote(combined_message)
        whatsapp_url = f"https://wa.me/91{phone}?text={whatsapp_message}"

        webbrowser.open(whatsapp_url)
        print("Opening WhatsApp Prescription + Payment...")