import csv

SOURCE_FILE = "customers.csv"
OUTPUT_FILE = "customers_normalized_preview.csv"

CURRENT_HEADER = [
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
]


def blank_row():
    return [""] * len(CURRENT_HEADER)


def normalize_row(row):
    new_row = blank_row()

    # Common first columns
    for i in range(min(6, len(row))):
        new_row[i] = row[i]

    row_len = len(row)

    # ---------------- 32 COLUMN OLD FORMAT ----------------
    if row_len == 32:
        new_row[5] = row[5]          # Name
        new_row[7] = row[6]          # Age
        new_row[8] = row[7]          # Phone
        new_row[9] = row[8]          # Address
        new_row[10] = row[9]         # Spectacle History
        new_row[11] = row[10]        # Years Using Glasses

        new_row[12:20] = row[11:19]  # Previous prescription

        new_row[20] = row[19]        # Frame Details
        new_row[24] = row[20]        # Lens Type

        new_row[28:36] = row[21:29]  # Current prescription

        new_row[42] = row[29]        # Total
        new_row[43] = row[30]        # Advance
        new_row[44] = row[31]        # Balance

    # ---------------- 36 COLUMN OLD FORMAT ----------------
    elif row_len == 36:
        new_row[5] = row[5]
        new_row[7] = row[6]
        new_row[8] = row[7]
        new_row[9] = row[8]
        new_row[10] = row[9]
        new_row[11] = row[10]

        new_row[12:20] = row[11:19]

        new_row[20] = row[19]
        new_row[24] = row[20]

        new_row[28:36] = row[21:29]

        new_row[38:42] = row[29:33]

        new_row[42] = row[33]
        new_row[43] = row[34]
        new_row[44] = row[35]

    # ---------------- 42 COLUMN OLD FORMAT ----------------
    elif row_len == 42:
        new_row[5] = row[5]
        new_row[7] = row[6]
        new_row[8] = row[7]
        new_row[9] = row[8]
        new_row[10] = row[9]
        new_row[11] = row[10]

        new_row[12:20] = row[11:19]

        new_row[20] = row[19]
        new_row[21] = row[20]
        new_row[22] = row[21]

        new_row[24] = row[22]
        new_row[25] = row[23]
        new_row[26] = row[24]

        new_row[28:36] = row[25:33]

        new_row[36] = row[33]
        new_row[37] = row[34]

        new_row[38:42] = row[35:39]

        new_row[42] = row[39]
        new_row[43] = row[40]
        new_row[44] = row[41]

    # ---------------- 44 COLUMN OLD FORMAT ----------------
    elif row_len == 44:
        new_row[5] = row[5]
        new_row[7] = row[6]
        new_row[8] = row[7]
        new_row[9] = row[8]
        new_row[10] = row[9]
        new_row[11] = row[10]

        new_row[12:20] = row[11:19]

        new_row[20] = row[19]
        new_row[21] = row[20]
        new_row[22] = row[21]
        new_row[23] = row[22]

        new_row[24] = row[23]
        new_row[25] = row[24]
        new_row[26] = row[25]
        new_row[27] = row[26]

        new_row[28:36] = row[27:35]

        new_row[36] = row[35]
        new_row[37] = row[36]

        new_row[38:42] = row[37:41]

        new_row[42] = row[41]
        new_row[43] = row[42]
        new_row[44] = row[43]

    # ---------------- 45 COLUMN FORMAT ----------------
    elif row_len == 45:
        new_row[:45] = row[:45]

    # ---------------- 46 COLUMN FORMAT ----------------
    elif row_len == 46:
        new_row[:45] = row[:45]
        new_row[45] = row[45]

    # ---------------- 47 COLUMN FORMAT ----------------
    elif row_len == 47:

        # Special older 47-column format
        # Lens Features was stored at [26] and duplicated at [46].
        if (
            row[46].strip()
            and row[26].strip()
            and row[46].strip() == row[26].strip()
        ):
            new_row[0:26] = row[0:26]

            new_row[26] = row[27]      # Lens Offer
            new_row[27] = row[28]      # Lens Price

            new_row[28:45] = row[29:46]

            new_row[45] = row[46]      # Lens Features
            new_row[46] = ""           # Full Address unavailable

        else:
            # Current 47-column format
            new_row[:] = row[:47]
    else:
        print(
            f"WARNING: Unsupported row length {row_len}. "
            f"Customer: {row[5] if len(row) > 5 else 'Unknown'}"
        )

    return new_row


with open(SOURCE_FILE, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)

if rows and rows[0] and rows[0][0] == "Date/Time":
    customer_rows = rows[1:]
else:
    customer_rows = rows

normalized_rows = [
    normalize_row(row)
    for row in customer_rows
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow(CURRENT_HEADER)
    writer.writerows(normalized_rows)

print("Normalization preview completed.")
print("Source customer rows:", len(customer_rows))
print("Normalized customer rows:", len(normalized_rows))
print("Output file:", OUTPUT_FILE)