import calendar
import csv
import os
import uuid
import shutil
import webbrowser
import urllib.parse
import hashlib
import hmac
import secrets
import getpass
from datetime import datetime
from store_config import store_name, store_city, store_address, store_phone, store_email, store_website, store_logo
def print_text_document(document_text):
    import tempfile

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8-sig"
        ) as print_file:
            print_file.write(document_text)
            print_file_path = print_file.name

        os.startfile(print_file_path, "print")

        print(
            "Print job sent to the Windows default printer."
        )

    except Exception as error:
        print(
            "Unable to print document:",
            error
        )
def normalize_offer(offer):
    offer = offer.strip()

    if not offer:
        return ""

    offer = offer.rstrip("%").strip()

    try:
        value = float(offer)

        if value.is_integer():
            return f"{int(value)}%"

        return f"{value}%"

    except ValueError:
        return offer
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

STORE_PROFILE_FILE = "store_profile.csv"
LICENSE_FILE = "license_data.csv"
LICENSE_AUDIT_FILE = "license_audit.csv"
STORE_REGISTRY_FILE = "stores.csv"
ADMIN_SECURITY_FILE = "admin_security.csv"


def load_store_profile():
    global store_name
    global store_city
    global store_address
    global store_phone
    global store_email
    global store_website
    global store_logo

    if not os.path.exists(STORE_PROFILE_FILE):
        return

    try:
        with open(
            STORE_PROFILE_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as profile_file:
            reader = csv.DictReader(profile_file)
            profile = next(reader, None)

        if not profile:
            return

        store_name = profile.get(
            "Store Name",
            store_name
        ).strip() or store_name

        store_city = profile.get(
            "Store City",
            store_city
        ).strip()

        store_address = profile.get(
            "Store Address",
            store_address
        ).strip()

        store_phone = profile.get(
            "Store Phone",
            store_phone
        ).strip()

        store_email = profile.get(
            "Store Email",
            store_email
        ).strip()

        store_website = profile.get(
            "Store Website",
            store_website
        ).strip()

        store_logo = profile.get(
            "Store Logo",
            store_logo
        ).strip()

    except Exception as error:
        print(
            "\nWarning: Store Profile could not be loaded."
        )
        print("Store Profile Error:", error)
def get_first_store_setup():
    global store_name, store_city, store_phone
    print("\n" + "=" * 50)
    print("          FIRST-TIME SHOP SETUP")
    print("=" * 50)

    while True:
        first_store_name = input(
            "Enter Store / Shop Name: "
        ).strip()

        if first_store_name:
            break

        print("Store / Shop Name is required.")

    while True:
        first_store_city = input(
            "Enter Store City / Town: "
        ).strip()

        if first_store_city:
            break

        print("Store City / Town is required.")
    while True:
        first_store_phone = input(
            "Enter Store Phone Number "
            "(Optional - press Enter if unavailable): "
        ).strip()

        if not first_store_phone:
            first_store_phone = ""
            break

        normalized_phone = normalize_indian_phone(
            first_store_phone
        )

        if (
            normalized_phone.isdigit()
            and len(normalized_phone) == 10
            and normalized_phone[0] in "6789"
        ):
            first_store_phone = normalized_phone
            break

        print(
            "Please enter a valid Indian mobile number "
            "or press Enter to skip."
        )

    store_name = first_store_name
    store_city = first_store_city
    store_phone = first_store_phone

    return first_store_name, first_store_city


def initialize_store_registry():
    if os.path.exists(STORE_REGISTRY_FILE):
        return

    fieldnames = [
        "Store ID",
        "Store Name",
        "Store City",
        "Status"
    ]

    first_store_name, first_store_city = get_first_store_setup()

    initial_store = {
        "Store ID": "STORE001",
        "Store Name": first_store_name,
        "Store City": first_store_city,
        "Status": "Active"
    }
    try:
        with open(
            STORE_REGISTRY_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as store_file:
            writer = csv.DictWriter(
                store_file,
                fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerow(initial_store)

    except Exception as error:
        print(
            "\nWarning: Store Registry could not be created."
        )
        print("Store Registry Error:", error)

def load_store_registry():
    stores = []

    try:
        with open(
            STORE_REGISTRY_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as store_file:
            reader = csv.DictReader(store_file)

            for row in reader:
                if row.get("Status", "").strip().lower() == "active":
                    stores.append(row)

    except Exception as error:
        print(
            "\nWarning: Store Registry could not be loaded."
        )
        print("Store Registry Error:", error)

    return stores

def update_current_store_registry():
    try:
        stores = []

        with open(
            STORE_REGISTRY_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as store_file:
            reader = csv.DictReader(store_file)
            stores = list(reader)

        for store in stores:
            if store.get("Store ID") == CURRENT_STORE_ID:
                store["Store Name"] = store_name
                store["Store City"] = store_city
                break

        with open(
            STORE_REGISTRY_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as store_file:
            writer = csv.DictWriter(
                store_file,
                fieldnames=[
                    "Store ID",
                    "Store Name",
                    "Store City",
                    "Status"
                ]
            )
            writer.writeheader()
            writer.writerows(stores)

        return True

    except Exception as error:
        print(
            "\nWarning: Store Registry could not be updated."
        )
        print("Store Registry Error:", error)
        return False


def get_license_fieldnames():
    return [
        "License ID",
        "Customer / Business Name",
        "Plan",
        "Start Date",
        "Expiry Date",
        "Allowed Stores",
        "License Status",
        "Last Updated"
    ]

def get_license_audit_fieldnames():
    return [
        "Audit Date Time",
        "License ID",
        "Action",
        "Old Value",
        "New Value",
        "Changed By",
        "Notes"
    ]


def generate_license_id():
    return f"LIC-{uuid.uuid4().hex[:12].upper()}"


def get_license_plans():
    return [
        "Trial",
        "1 Year",
        "2 Years",
        "Lifetime",
        "Free",
        "Custom"
    ]


def add_calendar_months(start_date, months):
    target_month = start_date.month - 1 + months
    target_year = start_date.year + target_month // 12
    target_month = target_month % 12 + 1

    last_day = calendar.monthrange(
        target_year,
        target_month
    )[1]

    target_day = min(start_date.day, last_day)

    return start_date.replace(
        year=target_year,
        month=target_month,
        day=target_day
    )


def calculate_license_expiry(start_date, plan):
    if plan == "Trial":
        return add_calendar_months(start_date, 6)

    if plan == "1 Year":
        return add_calendar_months(start_date, 12)

    if plan == "2 Years":
        return add_calendar_months(start_date, 24)

    if plan in ["Lifetime", "Free"]:
        return None

    return None


def get_custom_license_expiry_date(start_date):
    while True:
        custom_expiry_input = input(
            "Enter Custom Expiry Date "
            "(DD-MM-YYYY): "
        ).strip()

        accepted_formats = (
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d-%m-%y",
            "%d/%m/%y",
        )

        custom_expiry_date = None

        for date_format in accepted_formats:
            try:
                custom_expiry_date = datetime.strptime(
                    custom_expiry_input,
                    date_format
                ).date()
                break
            except ValueError:
                continue

        if (
            custom_expiry_date is not None
            and custom_expiry_date > start_date
        ):
            return custom_expiry_date

        print("Please enter a valid future expiry date.")
def initialize_license_file():
    if os.path.exists(LICENSE_FILE):
        return

    try:
        with open(
            LICENSE_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as license_file:
            writer = csv.DictWriter(
                license_file,
                fieldnames=get_license_fieldnames()
            )
            writer.writeheader()

    except Exception as error:
        print(
            "\nWarning: License file could not be created."
        )
        print("License File Error:", error)


def initialize_license_audit_file():
    if os.path.exists(LICENSE_AUDIT_FILE):
        return

    try:
        with open(
            LICENSE_AUDIT_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as audit_file:
            writer = csv.DictWriter(
                audit_file,
                fieldnames=get_license_audit_fieldnames()
            )
            writer.writeheader()

    except Exception as error:
        print(
            "\nWarning: License audit file could not be created."
        )
        print("License Audit File Error:", error)


def load_license_records():
    records = []

    try:
        with open(
            LICENSE_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as license_file:
            reader = csv.DictReader(license_file)
            records = list(reader)

    except Exception as error:
        print(
            "\nWarning: License file could not be loaded."
        )
        print("License File Error:", error)

    return records


def save_license_record(license_record):
    try:
        license_record["Last Updated"] = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        with open(
            LICENSE_FILE,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as license_file:
            writer = csv.DictWriter(
                license_file,
                fieldnames=get_license_fieldnames()
            )
            writer.writerow(license_record)

        return True

    except Exception as error:
        print(
            "\nWarning: License record could not be saved."
        )
        print("License File Error:", error)
        return False


def save_license_audit_record(
    license_id,
    action,
    old_value="",
    new_value="",
    changed_by="Developer/Admin",
    notes=""
):
    try:
        audit_record = {
            "Audit Date Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "License ID": license_id,
            "Action": action,
            "Old Value": old_value,
            "New Value": new_value,
            "Changed By": changed_by,
            "Notes": notes
        }

        with open(
            LICENSE_AUDIT_FILE,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as audit_file:
            writer = csv.DictWriter(
                audit_file,
                fieldnames=get_license_audit_fieldnames()
            )
            writer.writerow(audit_record)

        return True

    except Exception as error:
        print(
            "\nWarning: License audit record could not be saved."
        )
        print("License Audit Error:", error)
        return False


def get_active_store_ids():
    active_stores = load_store_registry()

    return [
        store["Store ID"]
        for store in active_stores
        if store.get("Store ID")
    ]


def license_record_exists():
    license_records = load_license_records()

    return len(license_records) > 0


def create_initial_license():
    if license_record_exists():
        return False

    active_store_ids = get_active_store_ids()

    if not active_store_ids:
        return False

    license_id = generate_license_id()
    business_name = store_name
    start_date = datetime.now().date()


    license_plans = get_license_plans()

    print("\n--- Select License Plan ---")

    for index, plan in enumerate(license_plans, start=1):
        print(f"{index}. {plan}")
    while True:
        plan_choice = input(
            f"Select License Plan (1-{len(license_plans)}): "
        ).strip()

        if plan_choice.isdigit():
            plan_index = int(plan_choice) - 1

            if 0 <= plan_index < len(license_plans):
                selected_plan = license_plans[plan_index]
                break

        print("Please select a valid License Plan number.")
    expiry_date = calculate_license_expiry(
        start_date,
        selected_plan
    )
    if selected_plan == "Custom":
        expiry_date = get_custom_license_expiry_date(
            start_date
        )
    allowed_stores = "|".join(active_store_ids)
    license_record = {
        "License ID": license_id,
        "Customer / Business Name": business_name,
        "Plan": selected_plan,
        "Start Date": start_date.strftime("%Y-%m-%d"),
        "Expiry Date": (
            expiry_date.strftime("%Y-%m-%d")
            if expiry_date is not None
            else ""
        ),
        "Allowed Stores": allowed_stores,
        "License Status": "Active",
        "Last Updated": ""
    }
    if save_license_record(license_record):
        return True

    return False

def get_current_license_record():
    license_records = load_license_records()

    if not license_records:
        return None

    return license_records[-1]


def display_current_license_details():
    license_record = get_current_license_record()

    if license_record is None:
        print("\nNo license record found.")
        return False

    print("\n--- Current License Details ---")
    print(
        "License ID:",
        license_record.get("License ID", "")
    )
    print(
        "Business Name:",
        license_record.get("Customer / Business Name", "")
    )
    print(
        "Plan:",
        license_record.get("Plan", "")
    )
    print(
        "Start Date:",
        license_record.get("Start Date", "")
    )
    print(
        "Expiry Date:",
        license_record.get("Expiry Date", "")
        or "No Expiry"
    )
    print(
        "Allowed Stores:",
        license_record.get("Allowed Stores", "")
    )
    print(
        "License Status:",
        license_record.get("License Status", "")
    )
    print(
        "Last Updated:",
        license_record.get("Last Updated", "")
    )

    return True


def change_license_status():
    license_record = get_current_license_record()

    if license_record is None:
        print("\nNo license record found.")
        return False

    current_status = (
        license_record.get("License Status", "").strip()
    )

    print("\n--- Change License Status ---")
    print("Current Status:", current_status or "Not Set")
    print("1. Active")
    print("2. Suspended")

    while True:
        status_choice = input(
            "Select New License Status (1/2): "
        ).strip()

        if status_choice == "1":
            new_status = "Active"
            break

        if status_choice == "2":
            new_status = "Suspended"
            break

        print("Please select 1 or 2.")

    if current_status.lower() == new_status.lower():
        print(
            "\nLicense status is already set to",
            new_status + "."
        )
        return False

    updated_license = license_record.copy()
    updated_license["License Status"] = new_status

    if not save_license_record(updated_license):
        print("\nLicense status could not be changed.")
        return False

    audit_saved = save_license_audit_record(
        license_record.get("License ID", ""),
        "LICENSE STATUS CHANGED",
        current_status,
        new_status,
        "Developer/Admin",
        "License status updated"
    )

    print(
        "\nLicense status changed successfully:",
        current_status,
        "->",
        new_status
    )

    if not audit_saved:
        print(
            "Warning: License changed, but audit history "
            "could not be saved."
        )

    return True
def change_license_plan():
    license_record = get_current_license_record()

    if license_record is None:
        print("\nNo license record found.")
        return False

    current_plan = license_record.get(
        "Plan",
        ""
    ).strip()

    license_plans = get_license_plans()

    print("\n--- Change License Plan ---")
    print("Current Plan:", current_plan or "Not Set")

    for index, plan in enumerate(license_plans, start=1):
        print(f"{index}. {plan}")

    while True:
        plan_choice = input(
            f"Select New License Plan "
            f"(1-{len(license_plans)}): "
        ).strip()

        if plan_choice.isdigit():
            plan_index = int(plan_choice) - 1

            if 0 <= plan_index < len(license_plans):
                new_plan = license_plans[plan_index]
                break

        print("Please select a valid License Plan number.")

    if current_plan.lower() == new_plan.lower():
        print(
            "\nLicense plan is already set to",
            new_plan + "."
        )
        return False

    new_start_date = datetime.now().date()

    new_expiry_date = calculate_license_expiry(
        new_start_date,
        new_plan
    )

    if new_plan == "Custom":
        new_expiry_date = get_custom_license_expiry_date(
            new_start_date
        )

    updated_license = license_record.copy()
    updated_license["Plan"] = new_plan
    updated_license["Start Date"] = (
        new_start_date.strftime("%Y-%m-%d")
    )
    updated_license["Expiry Date"] = (
        new_expiry_date.strftime("%Y-%m-%d")
        if new_expiry_date is not None
        else ""
    )

    if not save_license_record(updated_license):
        print("\nLicense plan could not be changed.")
        return False

    audit_saved = save_license_audit_record(
        license_record.get("License ID", ""),
        "LICENSE PLAN CHANGED",
        current_plan,
        new_plan,
        "Developer/Admin",
        "License plan updated"
    )

    print(
        "\nLicense plan changed successfully:",
        current_plan,
        "->",
        new_plan
    )

    print(
        "New Start Date:",
        updated_license["Start Date"]
    )

    print(
        "New Expiry Date:",
        updated_license["Expiry Date"]
        or "No Expiry"
    )

    if not audit_saved:
        print(
            "Warning: License changed, but audit history "
            "could not be saved."
        )

    return True

def change_license_allowed_stores():
    license_record = get_current_license_record()

    if license_record is None:
        print("\nNo license record found.")
        return False

    active_stores = load_store_registry()

    if not active_stores:
        print("\nNo active stores were found.")
        return False

    current_allowed_stores = [
        store_id.strip()
        for store_id in license_record.get(
            "Allowed Stores",
            ""
        ).split("|")
        if store_id.strip()
    ]
    print("\n--- Change Allowed Stores ---")
    print(
        "Current Allowed Stores:",
        "|".join(current_allowed_stores)
        or "None"
    )

    print("\n--- Active Stores ---")

    for index, store in enumerate(active_stores, start=1):
        store_id = store.get("Store ID", "")
        store_name = store.get("Store Name", "")
        store_city = store.get("Store City", "")

        selected_text = ""

        if store_id in current_allowed_stores:
            selected_text = " [Currently Allowed]"

        print(
            f"{index}. {store_id} - "
            f"{store_name} - {store_city}"
            f"{selected_text}"
        )
    while True:
        store_choice = input(
            "\nSelect Allowed Store Number(s) "
            "(example: 1,2): "
        ).strip()

        selected_parts = [
            part.strip()
            for part in store_choice.split(",")
            if part.strip()
        ]

        if not selected_parts:
            print("Please select at least one store.")
            continue

        if not all(
            part.isdigit()
            for part in selected_parts
        ):
            print(
                "Please enter store numbers only, "
                "separated by commas."
            )
            continue

        selected_indexes = [
            int(part) - 1
            for part in selected_parts
        ]

        if not all(
            0 <= index < len(active_stores)
            for index in selected_indexes
        ):
            print("Please select valid store numbers.")
            continue

        selected_indexes = list(
            dict.fromkeys(selected_indexes)
        )

        selected_store_ids = [
            active_stores[index].get("Store ID", "")
            for index in selected_indexes
        ]

        selected_store_ids = [
            store_id
            for store_id in selected_store_ids
            if store_id
        ]

        if selected_store_ids:
            break

        print("Please select at least one valid store.")
    new_allowed_stores = "|".join(selected_store_ids)

    if set(current_allowed_stores) == set(selected_store_ids):
        print(
            "\nSelected stores are already allowed "
            "under this license."
        )
        return False

    updated_license = license_record.copy()
    updated_license["Allowed Stores"] = new_allowed_stores

    if not save_license_record(updated_license):
        print("\nAllowed stores could not be changed.")
        return False

    old_allowed_stores = "|".join(current_allowed_stores)

    audit_saved = save_license_audit_record(
        license_record.get("License ID", ""),
        "LICENSE ALLOWED STORES CHANGED",
        old_allowed_stores,
        new_allowed_stores,
        "Developer/Admin",
        "Allowed stores updated"
    )

    print("\nAllowed stores changed successfully.")
    print(
        "Old Allowed Stores:",
        old_allowed_stores or "None"
    )
    print(
        "New Allowed Stores:",
        new_allowed_stores
    )

    if not audit_saved:
        print(
            "Warning: Allowed stores changed, but "
            "audit history could not be saved."
        )

    return True
def hash_admin_password(password, salt):
    password_bytes = password.encode("utf-8")

    return hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        200000
    )
def save_admin_security(password):
    try:
        salt = secrets.token_bytes(32)
        password_hash = hash_admin_password(
            password,
            salt
        )

        with open(
            ADMIN_SECURITY_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as security_file:
            writer = csv.writer(security_file)
            writer.writerow([
                "Salt",
                "Password Hash"
            ])
            writer.writerow([
                salt.hex(),
                password_hash.hex()
            ])

        return True

    except Exception as error:
        print(
            "\nAdmin security information "
            "could not be saved."
        )
        print("Admin Security Error:", error)
        return False
def load_admin_security():
    try:
        if not os.path.exists(ADMIN_SECURITY_FILE):
            return None

        with open(
            ADMIN_SECURITY_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as security_file:
            reader = csv.DictReader(security_file)
            security_record = next(reader, None)

        if security_record is None:
            return None

        salt_hex = security_record.get(
            "Salt",
            ""
        ).strip()

        password_hash_hex = security_record.get(
            "Password Hash",
            ""
        ).strip()

        if not salt_hex or not password_hash_hex:
            return None

        return {
            "salt": bytes.fromhex(salt_hex),
            "password_hash": bytes.fromhex(
                password_hash_hex
            )
        }

    except Exception as error:
        print(
            "\nAdmin security information "
            "could not be loaded."
        )
        print("Admin Security Error:", error)
        return None

def verify_admin_password(password):
    security_record = load_admin_security()

    if security_record is None:
        return False

    entered_password_hash = hash_admin_password(
        password,
        security_record["salt"]
    )

    return hmac.compare_digest(
        entered_password_hash,
        security_record["password_hash"]
    )
def setup_admin_password():
    if os.path.exists(ADMIN_SECURITY_FILE):
        print("\nAdmin security is already configured.")
        return False

    print("\n--- First-Time Admin Security Setup ---")

    password = input(
        "Create Developer/Admin Password: "
    ).strip()

    if len(password) < 8:
        print(
            "Admin password must contain "
            "at least 8 characters."
        )
        return False

    confirm_password = input(
        "Confirm Developer/Admin Password: "
    ).strip()

    if password != confirm_password:
        print("Passwords do not match.")
        return False

    if not save_admin_security(password):
        return False

    print("\nAdmin password created successfully.")
    return True
def open_protected_admin_control():
    if not os.path.exists(ADMIN_SECURITY_FILE):
        print("\nAdmin security is not configured.")
        return False

    password = getpass.getpass(
        "Enter Developer/Admin Password: "
    )

    if not verify_admin_password(password):
        print("\nIncorrect Admin password.")
        return False

    print("\nAdmin access granted.")
    developer_admin_license_control()
    return True
def developer_admin_license_control():
    while True:
        print("\n" + "=" * 50)
        print("      DEVELOPER / ADMIN LICENSE CONTROL")
        print("=" * 50)

        print("1. View Current License Details")
        print("2. Change License Status")
        print("3. Change License Plan")
        print("4. Change Allowed Stores")
        print("5. Exit Admin License Control")

        admin_choice = input(
            "Select Option (1-5): "
        ).strip()
        if admin_choice == "1":
            display_current_license_details()
            continue

        if admin_choice == "2":
            change_license_status()
            continue

        if admin_choice == "3":
            change_license_plan()
            continue

        if admin_choice == "4":
            change_license_allowed_stores()
            continue

        if admin_choice == "5":
            print("\nExiting Admin License Control.")
            break

        print("Please select a valid option from 1 to 5.")
def get_license_access_status():
    license_record = get_current_license_record()

    if license_record is None:
        return "NO_LICENSE"

    license_status = (
        license_record.get("License Status", "")
        .strip()
        .lower()
    )

    if license_status != "active":
        return "SUSPENDED"

    expiry_text = license_record.get(
        "Expiry Date",
        ""
    ).strip()

    if expiry_text:
        try:
            expiry_date = datetime.strptime(
                expiry_text,
                "%Y-%m-%d"
            ).date()

            if datetime.now().date() > expiry_date:
                return "EXPIRED"

        except ValueError:
            return "INVALID_LICENSE"
    allowed_stores_text = license_record.get(
        "Allowed Stores",
        ""
    ).strip()

    allowed_store_ids = [
        store_id.strip()
        for store_id in allowed_stores_text.split("|")
        if store_id.strip()
    ]

    if CURRENT_STORE_ID not in allowed_store_ids:
        return "STORE_NOT_ALLOWED"
    return "ACTIVE"



def get_license_access_message(status):
    messages = {
        "NO_LICENSE": "No valid license was found.",
        "SUSPENDED": "This license is currently suspended.",
        "EXPIRED": "This license has expired.",
        "INVALID_LICENSE": "The license information is invalid.",
        "STORE_NOT_ALLOWED": (
            "This store / branch is not allowed "
            "under the current license."
        )
    }

    return messages.get(
        status,
        "License access is restricted."
    )


def save_store_profile():
    fieldnames = [
        "Store Name",
        "Store City",
        "Store Address",
        "Store Phone",
        "Store Email",
        "Store Website",
        "Store Logo"
    ]

    profile_data = {
        "Store Name": store_name,
        "Store City": store_city,
        "Store Address": store_address,
        "Store Phone": store_phone,
        "Store Email": store_email,
        "Store Website": store_website,
        "Store Logo": store_logo
    }

    try:
        with open(
            STORE_PROFILE_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as profile_file:
            writer = csv.DictWriter(
                profile_file,
                fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerow(profile_data)

        return True

    except Exception as error:
        print(
            "\nStore Profile could not be saved."
        )
        print("Store Profile Error:", error)
        return False
record_date = datetime.now().strftime("%d-%m-%Y")
record_time = datetime.now().strftime("%I:%M %p")
CUSTOMER_DATA_FILE = "customers.csv"
PAYMENT_DATA_FILE = "payments.csv"
initialize_store_registry()
initialize_license_file()
initialize_license_audit_file()
active_stores = load_store_registry()

if not active_stores:
    print("\nNo active stores found.")
    input("Press Enter to exit...")
    raise SystemExit

print("\n--- Select Store / Branch ---")

for index, store in enumerate(active_stores, start=1):
    print(
        f"{index}. "
        f"{store['Store Name']} - "
        f"{store['Store City']}"
    )

while True:
    store_choice = input(
        f"Select Store / Branch (1-{len(active_stores)}): "
    ).strip()

    if store_choice.isdigit():
        store_index = int(store_choice) - 1

        if 0 <= store_index < len(active_stores):
            selected_store = active_stores[store_index]
            break

    print("Please select a valid Store / Branch number.")

CURRENT_STORE_ID = selected_store["Store ID"]
CURRENT_STORE_NAME = selected_store["Store Name"]
CURRENT_STORE_CITY = selected_store["Store City"]
if CURRENT_STORE_ID == "STORE001":
    STORE_PROFILE_FILE = "store_profile.csv"
else:
    STORE_PROFILE_FILE = (
        f"store_profile_{CURRENT_STORE_ID.lower()}.csv"
    )

if os.path.exists(STORE_PROFILE_FILE):
    load_store_profile()
else:
    save_store_profile()

if not license_record_exists():
    create_initial_license()

license_access_status = get_license_access_status()

print(
    f"\nSelected Store: "
    f"{CURRENT_STORE_NAME} - {CURRENT_STORE_CITY}"
)
print("==================================================")
print("          OPTICAL STORE CUSTOMER MANAGER")
print("==================================================")



print("\n--- Data Mode ---")
print("1. Real / Production Data")
print("2. Demo / Test Data")

while True:
    data_mode = input(
        "Select Data Mode (1/2): "
    ).strip()

    if data_mode == "1":
        if CURRENT_STORE_ID == "STORE001":
            CUSTOMER_DATA_FILE = "customers.csv"
            PAYMENT_DATA_FILE = "payments.csv"
        else:
            CUSTOMER_DATA_FILE = (
                f"customers_{CURRENT_STORE_ID.lower()}.csv"
            )
            PAYMENT_DATA_FILE = (
                f"payments_{CURRENT_STORE_ID.lower()}.csv"
            )
        break
    elif data_mode == "2":
        if CURRENT_STORE_ID == "STORE001":
            CUSTOMER_DATA_FILE = "demo_customers.csv"
            PAYMENT_DATA_FILE = "demo_payments.csv"
        else:
            CUSTOMER_DATA_FILE = (
                f"demo_customers_{CURRENT_STORE_ID.lower()}.csv"
            )
            PAYMENT_DATA_FILE = (
                f"demo_payments_{CURRENT_STORE_ID.lower()}.csv"
            )
        break
    else:
        print("Please select 1 for Real Data or 2 for Demo Data.")

def create_startup_backup():
    backup_folder = "backups"

    try:
        os.makedirs(backup_folder, exist_ok=True)

        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        files_to_backup = [
            CUSTOMER_DATA_FILE,
            PAYMENT_DATA_FILE
        ]

        backed_up_files = []

        for source_file in files_to_backup:
            if not os.path.exists(source_file):
                continue

            file_name, file_extension = os.path.splitext(
                os.path.basename(source_file)
            )

            backup_file = os.path.join(
                backup_folder,
                f"{file_name}_{backup_time}{file_extension}"
            )

            shutil.copy2(
                source_file,
                backup_file
            )

            backed_up_files.append(source_file)

        if backed_up_files:
            print(
                "\nAutomatic data backup completed successfully."
            )
        else:
            print(
                "\nNo existing data files found. "
                "Backup not required yet."
            )

    except Exception as error:
        print(
            "\nWarning: Automatic data backup could not be completed."
        )
        print("Backup Error:", error)


create_startup_backup()


def migrate_customer_csv(file_name):
    if not os.path.exists(file_name):
        return

    with open(
        file_name,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        rows = list(csv.reader(file))

    if not rows:
        return

    changed = False

    if len(rows[0]) == 53:
        rows[0].append("Previous Prescription Date")
        changed = True

    if len(rows[0]) == 54:
        rows[0].append("Prescription Source")
        changed = True

    if len(rows[0]) == 55:
        rows[0].append("Prescription From")
        changed = True

    if len(rows[0]) == 56:
        rows[0].append("C/O / S/O Details")
        changed = True

    if len(rows[0]) == 57:
        rows[0].append("Delivery Status")
        changed = True

    if len(rows[0]) == 58:
        rows[0].append("Delivered To")
        changed = True

    if len(rows[0]) == 59:
        rows[0].append("Receiver Name")
        changed = True
    for row in rows[1:]:
        while len(row) < 60:
            row.append("")
            changed = True

    if not changed:
        return

    with open(
        file_name,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def migrate_payment_csv(file_name):
    if not os.path.exists(file_name):
        return

    with open(
        file_name,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        rows = list(csv.reader(file))

    if not rows:
        return

    changed = False

    if len(rows[0]) == 14:
        rows[0].append("Delivered To")
        changed = True

    if len(rows[0]) == 15:
        rows[0].append("Receiver Name")
        changed = True

    for row in rows[1:]:
        while len(row) < 16:
            row.append("")
            changed = True

    if not changed:
        return

    with open(
        file_name,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerows(rows)
migrate_customer_csv(CUSTOMER_DATA_FILE)
migrate_payment_csv(PAYMENT_DATA_FILE)
# ==================================================
# 2. CUSTOMER / PATIENT DETAILS
# ==================================================

print("\n--- Customer Type ---")
print("1. New Customer")
print("2. Existing Customer")
print("3. Pending Balance Customers")
print("4. Pending Delivery Customers")
print("5. Old Customer / Historical Entry")
print("6. Store Profile / Settings")
print("7. Customer Reports")

while True:
    customer_type = input(
        "Select Customer Type (1/2/3/4/5/6/7): "
    ).strip()
    if customer_type.lower() == "admin":
        open_protected_admin_control()
        continue
    if (
        customer_type == "1"
        and license_access_status != "ACTIVE"
    ):
        print(
            "\n"
            + get_license_access_message(
                license_access_status
            )
        )
        print(
            "New Customer entry is not available "
            "until the license is active."
        )
        continue
    if (
        customer_type == "5"
        and license_access_status != "ACTIVE"
    ):
        print(
            "\n"
            + get_license_access_message(
                license_access_status
            )
        )
        print(
            "Old Customer / Historical Entry is not available "
            "until the license is active."
        )
        continue
    if customer_type in ["1", "2", "3", "4", "5", "6", "7"]:
        break

    print(
        "Please select 1 for New Customer, "
        "2 for Existing Customer, "
        "3 for Pending Balance Customers, "
        "4 for Pending Delivery Customers, "
        "5 for Old Customer / Historical Entry, "
        "6 for Store Profile / Settings, "
        "or 7 for Customer Reports."
    )
# --------------------------------------------------
# PHONE NORMALIZATION HELPER
# --------------------------------------------------

def get_old_prescription_date():
    while True:
        old_prescription_date = input(
            "Enter Old Prescription Date "
            "(DD-MM-YYYY or DD/MM/YYYY): "
        ).strip()

        accepted_formats = (
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d-%m-%y",
            "%d/%m/%y",
        )

        parsed_date = None

        for date_format in accepted_formats:
            try:
                parsed_date = datetime.strptime(
                    old_prescription_date,
                    date_format
                )
                break
            except ValueError:
                continue

        if parsed_date is not None:
            return parsed_date.strftime("%d-%m-%Y")

        print(
            "Invalid date. Examples: "
            "01-01-2025, 1-1-2025, "
            "01/01/2025 or 1/1/25."
        )
def get_old_add_requirement():
    print("\n--- Old Prescription ADD Requirement ---")
    print("1. No ADD")
    print("2. Both Eyes")
    print("3. Right Eye (OD) Only")
    print("4. Left Eye (OS) Only")

    while True:
        old_add_requirement = input(
            "Select ADD Requirement (1/2/3/4): "
        ).strip()

        if old_add_requirement in ("1", "2", "3", "4"):
            return old_add_requirement

        print("Please select 1, 2, 3 or 4.")

def get_old_sph(eye_name):
    while True:
        old_sph = input(
            f"Enter {eye_name} SPH (+/-): "
        ).strip()

        if old_sph.lower() == "plano":
            return "Plano"

        if old_sph == "0":
            return old_sph

        if old_sph.startswith(("+", "-")):
            number_part = old_sph[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 30
            ):
                return old_sph

        print(
            "Invalid SPH. "
            "Enter like -1.00, +1.25, 0 or Plano."
        )

def get_old_cyl(eye_name):
    while True:
        old_cyl = input(
            f"Enter {eye_name} CYL (+/-): "
        ).strip()

        if old_cyl in ("", "0"):
            return old_cyl

        if old_cyl.startswith(("+", "-")):
            number_part = old_cyl[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 10
            ):
                return old_cyl

        print(
            "Invalid CYL. "
            "Enter like -0.50, +1.25, 0 or leave blank."
        )

def get_old_axis(eye_name):
    while True:
        old_axis = input(
            f"Enter {eye_name} AXIS (0-180): "
        ).strip()

        if old_axis == "":
            return old_axis

        if old_axis.isdigit():
            axis_value = int(old_axis)

            if 0 <= axis_value <= 180:
                return old_axis

        print(
            "Invalid AXIS. "
            "Enter a number from 0 to 180 or leave blank."
        )

def get_old_add(eye_name):
    while True:
        old_add = input(
            f"Enter {eye_name} ADD / Near Power (+): "
        ).strip()

        if old_add in ("", "0"):
            print(f"ADD is required for {eye_name}.")
            continue

        if old_add.startswith("+"):
            number_part = old_add[1:]
            parts = number_part.split(".")

            if (
                len(parts) == 2
                and parts[0].isdigit()
                and len(parts[1]) == 2
                and parts[1] in ["00", "25", "50", "75"]
                and float(number_part) <= 5
            ):
                return old_add

        print(
            "Invalid ADD. "
            "Enter like +1.00, +1.25, +1.50 or +2.00."
        )
def get_old_prescription_details():
    print("\n--- Old Prescription Details ---")

    old_prescription_date = get_old_prescription_date()
    old_add_requirement = get_old_add_requirement()

    print("\n--- Old Prescription ---")
    print("\nRight Eye (OD)")

    old_right_sph = get_old_sph("Right Eye")
    old_right_cyl = get_old_cyl("Right Eye")
    old_right_axis = get_old_axis("Right Eye")

    if old_add_requirement in ("1", "4"):
        old_right_add = ""
    else:
        old_right_add = get_old_add("Right Eye")

    print("\nLeft Eye (OS)")

    old_left_sph = get_old_sph("Left Eye")
    old_left_cyl = get_old_cyl("Left Eye")
    old_left_axis = get_old_axis("Left Eye")

    if old_add_requirement in ("1", "3"):
        old_left_add = ""
    else:
        old_left_add = get_old_add("Left Eye")

    return (
        old_prescription_date,
        old_right_sph,
        old_right_cyl,
        old_right_axis,
        old_right_add,
        old_left_sph,
        old_left_cyl,
        old_left_axis,
        old_left_add,
    )
def build_old_prescription_row(
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
    full_address,
    previous_prescription_date,
    prescription_source,
    prescription_from,
    customer_relation,
):
    return [
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
        "",
        "",
        "",
        0.0,
        "",
        "",
        "",
        0.0,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        0.0,
        0.0,
        0.0,
        "",
        full_address,
        0.0,
        0.0,
        "",
        "",
        "",
        "",
        previous_prescription_date,
        prescription_source,
        prescription_from,
        customer_relation,
        "",
        "",
        "",
    ]
# ==================================================
# STORE PROFILE / SETTINGS
# ==================================================

if customer_type == "6":
    print("\n--- Store Profile / Settings ---")

    print("Store Name   :", store_name)
    print("Store City   :", store_city)
    print(
        "Store Address:",
        store_address if store_address else "Not Added"
    )
    print(
        "Store Phone  :",
        store_phone if store_phone else "Not Added"
    )
    print(
        "Store Email  :",
        store_email if store_email else "Not Added"
    )
    print(
        "Store Website:",
        store_website if store_website else "Not Added"
    )
    print(
        "Store Logo   :",
        store_logo if store_logo else "Not Added"
    )

    while True:
        edit_store_profile = input(
            "\nEdit Store Profile? (y/n): "
        ).strip().lower()

        if edit_store_profile in ("y", "n"):
            if (
                edit_store_profile == "y"
                and license_access_status != "ACTIVE"
            ):
                print(
                    "\n"
                    + get_license_access_message(
                        license_access_status
                    )
                )
                print(
                    "Store Profile editing is not available "
                    "until the license is active."
                )
                continue

            break
        print("Please enter y or n.")

    if edit_store_profile == "n":
        print("\nNo changes made to Store Profile.")
        input("\nPress Enter to close...")
        raise SystemExit

    while True:
        new_store_name = input(
            f"Store Name [{store_name}]: "
        ).strip()

        if new_store_name:
            store_name = new_store_name
            break

        if store_name:
            break

        print("Store Name is required.")

    new_store_city = input(
        f"Store City [{store_city}]: "
    ).strip()

    if new_store_city:
        store_city = new_store_city

    current_address_display = (
        store_address if store_address else "Not Added"
    )

    new_store_address = input(
        f"Store Address [{current_address_display}] "
        "(press Enter to keep current): "
    ).strip()

    if new_store_address:
        store_address = new_store_address

    while True:
        current_phone_display = (
            store_phone if store_phone else "Not Added"
        )

        new_store_phone = input(
            f"Store Phone [{current_phone_display}] "
            "(press Enter to keep current): "
        ).strip()

        if not new_store_phone:
            break

        normalized_store_phone = normalize_indian_phone(
            new_store_phone
        )

        if (
            normalized_store_phone.isdigit()
            and len(normalized_store_phone) == 10
            and normalized_store_phone[0] in "6789"
        ):
            store_phone = normalized_store_phone
            break

        print(
            "Please enter a valid 10-digit Indian mobile number."
        )

    current_email_display = (
        store_email if store_email else "Not Added"
    )

    new_store_email = input(
        f"Store Email [{current_email_display}] "
        "(press Enter to keep current): "
    ).strip()

    if new_store_email:
        store_email = new_store_email

    current_website_display = (
        store_website if store_website else "Not Added"
    )

    new_store_website = input(
        f"Store Website [{current_website_display}] "
        "(press Enter to keep current): "
    ).strip()

    if new_store_website:
        store_website = new_store_website

    current_logo_display = (
        store_logo if store_logo else "Not Added"
    )

    new_store_logo = input(
        f"Store Logo Path [{current_logo_display}] "
        "(Optional - press Enter to keep current): "
    ).strip()

    if new_store_logo:
        store_logo = new_store_logo

    print("\n--- Updated Store Profile ---")
    print("Store Name   :", store_name)
    print("Store City   :", store_city)
    print(
        "Store Address:",
        store_address if store_address else "Not Added"
    )
    print(
        "Store Phone  :",
        store_phone if store_phone else "Not Added"
    )
    print(
        "Store Email  :",
        store_email if store_email else "Not Added"
    )
    print(
        "Store Website:",
        store_website if store_website else "Not Added"
    )
    print(
        "Store Logo   :",
        store_logo if store_logo else "Not Added"
    )

    while True:
        confirm_store_profile = input(
            "\nSave these Store Profile details? (y/n): "
        ).strip().lower()

        if confirm_store_profile in ("y", "n"):
            break

        print("Please enter y or n.")

    if confirm_store_profile == "y":
        if save_store_profile():
            update_current_store_registry()
            print("\nStore Profile saved successfully.")
        else:
            print("\nStore Profile was not saved.")
    else:
        load_store_profile()
        print("\nStore Profile changes cancelled.")

    input("\nPress Enter to close...")
    raise SystemExit
# ==================================================
# CUSTOMER REPORTS
# ==================================================

if customer_type == "7":

    print("\n--- Customer Reports ---")
    print("1. Today's Customers")
    print("2. This Month Customers")
    print("3. Date-to-Date Customers")
    print("4. All Customers")

    while True:
        report_choice = input(
            "Select Report (1/2/3/4): "
        ).strip()

        if report_choice in ["1", "2", "3", "4"]:
            break

        print(
            "Please select 1 for Today's Customers, "
            "2 for This Month Customers, "
            "3 for Date-to-Date Customers, "
            "or 4 for All Customers."
        )
    if not os.path.exists(CUSTOMER_DATA_FILE):
        print(
            "\nNo customer data file found for the selected Data Mode."
        )
        input("\nPress Enter to close...")
        raise SystemExit

    with open(
        CUSTOMER_DATA_FILE,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as customer_file:
        customer_reader = csv.reader(customer_file)
        customer_rows = list(customer_reader)

    if len(customer_rows) <= 1:
        print(
            "\nNo customer records found for the selected Data Mode."
        )
        input("\nPress Enter to close...")
        raise SystemExit

    customer_records = customer_rows[1:]
    if report_choice == "1":

        today_date = datetime.now().date()
        report_records = []

        for customer_record in customer_records:

            if not customer_record:
                continue

            try:
                record_datetime = datetime.strptime(
                    customer_record[0].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except (ValueError, IndexError):
                continue

            if record_datetime.date() == today_date:
                report_records.append(customer_record)

        report_title = "Today's Customers"
    elif report_choice == "2":

        current_date = datetime.now()
        report_records = []

        for customer_record in customer_records:

            if not customer_record:
                continue

            try:
                record_datetime = datetime.strptime(
                    customer_record[0].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except (ValueError, IndexError):
                continue

            if (
                record_datetime.month == current_date.month
                and record_datetime.year == current_date.year
            ):
                report_records.append(customer_record)

        report_title = "This Month Customers"
    elif report_choice == "3":

        while True:
            from_date_input = input(
                "Enter From Date (DD-MM-YYYY): "
            ).strip()

            try:
                from_date = datetime.strptime(
                    from_date_input,
                    "%d-%m-%Y"
                ).date()
                break
            except ValueError:
                print(
                    "Invalid From Date. "
                    "Please use DD-MM-YYYY format."
                )

        while True:
            to_date_input = input(
                "Enter To Date (DD-MM-YYYY): "
            ).strip()

            try:
                to_date = datetime.strptime(
                    to_date_input,
                    "%d-%m-%Y"
                ).date()
            except ValueError:
                print(
                    "Invalid To Date. "
                    "Please use DD-MM-YYYY format."
                )
                continue

            if to_date < from_date:
                print(
                    "To Date cannot be earlier than From Date."
                )
                continue

            break

        report_records = []

        for customer_record in customer_records:

            if not customer_record:
                continue

            try:
                record_datetime = datetime.strptime(
                    customer_record[0].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except (ValueError, IndexError):
                continue

            if (
                from_date
                <= record_datetime.date()
                <= to_date
            ):
                report_records.append(customer_record)

        report_title = (
            "Customers from "
            f"{from_date.strftime('%d-%m-%Y')} "
            "to "
            f"{to_date.strftime('%d-%m-%Y')}"
        )
    elif report_choice == "4":

        report_records = customer_records.copy()
        report_title = "All Customers"        
    print("\n==================================================")
    print(f"          {report_title.upper()}")
    print("==================================================")

    if not report_records:
        print("\nNo customer records found for this report.")
        input("\nPress Enter to close...")
        raise SystemExit

    print(f"\nTotal Records: {len(report_records)}")

    for record_number, customer_record in enumerate(
        report_records,
        start=1
    ):
        frame_details = (
            customer_record[20].strip()
            if len(customer_record) > 20
            else ""
        )

        lens_type = (
            customer_record[24].strip()
            if len(customer_record) > 24
            else ""
        )

        if frame_details and lens_type:
            report_order_type = "Frame + Lenses"
        elif frame_details:
            report_order_type = "Frame Only"
        elif lens_type:
            report_order_type = "Lenses Only"
        else:
            report_order_type = "Prescription Only / Historical"

        print("\n----------------------------------------")
        print(f"Record No.    : {record_number}")
        print(f"Date / Time   : {customer_record[0]}")
        print(f"Customer Name : {customer_record[5]}")
        print(
            "Phone         :",
            customer_record[8]
            if customer_record[8].strip()
            else "No Phone"
        )
        print(f"Town / Village: {customer_record[9]}")
        print(f"Order Type    : {report_order_type}")
        print(f"Total Amount  : ₹{customer_record[42]}")
        print(f"Balance       : ₹{customer_record[44]}")

    print("\n==================================================")
    print(f"Total Records: {len(report_records)}")
    print("==================================================")

    input("\nPress Enter to close...")
    raise SystemExit
# ==================================================
# PENDING BALANCE CUST OMERS
# ==================================================

if customer_type == "3":

    print("\n--- Pending Balance Customers ---")

    latest_payment_orders = {}

    with open(
        PAYMENT_DATA_FILE,
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

        delivery_status = (
            payment_row[12].strip().lower()
            if len(payment_row) > 12
            else ""
        )

        if remaining_balance > 0:
            pending_balance_orders.append(
                payment_row
            )

    if not pending_balance_orders:

        print(
            "No pending payment or delivery orders found."
        )

        raise SystemExit

    pending_balance_orders.sort(
        key=lambda row: row[4],
        reverse=True
    )
    print("\n--- Pending Balance View ---")
    print("1. Search Customer")
    print("2. View All Pending Balance Customers")

    while True:
        pending_view_choice = input(
            "Select Option (1/2): "
        ).strip()

        if pending_view_choice in ("1", "2"):
            break

        print("Please select 1 or 2.")
    while True:

        if pending_view_choice == "2":
            matched_pending_orders = pending_balance_orders.copy()
            break

        pending_search = input(
            "\nEnter Customer Name / Phone / Town-Village: "
        ).strip()
        pending_search = input(
            "\nEnter Customer Name / Phone / Town-Village: "
        ).strip()

        if not pending_search:
            print(
                "Please enter Customer Name, Phone, "
                "or Town / Village."
            )
            continue

        search_text = pending_search.lower()
        search_phone = normalize_indian_phone(
            pending_search
        )

        matched_pending_orders = []

        for payment_row in pending_balance_orders:
            customer_name_match = (
                search_text
                in payment_row[1].strip().lower()
            )

            phone_match = (
                search_phone
                and search_phone
                in normalize_indian_phone(
                    payment_row[2]
                )
            )

            town_match = (
                search_text
                in payment_row[3].strip().lower()
            )

            if (
                customer_name_match
                or phone_match
                or town_match
            ):
                matched_pending_orders.append(
                    payment_row
                )

        if matched_pending_orders:
            pending_balance_orders = (
                matched_pending_orders
            )
            break

        print(
            "No pending payment / delivery "
            "records found for this search."
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
            "   Town / Village:",
            payment_row[3]
            if payment_row[3].strip()
            else "Not Provided"
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
    if pending_view_choice == "2":
        total_pending_balance_amount = sum(
            float(row[9])
            for row in matched_pending_orders
        )

        print("\n--- Pending Balance Summary ---")
        print(
            f"Total Pending Balance Orders: "
            f"{len(matched_pending_orders)}"
        )
        print(
            f"Total Pending Balance Amount: "
            f"₹{total_pending_balance_amount:.2f}"
        )

    while True:
        pending_choice_input = input(
            "\nSelect Pending Order Number (0 to Exit): "
        ).strip()

        if not pending_choice_input.isdigit():
            print(
                "Please enter a valid order number."
            )
            continue

        pending_choice = int(
            pending_choice_input
        )

        if pending_choice == 0:
            print("Pending Balance Customers closed.")
            raise SystemExit
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

    print("\n--- Pending Balance Action ---")
    print("1. Record Payment / Delivery Update")
    print("2. WhatsApp - Balance Payment Request")
    print("3. WhatsApp - Balance + Spectacles Collection Request")
    print("4. View Only / Close")

    while True:
        pending_action = input(
            "Select Action (1/2/3/4): "
        ).strip()

        if pending_action in ["1", "2", "3", "4"]:
            if (
                pending_action == "1"
                and license_access_status != "ACTIVE"
            ):
                print(
                    "\n"
                    + get_license_access_message(
                        license_access_status
                    )
                )
                print(
                    "Payment / Delivery Update is not available "
                    "until the license is active."
                )
                continue

            break
        print("Please select 1, 2, 3, or 4.")

    if pending_action == "4":
        raise SystemExit

    if pending_action in ["2", "3"]:

        pending_request_phone = normalize_indian_phone(
            selected_pending_order[2]
        )

        if not pending_request_phone:
            print(
                "WhatsApp Request cannot be sent - "
                "Customer phone number is not available."
            )
            raise SystemExit

        if pending_action == "2":

            request_message = f"""
{store_name}

Dear {selected_pending_order[1]},

This is a friendly reminder regarding your pending balance.

Order Type: {selected_pending_order[5]}
Order Date / Time: {selected_pending_order[4]}
Pending Balance: ₹{current_balance:.2f}

Kindly make the pending payment at your convenience.

Thank you,
{store_name}
"""

        else:

            if (
                len(selected_pending_order) > 12
                and selected_pending_order[12].strip().lower()
                == "delivered"
            ):
                print(
                    "This order is already marked as Delivered. "
                    "Use Balance Payment Request instead."
                )
                raise SystemExit

            request_message = f"""
{store_name}

Dear {selected_pending_order[1]},

Your spectacles/order are ready for collection.

Order Type: {selected_pending_order[5]}
Order Date / Time: {selected_pending_order[4]}
Pending Balance: ₹{current_balance:.2f}

Kindly collect your spectacles/order and complete the pending payment.

Thank you,
{store_name}
"""

        whatsapp_message = urllib.parse.quote(
            request_message
        )

        whatsapp_url = (
            f"https://wa.me/91{pending_request_phone}"
            f"?text={whatsapp_message}"
        )

        webbrowser.open(whatsapp_url)

        print("Opening WhatsApp Request Message...")

        raise SystemExit
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

    delivered_to = ""
    receiver_name = ""

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

            print("\n--- Delivered To / Received By ---")
            print("1. Customer / Same Person")
            print("2. Other Person")

            while True:
                delivered_to_choice = input(
                    "Select Delivered To (1/2): "
                ).strip()

                if delivered_to_choice == "1":
                    delivered_to = "Customer / Same Person"
                    receiver_name = selected_pending_order[1]
                    break

                if delivered_to_choice == "2":
                    delivered_to = "Other Person"
                    receiver_name = input(
                        "Receiver Name "
                        "(Optional - press Enter to skip): "
                    ).strip()
                    break

                print("Please select 1 or 2.")

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
        PAYMENT_DATA_FILE,
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
            ),
            delivered_to,
            receiver_name
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
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

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
# ==================================================
# PENDING DELIVERY CUSTOMERS
# ==================================================

if customer_type == "4":

    print("\n--- Pending Delivery Customers ---")

    latest_delivery_orders = {}

    with open(
        PAYMENT_DATA_FILE,
        "r",
        encoding="utf-8"
    ) as payment_file:

        payment_reader = csv.reader(payment_file)
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

            latest_delivery_orders[order_key] = payment_row

    pending_delivery_orders = []

    for payment_row in latest_delivery_orders.values():

        delivery_status = (
            payment_row[12].strip().lower()
            if len(payment_row) > 12
            else ""
        )

        if delivery_status != "delivered":
            pending_delivery_orders.append(
                payment_row
            )

    if not pending_delivery_orders:

        print("No pending delivery customers found.")
        raise SystemExit

    pending_delivery_orders.sort(
        key=lambda row: row[4],
        reverse=True
    )
    print("\n--- Pending Delivery View ---")
    print("1. Search Customer")
    print("2. View All Pending Delivery Customers")

    while True:
        delivery_view_choice = input(
            "Select Option (1/2): "
        ).strip()

        if delivery_view_choice in ("1", "2"):
            break

        print("Please select 1 or 2.")

    while True:
        if delivery_view_choice == "2":
            matched_delivery_orders = pending_delivery_orders.copy()
            break
        delivery_search = input(
            "\nEnter Customer Name / Phone / Town-Village: "
        ).strip()

        if not delivery_search:
            print(
                "Please enter Customer Name, Phone, "
                "or Town / Village."
            )
            continue

        search_text = delivery_search.lower()
        search_phone = normalize_indian_phone(
            delivery_search
        )

        matched_delivery_orders = []

        for payment_row in pending_delivery_orders:

            name_match = (
                search_text
                in payment_row[1].strip().lower()
            )

            phone_match = (
                search_phone
                and search_phone
                in normalize_indian_phone(
                    payment_row[2]
                )
            )

            town_match = (
                search_text
                in payment_row[3].strip().lower()
            )

            if name_match or phone_match or town_match:
                matched_delivery_orders.append(
                    payment_row
                )

        if matched_delivery_orders:
            pending_delivery_orders = (
                matched_delivery_orders
            )
            break

        print(
            "No pending delivery records "
            "found for this search."
        )

    for number, payment_row in enumerate(
        pending_delivery_orders,
        start=1
    ):

        try:
            total_value = float(payment_row[6])
            balance_value = float(payment_row[9])
        except ValueError:
            total_value = 0.0
            balance_value = 0.0

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
            "   Town / Village:",
            payment_row[3]
            if payment_row[3].strip()
            else "Not Provided"
        )

        print(
            f"   Order: {payment_row[5]} | "
            f"Date: {payment_row[4]}"
        )

        print(
            f"   Total: ₹{total_value:.2f} | "
            f"Balance: ₹{balance_value:.2f}"
        )

        print(
            f"   Payment: {payment_row[11]} | "
            f"Delivery: {payment_row[12]}"
        )

    if delivery_view_choice == "2":
        print("\n--- Pending Delivery Summary ---")
        print(
            f"Total Pending Delivery Orders: "
            f"{len(pending_delivery_orders)}"
        )

    while True:
        delivery_choice_input = input(
            "\nSelect Pending Delivery Order Number (0 to Exit): "
        ).strip()

        if not delivery_choice_input.isdigit():
            print(
                "Please enter a valid order number."
            )
            continue

        delivery_choice = int(
            delivery_choice_input
        )

        if delivery_choice == 0:
            print("Pending Delivery Customers closed.")
            raise SystemExit
        if (
            1
            <= delivery_choice
            <= len(pending_delivery_orders)
        ):
            break

        print(
            "Please select an order number "
            "from the list."
        )
    selected_delivery_order = (
        pending_delivery_orders[
         delivery_choice - 1
        ]
    )

    print("\n--- Selected Delivery Order ---")
    print(
        "Customer:",
        selected_delivery_order[1]
    )
    print(
        "Phone:",
        selected_delivery_order[2]
        if selected_delivery_order[2].strip()
        else "No Phone"
    )
    print(
        "Town / Village:",
        selected_delivery_order[3]
        if selected_delivery_order[3].strip()
        else "Not Provided"
    )
    print(
        "Order:",
        selected_delivery_order[5]
    )
    print(
        "Order Date / Time:",
        selected_delivery_order[4]
    )
    print(
        "Balance Due: ₹"
        f"{float(selected_delivery_order[9]):.2f}"
    )
    print(
        "Payment Status:",
        selected_delivery_order[11]
    )
    print(
        "Delivery Status:",
        selected_delivery_order[12]
    )

    print("\n--- Pending Delivery Action ---")
    print("1. Mark / Update as Delivered")
    print("2. WhatsApp - Spectacles Ready / Please Collect")
    print("3. WhatsApp - Balance + Spectacles Collection Request")
    print("4. View Only / Close")

    while True:
        delivery_action = input(
            "Select Action (1/2/3/4): "
        ).strip()

        if delivery_action in ["1", "2", "3", "4"]:
            if (
                delivery_action == "1"
                and license_access_status != "ACTIVE"
            ):
                print(
                    "\n"
                    + get_license_access_message(
                        license_access_status
                    )
                )
                print(
                    "Payment / Delivery Update is not available "
                    "until the license is active."
                )
                continue

            break
        print("Please select 1, 2, 3, or 4.")

    if delivery_action == "4":
        raise SystemExit

    if delivery_action == "1":

        current_balance = float(
            selected_delivery_order[9]
        )

        total_amount_value = float(
            selected_delivery_order[6]
        )

        previous_paid = (
            total_amount_value - current_balance
        )

        print("\n--- Payment at Delivery ---")
        print(
            f"Total Amount      : ₹{total_amount_value:.2f}"
        )
        print(
            f"Already Paid      : ₹{previous_paid:.2f}"
        )
        print(
            f"Current Balance   : ₹{current_balance:.2f}"
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
                        "than the Current Balance."
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

        if new_balance == 0:
            payment_status = "Paid"
        else:
            payment_status = "Pending"

        print(
            f"\nPaid Now          : ₹{amount_paid_now:.2f}"
        )
        print(
            f"Remaining Balance : ₹{new_balance:.2f}"
        )
        print(
            f"Payment Status    : {payment_status}"
        )

        print("\n--- Delivery Status ---")
        print("1. Delivered")
        print("2. Pending")

        while True:
            delivery_status_choice = input(
                "Select Delivery Status (1/2): "
            ).strip()

            if delivery_status_choice == "1":
                delivery_status = "Delivered"
                break

            if delivery_status_choice == "2":
                delivery_status = "Pending"
                break

            print("Please select 1 or 2.")

        delivered_to = ""
        receiver_name = ""

        if delivery_status == "Delivered":

            print("\n--- Delivered To / Received By ---")
            print("1. Customer / Same Person")
            print("2. Other Person")

            while True:
                delivered_to_choice = input(
                    "Select Delivered To (1/2): "
                ).strip()

                if delivered_to_choice == "1":
                    delivered_to = (
                        "Customer / Same Person"
                    )
                    receiver_name = (
                        selected_delivery_order[1]
                    )
                    break

                if delivered_to_choice == "2":
                    delivered_to = "Other Person"
                    receiver_name = input(
                        "Receiver Name "
                        "(Optional - press Enter to skip): "
                    ).strip()
                    break

                print("Please select 1 or 2.")

        delivery_update_datetime = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        if amount_paid_now == 0:
            payment_type = "Delivery Update"
        elif new_balance == 0:
            payment_type = "Balance Payment"
        else:
            payment_type = "Part Payment"

        with open(
            PAYMENT_DATA_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as payment_file:

            payment_writer = csv.writer(
                payment_file
            )

            payment_writer.writerow([
                delivery_update_datetime,
                selected_delivery_order[1],
                selected_delivery_order[2],
                selected_delivery_order[3],
                selected_delivery_order[4],
                selected_delivery_order[5],
                total_amount_value,
                previous_paid,
                amount_paid_now,
                new_balance,
                payment_type,
                payment_status,
                delivery_status,
                (
                    delivery_update_datetime
                    if delivery_status == "Delivered"
                    else ""
                ),
                delivered_to,
                receiver_name
            ])

        print("\n--- Payment / Delivery Update Completed ---")
        print(
            f"Previously Paid   : ₹{previous_paid:.2f}"
        )
        print(
            f"Paid Now          : ₹{amount_paid_now:.2f}"
        )
        print(
            f"Remaining Balance : ₹{new_balance:.2f}"
        )
        print(
            f"Payment Status    : {payment_status}"
        )
        print(
            f"Delivery Status   : {delivery_status}"
        )

        if delivery_status == "Delivered":
            print(
                "Delivered To      :",
                delivered_to
            )

            if receiver_name:
                print(
                    "Receiver Name     :",
                    receiver_name
                )

        raise SystemExit
    delivery_request_phone = normalize_indian_phone(
        selected_delivery_order[2]
    )

    if not delivery_request_phone:
        print(
            "WhatsApp Request cannot be sent - "
            "Customer phone number is not available."
        )
        raise SystemExit

    delivery_balance = float(
        selected_delivery_order[9]
    )

    if delivery_action == "2":

        request_message = f"""
{store_name}

Dear {selected_delivery_order[1]},

Your spectacles/order are ready for collection.

Order Type: {selected_delivery_order[5]}
Order Date / Time: {selected_delivery_order[4]}

Kindly collect your spectacles/order at your convenience.

Thank you,
{store_name}
"""

    else:

        if delivery_balance <= 0:
            print(
                "There is no pending balance for this order. "
                "Please use Spectacles Ready / Please Collect."
            )
            raise SystemExit

        request_message = f"""
{store_name}

Dear {selected_delivery_order[1]},

Your spectacles/order are ready for collection.

Order Type: {selected_delivery_order[5]}
Order Date / Time: {selected_delivery_order[4]}
Pending Balance: ₹{delivery_balance:.2f}

Kindly collect your spectacles/order and complete the pending payment.

Thank you,
{store_name}
"""

    whatsapp_message = urllib.parse.quote(
        request_message
    )

    whatsapp_url = (
        f"https://wa.me/91{delivery_request_phone}"
        f"?text={whatsapp_message}"
    )

    webbrowser.open(whatsapp_url)

    print("Opening WhatsApp Request Message...")

    raise SystemExit
# --------------------------------------------------
# EXISTING CUSTOMER SEARCH
# --------------------------------------------------

if customer_type == "2":

    # --------------------------------------------------
    # EXISTING CUSTOMER SEARCH
    # Search by Name OR Phone OR Town/Village
    # --------------------------------------------------

    while True:

        while True:
            search_value = input(
                "Enter Customer Name / Phone / Town-Village: "
            ).strip()

            if not search_value:
                print(
                    "Please enter Customer Name, Phone Number "
                    "or Town/Village."
                )
                continue

            phone_candidate = (
                search_value
                .replace("+", "")
                .replace(" ", "")
                .replace("-", "")
            )

            searching_by_phone = phone_candidate.isdigit()

            if searching_by_phone:
                search_phone = normalize_indian_phone(
                    search_value
                )

                if not (
                    search_phone.isdigit()
                    and len(search_phone) == 10
                    and search_phone[0] in ["6", "7", "8", "9"]
                ):
                    print(
                        "Invalid phone number. Please enter a valid "
                        "Indian 10-digit mobile number."
                    )
                    continue
            else:
                search_phone = ""

            break

        search_text = search_value.lower()

        matching_customers = []

        with open(
            CUSTOMER_DATA_FILE,
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

                row_town = row[9].strip().lower()

                if searching_by_phone:

                    if row_phone == search_phone:
                        matching_customers.append(
                            row
                        )

                else:

                    if (
                        search_text in row_name
                        or search_text in row_town
                    ):
                        matching_customers.append(
                            row
                        )

        # --------------------------------------------------
        # NO CUSTOMER FOUND
        # --------------------------------------------------

        if not matching_customers:

            print("\nCustomer not found.")

            while True:
                search_again = input(
                    "Search again? (y/n): "
                ).strip().lower()

                if search_again == "y":
                    break

                if search_again == "n":
                    print(
                        "Existing Customer search cancelled."
                    )
                    raise SystemExit

                print(
                    "Please enter y for Yes or n for No."
                )

            # Return to main Existing Customer search prompt
            continue

        # Keep complete matching history before
        # duplicate customer results are removed.
        customer_history_rows = (
            matching_customers.copy()
        )

        # --------------------------------------------------
        # REMOVE DUPLICATE CUSTOMER RESULTS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # CUSTOMER SELECTION / OPTIONAL REFINE SEARCH
        # --------------------------------------------------

        selected_customer = None

        while len(matching_customers) > 1:

            print(
                f"\nMatching Customers: "
                f"{len(matching_customers)}"
            )

            for number, customer in enumerate(
                matching_customers,
                start=1
            ):

                display_phone = (
                    customer[8].strip()
                    if customer[8].strip()
                    else "No Phone"
                )

                display_town = (
                    customer[9].strip()
                    if customer[9].strip()
                    else "No Town/Village"
                )

                print(
                    f"{number}. "
                    f"{customer[5]} | "
                    f"{display_phone} | "
                    f"{display_town}"
                )

            print(
                "\n--- Select / Refine Customer ---"
            )

            selection_value = input(
                "Enter Customer Number / Name / Phone: "
            ).strip()

            if not selection_value:
                print(
                    "Please enter Customer Number, "
                    "Name or Phone."
                )
                continue

            # ----------------------------------------------
            # DIRECT CUSTOMER NUMBER SELECTION
            # ----------------------------------------------

            if selection_value.isdigit():

                selection_number = int(
                    selection_value
                )

                if (
                    1
                    <= selection_number
                    <= len(matching_customers)
                ):
                    selected_customer = (
                        matching_customers[
                            selection_number - 1
                        ]
                    )
                    break

            # ----------------------------------------------
            # PHONE REFINE
            # ----------------------------------------------

            phone_candidate = (
                selection_value
                .replace("+", "")
                .replace(" ", "")
                .replace("-", "")
            )

            refined_customers = []

            if phone_candidate.isdigit():

                refine_phone = (
                    normalize_indian_phone(
                        selection_value
                    )
                )

                if not (
                    refine_phone.isdigit()
                    and len(refine_phone) == 10
                    and refine_phone[0]
                    in ["6", "7", "8", "9"]
                ):
                    print(
                        "Please enter a valid displayed "
                        "Customer Number or valid Phone Number."
                    )
                    continue

                for customer in matching_customers:

                    customer_phone = (
                        normalize_indian_phone(
                            customer[8]
                        )
                    )

                    if customer_phone == refine_phone:
                        refined_customers.append(
                            customer
                        )

            # ----------------------------------------------
            # NAME REFINE
            # ----------------------------------------------

            else:

                refine_name = (
                    selection_value
                    .strip()
                    .lower()
                )

                for customer in matching_customers:

                    customer_name_for_refine = (
                        customer[5]
                        .strip()
                        .lower()
                    )

                    if (
                        refine_name
                        in customer_name_for_refine
                    ):
                        refined_customers.append(
                            customer
                        )

            if not refined_customers:

                print(
                    "No matching customers found "
                    "for that Name / Phone."
                )
                continue

            matching_customers = (
                refined_customers
            )

        # --------------------------------------------------
        # ONE CUSTOMER REMAINS AFTER SEARCH / REFINE
        # --------------------------------------------------

        if selected_customer is None:

            if len(matching_customers) == 1:
                selected_customer = (
                    matching_customers[0]
                )
        # --------------------------------------------------
        # CUSTOMER CONFIRMATION
        # --------------------------------------------------

        customer_name = (
            selected_customer[5]
        )

        phone = (
            selected_customer[8]
        )

        display_phone = (
            phone.strip()
            if phone.strip()
            else "No Phone"
        )

        display_town = (
            selected_customer[9].strip()
            if selected_customer[9].strip()
            else "No Town/Village"
        )

        print(
            "\nSelected Customer:"
        )

        print(
            f"Name: {customer_name} | "
            f"Phone: {display_phone} | "
            f"Town/Village: {display_town}"
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

                break

            else:

                print(
                    "Please enter y for Yes or n for No."
                )

        # Correct customer confirmed:
        # leave the main search loop.
        if confirm == "y":
            break

        # confirm == "n":
        # return to search instead of closing app.
        print(
            "Please search for the customer again."
        )
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

            try:
                selected_customer[53] = datetime.strptime(
                    history_row[0],
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d-%m-%Y")
            except ValueError:
                selected_customer[53] = history_row[0]

            break

        if any(
            value.strip()
            for value in history_row[12:20]
        ):
            selected_customer[12:20] = history_row[12:20]

            if (
                len(history_row) > 53
                and history_row[53].strip()
            ):
                selected_customer[53] = history_row[53]
            else:
                selected_customer[53] = history_row[0]

            break

# ==================================================
# CUSTOMER DETAILS
# ==================================================

if customer_type == "5":
    print("\n--- Old Prescription Entry ---")

    print("\n--- Old Prescription Source ---")
    print("1. Our Shop Testing")
    print("2. External Doctor / Hospital Prescription")

    while True:
        old_prescription_source = input(
            "Select Prescription Source (1/2): "
        ).strip()

        if old_prescription_source in ("1", "2"):
            break

        print("Please select 1 or 2.")
    if old_prescription_source == "2":
        old_prescription_from = input(
            "Prescription From "
            "(Optional - Hospital / Doctor / Optical Shop): "
        ).strip()
    else:
        old_prescription_from = ""
    print("\n--- Old Customer / Historical Entry ---")
    old_customer_type = "1"

print(
    "\n--- Customer Details ---"
)

# --------------------------------------------------
# CUSTOMER NAME
# --------------------------------------------------

if customer_type == "1" or (
    customer_type == "5"
    and old_customer_type == "1"
):
    while True:

        customer_name = input(
            "Enter Customer Name: "
        ).strip().title()

        if (
            customer_name
            and all(
                char.isalnum()
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
            "Letters and numbers are allowed."
        )

else:

    customer_name = (
        selected_customer[5]
    )


if customer_type == "1":
    customer_relation = input(
        "C/O / S/O Details (Optional - press Enter to skip): "
    ).strip()
elif customer_type == "2":
    customer_relation = (
        selected_customer[56]
        if len(selected_customer) > 56
        else ""
    )
else:
    customer_relation = ""
# --------------------------------------------------
# GENDER
# --------------------------------------------------

if customer_type == "1" or (
    customer_type == "5"
    and old_customer_type == "1"
):

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

if customer_type == "1" or (
    customer_type == "5"
    and old_customer_type == "1"
):

    while True:

        age_input = input(
            "Enter Patient Age "
            "(Optional - press Enter if unknown): "
        ).strip()

        if age_input == "":
            age = ""
            break

        if age_input.isdigit() and int(age_input) > 0:
            age = int(age_input)
            break

        print(
            "Please enter age using numbers only "
            "or leave blank."
        )

else:

    saved_age = selected_customer[7].strip()

    if saved_age.isdigit():

        saved_year_text = (
            selected_customer[0].strip()[:4]
        )

        if saved_year_text.isdigit():

            from datetime import datetime

            saved_year = int(saved_year_text)
            current_year = datetime.now().year

            years_passed = max(
                current_year - saved_year,
                0
            )

            age = int(saved_age) + years_passed

        else:
            age = int(saved_age)

    else:
        age = ""
# --------------------------------------------------
# PHONE NUMBER
# --------------------------------------------------

if customer_type == "1" or (
    customer_type == "5"
    and old_customer_type == "1"
):

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

if customer_type == "1" or (
    customer_type == "5"
    and old_customer_type == "1"
):

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
                or char.isdigit()
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
previous_prescription_date = ""

previous_right_sph = ""
previous_right_cyl = ""
previous_right_axis = ""
previous_right_add = ""

previous_left_sph = ""
previous_left_cyl = ""
previous_left_axis = ""
previous_left_add = ""




if customer_type == "5":
    (
        old_prescription_date,
        old_right_sph,
        old_right_cyl,
        old_right_axis,
        old_right_add,
        old_left_sph,
        old_left_cyl,
        old_left_axis,
        old_left_add,
    ) = get_old_prescription_details()
    previous_prescription_date = old_prescription_date

    previous_right_sph = old_right_sph
    previous_right_cyl = old_right_cyl
    previous_right_axis = old_right_axis
    previous_right_add = old_right_add

    previous_left_sph = old_left_sph
    previous_left_cyl = old_left_cyl
    previous_left_axis = old_left_axis
    previous_left_add = old_left_add

    spectacle_history = "Historical"

    if old_prescription_source == "1":
        prescription_source = "In-Store Refraction"
    else:
        prescription_source = "External Prescription"

    prescription_from = old_prescription_from
    print("\n--- Old Prescription Summary ---")
    print(f"Customer Name: {customer_name}")
    print(f"Old Prescription Date: {previous_prescription_date}")
    print(f"Prescription Source: {prescription_source}")

    if prescription_from:
        print(f"Prescription From: {prescription_from}")

    print(
        "OD:",
        previous_right_sph,
        previous_right_cyl,
        previous_right_axis,
        previous_right_add if previous_right_add else "ADD Not Required"
    )

    print(
        "OS:",
        previous_left_sph,
        previous_left_cyl,
        previous_left_axis,
        previous_left_add if previous_left_add else "ADD Not Required"
    )
    frame_details = ""
    frame_brand = ""
    frame_offer = ""
    frame_price = 0.0

    lens_type = ""
    lens_brand = ""
    lens_offer = ""
    lens_price = 0.0

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

    lens_features = ""

    order_total = 0.0
    less_amount = 0.0
    total_amount = 0.0
    advance_amount = 0.0
    balance = 0.0
    eye_surgery = ""
    surgery_eye = ""
    right_iol = ""
    left_iol = ""

    delivery_status = ""
    delivered_to = ""
    receiver_name = ""
    old_prescription_row = build_old_prescription_row(
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
        full_address,
        previous_prescription_date,
        prescription_source,
        prescription_from,
        customer_relation,
    )
    print("Old Prescription Row Columns:", len(old_prescription_row))
    print("\n--- Old Prescription Order Details ---")
    print("1. Prescription Only")
    print("2. Frame Only")
    print("3. Lenses Only")
    print("4. Frame + Lenses")

    while True:
        old_order_type = input(
            "Select Old Order Type (1/2/3/4): "
        ).strip()

        if old_order_type in ("1", "2", "3", "4"):
            break

        print("Please select 1, 2, 3 or 4.")
    if old_order_type == "1":
        with open(
            CUSTOMER_DATA_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(old_prescription_row)

        print(
            "\nOld Prescription saved successfully."
        )
        print("\n--- Send Old Prescription ---")
        print("1. SMS Text / Copy")
        print("2. WhatsApp Prescription")
        print("3. Save Only / Skip Sending")
        while True:
            old_message_choice = input(
                "Select Message Option (1/2/3): "
            ).strip()

            if old_message_choice in ("1", "2", "3"):
                break

            print("Please select 1, 2 or 3.")
        old_prescription_message = f"""
{store_name}
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

PRESCRIPTION DETAILS

Customer Name: {customer_name}
Prescription Date: {previous_prescription_date}
Prescription Source: {"Ravi Opticals Eye Testing" if prescription_source == "In-Store Refraction" else prescription_source}
{f"Prescription From: {prescription_from}" if prescription_from else ""}

Right Eye (OD):
SPH: {previous_right_sph}
CYL: {previous_right_cyl if previous_right_cyl else "0"}
AXIS: {previous_right_axis if previous_right_axis else "Not Required"}
ADD: {previous_right_add if previous_right_add else "Not Required"}

Left Eye (OS):
SPH: {previous_left_sph}
CYL: {previous_left_cyl if previous_left_cyl else "0"}
AXIS: {previous_left_axis if previous_left_axis else "Not Required"}
ADD: {previous_left_add if previous_left_add else "Not Required"}

Please keep this prescription for your reference.
"""

        if old_message_choice == "1":
            if not phone:
                print(
                    "SMS Text cannot be prepared - "
                    "Customer phone number is not available."
                )
            else:
                print("\n--- SMS TEXT / COPY ---")
                print(old_prescription_message)
        if old_message_choice == "2":
            if not phone:
                print(
                    "WhatsApp Prescription cannot be sent - "
                    "Customer phone number is not available."
                )
            else:
                import urllib.parse
                import webbrowser

                whatsapp_message = urllib.parse.quote(
                    old_prescription_message
                )
                whatsapp_url = (
                    f"https://wa.me/91{phone}"
                    f"?text={whatsapp_message}"
                )

                webbrowser.open(whatsapp_url)
                print("Opening WhatsApp Old Prescription...")
        print("\nOld Prescription Entry completed.")
        raise SystemExit
# ==================================================
# 6. FRAME DETAILS
# ==================================================

if customer_type == "5":
    order_type = "7"

if customer_type != "5":

    print("\n--- Order Type ---")
    print("1. Frame Only")
    print("2. Lenses Only")
    print("3. Frame + Lenses")

    if customer_type == "2":
        print("4. Previous Prescription")
        print("5. Old Order History")
        print("6. Payment / Delivery Update")
        print("7. Add Old Prescription")
if customer_type != "5":
    while True:
        if customer_type == "2":
            order_type = input(
                "Select Order Type (1/2/3/4/5/6/7): "
            ).strip()
            valid_options = ["1", "2", "3", "4", "5", "6", "7"]
        else:
            order_type = input(
                "Select Order Type (1/2/3): "
            ).strip()
            valid_options = ["1", "2", "3"]

        if order_type in valid_options:
            if (
                customer_type == "2"
                and order_type in ["1", "2", "3", "6", "7"]
                and license_access_status != "ACTIVE"
            ):
                print(
                    "\n"
                    + get_license_access_message(
                        license_access_status
                    )
                )
                print(
                    "This Existing Customer action is not available "
                    "until the license is active."
                )
                continue

            break
        print("Please select a valid Order Type.")
if customer_type == "2" and order_type == "7":
    print("\n--- Old Prescription Entry ---")

    print("\n--- Old Prescription Source ---")
    print("1. Our Shop Testing")
    print("2. External Doctor / Hospital Prescription")

    while True:
        old_prescription_source = input(
            "Select Prescription Source (1/2): "
        ).strip()

        if old_prescription_source in ("1", "2"):
            break

        print("Please select 1 or 2.")

    if old_prescription_source == "2":
        old_prescription_from = input(
            "Prescription From "
            "(Optional - Hospital / Doctor / Optical Shop): "
        ).strip()
    else:
        old_prescription_from = ""
    (
        old_prescription_date,
        old_right_sph,
        old_right_cyl,
        old_right_axis,
        old_right_add,
        old_left_sph,
        old_left_cyl,
        old_left_axis,
        old_left_add,
    ) = get_old_prescription_details()
    previous_prescription_date = old_prescription_date

    previous_right_sph = old_right_sph
    previous_right_cyl = old_right_cyl
    previous_right_axis = old_right_axis
    previous_right_add = old_right_add

    previous_left_sph = old_left_sph
    previous_left_cyl = old_left_cyl
    previous_left_axis = old_left_axis
    previous_left_add = old_left_add

    spectacle_history = "Historical"

    if old_prescription_source == "1":
        prescription_source = "In-Store Refraction"
    else:
        prescription_source = "External Prescription"

    prescription_from = old_prescription_from
    old_prescription_row = build_old_prescription_row(
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
        full_address,
        previous_prescription_date,
        prescription_source,
        prescription_from,
        customer_relation,
    )
    print("\n--- Old Prescription Order Details ---")
    print("1. Prescription Only")
    print("2. Frame Only")
    print("3. Lenses Only")
    print("4. Frame + Lenses")

    while True:
        old_order_type = input(
            "Select Old Order Type (1/2/3/4): "
        ).strip()

        if old_order_type in ("1", "2", "3", "4"):
            break

        print("Please select 1, 2, 3 or 4.")
    if old_order_type == "1":
        with open(
            CUSTOMER_DATA_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(old_prescription_row)

        print(
            "\nOld Prescription saved successfully."
        )
        print("\n--- Old Prescription Actions ---")
        print("1. SMS Text / Copy")
        print("2. WhatsApp Prescription")
        print("3. Save Only / Skip Sending")

        while True:
            old_message_choice = input(
                "Select Action (1/2/3): "
            ).strip()

            if old_message_choice in ("1", "2", "3"):
                break

            print("Please select 1, 2 or 3.")

        old_prescription_message = f"""
{store_name}
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

PRESCRIPTION DETAILS

Customer Name: {customer_name}
Prescription Date: {previous_prescription_date}
Prescription Source: {"Ravi Opticals Eye Testing" if prescription_source == "In-Store Refraction" else prescription_source}
{f"Prescription From: {prescription_from}" if prescription_from else ""}

Right Eye (OD):
SPH: {previous_right_sph}
CYL: {previous_right_cyl if previous_right_cyl else "0"}
AXIS: {previous_right_axis if previous_right_axis else "Not Required"}
ADD: {previous_right_add if previous_right_add else "Not Required"}

Left Eye (OS):
SPH: {previous_left_sph}
CYL: {previous_left_cyl if previous_left_cyl else "0"}
AXIS: {previous_left_axis if previous_left_axis else "Not Required"}
ADD: {previous_left_add if previous_left_add else "Not Required"}

Please keep this prescription for your reference.
"""

        if old_message_choice == "1":
            if not phone:
                print(
                    "SMS Text cannot be prepared - "
                    "Customer phone number is not available."
                )
            else:
                print("\n--- SMS TEXT / COPY ---")
                print(old_prescription_message)

        elif old_message_choice == "2":
            if not phone:
                print(
                    "WhatsApp Prescription cannot be sent - "
                    "Customer phone number is not available."
                )
            else:
                whatsapp_message = urllib.parse.quote(
                    old_prescription_message
                )

                whatsapp_url = (
                    f"https://wa.me/91{phone}"
                    f"?text={whatsapp_message}"
                )

                webbrowser.open(whatsapp_url)

                print(
                    "Opening WhatsApp Old Prescription..."
                )

        else:
            print(
                "Old Prescription saved. "
                "Sending skipped."
            )

        print(
            "\nOld Prescription Entry completed."
        )

        raise SystemExit
if "old_order_type" in globals() and old_order_type == "2":
    print("\n--- Historical Frame Details ---")

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
    frame_offer = normalize_offer(
        input("Enter Frame Offer (Example: 10 or 10%): ")
    )
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
    old_prescription_row[20] = frame_details
    old_prescription_row[21] = frame_brand
    old_prescription_row[22] = frame_offer
    old_prescription_row[23] = frame_price
    with open(
        CUSTOMER_DATA_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(old_prescription_row)

    print(
        "\nHistorical Frame Only record saved successfully."
    )
    raise SystemExit
if "old_order_type" in globals() and old_order_type == "3":
    print("\n--- Historical Lens Details ---")

    print("\n--- Lens Type ---")
    print("1. Single Vision")
    print("2. Bifocal")

    while True:
        lens_type_choice = input(
            "Select Lens Type (1/2): "
        ).strip()

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
                        "Invalid option. "
                        "Please select 1, 2, 3 or 4."
                    )

            break

        else:
            print(
                "Invalid option. Please select 1 or 2."
            )
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
    lens_offer = normalize_offer(
        input("Enter Lens Offer (Example: 10 or 10%): ")
    )
    while True:
        lens_price_input = input(
            "Enter Lens Price: "
        ).strip()

        try:
            lens_price = float(lens_price_input)

            if lens_price < 0:
                print("Lens Price cannot be negative.")
                continue

            break

        except ValueError:
            print(
                "Please enter Lens Price using numbers only."
            )
    old_prescription_row[24] = lens_type
    old_prescription_row[25] = lens_brand
    old_prescription_row[26] = lens_offer
    old_prescription_row[27] = lens_price
    old_prescription_row[45] = lens_features
    with open(
        CUSTOMER_DATA_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(old_prescription_row)

    print(
        "\nHistorical Lenses Only record saved successfully."
    )
    raise SystemExit

    print("\n--- Historical Frame Details ---")

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
    frame_offer = normalize_offer(
        input("Enter Frame Offer (Example: 10 or 10%): ")
    )
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

    old_prescription_row[20] = frame_details
    old_prescription_row[21] = frame_brand
    old_prescription_row[22] = frame_offer
    old_prescription_row[23] = frame_price
    print("\n--- Historical Lens Details ---")

    print("\n--- Lens Type ---")
    print("1. Single Vision")
    print("2. Bifocal")

    while True:
        lens_type_choice = input(
            "Select Lens Type (1/2): "
        ).strip()

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
                        "Invalid option. "
                        "Please select 1, 2, 3 or 4."
                    )

            break

        else:
            print(
                "Invalid option. Please select 1 or 2."
            )
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

    lens_offer = normalize_offer(
        input("Enter Lens Offer (Example: 10 or 10%): ")
    )
    while True:
        lens_price_input = input(
            "Enter Lens Price: "
        ).strip()

        try:
            lens_price = float(lens_price_input)

            if lens_price < 0:
                print("Lens Price cannot be negative.")
                continue

            break

        except ValueError:
            print(
                "Please enter Lens Price using numbers only."
            )

    old_prescription_row[24] = lens_type
    old_prescription_row[25] = lens_brand
    old_prescription_row[26] = lens_offer
    old_prescription_row[27] = lens_price
    old_prescription_row[45] = lens_features
    with open(
        CUSTOMER_DATA_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(old_prescription_row)

    print(
        "\nHistorical Frame + Lenses record saved successfully."
    )
    raise SystemExit
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
        CUSTOMER_DATA_FILE,
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
            ) or any(
                value.strip()
                for value in customer[12:20]
            )
            if same_customer and has_prescription:
                if (
                    latest_prescription is None
                    or customer[0] > latest_prescription[0]
                ):
                    latest_prescription = customer

    print("\n--- Previous Prescription ---")

    if latest_prescription is not None:
        has_current_prescription = any(
            value.strip()
            for value in latest_prescription[28:36]
        )

        if has_current_prescription:
            try:
                display_prescription_date = datetime.strptime(
                    latest_prescription[0],
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d-%m-%Y")
            except ValueError:
                display_prescription_date = latest_prescription[0]

            right_sph = latest_prescription[28]
            right_cyl = latest_prescription[29]
            right_axis = latest_prescription[30]
            right_add = latest_prescription[31]

            left_sph = latest_prescription[32]
            left_cyl = latest_prescription[33]
            left_axis = latest_prescription[34]
            left_add = latest_prescription[35]

        else:
            if (
                len(latest_prescription) > 53
                and latest_prescription[53].strip()
            ):
                display_prescription_date = latest_prescription[53]
            else:
                try:
                    display_prescription_date = datetime.strptime(
                        latest_prescription[0],
                        "%Y-%m-%d %H:%M:%S"
                    ).strftime("%d-%m-%Y")
                except ValueError:
                    display_prescription_date = latest_prescription[0]

            right_sph = latest_prescription[12]
            right_cyl = latest_prescription[13]
            right_axis = latest_prescription[14]
            right_add = latest_prescription[15]

            left_sph = latest_prescription[16]
            left_cyl = latest_prescription[17]
            left_axis = latest_prescription[18]
            left_add = latest_prescription[19]

        print(
            "Previous Prescription Date:",
            display_prescription_date
        )

        print("OD:")
        print(
            f"SPH: {right_sph} | "
            f"CYL: {right_cyl if right_cyl else '0'} | "
            f"AXIS: {right_axis if right_axis else 'Not Required'} | "
            f"ADD: {right_add}"
        )

        print("OS:")
        print(
            f"SPH: {left_sph} | "
            f"CYL: {left_cyl if left_cyl else '0'} | "
            f"AXIS: {left_axis if left_axis else 'Not Required'} | "
            f"ADD: {left_add}"        )
    else:
        print("No previous prescription found.")
    previous_prescription_action = ""

    if latest_prescription is not None:

        previous_prescription_text = f"""{store_name}
Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}
Previous Prescription Date: {display_prescription_date}

Spectacle Prescription

Right Eye (OD):
SPH: {right_sph}
CYL: {right_cyl}
AXIS: {right_axis if right_axis else "Not Required"}
ADD: {right_add if right_add else "Not Required"}

Left Eye (OS):
SPH: {left_sph}
CYL: {left_cyl}
AXIS: {left_axis if left_axis else "Not Required"}
ADD: {left_add if left_add else "Not Required"}

Please keep this prescription for your reference.
"""

        while True:
            print("\n--- What would you like to do? ---")
            print("1. Use Same Prescription")
            print("2. New In-Store Refraction")
            print("3. Send Previous Prescription on WhatsApp")
            print("4. Print Previous Prescription")
            print("5. View Only / Close")

            previous_action_choice = input(
                "Select Option (1/2/3/4/5): "
            ).strip()

            if (
                previous_action_choice in ["1", "2"]
                and license_access_status != "ACTIVE"
            ):
                print(
                    "\n"
                    + get_license_access_message(
                        license_access_status
                    )
                )
                print(
                    "Creating a new order from the previous "
                    "prescription is not available until "
                    "the license is active."
                )
                continue

            if previous_action_choice == "1":
                previous_prescription_action = "use_same"

                print("\n--- New Order ---")
                print("1. Lenses Only")
                print("2. Frame + Lenses")

                while True:
                    new_order_choice = input(
                        "Select New Order (1/2): "
                    ).strip()

                    if new_order_choice == "1":
                        order_type = "2"
                        break

                    elif new_order_choice == "2":
                        order_type = "3"
                        break

                    else:
                        print("Please select 1 or 2.")

                break

            elif previous_action_choice == "2":
                previous_prescription_action = "new_refraction"

                print("\n--- New Order ---")
                print("1. Lenses Only")
                print("2. Frame + Lenses")

                while True:
                    new_order_choice = input(
                        "Select New Order (1/2): "
                    ).strip()

                    if new_order_choice == "1":
                        order_type = "2"
                        break

                    elif new_order_choice == "2":
                        order_type = "3"
                        break

                    else:
                        print("Please select 1 or 2.")

                break

            elif previous_action_choice == "3":
                if not phone:
                    print(
                        "WhatsApp Prescription cannot be sent - "
                        "Customer phone number is not available."
                    )
                else:
                    whatsapp_message = urllib.parse.quote(
                        previous_prescription_text
                    )
                    whatsapp_url = (
                        f"https://wa.me/91{phone}"
                        f"?text={whatsapp_message}"
                    )
                    webbrowser.open(whatsapp_url)
                    print(
                        "Opening WhatsApp Previous Prescription..."
                    )

            elif previous_action_choice == "4":
                print_text_document(
                    previous_prescription_text
                )

            elif previous_action_choice == "5":
                raise SystemExit

            else:
                print("Please select 1, 2, 3, 4, or 5.")

    else:
        input("\nPress Enter to close...")
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
        CUSTOMER_DATA_FILE,
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
    if selected_order[24].strip() and len(selected_order) > 49 and selected_order[49].strip():
        print("--- Eye Surgery / IOL History ---")
        print("Eye Surgery :", selected_order[49])

        if selected_order[49].strip() == "Yes":

            if len(selected_order) > 50 and selected_order[50].strip():
                print("Surgery Eye :", selected_order[50])

            if len(selected_order) > 51 and selected_order[51].strip():
                print("Right Eye IOL :", selected_order[51])

            if len(selected_order) > 52 and selected_order[52].strip():
                print("Left Eye IOL  :", selected_order[52])

    latest_payment_update = None

    if os.path.exists(PAYMENT_DATA_FILE):
        with open(
            PAYMENT_DATA_FILE,
            "r",
            encoding="utf-8"
        ) as payment_file:

            payment_reader = csv.reader(payment_file)
            next(payment_reader, None)

            for payment_row in payment_reader:
                if len(payment_row) < 14:
                    continue

                same_order = (
                    payment_row[4].strip()
                    == selected_order[0].strip()
                )

                same_customer = (
                    payment_row[1].strip().lower()
                    == selected_order[5].strip().lower()
                )

                if same_order and same_customer:
                    latest_payment_update = payment_row
    print("--- Payment / Delivery Details ---")

    if len(selected_order) > 47 and selected_order[47].strip():
        print("Order Total      : ₹", selected_order[47])

    if (
        len(selected_order) > 48
        and selected_order[48].strip()
        and selected_order[48].strip() not in ["0", "0.0"]
    ):
        print("Less Amount      : ₹", selected_order[48])

    if selected_order[42].strip():
        print("Final Total      : ₹", selected_order[42])

    if latest_payment_update is not None:
        try:
            latest_total = float(latest_payment_update[6])
            latest_balance = float(latest_payment_update[9])
            total_paid = latest_total - latest_balance
        except ValueError:
            latest_total = 0.0
            latest_balance = 0.0
            total_paid = 0.0

        latest_payment_status = (
            latest_payment_update[11].strip()
            if len(latest_payment_update) > 11
            else ""
        )

        latest_delivery_status = (
            latest_payment_update[12].strip()
            if len(latest_payment_update) > 12
            else ""
        )

        print(f"Total Paid       : ₹{total_paid:.2f}")
        print(f"Balance Due      : ₹{latest_balance:.2f}")
        print(
            "Payment Status   :",
            latest_payment_status
            if latest_payment_status
            else "Not Recorded"
        )
        print(
            "Delivery Status  :",
            latest_delivery_status
            if latest_delivery_status
            else "Not Recorded"
        )

        if latest_delivery_status == "Delivered":
            if latest_balance == 0:
                print(
                    "Delivery Condition: "
                    "Delivered / Fully Paid"
                )
            else:
                print(
                    "Delivery Condition: "
                    f"Delivered with Due Balance ₹{latest_balance:.2f}"
                )

        elif latest_delivery_status == "Pending":
            print("Delivery Condition: Pending Delivery")

    else:
        if selected_order[43].strip():
            print("Advance Amount   : ₹", selected_order[43])

        if selected_order[44].strip():
            print("Balance Due      : ₹", selected_order[44])

        print("Payment Status   : Not Updated")

        if len(selected_order) > 57 and selected_order[57].strip():
            print(
                "Delivery Status  :",
                selected_order[57]
            )
        else:
            print("Delivery Status  : Not Recorded")
    # --------------------------------------------------
    # SEND OLD PRESCRIPTION ON WHATSAPP
    # --------------------------------------------------

    old_prescription_available = (
        selected_order[24].strip()
        and any(
            selected_order[index].strip()
            for index in range(28, 36)
        )
    )

    if old_prescription_available:

        while True:
            resend_choice = input(
                "\nSend this old prescription on WhatsApp? (y/n): "
            ).strip().lower()

            if resend_choice in ["y", "yes", "n", "no"]:
                break

            print("Please enter y for Yes or n for No.")

        if resend_choice in ["y", "yes"]:

            if not phone:
                print(
                    "WhatsApp Prescription cannot be sent - "
                    "Customer phone number is not available."
                )

            else:
                import urllib.parse
                import webbrowser

                if (
                    len(selected_order) > 53
                    and selected_order[53].strip()
                ):
                    old_prescription_date = selected_order[53]

                    old_right_sph = selected_order[12]
                    old_right_cyl = selected_order[13]
                    old_right_axis = selected_order[14]
                    old_right_add = selected_order[15]

                    old_left_sph = selected_order[16]
                    old_left_cyl = selected_order[17]
                    old_left_axis = selected_order[18]
                    old_left_add = selected_order[19]

                else:
                    old_prescription_date = selected_order[0]

                    old_right_sph = selected_order[28]
                    old_right_cyl = selected_order[29]
                    old_right_axis = selected_order[30]
                    old_right_add = selected_order[31]

                    old_left_sph = selected_order[32]
                    old_left_cyl = selected_order[33]
                    old_left_axis = selected_order[34]
                    old_left_add = selected_order[35]

                old_prescription_message = f"""
{store_name}
Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}
Old Prescription Date: {old_prescription_date}

Spectacle Prescription

Right Eye (OD):
SPH: {old_right_sph}
CYL: {old_right_cyl}
AXIS: {old_right_axis}
ADD: {old_right_add if old_right_add else "Not Required"}

Left Eye (OS):
SPH: {old_left_sph}
CYL: {old_left_cyl}
AXIS: {old_left_axis}
ADD: {old_left_add if old_left_add else "Not Required"}

Please keep this prescription for your reference.
"""
                whatsapp_message = urllib.parse.quote(
                    old_prescription_message
                )

                whatsapp_url = (
                    f"https://wa.me/91{phone}"
                    f"?text={whatsapp_message}"
                )

                webbrowser.open(whatsapp_url)

                print(
                    "Opening WhatsApp Old Prescription..."
                )
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
        PAYMENT_DATA_FILE,
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
        PAYMENT_DATA_FILE,
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
            ),
            (
                selected_payment[14]
                if len(selected_payment) > 14
                else ""
            ),
            (
                selected_payment[15]
                if len(selected_payment) > 15
                else ""
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
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

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
    print("\n--- Frame Details ---")

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

    frame_offer = normalize_offer(
        input("Enter Frame Offer (Example: 10 or 10%): ")
    )
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
# 4. PRESCRIPTION SOURCE
# ==================================================

if customer_type == "5":
    if old_prescription_source == "1":
        prescription_source = "In-Store Refraction"
    else:
        prescription_source = "External Prescription"

        prescription_from = old_prescription_from
else:
    prescription_source = "Not Applicable"
    prescription_from = ""
if (
    order_type in ["2", "3"]
    and "previous_prescription_action" in globals()
    and previous_prescription_action == "use_same"
):
    prescription_source = "Existing Prescription on Record"

elif (
    order_type in ["2", "3"]
    and "previous_prescription_action" in globals()
    and previous_prescription_action == "new_refraction"
):
    prescription_source = "In-Store Refraction"

elif order_type in ["2", "3"]:

    print("\n--- Prescription Source ---")
    print("1. In-Store Refraction")
    print("2. External Prescription")

    if customer_type == "2":
        print("3. Existing Prescription on Record")

    while True:
        if customer_type == "2":
            prescription_source_choice = input(
                "Select Prescription Source (1/2/3): "
            ).strip()
        else:
            prescription_source_choice = input(
                "Select Prescription Source (1/2): "
            ).strip()
            if prescription_source_choice == "1":
                prescription_source = "In-Store Refraction"
                break

            elif prescription_source_choice == "2":
                prescription_source = "External Prescription"

                prescription_from = input(
                    "Prescription From "
                    "(Optional - Hospital / Doctor / Optical Shop): "
                ).strip()

                break

            elif prescription_source_choice == "3":

                if customer_type == "2":
                    prescription_source = (
                        "Existing Prescription on Record"
                    )
                    break

                else:
                    print(
                        "Existing Prescription on Record is "
                        "available only for Existing Customers."
                    )

            else:
                print("Please select 1, 2, or 3.")

order_purpose = "Not Applicable"

if prescription_source == "Existing Prescription on Record":

    print("\n--- Order Purpose ---")
    print("1. Regular / New Order")
    print("2. Replacement - Lost / Broken / Damaged")
    print("3. Additional / Spare Pair")

    while True:
        order_purpose_choice = input(
            "Select Order Purpose (1/2/3): "
        ).strip()

        if order_purpose_choice == "1":
            order_purpose = "Regular / New Order"
            break

        elif order_purpose_choice == "2":
            order_purpose = (
                "Replacement - Lost / Broken / Damaged"
            )
            break

        elif order_purpose_choice == "3":
            order_purpose = "Additional / Spare Pair"
            break

        else:
            print("Please select 1, 2, or 3.")
prescription_choice = "Not Applicable"

if "previous_prescription_action" in globals():
    if previous_prescription_action == "use_same":
        prescription_choice = "Use Previous Prescription"

    elif previous_prescription_action == "new_refraction":
        prescription_choice = "New In-Store Refraction"

if (
    prescription_source == "Existing Prescription on Record"
    and prescription_choice == "Not Applicable"
):
    print("\n--- Prescription Choice ---")
    print("1. Use Previous Prescription")
    print("2. New In-Store Refraction")

    while True:
        prescription_choice_input = input(
            "Select Prescription Choice (1/2): "
        ).strip()

        if prescription_choice_input == "1":
            prescription_choice = "Use Previous Prescription"
            previous_prescription_action = "use_same"
            break

        elif prescription_choice_input == "2":
            prescription_choice = "New In-Store Refraction"
            prescription_source = "In-Store Refraction"
            break

        else:
            print("Please select 1 or 2.")
# ==================================================
# 7. LENS TYPE
# ==================================================

if (
    order_type in ["2", "3"]
    and not (
        "previous_prescription_action" in globals()
        and previous_prescription_action == "use_same"
    )
):
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

elif (
    order_type in ["2", "3"]
    and "previous_prescription_action" in globals()
    and previous_prescription_action == "use_same"
):
    if (
        "latest_prescription" in globals()
        and latest_prescription is not None
        and len(latest_prescription) > 24
    ):
        lens_type = latest_prescription[24]

    elif customer_type == "2" and len(selected_customer) > 24:
        lens_type = selected_customer[24]

    else:
        lens_type = ""
    add_requirement = ""

    print(
        "Previous Lens Type loaded:",
        lens_type if lens_type else "Not Recorded"
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


if customer_type == "2" and order_type in ["2", "3"]:
    spectacle_history = "Existing"

    years_using_glasses = selected_customer[11]

    previous_prescription_date = (
        selected_customer[53]
        if len(selected_customer) > 53
        else ""
    )

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

    if previous_prescription_date:
        print(
            "Previous Prescription Date:",
            previous_prescription_date
        )

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

    print("\n--- Spectacle History ---")

    print("1. First-time Spectacle User")
    print("2. Existing Spectacle User")

    while True:
        spectacle_history_choice = input(
            "Select Spectacle History (1/2): "
        ).strip()

        if spectacle_history_choice == "1":
            spectacle_history = "First-time"
            break

        elif spectacle_history_choice == "2":
            spectacle_history = "Existing"
            break

        else:
            print("Please select 1 or 2.")
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
            while True:
                previous_prescription_date = input(
                    "Enter Previous Prescription Date "
                    "(DD-MM-YYYY, Optional - press Enter if unknown): "
                ).strip()

                if previous_prescription_date == "":
                    break

                try:
                    from datetime import datetime

                    datetime.strptime(
                        previous_prescription_date,
                        "%d-%m-%Y"
                    )
                    break

                except ValueError:
                    print(
                        "Invalid date. Please enter date as "
                        "DD-MM-YYYY or leave blank."
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
# 7. EYE SURGERY / IOL HISTORY
# ==================================================

eye_surgery = "No"
surgery_eye = ""
right_iol = "No"
left_iol = "No"

if (
    order_type in ["2", "3"]
    and not (
        "previous_prescription_action" in globals()
        and previous_prescription_action == "use_same"
    )
):

    print("\n--- Eye Surgery / IOL History ---")
    print("1. No Eye Surgery")
    print("2. Right Eye (OD)")
    print("3. Left Eye (OS)")
    print("4. Both Eyes")

    while True:
        surgery_choice = input(
            "Select Eye Surgery Status (1/2/3/4): "
        ).strip()

        if surgery_choice == "1":
            eye_surgery = "No"
            surgery_eye = ""
            break

        elif surgery_choice == "2":
            eye_surgery = "Yes"
            surgery_eye = "Right Eye (OD)"

            while True:
                right_iol_input = input(
                    "Right Eye IOL implanted? (y/n): "
                ).strip().lower()

                if right_iol_input in ["y", "yes"]:
                    right_iol = "Yes"
                    break

                elif right_iol_input in ["n", "no"]:
                    right_iol = "No"
                    break

                else:
                    print(
                        "Please enter y for Yes or n for No."
                    )

            break

        elif surgery_choice == "3":
            eye_surgery = "Yes"
            surgery_eye = "Left Eye (OS)"

            while True:
                left_iol_input = input(
                    "Left Eye IOL implanted? (y/n): "
                ).strip().lower()

                if left_iol_input in ["y", "yes"]:
                    left_iol = "Yes"
                    break

                elif left_iol_input in ["n", "no"]:
                    left_iol = "No"
                    break

                else:
                    print(
                        "Please enter y for Yes or n for No."
                    )

            break

        elif surgery_choice == "4":
            eye_surgery = "Yes"
            surgery_eye = "Both Eyes"

            while True:
                right_iol_input = input(
                    "Right Eye IOL implanted? (y/n): "
                ).strip().lower()

                if right_iol_input in ["y", "yes"]:
                    right_iol = "Yes"
                    break

                elif right_iol_input in ["n", "no"]:
                    right_iol = "No"
                    break

                else:
                    print(
                        "Please enter y for Yes or n for No."
                    )

            while True:
                left_iol_input = input(
                    "Left Eye IOL implanted? (y/n): "
                ).strip().lower()

                if left_iol_input in ["y", "yes"]:
                    left_iol = "Yes"
                    break

                elif left_iol_input in ["n", "no"]:
                    left_iol = "No"
                    break

                else:
                    print(
                        "Please enter y for Yes or n for No."
                    )

            break

        else:
            print("Please select 1, 2, 3 or 4.")
# ==================================================
# 8. CURRENT PRESCRIPTION
# ==================================================

if (
    order_type in ["2", "3"]
    and prescription_source == "Existing Prescription on Record"
):
    right_sph = previous_right_sph
    right_cyl = previous_right_cyl
    right_axis = previous_right_axis
    right_add = previous_right_add

    left_sph = previous_left_sph
    left_cyl = previous_left_cyl
    left_axis = previous_left_axis
    left_add = previous_left_add

    print("\n--- Current Prescription ---")
    print(
        "Existing prescription on record "
        "loaded automatically."
    )

elif order_type in ["2", "3"]:
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
distance_pd = ""
near_pd = ""
right_va = ""
left_va = ""
right_pinhole = ""
left_pinhole = ""
if order_type in ["2", "3"]:
    if not (
        "previous_prescription_action" in globals()
        and previous_prescription_action == "use_same"
    ):
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

    lens_offer = normalize_offer(
        input("Enter Lens Offer (Example: 10 or 10%): ")
    )
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
delivery_status = ""
delivered_to = ""
receiver_name = ""

print("\n--- Delivery Status ---")
print("1. Delivered")
print("2. Pending")

while True:
    delivery_choice = input(
        "Select Delivery Status (1/2): "
    ).strip()

    if delivery_choice == "1":
        delivery_status = "Delivered"

        print("\n--- Delivered To / Received By ---")
        print("1. Customer / Same Person")
        print("2. Other Person")

        while True:
            delivered_to_choice = input(
                "Select Delivered To (1/2): "
            ).strip()

            if delivered_to_choice == "1":
                delivered_to = "Customer / Same Person"
                receiver_name = ""
                break

            elif delivered_to_choice == "2":
                delivered_to = "Other Person"
                receiver_name = input(
                    "Enter Receiver Name "
                    "(Optional - press Enter to skip): "
                ).strip()
                break

            else:
                print("Please select 1 or 2.")

        break

    elif delivery_choice == "2":
        delivery_status = "Pending"
        delivered_to = ""
        receiver_name = ""
        break

    else:
        print("Please select 1 or 2.")
# ==================================================
# FINAL REVIEW BEFORE SAVE
# ==================================================
if customer_type in ["1", "2"] and order_type == "1":

    while True:

        # Always recalculate payment values
        order_total = frame_price + lens_price
        total_amount = order_total - less_amount
        balance = total_amount - advance_amount

        print("\n")
        print("==================================================")
        print("              FINAL REVIEW BEFORE SAVE")
        print("==================================================")

        print("\n--- ORDER ---")
        print("Order Type : Frame Only")

        print("\n1. Customer Details")
        print(
            f"   Name         : {customer_name}"
        )
        print(
            f"   C/O / S/O    : "
            f"{customer_relation if customer_relation else 'Not Provided'}"
        )
        print(
            f"   Gender       : {gender}"
        )
        print(
            f"   Age          : "
            f"{age if age != '' else 'Not Provided'}"
        )
        print(
            f"   Phone        : "
            f"{phone if phone else 'Not Provided'}"
        )
        print(
            f"   Town/Village : {address}"
        )
        print(
            f"   Full Address : "
            f"{full_address if full_address else 'Not Provided'}"
        )

        print("\n2. Frame Details")
        print(
            f"   Frame Details : "
            f"{frame_details if frame_details else 'Not Provided'}"
        )
        print(
            f"   Category      : "
            f"{'Brand' if frame_category == '1' else 'Non-Brand'}"
        )
        print(
            f"   Frame Brand   : {frame_brand}"
        )
        print(
            f"   Frame Offer   : "
            f"{frame_offer if frame_offer else 'None'}"
        )
        print(
            f"   Frame Price   : ₹{frame_price:.2f}"
        )

        print("\n3. Payment Details")
        print(
            f"   Order Total    : ₹{order_total:.2f}"
        )
        print(
            f"   Less Amount    : ₹{less_amount:.2f}"
        )
        print(
            f"   Final Total    : ₹{total_amount:.2f}"
        )
        print(
            f"   Advance Amount : ₹{advance_amount:.2f}"
        )
        print(
            f"   Balance        : ₹{balance:.2f}"
        )

        print("\n4. Delivery Details")
        print(
            f"   Delivery Status : {delivery_status}"
        )

        if delivery_status == "Delivered":
            print(
                f"   Delivered To    : {delivered_to}"
            )

            if (
                delivered_to == "Other Person"
                and receiver_name
            ):
                print(
                    f"   Receiver Name   : {receiver_name}"
                )

        print("\n--------------------------------------------------")
        print("--- Review / Edit Options ---")
        print("1. Customer Details")
        print("2. Frame Details")
        print("3. Payment Details")
        print("4. Delivery Details")
        print("5. Confirm & Save")
        print("6. Cancel / Exit Without Saving")
        print("--------------------------------------------------")
        review_choice = input(
            "Select Section / Action (1/2/3/4/5/6): "
        ).strip()

        if review_choice == "5":
            break

        if review_choice == "6":
            print(
                "\nOrder cancelled. "
                "No customer/order data was saved."
            )
            raise SystemExit

        if review_choice == "1":

            while True:

                print("\n--- Edit Customer Details ---")
                print("1. Customer Name")
                print("2. C/O / S/O Details")
                print("3. Gender")
                print("4. Age")
                print("5. Phone")
                print("6. Town / Village")
                print("7. Full Address")
                print("8. Back")

                customer_edit_choice = input(
                    "Select Field (1/2/3/4/5/6/7/8): "
                ).strip()

                if customer_edit_choice == "8":
                    break

                if customer_edit_choice not in [
                    "1", "2", "3", "4",
                    "5", "6", "7"
                ]:
                    print(
                        "Please select a number from 1 to 8."
                    )
                    continue

                if customer_edit_choice == "1":

                    while True:

                        new_customer_name = input(
                            "Enter Customer Name: "
                        ).strip().title()

                        if (
                            new_customer_name
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", "'", "-"]
                                for char in new_customer_name
                            )
                        ):
                            customer_name = new_customer_name
                            print(
                                "Customer Name updated successfully."
                            )
                            break

                        print(
                            "Invalid customer name. "
                            "Letters and numbers are allowed."
                        )

                    continue

                if customer_edit_choice == "2":

                    customer_relation = input(
                        "Enter C/O / S/O Details "
                        "(Optional - press Enter to clear): "
                    ).strip()

                    print(
                        "C/O / S/O Details updated successfully."
                    )

                    continue

                if customer_edit_choice == "3":

                    print("\n--- Gender ---")
                    print("1. Male")
                    print("2. Female")

                    while True:

                        new_gender_choice = input(
                            "Select Gender (1/2): "
                        ).strip()

                        if new_gender_choice == "1":
                            gender = "Male"
                            break

                        if new_gender_choice == "2":
                            gender = "Female"
                            break

                        print(
                            "Please select 1 for Male "
                            "or 2 for Female."
                        )

                    print(
                        "Gender updated successfully."
                    )

                    continue

                if customer_edit_choice == "4":

                    while True:

                        new_age_input = input(
                            "Enter Patient Age "
                            "(Optional - press Enter if unknown): "
                        ).strip()

                        if new_age_input == "":
                            age = ""
                            break

                        if (
                            new_age_input.isdigit()
                            and int(new_age_input) > 0
                        ):
                            age = int(new_age_input)
                            break

                        print(
                            "Please enter age using "
                            "numbers only."
                        )

                    print(
                        "Age updated successfully."
                    )

                    continue

                if customer_edit_choice == "5":

                    while True:

                        raw_phone = input(
                            "Enter Customer Phone Number "
                            "(Optional - press Enter if unavailable): "
                        ).strip()

                        if raw_phone == "":
                            phone = ""
                            break

                        normalized_phone = normalize_indian_phone(
                            raw_phone
                        )

                        if (
                            len(normalized_phone) == 10
                            and normalized_phone.isdigit()
                            and normalized_phone[0] in "6789"
                        ):
                            phone = normalized_phone
                            break

                        print(
                            "Invalid phone number. "
                            "Enter a valid Indian mobile number."
                        )

                    print(
                        "Phone updated successfully."
                    )

                    continue

                if customer_edit_choice == "6":

                    while True:

                        new_address = input(
                            "Enter Town / Village (Required): "
                        ).strip().title()

                        if (
                            new_address
                            and any(
                                char.isalpha()
                                for char in new_address
                            )
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", ",", "-", "'"]
                                for char in new_address
                            )
                        ):
                            address = new_address
                            break

                        print(
                            "Invalid Town / Village. "
                            "Letters and numbers are allowed."
                        )

                    print(
                        "Town / Village updated successfully."
                    )

                    continue

                if customer_edit_choice == "7":

                    full_address = input(
                        "Enter Full Address "
                        "(Optional - press Enter to clear): "
                    ).strip().title()

                    print(
                        "Full Address updated successfully."
                    )

                    continue

                print(
                    "Please select a number from 1 to 8."
                )
            continue

        if review_choice == "2":
            while True:

                print("\n--- Edit Frame Details ---")
                print("1. Frame Details")
                print("2. Frame Category")

                if frame_category == "1":
                    print("3. Frame Brand")
                    print("4. Frame Offer")
                    print("5. Frame Price")
                    print("6. Back")
                else:
                    print("3. Frame Offer")
                    print("4. Frame Price")
                    print("5. Back")

                frame_edit_choice = input(
                    "Select Field / Back: "
                ).strip()

                if (
                    frame_category == "1"
                    and frame_edit_choice == "6"
                ):
                    break

                if (
                    frame_category == "2"
                    and frame_edit_choice == "5"
                ):
                    break

                if frame_edit_choice == "1":

                    frame_details = input(
                        "Enter Frame Details: "
                    ).strip()

                    print(
                        "Frame Details updated successfully."
                    )

                    continue

                if frame_edit_choice == "2":

                    print("\n--- Frame Category ---")
                    print("1. Brand")
                    print("2. Non-Brand")

                    while True:

                        new_frame_category = input(
                            "Select Frame Category (1/2): "
                        ).strip()

                        if new_frame_category == "1":
                            frame_category = "1"

                            frame_brand = input(
                                "Enter Frame Brand: "
                            ).strip()

                            break

                        if new_frame_category == "2":
                            frame_category = "2"
                            frame_brand = "Non-Brand"
                            break

                        print(
                            "Please enter 1 or 2 only."
                        )

                    print(
                        "Frame Category updated successfully."
                    )

                    continue

                if (
                    frame_category == "1"
                    and frame_edit_choice == "3"
                ):

                    frame_brand = input(
                        "Enter Frame Brand: "
                    ).strip()

                    print(
                        "Frame Brand updated successfully."
                    )

                    continue

                if (
                    (
                        frame_category == "1"
                        and frame_edit_choice == "4"
                    )
                    or (
                        frame_category == "2"
                        and frame_edit_choice == "3"
                    )
                ):

                    frame_offer = normalize_offer(
                        input("Enter Frame Offer (Example: 10 or 10%): ")
                    )
                    print(
                        "Frame Offer updated successfully."
                    )

                    continue

                if (
                    (
                        frame_category == "1"
                        and frame_edit_choice == "5"
                    )
                    or (
                        frame_category == "2"
                        and frame_edit_choice == "4"
                    )
                ):

                    while True:

                        try:
                            new_frame_price = float(
                                input(
                                    "Enter Frame Price: "
                                ).strip()
                            )

                            if new_frame_price < 0:
                                print(
                                    "Frame Price cannot be negative."
                                )
                                continue

                            new_order_total = (
                                new_frame_price + lens_price
                            )

                            if less_amount > new_order_total:
                                print(
                                    "Frame Price cannot be reduced "
                                    "to this amount because the current "
                                    "Less Amount would be greater than "
                                    "Order Total."
                                )
                                continue

                            new_total_amount = (
                                new_order_total - less_amount
                            )

                            if advance_amount > new_total_amount:
                                print(
                                    "Frame Price cannot be reduced "
                                    "to this amount because the current "
                                    "Advance Amount would be greater than "
                                    "Final Total Amount."
                                )
                                continue

                            frame_price = new_frame_price
                            break

                        except ValueError:
                            print(
                                "Please enter Frame Price "
                                "using numbers only."
                            )

                    print(
                        "Frame Price updated successfully."
                    )

                    continue

                print(
                    "Please select a valid Frame Details option."
                )
            continue

        if review_choice in ["3", "4"]:
          if review_choice == "3":

            while True:

                print("\n--- Edit Payment Details ---")
                print(f"Order Total    : ₹{order_total:.2f}")
                print(f"Less Amount    : ₹{less_amount:.2f}")
                print(f"Final Total    : ₹{total_amount:.2f}")
                print(f"Advance Amount : ₹{advance_amount:.2f}")
                print(f"Balance        : ₹{balance:.2f}")

                print("\n1. Less Amount")
                print("2. Advance Amount")
                print("3. Back")

                payment_edit_choice = input(
                    "Select Field / Back (1/2/3): "
                ).strip()

                if payment_edit_choice == "3":
                    break

                if payment_edit_choice == "1":

                    while True:

                        new_less_input = input(
                            "Enter Less Amount "
                            "(Optional - press Enter for 0): "
                        ).strip()

                        if new_less_input == "":
                            new_less_amount = 0.0
                        else:
                            try:
                                new_less_amount = float(
                                    new_less_input
                                )
                            except ValueError:
                                print(
                                    "Please enter Less Amount "
                                    "using numbers only."
                                )
                                continue

                        if new_less_amount < 0:
                            print(
                                "Less Amount cannot be negative."
                            )
                            continue

                        if new_less_amount > order_total:
                            print(
                                "Less Amount cannot be greater "
                                "than Order Total."
                            )
                            continue

                        new_total_amount = (
                            order_total - new_less_amount
                        )

                        if advance_amount > new_total_amount:
                            print(
                                "This Less Amount cannot be used "
                                "because the current Advance Amount "
                                "would be greater than "
                                "Final Total Amount."
                            )
                            continue

                        less_amount = new_less_amount
                        total_amount = new_total_amount
                        balance = (
                            total_amount - advance_amount
                        )
                        break

                    print(
                        "Less Amount updated successfully."
                    )

                    continue

                if payment_edit_choice == "2":

                    while True:

                        new_advance_input = input(
                            "Enter Advance Amount: "
                        ).strip()

                        try:
                            new_advance_amount = float(
                                new_advance_input
                            )

                            if new_advance_amount < 0:
                                print(
                                    "Advance amount cannot be negative."
                                )
                                continue

                            if new_advance_amount > total_amount:
                                print(
                                    "Advance amount cannot be greater "
                                    "than Final Total Amount."
                                )
                                continue

                            advance_amount = new_advance_amount
                            balance = (
                                total_amount - advance_amount
                            )
                            break

                        except ValueError:
                            print(
                                "Please enter amount "
                                "using numbers only."
                            )

                    print(
                        "Advance Amount updated successfully."
                    )

                    continue

                print(
                    "Please select 1, 2 or 3."
                )
            continue

        if review_choice == "4":

            while True:

                print("\n--- Edit Delivery Details ---")
                print("1. Delivery Status")

                if delivery_status == "Pending":
                    print("2. Back")

                elif (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                ):
                    print("2. Delivered To")
                    print("3. Back")

                else:
                    print("2. Delivered To")
                    print("3. Receiver Name")
                    print("4. Back")

                delivery_edit_choice = input(
                    "Select Field / Back: "
                ).strip()

                if (
                    delivery_status == "Pending"
                    and delivery_edit_choice == "2"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                    and delivery_edit_choice == "3"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "4"
                ):
                    break

                if delivery_edit_choice == "1":

                    while True:

                        print("\n--- Delivery Status ---")
                        print("1. Delivered")
                        print("2. Pending")

                        new_delivery_choice = input(
                            "Select Delivery Status (1/2): "
                        ).strip()

                        if new_delivery_choice == "1":
                            delivery_status = "Delivered"
                            delivered_to = "Customer / Same Person"
                            receiver_name = ""
                            break

                        if new_delivery_choice == "2":
                            delivery_status = "Pending"
                            delivered_to = ""
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivery Status updated successfully."
                    )

                    continue

                if (
                    delivery_status == "Delivered"
                    and delivery_edit_choice == "2"
                ):

                    while True:

                        print("\n--- Delivered To ---")
                        print("1. Customer / Same Person")
                        print("2. Other Person")

                        new_delivered_to_choice = input(
                            "Select Delivered To (1/2): "
                        ).strip()

                        if new_delivered_to_choice == "1":
                            delivered_to = (
                                "Customer / Same Person"
                            )
                            receiver_name = ""
                            break

                        if new_delivered_to_choice == "2":
                            delivered_to = "Other Person"
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivered To updated successfully."
                    )

                    continue

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "3"
                ):
                    receiver_name = input(
                        "Enter Receiver Name "
                        "(Optional - press Enter to skip): "
                    ).strip().title()

                    print(
                        "Receiver Name updated successfully."
                    )

                    continue

                print(
                    "Please select a valid "
                    "Delivery Details option."
                )
            continue
        print("Please select 1, 2, 3, 4, 5 or 6.")
# ==================================================
# NEW CUSTOMER - LENSES ONLY FINAL REVIEW
# ==================================================

if customer_type in ["1", "2"] and order_type == "2":
    while True:

        # Always recalculate payment values
        order_total = frame_price + lens_price
        total_amount = order_total - less_amount
        balance = total_amount - advance_amount

        print("\n")
        print("==================================================")
        print("              FINAL REVIEW BEFORE SAVE")
        print("==================================================")

        print("\n--- ORDER ---")
        print("Order Type : Lenses Only")

        print("\n1. Customer Details")
        print(f"   Name         : {customer_name}")
        print(
            f"   C/O / S/O    : "
            f"{customer_relation if customer_relation else 'Not Provided'}"
        )
        print(f"   Gender       : {gender}")
        print(
            f"   Age          : "
            f"{age if age else 'Not Provided'}"
        )
        print(
            f"   Phone        : "
            f"{phone if phone else 'Not Provided'}"
        )
        print(f"   Town/Village : {address}")
        print(
            f"   Full Address : "
            f"{full_address if full_address else 'Not Provided'}"
        )

        print("\n2. Prescription & Eye Details")
        print(f"   Source       : {prescription_source}")

        if (
            prescription_source == "External Prescription"
            and prescription_from
        ):
            print(f"   From         : {prescription_from}")

        print(f"   History      : {spectacle_history}")

        if spectacle_history == "Existing":
            print(
                f"   Using Glasses: "
                f"{years_using_glasses if years_using_glasses else 'Not Recorded'}"
            )

        print(
            f"   Eye Surgery  : "
            f"{eye_surgery}"
        )

        if eye_surgery == "Yes":
            print(f"   Surgery Eye  : {surgery_eye}")

            if surgery_eye in ["Right Eye (OD)", "Both Eyes"]:
                print(f"   Right IOL    : {right_iol}")

            if surgery_eye in ["Left Eye (OS)", "Both Eyes"]:
                print(f"   Left IOL     : {left_iol}")

        print("\n   Current Prescription")
        print(
            f"   OD: SPH {right_sph} | "
            f"CYL {right_cyl if right_cyl else '0'} | "
            f"AXIS {right_axis if right_axis else 'Not Required'} | "
            f"ADD {right_add if right_add else 'Not Required'}"
        )
        print(
            f"   OS: SPH {left_sph} | "
            f"CYL {left_cyl if left_cyl else '0'} | "
            f"AXIS {left_axis if left_axis else 'Not Required'} | "
            f"ADD {left_add if left_add else 'Not Required'}"
        )

        print("\n3. Lens Details")
        print(f"   Lens Type    : {lens_type}")

        if lens_type != "Single Vision":
            if add_requirement == "1":
                add_display = "Both Eyes"
            elif add_requirement == "2":
                add_display = "Right Eye (OD) Only"
            elif add_requirement == "3":
                add_display = "Left Eye (OS) Only"
            else:
                add_display = "Not Recorded"

            print(f"   ADD Required : {add_display}")

        print(
            f"   Features     : "
            f"{lens_features if lens_features else 'Not Provided'}"
        )
        print(
            f"   Brand        : "
            f"{lens_brand if lens_brand else 'Not Provided'}"
        )
        print(
            f"   Offer        : "
            f"{lens_offer if lens_offer else 'Not Provided'}"
        )
        print(f"   Lens Price   : ₹{lens_price:.2f}")

        print("\n4. Payment Details")
        print(f"   Order Total  : ₹{order_total:.2f}")
        print(f"   Less Amount  : ₹{less_amount:.2f}")
        print(f"   Final Total  : ₹{total_amount:.2f}")
        print(f"   Advance      : ₹{advance_amount:.2f}")
        print(f"   Balance      : ₹{balance:.2f}")

        print("\n5. Delivery Details")
        print(f"   Status       : {delivery_status}")

        if delivery_status == "Delivered":
            print(f"   Delivered To : {delivered_to}")

            if delivered_to == "Other Person":
                print(
                    f"   Receiver     : "
                    f"{receiver_name if receiver_name else 'Not Provided'}"
                )

        print("\n--------------------------------------------------")
        print("--- Review / Edit Options ---")
        print("1. Customer Details")
        print("2. Prescription & Eye Details")
        print("3. Lens Details")
        print("4. Payment Details")
        print("5. Delivery Details")
        print("6. Confirm & Save")
        print("7. Cancel / Exit Without Saving")
        print("--------------------------------------------------")

        review_choice = input(
            "Select Review / Edit Option (1/2/3/4/5/6/7): "
        ).strip()

        if review_choice == "6":
            add_missing = False

            if lens_type_choice == "2":
                if (
                    add_requirement in ["1", "2"]
                    and right_add in ["", "0"]
                ):
                    print(
                        "\nRight Eye (OD) ADD is required "
                        "for this Bifocal order."
                    )
                    add_missing = True

                if (
                    add_requirement in ["1", "3"]
                    and left_add in ["", "0"]
                ):
                    print(
                        "\nLeft Eye (OS) ADD is required "
                        "for this Bifocal order."
                    )
                    add_missing = True

            if add_missing:
                print(
                    "Please edit Current Prescription "
                    "and enter the required ADD power."
                )
                continue

            print(
                "\nFinal review confirmed. "
                "Saving customer/order record..."
            )
            break
        if review_choice == "7":
            print(
                "\nOrder cancelled. "
                "No customer/order data was saved."
            )
            raise SystemExit

        if review_choice == "1":

            while True:

                print("\n--- Edit Customer Details ---")
                print("1. Customer Name")
                print("2. C/O / S/O Details")
                print("3. Gender")
                print("4. Age")
                print("5. Phone")
                print("6. Town / Village")
                print("7. Full Address")
                print("8. Back")

                customer_edit_choice = input(
                    "Select Field (1/2/3/4/5/6/7/8): "
                ).strip()

                if customer_edit_choice == "8":
                    break

                if customer_edit_choice not in [
                    "1", "2", "3", "4",
                    "5", "6", "7"
                ]:
                    print(
                        "Please select a number from 1 to 8."
                    )
                    continue

                if customer_edit_choice == "1":

                    while True:

                        new_customer_name = input(
                            "Enter Customer Name: "
                        ).strip().title()

                        if (
                            new_customer_name
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", "'", "-"]
                                for char in new_customer_name
                            )
                        ):
                            customer_name = new_customer_name
                            print(
                                "Customer Name updated successfully."
                            )
                            break

                        print(
                            "Invalid customer name. "
                            "Letters and numbers are allowed."
                        )

                    continue

                if customer_edit_choice == "2":

                    customer_relation = input(
                        "Enter C/O / S/O Details "
                        "(Optional - press Enter to clear): "
                    ).strip()

                    print(
                        "C/O / S/O Details updated successfully."
                    )

                    continue

                if customer_edit_choice == "3":

                    print("\n--- Gender ---")
                    print("1. Male")
                    print("2. Female")

                    while True:

                        new_gender_choice = input(
                            "Select Gender (1/2): "
                        ).strip()

                        if new_gender_choice == "1":
                            gender = "Male"
                            break

                        if new_gender_choice == "2":
                            gender = "Female"
                            break

                        print(
                            "Please select 1 for Male "
                            "or 2 for Female."
                        )

                    print("Gender updated successfully.")
                    continue

                if customer_edit_choice == "4":

                    while True:

                        new_age_input = input(
                            "Enter Patient Age "
                            "(Optional - press Enter if unknown): "
                        ).strip()

                        if new_age_input == "":
                            age = ""
                            break

                        if (
                            new_age_input.isdigit()
                            and int(new_age_input) > 0
                        ):
                            age = int(new_age_input)
                            break

                        print(
                            "Please enter age using "
                            "numbers only."
                        )

                    print("Age updated successfully.")
                    continue

                if customer_edit_choice == "5":

                    while True:

                        raw_phone = input(
                            "Enter Customer Phone Number "
                            "(Optional - press Enter if unavailable): "
                        ).strip()

                        if raw_phone == "":
                            phone = ""
                            break

                        normalized_phone = normalize_indian_phone(
                            raw_phone
                        )

                        if (
                            len(normalized_phone) == 10
                            and normalized_phone.isdigit()
                            and normalized_phone[0] in "6789"
                        ):
                            phone = normalized_phone
                            break

                        print(
                            "Invalid phone number. "
                            "Enter a valid Indian mobile number."
                        )

                    print("Phone updated successfully.")
                    continue

                if customer_edit_choice == "6":

                    while True:

                        new_address = input(
                            "Enter Town / Village (Required): "
                        ).strip().title()

                        if (
                            new_address
                            and any(
                                char.isalpha()
                                for char in new_address
                            )
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", ",", "-", "'"]
                                for char in new_address
                            )
                        ):
                            address = new_address
                            break

                        print(
                            "Invalid Town / Village. "
                            "Letters and numbers are allowed."
                        )

                    print(
                        "Town / Village updated successfully."
                    )
                    continue

                if customer_edit_choice == "7":

                    full_address = input(
                        "Enter Full Address "
                        "(Optional - press Enter to clear): "
                    ).strip().title()

                    print(
                        "Full Address updated successfully."
                    )
                    continue

            continue

        if review_choice == "2":

            while True:

                has_previous_rx = (
                    spectacle_history == "Existing"
                    and "has_previous_prescription" in globals()
                    and has_previous_prescription == "y"
                )

                print("\n--- Prescription & Eye Details ---")
                print("1. Prescription Source")
                print("2. Spectacle History")

                if has_previous_rx:
                    print("3. Previous Prescription")
                    print("4. Eye Surgery / IOL History")
                    print("5. Current Prescription")
                    print("6. PD / Vision Details")
                    print("7. Back")
                else:
                    print("3. Eye Surgery / IOL History")
                    print("4. Current Prescription")
                    print("5. PD / Vision Details")
                    print("6. Back")

                prescription_edit_choice = input(
                    "Select Field / Section: "
                ).strip()

                if (
                    has_previous_rx
                    and prescription_edit_choice == "7"
                ):
                    break

                if (
                    not has_previous_rx
                    and prescription_edit_choice == "6"
                ):
                    break

                # ------------------------------------------
                # 1. PRESCRIPTION SOURCE
                # ------------------------------------------
                if prescription_edit_choice == "1":

                    print("\n--- Edit Prescription Source ---")
                    print("1. In-Store Refraction")
                    print("2. External Prescription")

                    while True:

                        new_source_choice = input(
                            "Select Prescription Source (1/2): "
                        ).strip()

                        if new_source_choice == "1":
                            prescription_source = (
                                "In-Store Refraction"
                            )
                            prescription_from = ""
                            break

                        if new_source_choice == "2":
                            prescription_source = (
                                "External Prescription"
                            )

                            prescription_from = input(
                                "Prescription From "
                                "(Optional - Hospital / Doctor / "
                                "Optical Shop): "
                            ).strip()

                            break

                        print("Please select 1 or 2.")

                    print(
                        "Prescription Source updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 2. SPECTACLE HISTORY
                # ------------------------------------------
                if prescription_edit_choice == "2":

                    print("\n--- Edit Spectacle History ---")
                    print("1. First-time Spectacle User")
                    print("2. Existing Spectacle User")

                    while True:

                        new_history_choice = input(
                            "Select Spectacle History (1/2): "
                        ).strip()

                        if new_history_choice == "1":

                            spectacle_history = "First-time"
                            years_using_glasses = ""
                            has_previous_prescription = "n"

                            previous_prescription_date = ""

                            previous_right_sph = ""
                            previous_right_cyl = ""
                            previous_right_axis = ""
                            previous_right_add = ""

                            previous_left_sph = ""
                            previous_left_cyl = ""
                            previous_left_axis = ""
                            previous_left_add = ""

                            print(
                                "Spectacle History updated to "
                                "First-time."
                            )
                            break

                        if new_history_choice == "2":

                            spectacle_history = "Existing"

                            years_using_glasses = input(
                                "How long have you been "
                                "using glasses?: "
                            ).strip()

                            print(
                                "\nDo you have previous "
                                "prescription details?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                previous_rx_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if previous_rx_choice == "1":
                                    has_previous_prescription = "y"
                                    break

                                if previous_rx_choice == "2":
                                    has_previous_prescription = "n"

                                    previous_prescription_date = ""

                                    previous_right_sph = ""
                                    previous_right_cyl = ""
                                    previous_right_axis = ""
                                    previous_right_add = ""

                                    previous_left_sph = ""
                                    previous_left_cyl = ""
                                    previous_left_axis = ""
                                    previous_left_add = ""

                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            print(
                                "Spectacle History updated "
                                "successfully."
                            )
                            break

                        print("Please select 1 or 2.")

                    continue

                # ------------------------------------------
                # 3. PREVIOUS PRESCRIPTION
                # Only shown when previous Rx is available
                # ------------------------------------------
                if (
                    has_previous_rx
                    and prescription_edit_choice == "3"
                ):

                    while True:

                        print("\n--- Edit Previous Prescription ---")
                        print(
                            "1. Previous Prescription Date"
                        )
                        print("2. Right Eye (OD) SPH")
                        print("3. Right Eye (OD) CYL")
                        print("4. Right Eye (OD) AXIS")
                        print("5. Right Eye (OD) ADD")
                        print("6. Left Eye (OS) SPH")
                        print("7. Left Eye (OS) CYL")
                        print("8. Left Eye (OS) AXIS")
                        print("9. Left Eye (OS) ADD")
                        print("10. Back")

                        previous_edit_choice = input(
                            "Select Field (1-10): "
                        ).strip()

                        if previous_edit_choice == "10":
                            break

                        if previous_edit_choice == "1":

                            while True:

                                new_previous_date = input(
                                    "Enter Previous Prescription Date "
                                    "(DD-MM-YYYY, Optional - "
                                    "press Enter if unknown): "
                                ).strip()

                                if new_previous_date == "":
                                    previous_prescription_date = ""
                                    break

                                try:
                                    parsed_previous_date = (
                                        datetime.strptime(
                                            new_previous_date,
                                            "%d-%m-%Y"
                                        )
                                    )

                                    previous_prescription_date = (
                                        parsed_previous_date.strftime(
                                            "%d-%m-%Y"
                                        )
                                    )
                                    break

                                except ValueError:
                                    print(
                                        "Invalid date. Please enter "
                                        "date as DD-MM-YYYY "
                                        "or leave blank."
                                    )

                            print(
                                "Previous Prescription Date "
                                "updated successfully."
                            )
                            continue

                        if previous_edit_choice == "2":
                            previous_right_sph = get_old_sph(
                                "Right Eye"
                            )
                            print(
                                "Right Eye SPH updated successfully."
                            )
                            continue

                        if previous_edit_choice == "3":
                            previous_right_cyl = get_old_cyl(
                                "Right Eye"
                            )
                            print(
                                "Right Eye CYL updated successfully."
                            )
                            continue

                        if previous_edit_choice == "4":
                            previous_right_axis = get_old_axis(
                                "Right Eye"
                            )
                            print(
                                "Right Eye AXIS updated successfully."
                            )
                            continue

                        if previous_edit_choice == "5":

                            while True:

                                new_right_add = input(
                                    "Enter Right Eye ADD / "
                                    "Near Power "
                                    "(Optional - press Enter "
                                    "if not required): "
                                ).strip()

                                if new_right_add in ("", "0"):
                                    previous_right_add = ""
                                    break

                                if new_right_add.startswith("+"):
                                    number_part = new_right_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1] in [
                                            "00", "25", "50", "75"
                                        ]
                                        and float(number_part) <= 5
                                    ):
                                        previous_right_add = (
                                            new_right_add
                                        )
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50, "
                                    "+2.00 or leave blank."
                                )

                            print(
                                "Right Eye ADD updated successfully."
                            )
                            continue

                        if previous_edit_choice == "6":
                            previous_left_sph = get_old_sph(
                                "Left Eye"
                            )
                            print(
                                "Left Eye SPH updated successfully."
                            )
                            continue

                        if previous_edit_choice == "7":
                            previous_left_cyl = get_old_cyl(
                                "Left Eye"
                            )
                            print(
                                "Left Eye CYL updated successfully."
                            )
                            continue

                        if previous_edit_choice == "8":
                            previous_left_axis = get_old_axis(
                                "Left Eye"
                            )
                            print(
                                "Left Eye AXIS updated successfully."
                            )
                            continue

                        if previous_edit_choice == "9":

                            while True:

                                new_left_add = input(
                                    "Enter Left Eye ADD / "
                                    "Near Power "
                                    "(Optional - press Enter "
                                    "if not required): "
                                ).strip()

                                if new_left_add in ("", "0"):
                                    previous_left_add = ""
                                    break

                                if new_left_add.startswith("+"):
                                    number_part = new_left_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1] in [
                                            "00", "25", "50", "75"
                                        ]
                                        and float(number_part) <= 5
                                    ):
                                        previous_left_add = (
                                            new_left_add
                                        )
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50, "
                                    "+2.00 or leave blank."
                                )

                            print(
                                "Left Eye ADD updated successfully."
                            )
                            continue

                        print(
                            "Please select a number from 1 to 10."
                        )

                    continue

                # ------------------------------------------
                # EYE SURGERY / IOL HISTORY
                # Previous Rx available  -> Option 4
                # Previous Rx unavailable -> Option 3
                # ------------------------------------------
                eye_surgery_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "4"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "3"
                    )
                )

                if eye_surgery_selected:

                    print("\n--- Edit Eye Surgery / IOL History ---")
                    print("1. No Eye Surgery")
                    print("2. Right Eye (OD)")
                    print("3. Left Eye (OS)")
                    print("4. Both Eyes")

                    while True:

                        new_surgery_choice = input(
                            "Select Eye Surgery Status "
                            "(1/2/3/4): "
                        ).strip()

                        if new_surgery_choice == "1":

                            eye_surgery = "No"
                            surgery_eye = ""
                            right_iol = "No"
                            left_iol = "No"

                            break

                        if new_surgery_choice == "2":

                            eye_surgery = "Yes"
                            surgery_eye = "Right Eye (OD)"
                            left_iol = "No"

                            print(
                                "\nRight Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_right_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_right_iol_choice == "1":
                                    right_iol = "Yes"
                                    break

                                if new_right_iol_choice == "2":
                                    right_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        if new_surgery_choice == "3":

                            eye_surgery = "Yes"
                            surgery_eye = "Left Eye (OS)"
                            right_iol = "No"

                            print(
                                "\nLeft Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_left_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_left_iol_choice == "1":
                                    left_iol = "Yes"
                                    break

                                if new_left_iol_choice == "2":
                                    left_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        if new_surgery_choice == "4":

                            eye_surgery = "Yes"
                            surgery_eye = "Both Eyes"

                            print(
                                "\nRight Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_right_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_right_iol_choice == "1":
                                    right_iol = "Yes"
                                    break

                                if new_right_iol_choice == "2":
                                    right_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            print(
                                "\nLeft Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_left_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_left_iol_choice == "1":
                                    left_iol = "Yes"
                                    break

                                if new_left_iol_choice == "2":
                                    left_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        print(
                            "Please select 1, 2, 3 or 4."
                        )

                    print(
                        "Eye Surgery / IOL History "
                        "updated successfully."
                    )
                    continue

                # ------------------------------------------
                # CURRENT PRESCRIPTION
                # Previous Rx available  -> Option 5
                # Previous Rx unavailable -> Option 4
                # ------------------------------------------
                current_rx_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "5"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "4"
                    )
                )

                if current_rx_selected:

                    while True:

                        print("\n--- Edit Current Prescription ---")
                        print("1. Right Eye (OD) SPH")
                        print("2. Right Eye (OD) CYL")
                        print("3. Right Eye (OD) AXIS")

                        if (
                            lens_type_choice != "1"
                            and add_requirement != "3"
                        ):
                            print("4. Right Eye (OD) ADD")
                        else:
                            print("4. Right Eye (OD) ADD - Not Required")

                        print("5. Left Eye (OS) SPH")
                        print("6. Left Eye (OS) CYL")
                        print("7. Left Eye (OS) AXIS")

                        if (
                            lens_type_choice != "1"
                            and add_requirement != "2"
                        ):
                            print("8. Left Eye (OS) ADD")
                        else:
                            print("8. Left Eye (OS) ADD - Not Required")

                        print("9. Back")

                        current_rx_edit_choice = input(
                            "Select Field (1-9): "
                        ).strip()

                        if current_rx_edit_choice == "9":
                            break

                        # ----------------------------------
                        # 1. RIGHT EYE (OD) SPH
                        # ----------------------------------
                        if current_rx_edit_choice == "1":

                            while True:

                                new_right_sph = input(
                                    "Enter Right Eye SPH (+/-): "
                                ).strip()

                                if new_right_sph.lower() == "plano":
                                    right_sph = "Plano"
                                    break

                                if new_right_sph == "0":
                                    right_sph = "0"
                                    break

                                if new_right_sph.startswith(("+", "-")):
                                    number_part = new_right_sph[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 30
                                    ):
                                        right_sph = new_right_sph
                                        break

                                print(
                                    "Invalid SPH. Enter like "
                                    "-1.00, +1.25, 0 or Plano."
                                )

                            print(
                                "Right Eye SPH updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 2. RIGHT EYE (OD) CYL
                        # ----------------------------------
                        if current_rx_edit_choice == "2":

                            while True:

                                new_right_cyl = input(
                                    "Enter Right Eye CYL (+/-): "
                                ).strip()

                                if new_right_cyl == "":
                                    right_cyl = ""
                                    break

                                if new_right_cyl == "0":
                                    right_cyl = "0"
                                    break

                                if new_right_cyl.startswith(("+", "-")):
                                    number_part = new_right_cyl[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 10
                                    ):
                                        right_cyl = new_right_cyl
                                        break

                                print(
                                    "Invalid CYL. Enter like "
                                    "-0.50, +1.25, 0 or leave blank."
                                )

                            print(
                                "Right Eye CYL updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 3. RIGHT EYE (OD) AXIS
                        # ----------------------------------
                        if current_rx_edit_choice == "3":

                            while True:

                                new_right_axis = input(
                                    "Enter Right Eye AXIS (0-180): "
                                ).strip()

                                if new_right_axis == "":
                                    right_axis = ""
                                    break

                                if new_right_axis.isdigit():
                                    axis_value = int(new_right_axis)

                                    if 0 <= axis_value <= 180:
                                        right_axis = new_right_axis
                                        break

                                print(
                                    "Invalid AXIS. Enter a number "
                                    "from 0 to 180 or leave blank."
                                )

                            print(
                                "Right Eye AXIS updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 4. RIGHT EYE (OD) ADD
                        # ----------------------------------
                        if current_rx_edit_choice == "4":

                            if (
                                lens_type_choice == "1"
                                or add_requirement == "3"
                            ):
                                right_add = ""
                                print(
                                    "Right Eye ADD is Not Required."
                                )
                                continue

                            while True:

                                new_right_add = input(
                                    "Enter Right Eye ADD / "
                                    "Near Power (+): "
                                ).strip()

                                if new_right_add in ["", "0"]:
                                    print(
                                        "ADD is required for Right Eye."
                                    )
                                    continue

                                if new_right_add.startswith("+"):
                                    number_part = new_right_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 5
                                    ):
                                        right_add = new_right_add
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50 or +2.00."
                                )

                            print(
                                "Right Eye ADD updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 5. LEFT EYE (OS) SPH
                        # ----------------------------------
                        if current_rx_edit_choice == "5":

                            while True:

                                new_left_sph = input(
                                    "Enter Left Eye SPH (+/-): "
                                ).strip()

                                if new_left_sph.lower() == "plano":
                                    left_sph = "Plano"
                                    break

                                if new_left_sph == "0":
                                    left_sph = "0"
                                    break

                                if new_left_sph.startswith(("+", "-")):
                                    number_part = new_left_sph[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 30
                                    ):
                                        left_sph = new_left_sph
                                        break

                                print(
                                    "Invalid SPH. Enter like "
                                    "-1.00, +1.25, 0 or Plano."
                                )

                            print(
                                "Left Eye SPH updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 6. LEFT EYE (OS) CYL
                        # ----------------------------------
                        if current_rx_edit_choice == "6":

                            while True:

                                new_left_cyl = input(
                                    "Enter Left Eye CYL (+/-): "
                                ).strip()

                                if new_left_cyl == "":
                                    left_cyl = ""
                                    break

                                if new_left_cyl == "0":
                                    left_cyl = "0"
                                    break

                                if new_left_cyl.startswith(("+", "-")):
                                    number_part = new_left_cyl[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 10
                                    ):
                                        left_cyl = new_left_cyl
                                        break

                                print(
                                    "Invalid CYL. Enter like "
                                    "-1.00, +0.50, 0 or leave blank."
                                )

                            print(
                                "Left Eye CYL updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 7. LEFT EYE (OS) AXIS
                        # ----------------------------------
                        if current_rx_edit_choice == "7":

                            while True:

                                new_left_axis = input(
                                    "Enter Left Eye AXIS (0-180): "
                                ).strip()

                                if new_left_axis == "":
                                    left_axis = ""
                                    break

                                if new_left_axis.isdigit():
                                    axis_value = int(new_left_axis)

                                    if 0 <= axis_value <= 180:
                                        left_axis = new_left_axis
                                        break

                                print(
                                    "Invalid AXIS. Enter a number "
                                    "from 0 to 180 or leave blank."
                                )

                            print(
                                "Left Eye AXIS updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 8. LEFT EYE (OS) ADD
                        # ----------------------------------
                        if current_rx_edit_choice == "8":

                            if (
                                lens_type_choice == "1"
                                or add_requirement == "2"
                            ):
                                left_add = ""
                                print(
                                    "Left Eye ADD is Not Required."
                                )
                                continue

                            while True:

                                new_left_add = input(
                                    "Enter Left Eye ADD / "
                                    "Near Power (+): "
                                ).strip()

                                if new_left_add in ["", "0"]:
                                    print(
                                        "ADD is required for Left Eye."
                                    )
                                    continue

                                if new_left_add.startswith("+"):
                                    number_part = new_left_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 5
                                    ):
                                        left_add = new_left_add
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50 or +2.00."
                                )

                            print(
                                "Left Eye ADD updated successfully."
                            )
                            continue

                        print(
                            "Please select a number from 1 to 9."
                        )
                    continue

                # ------------------------------------------
                # PD / VISION DETAILS
                # Previous Rx available  -> Option 6
                # Previous Rx unavailable -> Option 5
                # ------------------------------------------
                pd_vision_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "6"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "5"
                    )
                )

                if pd_vision_selected:

                    while True:

                        print("\n--- Edit PD / Vision Details ---")
                        print("1. Distance PD")
                        print("2. Near PD")
                        print("3. Right Eye Visual Acuity")
                        print("4. Left Eye Visual Acuity")
                        print("5. Right Eye Pinhole")
                        print("6. Left Eye Pinhole")
                        print("7. Back")

                        pd_vision_edit_choice = input(
                            "Select Field (1-7): "
                        ).strip()

                        if pd_vision_edit_choice == "1":
                            distance_pd = input(
                                "Enter Distance PD in mm "
                                "(Example: 62, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Distance PD updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "2":
                            near_pd = input(
                                "Enter Near PD in mm "
                                "(Example: 59, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Near PD updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "3":
                            right_va = input(
                                "Right Eye Visual Acuity "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Right Eye Visual Acuity "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "4":
                            left_va = input(
                                "Left Eye Visual Acuity "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Left Eye Visual Acuity "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "5":
                            right_pinhole = input(
                                "Right Eye Pinhole "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Right Eye Pinhole "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "6":
                            left_pinhole = input(
                                "Left Eye Pinhole "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Left Eye Pinhole "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "7":
                            break

                        print(
                            "Please select a number from 1 to 7."
                        )

                    continue

                print(
                    "Please select a valid "
                    "Prescription / Eye Details option."
                )
            continue

        # ==================================================
        # 3. LENS DETAILS
        # ==================================================
        if review_choice == "3":

            while True:

                print("\n--- Edit Lens Details ---")
                print("1. Lens Type")

                if lens_type != "Single Vision":
                    print("2. ADD Requirement")
                else:
                    print("2. ADD Requirement - Not Required")

                print("3. Lens Features / Coating")
                print("4. Lens Brand")
                print("5. Lens Offer")
                print("6. Lens Price")
                print("7. Back")

                lens_edit_choice = input(
                    "Select Field (1-7): "
                ).strip()

                # ------------------------------------------
                # 1. LENS TYPE
                # ------------------------------------------
                if lens_edit_choice == "1":

                    print("\n--- Edit Lens Type ---")
                    print("1. Single Vision")
                    print("2. Bifocal")

                    while True:

                        new_lens_type_choice = input(
                            "Select Lens Type (1/2): "
                        ).strip()

                        if new_lens_type_choice == "1":

                            lens_type_choice = "1"
                            lens_type = "Single Vision"
                            add_requirement = ""

                            right_add = ""
                            left_add = ""

                            break

                        if new_lens_type_choice == "2":

                            lens_type_choice = "2"

                            print("\n--- Bifocal Type ---")
                            print("1. Kryptok Bifocal")
                            print("2. D Bifocal")
                            print("3. Progressive Bifocal")
                            print("4. Other")

                            while True:

                                new_bifocal_choice = input(
                                    "Select Bifocal Type "
                                    "(1/2/3/4): "
                                ).strip()

                                if new_bifocal_choice == "1":
                                    lens_type = "Kryptok Bifocal"
                                    break

                                if new_bifocal_choice == "2":
                                    lens_type = "D Bifocal"
                                    break

                                if new_bifocal_choice == "3":
                                    lens_type = (
                                        "Progressive Bifocal"
                                    )
                                    break

                                if new_bifocal_choice == "4":
                                    lens_type = "Other"
                                    break

                                print(
                                    "Invalid option. Please select "
                                    "1, 2, 3 or 4."
                                )

                            print("\n--- ADD Requirement ---")
                            print("1. Both Eyes")
                            print("2. Right Eye (OD) Only")
                            print("3. Left Eye (OS) Only")

                            while True:

                                add_requirement = input(
                                    "Select ADD Requirement "
                                    "(1/2/3): "
                                ).strip()

                                if add_requirement in [
                                    "1", "2", "3"
                                ]:
                                    break

                                print(
                                    "Invalid option. Please select "
                                    "1, 2 or 3."
                                )

                            if add_requirement == "2":
                                left_add = ""

                            elif add_requirement == "3":
                                right_add = ""

                            break

                        print(
                            "Invalid option. Please select 1 or 2."
                        )

                    print(
                        "Lens Type updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 2. ADD REQUIREMENT
                # ------------------------------------------
                if lens_edit_choice == "2":

                    if lens_type == "Single Vision":
                        add_requirement = ""
                        right_add = ""
                        left_add = ""

                        print(
                            "ADD Requirement is Not Required "
                            "for Single Vision."
                        )
                        continue

                    print("\n--- Edit ADD Requirement ---")
                    print("1. Both Eyes")
                    print("2. Right Eye (OD) Only")
                    print("3. Left Eye (OS) Only")

                    while True:

                        new_add_requirement = input(
                            "Select ADD Requirement "
                            "(1/2/3): "
                        ).strip()

                        if new_add_requirement in [
                            "1", "2", "3"
                        ]:
                            add_requirement = (
                                new_add_requirement
                            )
                            break

                        print(
                            "Invalid option. Please select "
                            "1, 2 or 3."
                        )

                    if add_requirement == "2":
                        left_add = ""

                    elif add_requirement == "3":
                        right_add = ""

                    print(
                        "ADD Requirement updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 3. LENS FEATURES / COATING
                # ------------------------------------------
                if lens_edit_choice == "3":

                    while True:

                        new_lens_features = input(
                            "Enter Lens Features / Coating "
                            "(Optional): "
                        ).strip().title()

                        normalized_features = (
                            new_lens_features.lower()
                            .replace(".", " ")
                            .replace("-", " ")
                            .replace("/", " ")
                            .replace(",", " ")
                            .replace("_", " ")
                        )

                        feature_words = (
                            normalized_features.split()
                        )

                        has_kt = (
                            "kt" in feature_words
                            or "kryptok" in feature_words
                        )

                        has_progressive = (
                            "progressive" in feature_words
                        )

                        has_d_bifocal = (
                            "d bifocal"
                            in normalized_features
                            or "dbifocal"
                            in normalized_features
                        )

                        if lens_type == "Single Vision":

                            if has_kt:
                                print(
                                    "KT / Kryptok is a Bifocal "
                                    "type and cannot be used "
                                    "with Single Vision."
                                )
                                continue

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with Single Vision."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Single Vision."
                                )
                                continue

                        elif lens_type == "Kryptok Bifocal":

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with Kryptok Bifocal."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Kryptok Bifocal."
                                )
                                continue

                        elif lens_type == "D Bifocal":

                            if has_kt:
                                print(
                                    "KT / Kryptok cannot be used "
                                    "with D Bifocal."
                                )
                                continue

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with D Bifocal."
                                )
                                continue

                        elif lens_type == "Progressive Bifocal":

                            if has_kt:
                                print(
                                    "KT / Kryptok cannot be used "
                                    "with Progressive Bifocal."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Progressive Bifocal."
                                )
                                continue

                        lens_features = new_lens_features
                        break

                    print(
                        "Lens Features / Coating "
                        "updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 4. LENS BRAND
                # ------------------------------------------
                if lens_edit_choice == "4":

                    lens_brand = input(
                        "Enter Lens Brand (Optional): "
                    ).strip().title()

                    print(
                        "Lens Brand updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 5. LENS OFFER
                # ------------------------------------------
                if lens_edit_choice == "5":

                    lens_offer = normalize_offer(
                        input("Enter Lens Offer (Example: 10 or 10%): ")
                    )
                    print(
                        "Lens Offer updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 6. LENS PRICE
                # ------------------------------------------
                if lens_edit_choice == "6":

                    while True:

                        new_lens_price_input = input(
                            "Enter Lens Price: "
                        ).strip()

                        try:
                            new_lens_price = float(
                                new_lens_price_input
                            )

                            if new_lens_price < 0:
                                print(
                                    "Lens Price cannot be negative."
                                )
                                continue

                            lens_price = new_lens_price
                            break

                        except ValueError:
                            print(
                                "Please enter Lens Price "
                                "using numbers only."
                            )

                    # Recalculate all dependent payment values
                    order_total = frame_price + lens_price

                    if less_amount > order_total:
                        less_amount = order_total

                    total_amount = (
                        order_total - less_amount
                    )

                    if advance_amount > total_amount:
                        advance_amount = total_amount

                    balance = (
                        total_amount - advance_amount
                    )

                    print(
                        "Lens Price updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 7. BACK
                # ------------------------------------------
                if lens_edit_choice == "7":
                    break

                print(
                    "Please select a number from 1 to 7."
                )

            continue

        # ==================================================
        # 4. PAYMENT DETAILS
        # ==================================================
        if review_choice == "4":

            while True:

                print("\n--- Edit Payment Details ---")
                print(f"Order Total    : ₹{order_total:.2f}")
                print(f"Less Amount    : ₹{less_amount:.2f}")
                print(f"Final Total    : ₹{total_amount:.2f}")
                print(f"Advance Amount : ₹{advance_amount:.2f}")
                print(f"Balance        : ₹{balance:.2f}")

                print("\n1. Less Amount")
                print("2. Advance Amount")
                print("3. Back")

                payment_edit_choice = input(
                    "Select Field / Back (1/2/3): "
                ).strip()

                if payment_edit_choice == "3":
                    break

                if payment_edit_choice == "1":

                    while True:

                        new_less_input = input(
                            "Enter Less Amount "
                            "(Optional - press Enter for 0): "
                        ).strip()

                        if new_less_input == "":
                            new_less_amount = 0.0
                        else:
                            try:
                                new_less_amount = float(
                                    new_less_input
                                )
                            except ValueError:
                                print(
                                    "Please enter Less Amount "
                                    "using numbers only."
                                )
                                continue

                        if new_less_amount < 0:
                            print(
                                "Less Amount cannot be negative."
                            )
                            continue

                        if new_less_amount > order_total:
                            print(
                                "Less Amount cannot be greater "
                                "than Order Total."
                            )
                            continue

                        new_total_amount = (
                            order_total - new_less_amount
                        )

                        if advance_amount > new_total_amount:
                            print(
                                "This Less Amount cannot be used "
                                "because the current Advance Amount "
                                "would be greater than "
                                "Final Total Amount."
                            )
                            continue

                        less_amount = new_less_amount
                        total_amount = new_total_amount
                        balance = (
                            total_amount - advance_amount
                        )
                        break

                    print(
                        "Less Amount updated successfully."
                    )
                    continue

                if payment_edit_choice == "2":

                    while True:

                        new_advance_input = input(
                            "Enter Advance Amount: "
                        ).strip()

                        try:
                            new_advance_amount = float(
                                new_advance_input
                            )

                            if new_advance_amount < 0:
                                print(
                                    "Advance amount cannot be negative."
                                )
                                continue

                            if new_advance_amount > total_amount:
                                print(
                                    "Advance amount cannot be greater "
                                    "than Final Total Amount."
                                )
                                continue

                            advance_amount = new_advance_amount
                            balance = (
                                total_amount - advance_amount
                            )
                            break

                        except ValueError:
                            print(
                                "Please enter amount "
                                "using numbers only."
                            )

                    print(
                        "Advance Amount updated successfully."
                    )
                    continue

                print(
                    "Please select 1, 2 or 3."
                )

            continue

        # ==================================================
        # 5. DELIVERY DETAILS
        # ==================================================
        if review_choice == "5":

            while True:

                print("\n--- Edit Delivery Details ---")
                print("1. Delivery Status")

                if delivery_status == "Pending":
                    print("2. Back")

                elif (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                ):
                    print("2. Delivered To")
                    print("3. Back")

                else:
                    print("2. Delivered To")
                    print("3. Receiver Name")
                    print("4. Back")

                delivery_edit_choice = input(
                    "Select Field / Back: "
                ).strip()

                if (
                    delivery_status == "Pending"
                    and delivery_edit_choice == "2"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                    and delivery_edit_choice == "3"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "4"
                ):
                    break

                if delivery_edit_choice == "1":

                    while True:

                        print("\n--- Delivery Status ---")
                        print("1. Delivered")
                        print("2. Pending")

                        new_delivery_choice = input(
                            "Select Delivery Status (1/2): "
                        ).strip()

                        if new_delivery_choice == "1":
                            delivery_status = "Delivered"
                            delivered_to = (
                                "Customer / Same Person"
                            )
                            receiver_name = ""
                            break

                        if new_delivery_choice == "2":
                            delivery_status = "Pending"
                            delivered_to = ""
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivery Status updated successfully."
                    )
                    continue

                if (
                    delivery_status == "Delivered"
                    and delivery_edit_choice == "2"
                ):

                    while True:

                        print("\n--- Delivered To ---")
                        print("1. Customer / Same Person")
                        print("2. Other Person")

                        new_delivered_to_choice = input(
                            "Select Delivered To (1/2): "
                        ).strip()

                        if new_delivered_to_choice == "1":
                            delivered_to = (
                                "Customer / Same Person"
                            )
                            receiver_name = ""
                            break

                        if new_delivered_to_choice == "2":
                            delivered_to = "Other Person"
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivered To updated successfully."
                    )
                    continue

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "3"
                ):

                    receiver_name = input(
                        "Enter Receiver Name "
                        "(Optional - press Enter to skip): "
                    ).strip().title()

                    print(
                        "Receiver Name updated successfully."
                    )
                    continue

                print(
                    "Please select a valid "
                    "Delivery Details option."
                )

            continue

        print(
            "Please select 1, 2, 3, 4, 5, 6 or 7."
        )
# ==================================================
# NEW CUSTOMER - FRAME + LENSES FINAL REVIEW
# ==================================================

if customer_type in ["1", "2"] and order_type == "3":
    while True:

        # Always recalculate payment values
        order_total = frame_price + lens_price
        total_amount = order_total - less_amount
        balance = total_amount - advance_amount

        print("\n")
        print("==================================================")
        print("              FINAL REVIEW BEFORE SAVE")
        print("==================================================")

        print("\n--- ORDER ---")
        print("Order Type : Frame + Lenses")

        print("\n1. Customer Details")
        print(f"   Name         : {customer_name}")
        print(
            f"   C/O / S/O    : "
            f"{customer_relation if customer_relation else 'Not Provided'}"
        )
        print(f"   Gender       : {gender}")
        print(
            f"   Age          : "
            f"{age if age else 'Not Provided'}"
        )
        print(
            f"   Phone        : "
            f"{phone if phone else 'Not Provided'}"
        )
        print(f"   Town/Village : {address}")
        print(
            f"   Full Address : "
            f"{full_address if full_address else 'Not Provided'}"
        )

        print("\n2. Frame Details")
        print(
            f"   Frame Details : "
            f"{frame_details if frame_details else 'Not Provided'}"
        )
        print(
            f"   Category      : "
            f"{'Brand' if frame_category == '1' else 'Non-Brand'}"
        )

        if frame_category == "1":
            print(
                f"   Frame Brand   : "
                f"{frame_brand if frame_brand else 'Not Provided'}"
            )

        print(
            f"   Frame Offer   : "
            f"{frame_offer if frame_offer else 'None'}"
        )
        print(f"   Frame Price   : ₹{frame_price:.2f}")

        print("\n3. Prescription & Eye Details")
        print(f"   Source       : {prescription_source}")

        if (
            prescription_source == "External Prescription"
            and prescription_from
        ):
            print(f"   From         : {prescription_from}")

        print(f"   History      : {spectacle_history}")

        if spectacle_history == "Existing":
            print(
                f"   Using Glasses: "
                f"{years_using_glasses if years_using_glasses else 'Not Recorded'}"
            )

        print(
            f"   Eye Surgery  : "
            f"{eye_surgery}"
        )

        if eye_surgery == "Yes":
            print(f"   Surgery Eye  : {surgery_eye}")

            if surgery_eye in ["Right Eye (OD)", "Both Eyes"]:
                print(f"   Right IOL    : {right_iol}")

            if surgery_eye in ["Left Eye (OS)", "Both Eyes"]:
                print(f"   Left IOL     : {left_iol}")

        print("\n   Current Prescription")
        print(
            f"   OD: SPH {right_sph} | "
            f"CYL {right_cyl if right_cyl else '0'} | "
            f"AXIS {right_axis if right_axis else 'Not Required'} | "
            f"ADD {right_add if right_add else 'Not Required'}"
        )
        print(
            f"   OS: SPH {left_sph} | "
            f"CYL {left_cyl if left_cyl else '0'} | "
            f"AXIS {left_axis if left_axis else 'Not Required'} | "
            f"ADD {left_add if left_add else 'Not Required'}"
        )

        print("\n4. Lens Details")
        print(f"   Lens Type    : {lens_type}")

        if lens_type != "Single Vision":
            if add_requirement == "1":
                add_display = "Both Eyes"
            elif add_requirement == "2":
                add_display = "Right Eye (OD) Only"
            elif add_requirement == "3":
                add_display = "Left Eye (OS) Only"
            else:
                add_display = "Not Recorded"

            print(f"   ADD Required : {add_display}")

        print(
            f"   Features     : "
            f"{lens_features if lens_features else 'Not Provided'}"
        )
        print(
            f"   Brand        : "
            f"{lens_brand if lens_brand else 'Not Provided'}"
        )
        print(
            f"   Offer        : "
            f"{lens_offer if lens_offer else 'Not Provided'}"
        )
        print(f"   Lens Price   : ₹{lens_price:.2f}")

        print("\n5. Payment Details")
        print(f"   Order Total  : ₹{order_total:.2f}")
        print(f"   Less Amount  : ₹{less_amount:.2f}")
        print(f"   Final Total  : ₹{total_amount:.2f}")
        print(f"   Advance      : ₹{advance_amount:.2f}")
        print(f"   Balance      : ₹{balance:.2f}")

        print("\n6. Delivery Details")
        print(f"   Status       : {delivery_status}")

        if delivery_status == "Delivered":
            print(f"   Delivered To : {delivered_to}")

            if delivered_to == "Other Person":
                print(
                    f"   Receiver     : "
                    f"{receiver_name if receiver_name else 'Not Provided'}"
                )

        print("\n--------------------------------------------------")
        print("--- Review / Edit Options ---")
        print("1. Customer Details")
        print("2. Frame Details")
        print("3. Prescription & Eye Details")
        print("4. Lens Details")
        print("5. Payment Details")
        print("6. Delivery Details")
        print("7. Confirm & Save")
        print("8. Cancel / Exit Without Saving")
        print("--------------------------------------------------")

        review_choice = input(
            "Select Review / Edit Option "
            "(1/2/3/4/5/6/7/8): "
        ).strip()

        if review_choice == "7":
            add_missing = False

            if lens_type_choice == "2":
                if (
                    add_requirement in ["1", "2"]
                    and right_add in ["", "0"]
                ):
                    print(
                        "\nRight Eye (OD) ADD is required "
                        "for this Bifocal order."
                    )
                    add_missing = True

                if (
                    add_requirement in ["1", "3"]
                    and left_add in ["", "0"]
                ):
                    print(
                        "\nLeft Eye (OS) ADD is required "
                        "for this Bifocal order."
                    )
                    add_missing = True

            if add_missing:
                print(
                    "Please edit Current Prescription "
                    "and enter the required ADD power."
                )
                continue

            print(
                "\nFinal review confirmed. "
                "Saving customer/order record..."
            )
            break
        if review_choice == "8":
            print(
                "\nOrder cancelled. "
                "No customer/order data was saved."
            )
            raise SystemExit

        if review_choice == "1":

            while True:

                print("\n--- Edit Customer Details ---")
                print("1. Customer Name")
                print("2. C/O / S/O Details")
                print("3. Gender")
                print("4. Age")
                print("5. Phone")
                print("6. Town / Village")
                print("7. Full Address")
                print("8. Back")

                customer_edit_choice = input(
                    "Select Field (1/2/3/4/5/6/7/8): "
                ).strip()

                if customer_edit_choice == "8":
                    break

                if customer_edit_choice not in [
                    "1", "2", "3", "4",
                    "5", "6", "7"
                ]:
                    print(
                        "Please select a number from 1 to 8."
                    )
                    continue

                if customer_edit_choice == "1":

                    while True:

                        new_customer_name = input(
                            "Enter Customer Name: "
                        ).strip().title()

                        if (
                            new_customer_name
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", "'", "-"]
                                for char in new_customer_name
                            )
                        ):
                            customer_name = new_customer_name
                            print(
                                "Customer Name updated successfully."
                            )
                            break

                        print(
                            "Invalid customer name. "
                            "Letters and numbers are allowed."
                        )

                    continue

                if customer_edit_choice == "2":

                    customer_relation = input(
                        "Enter C/O / S/O Details "
                        "(Optional - press Enter to clear): "
                    ).strip()

                    print(
                        "C/O / S/O Details updated successfully."
                    )

                    continue

                if customer_edit_choice == "3":

                    print("\n--- Gender ---")
                    print("1. Male")
                    print("2. Female")

                    while True:

                        new_gender_choice = input(
                            "Select Gender (1/2): "
                        ).strip()

                        if new_gender_choice == "1":
                            gender = "Male"
                            break

                        if new_gender_choice == "2":
                            gender = "Female"
                            break

                        print(
                            "Please select 1 for Male "
                            "or 2 for Female."
                        )

                    print("Gender updated successfully.")
                    continue

                if customer_edit_choice == "4":

                    while True:

                        new_age_input = input(
                            "Enter Patient Age "
                            "(Optional - press Enter if unknown): "
                        ).strip()

                        if new_age_input == "":
                            age = ""
                            break

                        if (
                            new_age_input.isdigit()
                            and int(new_age_input) > 0
                        ):
                            age = int(new_age_input)
                            break

                        print(
                            "Please enter age using "
                            "numbers only."
                        )

                    print("Age updated successfully.")
                    continue

                if customer_edit_choice == "5":

                    while True:

                        raw_phone = input(
                            "Enter Customer Phone Number "
                            "(Optional - press Enter if unavailable): "
                        ).strip()

                        if raw_phone == "":
                            phone = ""
                            break

                        normalized_phone = normalize_indian_phone(
                            raw_phone
                        )

                        if (
                            len(normalized_phone) == 10
                            and normalized_phone.isdigit()
                            and normalized_phone[0] in "6789"
                        ):
                            phone = normalized_phone
                            break

                        print(
                            "Invalid phone number. "
                            "Enter a valid Indian mobile number."
                        )

                    print("Phone updated successfully.")
                    continue

                if customer_edit_choice == "6":

                    while True:

                        new_address = input(
                            "Enter Town / Village (Required): "
                        ).strip().title()

                        if (
                            new_address
                            and any(
                                char.isalpha()
                                for char in new_address
                            )
                            and all(
                                char.isalnum()
                                or char.isspace()
                                or char in [".", ",", "-", "'"]
                                for char in new_address
                            )
                        ):
                            address = new_address
                            break

                        print(
                            "Invalid Town / Village. "
                            "Letters and numbers are allowed."
                        )

                    print(
                        "Town / Village updated successfully."
                    )
                    continue

                if customer_edit_choice == "7":

                    full_address = input(
                        "Enter Full Address "
                        "(Optional - press Enter to clear): "
                    ).strip().title()

                    print(
                        "Full Address updated successfully."
                    )
                    continue

            continue
        if review_choice == "2":
            while True:

                print("\n--- Edit Frame Details ---")
                print("1. Frame Details")
                print("2. Frame Category")

                if frame_category == "1":
                    print("3. Frame Brand")
                    print("4. Frame Offer")
                    print("5. Frame Price")
                    print("6. Back")
                else:
                    print("3. Frame Offer")
                    print("4. Frame Price")
                    print("5. Back")

                frame_edit_choice = input(
                    "Select Field / Back: "
                ).strip()

                if (
                    frame_category == "1"
                    and frame_edit_choice == "6"
                ):
                    break

                if (
                    frame_category == "2"
                    and frame_edit_choice == "5"
                ):
                    break

                if frame_edit_choice == "1":

                    frame_details = input(
                        "Enter Frame Details: "
                    ).strip()

                    print(
                        "Frame Details updated successfully."
                    )

                    continue

                if frame_edit_choice == "2":

                    print("\n--- Frame Category ---")
                    print("1. Brand")
                    print("2. Non-Brand")

                    while True:

                        new_frame_category = input(
                            "Select Frame Category (1/2): "
                        ).strip()

                        if new_frame_category == "1":
                            frame_category = "1"

                            frame_brand = input(
                                "Enter Frame Brand: "
                            ).strip()

                            break

                        if new_frame_category == "2":
                            frame_category = "2"
                            frame_brand = "Non-Brand"
                            break

                        print(
                            "Please enter 1 or 2 only."
                        )

                    print(
                        "Frame Category updated successfully."
                    )

                    continue

                if (
                    frame_category == "1"
                    and frame_edit_choice == "3"
                ):

                    frame_brand = input(
                        "Enter Frame Brand: "
                    ).strip()

                    print(
                        "Frame Brand updated successfully."
                    )

                    continue

                if (
                    (
                        frame_category == "1"
                        and frame_edit_choice == "4"
                    )
                    or (
                        frame_category == "2"
                        and frame_edit_choice == "3"
                    )
                ):

                    frame_offer = normalize_offer(
                        input("Enter Frame Offer (Example: 10 or 10%): ")
                    )
                    print(
                        "Frame Offer updated successfully."
                    )

                    continue

                if (
                    (
                        frame_category == "1"
                        and frame_edit_choice == "5"
                    )
                    or (
                        frame_category == "2"
                        and frame_edit_choice == "4"
                    )
                ):

                    while True:

                        try:
                            new_frame_price = float(
                                input(
                                    "Enter Frame Price: "
                                ).strip()
                            )

                            if new_frame_price < 0:
                                print(
                                    "Frame Price cannot be negative."
                                )
                                continue

                            new_order_total = (
                                new_frame_price + lens_price
                            )

                            if less_amount > new_order_total:
                                print(
                                    "Frame Price cannot be reduced "
                                    "to this amount because the current "
                                    "Less Amount would be greater than "
                                    "Order Total."
                                )
                                continue

                            new_total_amount = (
                                new_order_total - less_amount
                            )

                            if advance_amount > new_total_amount:
                                print(
                                    "Frame Price cannot be reduced "
                                    "to this amount because the current "
                                    "Advance Amount would be greater than "
                                    "Final Total Amount."
                                )
                                continue

                            frame_price = new_frame_price
                            break

                        except ValueError:
                            print(
                                "Please enter Frame Price "
                                "using numbers only."
                            )

                    print(
                        "Frame Price updated successfully."
                    )

                    continue

                print(
                    "Please select a valid Frame Details option."
                )
            continue
        if review_choice == "3":

            while True:

                has_previous_rx = (
                    spectacle_history == "Existing"
                    and "has_previous_prescription" in globals()
                    and has_previous_prescription == "y"
                )

                print("\n--- Prescription & Eye Details ---")
                print("1. Prescription Source")
                print("2. Spectacle History")

                if has_previous_rx:
                    print("3. Previous Prescription")
                    print("4. Eye Surgery / IOL History")
                    print("5. Current Prescription")
                    print("6. PD / Vision Details")
                    print("7. Back")
                else:
                    print("3. Eye Surgery / IOL History")
                    print("4. Current Prescription")
                    print("5. PD / Vision Details")
                    print("6. Back")

                prescription_edit_choice = input(
                    "Select Field / Section: "
                ).strip()

                if (
                    has_previous_rx
                    and prescription_edit_choice == "7"
                ):
                    break

                if (
                    not has_previous_rx
                    and prescription_edit_choice == "6"
                ):
                    break

                # ------------------------------------------
                # 1. PRESCRIPTION SOURCE
                # ------------------------------------------
                if prescription_edit_choice == "1":

                    print("\n--- Edit Prescription Source ---")
                    print("1. In-Store Refraction")
                    print("2. External Prescription")

                    while True:

                        new_source_choice = input(
                            "Select Prescription Source (1/2): "
                        ).strip()

                        if new_source_choice == "1":
                            prescription_source = (
                                "In-Store Refraction"
                            )
                            prescription_from = ""
                            break

                        if new_source_choice == "2":
                            prescription_source = (
                                "External Prescription"
                            )

                            prescription_from = input(
                                "Prescription From "
                                "(Optional - Hospital / Doctor / "
                                "Optical Shop): "
                            ).strip()

                            break

                        print("Please select 1 or 2.")

                    print(
                        "Prescription Source updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 2. SPECTACLE HISTORY
                # ------------------------------------------
                if prescription_edit_choice == "2":

                    print("\n--- Edit Spectacle History ---")
                    print("1. First-time Spectacle User")
                    print("2. Existing Spectacle User")

                    while True:

                        new_history_choice = input(
                            "Select Spectacle History (1/2): "
                        ).strip()

                        if new_history_choice == "1":

                            spectacle_history = "First-time"
                            years_using_glasses = ""
                            has_previous_prescription = "n"

                            previous_prescription_date = ""

                            previous_right_sph = ""
                            previous_right_cyl = ""
                            previous_right_axis = ""
                            previous_right_add = ""

                            previous_left_sph = ""
                            previous_left_cyl = ""
                            previous_left_axis = ""
                            previous_left_add = ""

                            print(
                                "Spectacle History updated to "
                                "First-time."
                            )
                            break

                        if new_history_choice == "2":

                            spectacle_history = "Existing"

                            years_using_glasses = input(
                                "How long have you been "
                                "using glasses?: "
                            ).strip()

                            print(
                                "\nDo you have previous "
                                "prescription details?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                previous_rx_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if previous_rx_choice == "1":
                                    has_previous_prescription = "y"
                                    break

                                if previous_rx_choice == "2":
                                    has_previous_prescription = "n"

                                    previous_prescription_date = ""

                                    previous_right_sph = ""
                                    previous_right_cyl = ""
                                    previous_right_axis = ""
                                    previous_right_add = ""

                                    previous_left_sph = ""
                                    previous_left_cyl = ""
                                    previous_left_axis = ""
                                    previous_left_add = ""

                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            print(
                                "Spectacle History updated "
                                "successfully."
                            )
                            break

                        print("Please select 1 or 2.")

                    continue

                # ------------------------------------------
                # 3. PREVIOUS PRESCRIPTION
                # Only shown when previous Rx is available
                # ------------------------------------------
                if (
                    has_previous_rx
                    and prescription_edit_choice == "3"
                ):

                    while True:

                        print("\n--- Edit Previous Prescription ---")
                        print(
                            "1. Previous Prescription Date"
                        )
                        print("2. Right Eye (OD) SPH")
                        print("3. Right Eye (OD) CYL")
                        print("4. Right Eye (OD) AXIS")
                        print("5. Right Eye (OD) ADD")
                        print("6. Left Eye (OS) SPH")
                        print("7. Left Eye (OS) CYL")
                        print("8. Left Eye (OS) AXIS")
                        print("9. Left Eye (OS) ADD")
                        print("10. Back")

                        previous_edit_choice = input(
                            "Select Field (1-10): "
                        ).strip()

                        if previous_edit_choice == "10":
                            break

                        if previous_edit_choice == "1":

                            while True:

                                new_previous_date = input(
                                    "Enter Previous Prescription Date "
                                    "(DD-MM-YYYY, Optional - "
                                    "press Enter if unknown): "
                                ).strip()

                                if new_previous_date == "":
                                    previous_prescription_date = ""
                                    break

                                try:
                                    parsed_previous_date = (
                                        datetime.strptime(
                                            new_previous_date,
                                            "%d-%m-%Y"
                                        )
                                    )

                                    previous_prescription_date = (
                                        parsed_previous_date.strftime(
                                            "%d-%m-%Y"
                                        )
                                    )
                                    break

                                except ValueError:
                                    print(
                                        "Invalid date. Please enter "
                                        "date as DD-MM-YYYY "
                                        "or leave blank."
                                    )

                            print(
                                "Previous Prescription Date "
                                "updated successfully."
                            )
                            continue

                        if previous_edit_choice == "2":
                            previous_right_sph = get_old_sph(
                                "Right Eye"
                            )
                            print(
                                "Right Eye SPH updated successfully."
                            )
                            continue

                        if previous_edit_choice == "3":
                            previous_right_cyl = get_old_cyl(
                                "Right Eye"
                            )
                            print(
                                "Right Eye CYL updated successfully."
                            )
                            continue

                        if previous_edit_choice == "4":
                            previous_right_axis = get_old_axis(
                                "Right Eye"
                            )
                            print(
                                "Right Eye AXIS updated successfully."
                            )
                            continue

                        if previous_edit_choice == "5":

                            while True:

                                new_right_add = input(
                                    "Enter Right Eye ADD / "
                                    "Near Power "
                                    "(Optional - press Enter "
                                    "if not required): "
                                ).strip()

                                if new_right_add in ("", "0"):
                                    previous_right_add = ""
                                    break

                                if new_right_add.startswith("+"):
                                    number_part = new_right_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1] in [
                                            "00", "25", "50", "75"
                                        ]
                                        and float(number_part) <= 5
                                    ):
                                        previous_right_add = (
                                            new_right_add
                                        )
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50, "
                                    "+2.00 or leave blank."
                                )

                            print(
                                "Right Eye ADD updated successfully."
                            )
                            continue

                        if previous_edit_choice == "6":
                            previous_left_sph = get_old_sph(
                                "Left Eye"
                            )
                            print(
                                "Left Eye SPH updated successfully."
                            )
                            continue

                        if previous_edit_choice == "7":
                            previous_left_cyl = get_old_cyl(
                                "Left Eye"
                            )
                            print(
                                "Left Eye CYL updated successfully."
                            )
                            continue

                        if previous_edit_choice == "8":
                            previous_left_axis = get_old_axis(
                                "Left Eye"
                            )
                            print(
                                "Left Eye AXIS updated successfully."
                            )
                            continue

                        if previous_edit_choice == "9":

                            while True:

                                new_left_add = input(
                                    "Enter Left Eye ADD / "
                                    "Near Power "
                                    "(Optional - press Enter "
                                    "if not required): "
                                ).strip()

                                if new_left_add in ("", "0"):
                                    previous_left_add = ""
                                    break

                                if new_left_add.startswith("+"):
                                    number_part = new_left_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1] in [
                                            "00", "25", "50", "75"
                                        ]
                                        and float(number_part) <= 5
                                    ):
                                        previous_left_add = (
                                            new_left_add
                                        )
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50, "
                                    "+2.00 or leave blank."
                                )

                            print(
                                "Left Eye ADD updated successfully."
                            )
                            continue

                        print(
                            "Please select a number from 1 to 10."
                        )

                    continue

                # ------------------------------------------
                # EYE SURGERY / IOL HISTORY
                # Previous Rx available  -> Option 4
                # Previous Rx unavailable -> Option 3
                # ------------------------------------------
                eye_surgery_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "4"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "3"
                    )
                )

                if eye_surgery_selected:

                    print("\n--- Edit Eye Surgery / IOL History ---")
                    print("1. No Eye Surgery")
                    print("2. Right Eye (OD)")
                    print("3. Left Eye (OS)")
                    print("4. Both Eyes")

                    while True:

                        new_surgery_choice = input(
                            "Select Eye Surgery Status "
                            "(1/2/3/4): "
                        ).strip()

                        if new_surgery_choice == "1":

                            eye_surgery = "No"
                            surgery_eye = ""
                            right_iol = "No"
                            left_iol = "No"

                            break

                        if new_surgery_choice == "2":

                            eye_surgery = "Yes"
                            surgery_eye = "Right Eye (OD)"
                            left_iol = "No"

                            print(
                                "\nRight Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_right_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_right_iol_choice == "1":
                                    right_iol = "Yes"
                                    break

                                if new_right_iol_choice == "2":
                                    right_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        if new_surgery_choice == "3":

                            eye_surgery = "Yes"
                            surgery_eye = "Left Eye (OS)"
                            right_iol = "No"

                            print(
                                "\nLeft Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_left_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_left_iol_choice == "1":
                                    left_iol = "Yes"
                                    break

                                if new_left_iol_choice == "2":
                                    left_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        if new_surgery_choice == "4":

                            eye_surgery = "Yes"
                            surgery_eye = "Both Eyes"

                            print(
                                "\nRight Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_right_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_right_iol_choice == "1":
                                    right_iol = "Yes"
                                    break

                                if new_right_iol_choice == "2":
                                    right_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            print(
                                "\nLeft Eye IOL implanted?"
                            )
                            print("1. Yes")
                            print("2. No")

                            while True:

                                new_left_iol_choice = input(
                                    "Select (1/2): "
                                ).strip()

                                if new_left_iol_choice == "1":
                                    left_iol = "Yes"
                                    break

                                if new_left_iol_choice == "2":
                                    left_iol = "No"
                                    break

                                print(
                                    "Please select 1 for Yes "
                                    "or 2 for No."
                                )

                            break

                        print(
                            "Please select 1, 2, 3 or 4."
                        )

                    print(
                        "Eye Surgery / IOL History "
                        "updated successfully."
                    )
                    continue

                # ------------------------------------------
                # CURRENT PRESCRIPTION
                # Previous Rx available  -> Option 5
                # Previous Rx unavailable -> Option 4
                # ------------------------------------------
                current_rx_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "5"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "4"
                    )
                )

                if current_rx_selected:

                    while True:

                        print("\n--- Edit Current Prescription ---")
                        print("1. Right Eye (OD) SPH")
                        print("2. Right Eye (OD) CYL")
                        print("3. Right Eye (OD) AXIS")

                        if (
                            lens_type_choice != "1"
                            and add_requirement != "3"
                        ):
                            print("4. Right Eye (OD) ADD")
                        else:
                            print("4. Right Eye (OD) ADD - Not Required")

                        print("5. Left Eye (OS) SPH")
                        print("6. Left Eye (OS) CYL")
                        print("7. Left Eye (OS) AXIS")

                        if (
                            lens_type_choice != "1"
                            and add_requirement != "2"
                        ):
                            print("8. Left Eye (OS) ADD")
                        else:
                            print("8. Left Eye (OS) ADD - Not Required")

                        print("9. Back")

                        current_rx_edit_choice = input(
                            "Select Field (1-9): "
                        ).strip()

                        if current_rx_edit_choice == "9":
                            break

                        # ----------------------------------
                        # 1. RIGHT EYE (OD) SPH
                        # ----------------------------------
                        if current_rx_edit_choice == "1":

                            while True:

                                new_right_sph = input(
                                    "Enter Right Eye SPH (+/-): "
                                ).strip()

                                if new_right_sph.lower() == "plano":
                                    right_sph = "Plano"
                                    break

                                if new_right_sph == "0":
                                    right_sph = "0"
                                    break

                                if new_right_sph.startswith(("+", "-")):
                                    number_part = new_right_sph[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 30
                                    ):
                                        right_sph = new_right_sph
                                        break

                                print(
                                    "Invalid SPH. Enter like "
                                    "-1.00, +1.25, 0 or Plano."
                                )

                            print(
                                "Right Eye SPH updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 2. RIGHT EYE (OD) CYL
                        # ----------------------------------
                        if current_rx_edit_choice == "2":

                            while True:

                                new_right_cyl = input(
                                    "Enter Right Eye CYL (+/-): "
                                ).strip()

                                if new_right_cyl == "":
                                    right_cyl = ""
                                    break

                                if new_right_cyl == "0":
                                    right_cyl = "0"
                                    break

                                if new_right_cyl.startswith(("+", "-")):
                                    number_part = new_right_cyl[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 10
                                    ):
                                        right_cyl = new_right_cyl
                                        break

                                print(
                                    "Invalid CYL. Enter like "
                                    "-0.50, +1.25, 0 or leave blank."
                                )

                            print(
                                "Right Eye CYL updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 3. RIGHT EYE (OD) AXIS
                        # ----------------------------------
                        if current_rx_edit_choice == "3":

                            while True:

                                new_right_axis = input(
                                    "Enter Right Eye AXIS (0-180): "
                                ).strip()

                                if new_right_axis == "":
                                    right_axis = ""
                                    break

                                if new_right_axis.isdigit():
                                    axis_value = int(new_right_axis)

                                    if 0 <= axis_value <= 180:
                                        right_axis = new_right_axis
                                        break

                                print(
                                    "Invalid AXIS. Enter a number "
                                    "from 0 to 180 or leave blank."
                                )

                            print(
                                "Right Eye AXIS updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 4. RIGHT EYE (OD) ADD
                        # ----------------------------------
                        if current_rx_edit_choice == "4":

                            if (
                                lens_type_choice == "1"
                                or add_requirement == "3"
                            ):
                                right_add = ""
                                print(
                                    "Right Eye ADD is Not Required."
                                )
                                continue

                            while True:

                                new_right_add = input(
                                    "Enter Right Eye ADD / "
                                    "Near Power (+): "
                                ).strip()

                                if new_right_add in ["", "0"]:
                                    print(
                                        "ADD is required for Right Eye."
                                    )
                                    continue

                                if new_right_add.startswith("+"):
                                    number_part = new_right_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 5
                                    ):
                                        right_add = new_right_add
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50 or +2.00."
                                )

                            print(
                                "Right Eye ADD updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 5. LEFT EYE (OS) SPH
                        # ----------------------------------
                        if current_rx_edit_choice == "5":

                            while True:

                                new_left_sph = input(
                                    "Enter Left Eye SPH (+/-): "
                                ).strip()

                                if new_left_sph.lower() == "plano":
                                    left_sph = "Plano"
                                    break

                                if new_left_sph == "0":
                                    left_sph = "0"
                                    break

                                if new_left_sph.startswith(("+", "-")):
                                    number_part = new_left_sph[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 30
                                    ):
                                        left_sph = new_left_sph
                                        break

                                print(
                                    "Invalid SPH. Enter like "
                                    "-1.00, +1.25, 0 or Plano."
                                )

                            print(
                                "Left Eye SPH updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 6. LEFT EYE (OS) CYL
                        # ----------------------------------
                        if current_rx_edit_choice == "6":

                            while True:

                                new_left_cyl = input(
                                    "Enter Left Eye CYL (+/-): "
                                ).strip()

                                if new_left_cyl == "":
                                    left_cyl = ""
                                    break

                                if new_left_cyl == "0":
                                    left_cyl = "0"
                                    break

                                if new_left_cyl.startswith(("+", "-")):
                                    number_part = new_left_cyl[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 10
                                    ):
                                        left_cyl = new_left_cyl
                                        break

                                print(
                                    "Invalid CYL. Enter like "
                                    "-1.00, +0.50, 0 or leave blank."
                                )

                            print(
                                "Left Eye CYL updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 7. LEFT EYE (OS) AXIS
                        # ----------------------------------
                        if current_rx_edit_choice == "7":

                            while True:

                                new_left_axis = input(
                                    "Enter Left Eye AXIS (0-180): "
                                ).strip()

                                if new_left_axis == "":
                                    left_axis = ""
                                    break

                                if new_left_axis.isdigit():
                                    axis_value = int(new_left_axis)

                                    if 0 <= axis_value <= 180:
                                        left_axis = new_left_axis
                                        break

                                print(
                                    "Invalid AXIS. Enter a number "
                                    "from 0 to 180 or leave blank."
                                )

                            print(
                                "Left Eye AXIS updated successfully."
                            )
                            continue

                        # ----------------------------------
                        # 8. LEFT EYE (OS) ADD
                        # ----------------------------------
                        if current_rx_edit_choice == "8":

                            if (
                                lens_type_choice == "1"
                                or add_requirement == "2"
                            ):
                                left_add = ""
                                print(
                                    "Left Eye ADD is Not Required."
                                )
                                continue

                            while True:

                                new_left_add = input(
                                    "Enter Left Eye ADD / "
                                    "Near Power (+): "
                                ).strip()

                                if new_left_add in ["", "0"]:
                                    print(
                                        "ADD is required for Left Eye."
                                    )
                                    continue

                                if new_left_add.startswith("+"):
                                    number_part = new_left_add[1:]
                                    parts = number_part.split(".")

                                    if (
                                        len(parts) == 2
                                        and parts[0].isdigit()
                                        and len(parts[1]) == 2
                                        and parts[1]
                                        in ["00", "25", "50", "75"]
                                        and float(number_part) <= 5
                                    ):
                                        left_add = new_left_add
                                        break

                                print(
                                    "Invalid ADD. Enter like "
                                    "+1.00, +1.25, +1.50 or +2.00."
                                )

                            print(
                                "Left Eye ADD updated successfully."
                            )
                            continue

                        print(
                            "Please select a number from 1 to 9."
                        )
                    continue

                # ------------------------------------------
                # PD / VISION DETAILS
                # Previous Rx available  -> Option 6
                # Previous Rx unavailable -> Option 5
                # ------------------------------------------
                pd_vision_selected = (
                    (
                        has_previous_rx
                        and prescription_edit_choice == "6"
                    )
                    or (
                        not has_previous_rx
                        and prescription_edit_choice == "5"
                    )
                )

                if pd_vision_selected:

                    while True:

                        print("\n--- Edit PD / Vision Details ---")
                        print("1. Distance PD")
                        print("2. Near PD")
                        print("3. Right Eye Visual Acuity")
                        print("4. Left Eye Visual Acuity")
                        print("5. Right Eye Pinhole")
                        print("6. Left Eye Pinhole")
                        print("7. Back")

                        pd_vision_edit_choice = input(
                            "Select Field (1-7): "
                        ).strip()

                        if pd_vision_edit_choice == "1":
                            distance_pd = input(
                                "Enter Distance PD in mm "
                                "(Example: 62, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Distance PD updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "2":
                            near_pd = input(
                                "Enter Near PD in mm "
                                "(Example: 59, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Near PD updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "3":
                            right_va = input(
                                "Right Eye Visual Acuity "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Right Eye Visual Acuity "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "4":
                            left_va = input(
                                "Left Eye Visual Acuity "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Left Eye Visual Acuity "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "5":
                            right_pinhole = input(
                                "Right Eye Pinhole "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Right Eye Pinhole "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "6":
                            left_pinhole = input(
                                "Left Eye Pinhole "
                                "(Example: 6/6, press Enter "
                                "if not measured): "
                            ).strip()

                            print(
                                "Left Eye Pinhole "
                                "updated successfully."
                            )
                            continue

                        if pd_vision_edit_choice == "7":
                            break

                        print(
                            "Please select a number from 1 to 7."
                        )

                    continue

                print(
                    "Please select a valid "
                    "Prescription / Eye Details option."
                )
            continue
        if review_choice == "4":

            while True:

                print("\n--- Edit Lens Details ---")
                print("1. Lens Type")

                if lens_type != "Single Vision":
                    print("2. ADD Requirement")
                else:
                    print("2. ADD Requirement - Not Required")

                print("3. Lens Features / Coating")
                print("4. Lens Brand")
                print("5. Lens Offer")
                print("6. Lens Price")
                print("7. Back")

                lens_edit_choice = input(
                    "Select Field (1-7): "
                ).strip()

                # ------------------------------------------
                # 1. LENS TYPE
                # ------------------------------------------
                if lens_edit_choice == "1":

                    print("\n--- Edit Lens Type ---")
                    print("1. Single Vision")
                    print("2. Bifocal")

                    while True:

                        new_lens_type_choice = input(
                            "Select Lens Type (1/2): "
                        ).strip()

                        if new_lens_type_choice == "1":

                            lens_type_choice = "1"
                            lens_type = "Single Vision"
                            add_requirement = ""

                            right_add = ""
                            left_add = ""

                            break

                        if new_lens_type_choice == "2":

                            lens_type_choice = "2"

                            print("\n--- Bifocal Type ---")
                            print("1. Kryptok Bifocal")
                            print("2. D Bifocal")
                            print("3. Progressive Bifocal")
                            print("4. Other")

                            while True:

                                new_bifocal_choice = input(
                                    "Select Bifocal Type "
                                    "(1/2/3/4): "
                                ).strip()

                                if new_bifocal_choice == "1":
                                    lens_type = "Kryptok Bifocal"
                                    break

                                if new_bifocal_choice == "2":
                                    lens_type = "D Bifocal"
                                    break

                                if new_bifocal_choice == "3":
                                    lens_type = (
                                        "Progressive Bifocal"
                                    )
                                    break

                                if new_bifocal_choice == "4":
                                    lens_type = "Other"
                                    break

                                print(
                                    "Invalid option. Please select "
                                    "1, 2, 3 or 4."
                                )

                            print("\n--- ADD Requirement ---")
                            print("1. Both Eyes")
                            print("2. Right Eye (OD) Only")
                            print("3. Left Eye (OS) Only")

                            while True:

                                add_requirement = input(
                                    "Select ADD Requirement "
                                    "(1/2/3): "
                                ).strip()

                                if add_requirement in [
                                    "1", "2", "3"
                                ]:
                                    break

                                print(
                                    "Invalid option. Please select "
                                    "1, 2 or 3."
                                )

                            if add_requirement == "2":
                                left_add = ""

                            elif add_requirement == "3":
                                right_add = ""

                            break

                        print(
                            "Invalid option. Please select 1 or 2."
                        )

                    print(
                        "Lens Type updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 2. ADD REQUIREMENT
                # ------------------------------------------
                if lens_edit_choice == "2":

                    if lens_type == "Single Vision":
                        add_requirement = ""
                        right_add = ""
                        left_add = ""

                        print(
                            "ADD Requirement is Not Required "
                            "for Single Vision."
                        )
                        continue

                    print("\n--- Edit ADD Requirement ---")
                    print("1. Both Eyes")
                    print("2. Right Eye (OD) Only")
                    print("3. Left Eye (OS) Only")

                    while True:

                        new_add_requirement = input(
                            "Select ADD Requirement "
                            "(1/2/3): "
                        ).strip()

                        if new_add_requirement in [
                            "1", "2", "3"
                        ]:
                            add_requirement = (
                                new_add_requirement
                            )
                            break

                        print(
                            "Invalid option. Please select "
                            "1, 2 or 3."
                        )

                    if add_requirement == "2":
                        left_add = ""

                    elif add_requirement == "3":
                        right_add = ""

                    print(
                        "ADD Requirement updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 3. LENS FEATURES / COATING
                # ------------------------------------------
                if lens_edit_choice == "3":

                    while True:

                        new_lens_features = input(
                            "Enter Lens Features / Coating "
                            "(Optional): "
                        ).strip().title()

                        normalized_features = (
                            new_lens_features.lower()
                            .replace(".", " ")
                            .replace("-", " ")
                            .replace("/", " ")
                            .replace(",", " ")
                            .replace("_", " ")
                        )

                        feature_words = (
                            normalized_features.split()
                        )

                        has_kt = (
                            "kt" in feature_words
                            or "kryptok" in feature_words
                        )

                        has_progressive = (
                            "progressive" in feature_words
                        )

                        has_d_bifocal = (
                            "d bifocal"
                            in normalized_features
                            or "dbifocal"
                            in normalized_features
                        )

                        if lens_type == "Single Vision":

                            if has_kt:
                                print(
                                    "KT / Kryptok is a Bifocal "
                                    "type and cannot be used "
                                    "with Single Vision."
                                )
                                continue

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with Single Vision."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Single Vision."
                                )
                                continue

                        elif lens_type == "Kryptok Bifocal":

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with Kryptok Bifocal."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Kryptok Bifocal."
                                )
                                continue

                        elif lens_type == "D Bifocal":

                            if has_kt:
                                print(
                                    "KT / Kryptok cannot be used "
                                    "with D Bifocal."
                                )
                                continue

                            if has_progressive:
                                print(
                                    "Progressive cannot be used "
                                    "with D Bifocal."
                                )
                                continue

                        elif lens_type == "Progressive Bifocal":

                            if has_kt:
                                print(
                                    "KT / Kryptok cannot be used "
                                    "with Progressive Bifocal."
                                )
                                continue

                            if has_d_bifocal:
                                print(
                                    "D Bifocal cannot be used "
                                    "with Progressive Bifocal."
                                )
                                continue

                        lens_features = new_lens_features
                        break

                    print(
                        "Lens Features / Coating "
                        "updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 4. LENS BRAND
                # ------------------------------------------
                if lens_edit_choice == "4":

                    lens_brand = input(
                        "Enter Lens Brand (Optional): "
                    ).strip().title()

                    print(
                        "Lens Brand updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 5. LENS OFFER
                # ------------------------------------------
                if lens_edit_choice == "5":

                    lens_offer = normalize_offer(
                        input("Enter Lens Offer (Example: 10 or 10%): ")
                    )
                    print(
                        "Lens Offer updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 6. LENS PRICE
                # ------------------------------------------
                if lens_edit_choice == "6":

                    while True:

                        new_lens_price_input = input(
                            "Enter Lens Price: "
                        ).strip()

                        try:
                            new_lens_price = float(
                                new_lens_price_input
                            )

                            if new_lens_price < 0:
                                print(
                                    "Lens Price cannot be negative."
                                )
                                continue

                            lens_price = new_lens_price
                            break

                        except ValueError:
                            print(
                                "Please enter Lens Price "
                                "using numbers only."
                            )

                    # Recalculate all dependent payment values
                    order_total = frame_price + lens_price

                    if less_amount > order_total:
                        less_amount = order_total

                    total_amount = (
                        order_total - less_amount
                    )

                    if advance_amount > total_amount:
                        advance_amount = total_amount

                    balance = (
                        total_amount - advance_amount
                    )

                    print(
                        "Lens Price updated successfully."
                    )
                    continue

                # ------------------------------------------
                # 7. BACK
                # ------------------------------------------
                if lens_edit_choice == "7":
                    break

                print(
                    "Please select a number from 1 to 7."
                )

            continue
        if review_choice == "5":

            while True:

                print("\n--- Edit Payment Details ---")
                print(f"Order Total    : ₹{order_total:.2f}")
                print(f"Less Amount    : ₹{less_amount:.2f}")
                print(f"Final Total    : ₹{total_amount:.2f}")
                print(f"Advance Amount : ₹{advance_amount:.2f}")
                print(f"Balance        : ₹{balance:.2f}")

                print("\n1. Less Amount")
                print("2. Advance Amount")
                print("3. Back")

                payment_edit_choice = input(
                    "Select Field / Back (1/2/3): "
                ).strip()

                if payment_edit_choice == "3":
                    break

                if payment_edit_choice == "1":

                    while True:

                        new_less_input = input(
                            "Enter Less Amount "
                            "(Optional - press Enter for 0): "
                        ).strip()

                        if new_less_input == "":
                            new_less_amount = 0.0
                        else:
                            try:
                                new_less_amount = float(
                                    new_less_input
                                )
                            except ValueError:
                                print(
                                    "Please enter Less Amount "
                                    "using numbers only."
                                )
                                continue

                        if new_less_amount < 0:
                            print(
                                "Less Amount cannot be negative."
                            )
                            continue

                        if new_less_amount > order_total:
                            print(
                                "Less Amount cannot be greater "
                                "than Order Total."
                            )
                            continue

                        new_total_amount = (
                            order_total - new_less_amount
                        )

                        if advance_amount > new_total_amount:
                            print(
                                "This Less Amount cannot be used "
                                "because the current Advance Amount "
                                "would be greater than "
                                "Final Total Amount."
                            )
                            continue

                        less_amount = new_less_amount
                        total_amount = new_total_amount
                        balance = (
                            total_amount - advance_amount
                        )
                        break

                    print(
                        "Less Amount updated successfully."
                    )
                    continue

                if payment_edit_choice == "2":

                    while True:

                        new_advance_input = input(
                            "Enter Advance Amount: "
                        ).strip()

                        try:
                            new_advance_amount = float(
                                new_advance_input
                            )

                            if new_advance_amount < 0:
                                print(
                                    "Advance amount cannot be negative."
                                )
                                continue

                            if new_advance_amount > total_amount:
                                print(
                                    "Advance amount cannot be greater "
                                    "than Final Total Amount."
                                )
                                continue

                            advance_amount = new_advance_amount
                            balance = (
                                total_amount - advance_amount
                            )
                            break

                        except ValueError:
                            print(
                                "Please enter amount "
                                "using numbers only."
                            )

                    print(
                        "Advance Amount updated successfully."
                    )
                    continue

                print(
                    "Please select 1, 2 or 3."
                )

            continue
        if review_choice == "6":

            while True:

                print("\n--- Edit Delivery Details ---")
                print("1. Delivery Status")

                if delivery_status == "Pending":
                    print("2. Back")

                elif (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                ):
                    print("2. Delivered To")
                    print("3. Back")

                else:
                    print("2. Delivered To")
                    print("3. Receiver Name")
                    print("4. Back")

                delivery_edit_choice = input(
                    "Select Field / Back: "
                ).strip()

                if (
                    delivery_status == "Pending"
                    and delivery_edit_choice == "2"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Customer / Same Person"
                    and delivery_edit_choice == "3"
                ):
                    break

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "4"
                ):
                    break

                if delivery_edit_choice == "1":

                    while True:

                        print("\n--- Delivery Status ---")
                        print("1. Delivered")
                        print("2. Pending")

                        new_delivery_choice = input(
                            "Select Delivery Status (1/2): "
                        ).strip()

                        if new_delivery_choice == "1":
                            delivery_status = "Delivered"
                            delivered_to = (
                                "Customer / Same Person"
                            )
                            receiver_name = ""
                            break

                        if new_delivery_choice == "2":
                            delivery_status = "Pending"
                            delivered_to = ""
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivery Status updated successfully."
                    )
                    continue

                if (
                    delivery_status == "Delivered"
                    and delivery_edit_choice == "2"
                ):

                    while True:

                        print("\n--- Delivered To ---")
                        print("1. Customer / Same Person")
                        print("2. Other Person")

                        new_delivered_to_choice = input(
                            "Select Delivered To (1/2): "
                        ).strip()

                        if new_delivered_to_choice == "1":
                            delivered_to = (
                                "Customer / Same Person"
                            )
                            receiver_name = ""
                            break

                        if new_delivered_to_choice == "2":
                            delivered_to = "Other Person"
                            receiver_name = ""
                            break

                        print("Please select 1 or 2.")

                    print(
                        "Delivered To updated successfully."
                    )
                    continue

                if (
                    delivery_status == "Delivered"
                    and delivered_to == "Other Person"
                    and delivery_edit_choice == "3"
                ):

                    receiver_name = input(
                        "Enter Receiver Name "
                        "(Optional - press Enter to skip): "
                    ).strip().title()

                    print(
                        "Receiver Name updated successfully."
                    )
                    continue

                print(
                    "Please select a valid "
                    "Delivery Details option."
                )

            continue
# ==================================================
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
        PAYMENT_DATA_FILE,
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
            delivery_status,
            payment_datetime if delivery_status == "Delivered" else "",
            delivered_to,
            receiver_name
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
if store_address:
    print(
        "Store Address:",
        store_address
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

if order_type in ["2", "3"]:
    if order_type in ["2", "3"]:
       print("Prescription Source:", prescription_source)

    if (
        prescription_source == "External Prescription"
        and prescription_from
    ):
        print("Prescription From:", prescription_from)

    print("\n--- Eye Surgery / IOL History ---")

    if eye_surgery == "No":
        print("Eye Surgery: No")

    else:
        print("Eye Surgery: Yes")
        print("Surgery Eye:", surgery_eye)

        if surgery_eye in ["Right Eye (OD)", "Both Eyes"]:
            print("Right Eye IOL:", right_iol)

        if surgery_eye in ["Left Eye (OS)", "Both Eyes"]:
            print("Left Eye IOL:", left_iol)


# ---------------- PREVIOUS PRESCRIPTION ----------------

if spectacle_history == "Existing":

    print("\n--- Previous Prescription ---")

    print(
        "Using Glasses Since:",
        years_using_glasses
    )
    if previous_prescription_date:
        print(
            "Previous Prescription Date:",
            previous_prescription_date
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
csv_file_exists = os.path.exists(CUSTOMER_DATA_FILE)
# Save customer record to CSV
with open(CUSTOMER_DATA_FILE, "a", newline="", encoding="utf-8") as file:
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
    "Full Address",
    "Order Total",
    "Less Amount",
    "Eye Surgery",
    "Surgery Eye",
    "Right Eye IOL",
    "Left Eye IOL",
    "Previous Prescription Date",
    "Prescription Source",
    "Prescription From",
    "C/O / S/O Details",
    "Delivery Status",
    "Delivered To",
    "Receiver Name"
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
    order_total,
    less_amount,
    eye_surgery,
    surgery_eye,
    right_iol,
    left_iol,
    previous_prescription_date,
     prescription_source,
    prescription_from,
    customer_relation,
    delivery_status,
    delivered_to,
    receiver_name
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
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}
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
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}
Date: {record_date}
Time: {record_time}
Prescription Source: {prescription_source}
{f"Prescription From: {prescription_from}" if prescription_source == "External Prescription" and prescription_from else ""}
{("Prescription details are as provided in the external prescription." if prescription_source == "External Prescription" else "Prescription details are based on the existing prescription on record." if prescription_source == "Existing Prescription on Record" else "")}

Spectacle Prescription
Right Eye (OD):
SPH: {right_sph}
CYL: {right_cyl}
AXIS: {right_axis if right_axis else "Not Required"}
ADD: {right_add if right_add else "Not Required"}

Left Eye (OS):
SPH: {left_sph}
CYL: {left_cyl}
AXIS: {left_axis if left_axis else "Not Required"}
ADD: {left_add if left_add else "Not Required"}
{f"Pupillary Distance (PD):\nDistance PD: {distance_pd}\nNear PD: {near_pd}\n" if distance_pd or near_pd else ""}

{f"Visual Acuity / Pinhole Test:\nRight Eye Visual Acuity: {right_va}\nLeft Eye Visual Acuity: {left_va}\nRight Eye Pinhole: {right_pinhole}\nLeft Eye Pinhole: {left_pinhole}\n" if right_va or left_va or right_pinhole or left_pinhole else ""}
Please keep this prescription for your reference.
"""
print(prescription_message)
print("\n--- Send Message ---")
print("1. SMS Text / Copy")

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
        print("SMS Text cannot be prepared - Customer phone number is not available.")
    else:
        sms_message = prescription_message

        print("\n--- SMS TEXT / COPY ---")
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

        if order_type == "1":
            payment_order_details = (
                "Order Type: Frame Only\n"
                f"Frame Details: {frame_details}\n"
                f"Frame Brand: {frame_brand}\n"
                f"Frame Price: ₹{frame_price}"
            )

        elif order_type == "2":
            payment_order_details = (
                "Order Type: Lenses Only\n"
                f"Lens Type: {lens_type}\n"
                f"{f'Lens Features / Coating: {lens_features}' if lens_features else ''}\n"
                f"{f'Lens Brand: {lens_brand}' if lens_brand else ''}\n"
                f"Lens Price: ₹{lens_price}"
            )

        else:
            payment_order_details = (
                "Order Type: Frame + Lenses\n"
                f"Frame Details: {frame_details}\n"
                f"Frame Brand: {frame_brand}\n"
                f"Lens Type: {lens_type}\n"
                f"{f'Lens Features / Coating: {lens_features}' if lens_features else ''}\n"
                f"{f'Lens Brand: {lens_brand}' if lens_brand else ''}\n"
                f"Frame & Lenses Price: ₹{order_total}"
            )
        payment_message = f"""{store_name}
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}

Payment Receipt

Order Details
{payment_order_details}

Payment Details
Order Total: ₹{order_total}
Less Amount: ₹{less_amount}
Final Total: ₹{total_amount}
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
{store_city}
{f"Address: {store_address}" if store_address else ""}
{f"Phone: {store_phone}" if store_phone else ""}

Customer Name: {customer_name}
Phone: {phone if phone else "Not Provided"}
Town / Village: {address}

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
# ==================================================
# PRINT HELPERS
# ==================================================

# ==================================================
# PRINT MENU
# ==================================================

print("\n--- Print ---")
print("1. Print Prescription")
print("2. Print Bill / Payment Receipt")
print("3. Print Full Customer Record")
print("4. Print Prescription + Bill")
print("5. Skip")

while True:
    print_choice = input(
        "Select Print Option (1/2/3/4/5): "
    ).strip()

    if print_choice in ["1", "2", "3", "4", "5"]:
        break

    print("Please select a valid Print Option (1-5).")
if print_choice == "1":
    if order_type in ["2", "3"]:
        print_text_document(
            prescription_message
        )
    else:
        print(
            "Prescription print is not available "
            "for Frame Only orders."
        )
if print_choice == "2":
    bill_print_text = f"""
{store_name}
{store_city}
{f"Address: {store_address}" if store_address else ""}
Phone: {store_phone}

PAYMENT RECEIPT
========================================

Customer Name : {customer_name}
Phone         : {phone}
Address       : {address}

----------------------------------------
Order Total   : Rs. {order_total}
Less Amount   : Rs. {less_amount}
Final Total   : Rs. {total_amount}
Advance       : Rs. {advance_amount}
Balance       : Rs. {balance}
----------------------------------------

Thank you for choosing {store_name}.
"""

    print_text_document(
        bill_print_text
    )

if print_choice == "3":
    full_record_lines = [
        store_name,
        store_city,
        f"Address: {store_address}" if store_address else "",
        f"Phone: {store_phone}",
        "",
        "FULL CUSTOMER RECORD",
        "=" * 45,
        "",
        "CUSTOMER DETAILS",
        f"Customer Name : {customer_name}",
        f"Gender        : {gender}",
        f"Age           : {age if age != '' else 'Not Provided'}",
        f"Phone         : {phone if phone else 'Not Provided'}",
        f"Town/Village  : {address}",
    ]
    if full_address:
        full_record_lines.append(
            f"Full Address  : {full_address}"
        )

    full_record_lines.extend([
        "",
        "SPECTACLE HISTORY",
        f"History       : {spectacle_history}",
    ])
    if spectacle_history == "Existing":
        full_record_lines.append(
            f"Using Glasses : {years_using_glasses}"
        )

        if previous_prescription_date:
            full_record_lines.append(
                f"Previous Rx Date: {previous_prescription_date}"
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
            full_record_lines.extend([
                "",
                "PREVIOUS PRESCRIPTION",
                (
                    "OD: "
                    f"SPH {previous_right_sph} | "
                    f"CYL {previous_right_cyl} | "
                    f"AXIS {previous_right_axis} | "
                    f"ADD {previous_right_add if previous_right_add else 'Not Required'}"
                ),
                (
                    "OS: "
                    f"SPH {previous_left_sph} | "
                    f"CYL {previous_left_cyl} | "
                    f"AXIS {previous_left_axis} | "
                    f"ADD {previous_left_add if previous_left_add else 'Not Required'}"
                ),
            ])

        if order_type in ["1", "3"]:
            full_record_lines.extend([
            "",
            "FRAME DETAILS",
            f"Frame Details : {frame_details}",
            f"Frame Brand   : {frame_brand if frame_brand else 'Not Provided'}",
            f"Frame Offer   : {frame_offer if frame_offer else 'None'}",
            f"Frame Price   : Rs. {frame_price}",
        ])

        if order_type in ["2", "3"]:
            full_record_lines.extend([
            "",
            "LENS DETAILS",
            f"Lens Type     : {lens_type}",
            f"Lens Features : {lens_features if lens_features else 'Not Provided'}",
            f"Lens Brand    : {lens_brand if lens_brand else 'Not Provided'}",
            f"Lens Offer    : {lens_offer if lens_offer else 'None'}",
            f"Lens Price    : Rs. {lens_price}",
        ])
            full_record_lines.extend([
            "",
            "CURRENT PRESCRIPTION",
            (
                "OD: "
                f"SPH {right_sph} | "
                f"CYL {right_cyl} | "
                f"AXIS {right_axis} | "
                f"ADD {right_add if right_add else 'Not Required'}"
            ),
            (
                "OS: "
                f"SPH {left_sph} | "
                f"CYL {left_cyl} | "
                f"AXIS {left_axis} | "
                f"ADD {left_add if left_add else 'Not Required'}"
            ),
        ])
        if distance_pd or near_pd:
            full_record_lines.extend([
                "",
                "PUPILLARY DISTANCE (PD)",
                f"Distance PD   : {distance_pd if distance_pd else 'Not Measured'}",
                f"Near PD       : {near_pd if near_pd else 'Not Measured'}",
            ])
            if any([
            right_va,
            left_va,
            right_pinhole,
            left_pinhole
        ]):
                full_record_lines.extend([
                "",
                "VISUAL ACUITY / PINHOLE",
                f"Right VA      : {right_va if right_va else 'Not Measured'}",
                f"Left VA       : {left_va if left_va else 'Not Measured'}",
                f"Right Pinhole : {right_pinhole if right_pinhole else 'Not Measured'}",
                f"Left Pinhole  : {left_pinhole if left_pinhole else 'Not Measured'}",
            ])
                full_record_lines.extend([
            "",
            "EYE SURGERY / IOL",
            f"Eye Surgery   : {eye_surgery}",
        ])

        if eye_surgery != "No":
            full_record_lines.append(
                f"Surgery Eye   : {surgery_eye}"
            )

            if surgery_eye in ["Right Eye (OD)", "Both Eyes"]:
                full_record_lines.append(
                    f"Right Eye IOL : {right_iol}"
                )

            if surgery_eye in ["Left Eye (OS)", "Both Eyes"]:
                full_record_lines.append(
                    f"Left Eye IOL  : {left_iol}"
                )


        full_record_lines.extend([
        "",
        "PAYMENT DETAILS",
        f"Order Total   : Rs. {order_total}",
        f"Less Amount   : Rs. {less_amount}",
        f"Final Total   : Rs. {total_amount}",
        f"Advance       : Rs. {advance_amount}",
        f"Balance       : Rs. {balance}",
        "",
        "=" * 45,
        f"Thank you for choosing {store_name}.",
    ])

    full_customer_record = "\n".join(
        full_record_lines
    )

    print_text_document(
        full_customer_record
    )

if print_choice == "4":
    if order_type in ["2", "3"]:
        prescription_bill_text = f"""{prescription_message}

========================================
PAYMENT RECEIPT
========================================

Customer Name : {customer_name}
Phone         : {phone}

Order Total   : Rs. {order_total}
Less Amount   : Rs. {less_amount}
Final Total   : Rs. {total_amount}
Advance       : Rs. {advance_amount}
Balance       : Rs. {balance}

Thank you for choosing {store_name}.
"""

        print_text_document(
            prescription_bill_text
        )

    else:
        print(
            "Prescription + Bill print is not available "
            "for Frame Only orders."
        )

input("\nPress Enter to close...")
