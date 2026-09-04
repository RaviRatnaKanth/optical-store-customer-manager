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

customer_type = input("Select Customer Type (1/2): ").strip()

if customer_type == "2":
    search_value = input(
        "Enter Existing Customer Name or Phone: "
    ).strip().lower()

    matching_customers = []

    with open("customers.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) > 8 and (
                row[5].strip().lower() == search_value
                or row[8].strip().lower() == search_value
            ):
                matching_customers.append(row)

    if len(matching_customers) == 1:
        selected_customer = matching_customers[0]
        customer_name = selected_customer[5]
        phone = selected_customer[8]

        print("\nSelected Customer:")
        print(f"Name: {customer_name} | Phone: {phone}")

        confirm = input(
            "Is this the correct customer? (y/n): "
        ).strip().lower()

        if confirm == "y":
            print("Customer confirmed.")
            print("Customer selection successful.")
        else:
            print("Customer not confirmed.")
            raise SystemExit

    elif len(matching_customers) > 1:
        print("\nMultiple customers found:")

        for number, customer in enumerate(
            matching_customers,
            start=1
        ):
          print(
    f"{number}. Name: {customer[5]} | "
    f"Phone: {customer[8]} | "
    f"Address: {customer[9]}"
)

        choice = input(
            "Select Customer Number: "
        ).strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(matching_customers):
                selected_customer = matching_customers[
                    choice - 1
                ]

                customer_name = selected_customer[5]
                phone = selected_customer[8]

                print("\nSelected Customer:")
                print(
                    f"Name: {customer_name} | "
                    f"Phone: {phone}"
                )

                confirm = input(
                    "Is this the correct customer? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    print("Customer confirmed.")
                    print(
                        "Customer selection successful."
                    )
                else:
                    print("Customer not confirmed.")
                    raise SystemExit

            else:
                print("Invalid customer number.")
                raise SystemExit
        else:
            print("Please enter a valid customer number.")
            raise SystemExit

    else:
        print("Customer not found.")
        raise SystemExit
print("\n--- Customer Details ---")
if customer_type == "1":
    customer_name = input("Enter Customer Name: ").strip().title()
else:
    customer_name = selected_customer[5]
if customer_type == "1":
    print("\n--- Gender ---")
    print("1. Male")
    print("2. Female")

    while True:
        gender_choice = input("Select Gender (1/2): ").strip()

        if gender_choice == "1":
            gender = "Male"
            break
        elif gender_choice == "2":
            gender = "Female"
            break
        else:
            print("Please select 1 for Male or 2 for Female.")
else:
    gender = selected_customer[6]
# Age / Phone / Address
if customer_type == "1":
    while True:
        try:
            age = int(input("Enter Patient Age: "))

            if age > 0:
                break
            else:
                print("Please enter a valid age.")

        except ValueError:
            print("Please enter age using numbers only.")

    phone = input("Enter Customer Phone Number (Optional - press Enter if unavailable): ").strip()
    address = input("Enter Customer Address: ").strip().title()
else:
    age = selected_customer[7]
    phone = selected_customer[8]
    address = selected_customer[9]



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
    if len(selected_order) > 44 and selected_order[-1].strip():
       print("Features   :", selected_order[-1])
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

    lens_type = input(
        "Enter Lens Type "
        "(Single Vision / Bifocal / Progressive / Other): "
    ).strip().title()
    lens_features = input("Enter Lens Features / Coating (Optional): ").strip().title()
    lens_brand = input("Enter Lens Brand (Optional): ").strip().title()
    lens_offer = input(
        "Enter Lens Offer: "
    ).strip()
    lens_price = float(input("Enter Lens Price: "))

else:
    lens_type = ""
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

    while True:
        right_add = input("Enter Right Eye ADD / Near Power (+): ").strip()

        if right_add == "":
            break

        if right_add == "0":
            break

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

        print("Invalid ADD. Enter like +1.00, +1.25, +2.00, 0 or leave blank.")

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

    while True:
        left_add = input("Enter Left Eye ADD / Near Power (+): ").strip()

        if left_add == "":
            break

        if left_add == "0":
            break

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

        print("Invalid ADD. Enter like +1.00, +1.25, +2.00, 0 or leave blank.")

 
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
    distance_pd = input("Enter Distance PD in mm (Example: 62): ").strip()
    near_pd = input("Enter Near PD in mm (Example: 59): ").strip()
    print("\n--- Visual Acuity Test (Optional) ---")
    right_va = input("Right Eye Visual Acuity (Example: 6/6): ").strip()
    left_va = input("Left Eye Visual Acuity (Example: 6/6): ").strip()
    right_pinhole = input("Right Eye Pinhole (Example: 6/6): ").strip()
    left_pinhole = input("Left Eye Pinhole (Example: 6/6): ").strip()
    
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

print("Frame Details:", frame_details)

if frame_brand:
    print("Frame Brand:", frame_brand)

if frame_offer:
    print("Frame Offer:", frame_offer)
    print("Frame Price:", frame_price)

print("Lens Type:", lens_type)
if lens_features:
    print("Lens Features / Coating:", lens_features)
if lens_brand:
    print("Lens Brand:", lens_brand)

if lens_offer:
    print("Lens Offer:", lens_offer)
    print("Lens Price:", lens_price)


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
    "Lens Features / Coating"
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
])
print("\n==================================================")
print("        CUSTOMER RECORD COMPLETED SUCCESSFULLY")
print("==================================================")
print("\n--- PRESCRIPTION MESSAGE ---")

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
send_whatsapp = input("\nSend prescription on WhatsApp? (y/n): ").strip().lower()

if send_whatsapp == "y":
    import urllib.parse
    import webbrowser

    whatsapp_message = urllib.parse.quote(prescription_message)
    whatsapp_url = f"https://wa.me/91{phone}?text={whatsapp_message}"

    webbrowser.open(whatsapp_url)
    print("Opening WhatsApp...")
else:
    print("Prescription not sent on WhatsApp.")
