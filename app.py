import csv
import os
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

while True:
    customer_type = input(
        "Select Customer Type (1/2): "
    ).strip()

    if customer_type in ["1", "2"]:
        break

    print(
        "Please select 1 for New Customer or 2 for Existing Customer."
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


while True:
    if customer_type == "2":
        order_type = input(
            "Select Order Type (1/2/3/4/5): "
        ).strip()
        valid_options = ["1", "2", "3", "4", "5"]
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
    print("\n--- Previous Prescription ---")

    print("OD:")
    print(
        f"SPH: {selected_customer[28]} | "
        f"CYL: {selected_customer[29]} | "
        f"AXIS: {selected_customer[30]} | "
        f"ADD: {selected_customer[31]}"
    )

    print("OS:")
    print(
        f"SPH: {selected_customer[32]} | "
        f"CYL: {selected_customer[33]} | "
        f"AXIS: {selected_customer[34]} | "
        f"ADD: {selected_customer[35]}"
    )

    raise SystemExit


# ==================================================
# OLD ORDER HISTORY
# ==================================================

if customer_type == "2" and order_type == "5":
    customer_orders = [
        customer
        for customer in matching_customers
        if customer[5].strip().lower() == selected_customer[5].strip().lower()
        and customer[8].strip() == selected_customer[8].strip()
        and customer[9].strip().lower() == selected_customer[9].strip().lower()
    ]

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

    frame_price = float(
        input("Enter Frame Price: ")
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

    lens_price = float(
        input("Enter Lens Price: ")
    )

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

    previous_right_sph = selected_customer[28]
    previous_right_cyl = selected_customer[29]
    previous_right_axis = selected_customer[30]
    previous_right_add = selected_customer[31]

    previous_left_sph = selected_customer[32]
    previous_left_cyl = selected_customer[33]
    previous_left_axis = selected_customer[34]
    previous_left_add = selected_customer[35]

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


# Total Amount Validation
total_amount = frame_price + lens_price
print(f"Total Amount: ₹{total_amount:.2f}")

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
    "Lens Features / Coating",
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
Frame Offer: {frame_offer}
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
print("2. WhatsApp Prescription")
print("3. WhatsApp Payment Receipt")
print("4. WhatsApp Balance Reminder")
print("5. WhatsApp Prescription + Payment")
print("6. Skip")

message_choice = input("Select Message Option (1/2/3/4/5/6): ").strip()
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