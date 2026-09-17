# ============================================================
# Business Data Quality Audit
# File: 01_generate_data.py
#
# Purpose:
# Generate a reproducible synthetic operational sales dataset
# and a ground-truth data-quality error injection log.
#
# Random seed: 42
# Final records: 10,000
# ============================================================

from pathlib import Path
import random

import numpy as np
import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

SEED = 42

FINAL_RECORDS = 10_000
BASE_RECORDS = 9_850
DUPLICATE_RECORDS = 150

N_CUSTOMERS = 3_500

REPORT_START = pd.Timestamp("2025-01-01")
REPORT_END = pd.Timestamp("2026-06-30")

random.seed(SEED)
np.random.seed(SEED)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

# Works when the script is:
#   a) executed from the GitHub repository locally, or
#   b) copied/executed from a Kaggle notebook.

if "__file__" in globals():
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
else:
    PROJECT_ROOT = Path.cwd()

RAW_DIR = PROJECT_ROOT / "data" / "raw"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = RAW_DIR / "operational_sales_raw.csv"
ERROR_LOG_FILE = (
    METADATA_DIR / "error_injection_log.csv"
)


# ============================================================
# 3. APPROVED VOCABULARIES
# ============================================================

REGIONS = [
    "Nairobi",
    "Central",
    "Eastern",
    "Coast",
    "Rift Valley",
    "Western",
    "Nyanza",
    "North Eastern",
]

SALES_CHANNELS = [
    "Online",
    "Retail Store",
    "Mobile App",
    "Sales Representative",
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Home & Kitchen",
    "Clothing",
    "Beauty",
    "Groceries",
    "Office Supplies",
]

CUSTOMER_SEGMENTS = [
    "Individual",
    "Small Business",
    "Corporate",
    "Government",
]

PAYMENT_METHODS = [
    "Cash",
    "Card",
    "Mobile Money",
    "Bank Transfer",
]

ORDER_STATUSES = [
    "Completed",
    "Pending",
    "Cancelled",
    "Returned",
]

SOURCE_SYSTEMS = [
    "ERP",
    "CRM",
    "E-commerce",
    "Mobile App",
]


# ============================================================
# 4. GENERATE CLEAN BASELINE
# ============================================================

print("Generating clean baseline dataset...")

customer_ids = [
    f"CUST{i:05d}"
    for i in range(1, N_CUSTOMERS + 1)
]

order_ids = [
    f"ORD{i:06d}"
    for i in range(1, BASE_RECORDS + 1)
]

customer_segment_map = {
    customer_id: np.random.choice(
        CUSTOMER_SEGMENTS,
        p=[0.60, 0.20, 0.15, 0.05],
    )
    for customer_id in customer_ids
}


price_ranges = {
    "Electronics": (1_000, 150_000),
    "Home & Kitchen": (500, 50_000),
    "Clothing": (300, 20_000),
    "Beauty": (200, 15_000),
    "Groceries": (50, 10_000),
    "Office Supplies": (100, 20_000),
}


records = []

for i in range(BASE_RECORDS):

    customer_id = random.choice(customer_ids)

    order_date = (
        REPORT_START
        + pd.Timedelta(
            days=random.randint(
                0,
                (REPORT_END - REPORT_START).days,
            )
        )
    )

    region = np.random.choice(
        REGIONS,
        p=[
            0.35,
            0.10,
            0.10,
            0.08,
            0.15,
            0.08,
            0.10,
            0.04,
        ],
    )

    sales_channel = np.random.choice(
        SALES_CHANNELS,
        p=[0.30, 0.30, 0.20, 0.20],
    )

    product_category = np.random.choice(
        PRODUCT_CATEGORIES,
        p=[0.20, 0.18, 0.18, 0.12, 0.20, 0.12],
    )

    quantity = random.randint(1, 10)

    min_price, max_price = price_ranges[
        product_category
    ]

    unit_price = round(
        random.uniform(min_price, max_price),
        2,
    )

    total_sales = round(
        quantity * unit_price,
        2,
    )

    customer_segment = customer_segment_map[
        customer_id
    ]

    payment_method = np.random.choice(
        PAYMENT_METHODS,
        p=[0.15, 0.30, 0.40, 0.15],
    )

    order_status = np.random.choice(
        ORDER_STATUSES,
        p=[0.75, 0.10, 0.10, 0.05],
    )

    source_system = np.random.choice(
        SOURCE_SYSTEMS,
        p=[0.35, 0.20, 0.30, 0.15],
    )

    records.append(
        {
            "customer_id": customer_id,
            "order_id": order_ids[i],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "region": region,
            "sales_channel": sales_channel,
            "product_category": product_category,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_sales": total_sales,
            "customer_segment": customer_segment,
            "payment_method": payment_method,
            "order_status": order_status,
            "source_system": source_system,
        }
    )


df = pd.DataFrame(records)

print(
    f"Clean baseline records: {len(df):,}"
)


# ============================================================
# 5. STABLE TECHNICAL RECORD IDENTIFIER
# ============================================================

# This identifier is NOT part of the raw dataset.
# It exists only so the ground-truth error log can continue
# to identify a record after the dataset is shuffled.

df["_record_id"] = np.arange(
    1,
    len(df) + 1,
)


# ============================================================
# 6. ERROR LOG
# ============================================================

error_log = []


def log_error(
    record_id,
    error_type,
    rule_id,
    field,
    original_value,
    modified_value,
):
    error_log.append(
        {
            "record_id": record_id,
            "error_type": error_type,
            "rule_id": rule_id,
            "field_affected": field,
            "original_value": str(original_value),
            "modified_value": str(modified_value),
        }
    )


def choose_rows(n):
    return np.random.choice(
        df.index,
        size=n,
        replace=False,
    )


# ============================================================
# 7. CREATE DUPLICATE RECORDS
# ============================================================

print("Creating controlled duplicate records...")

duplicate_source_rows = np.random.choice(
    df.index,
    size=DUPLICATE_RECORDS,
    replace=False,
)

duplicate_rows = df.loc[
    duplicate_source_rows
].copy()

EXACT_DUPLICATES = 75
CONFLICTING_DUPLICATES = 75


# ------------------------------------------------------------
# 7A. Exact duplicates
# ------------------------------------------------------------

exact_duplicates = duplicate_rows.iloc[
    :EXACT_DUPLICATES
].copy()

# Give every duplicated record a new technical record ID.
exact_duplicates["_record_id"] = np.arange(
    len(df) + 1,
    len(df) + EXACT_DUPLICATES + 1,
)

df = pd.concat(
    [df, exact_duplicates],
    ignore_index=True,
)


for new_record_id, source_index in zip(
    exact_duplicates["_record_id"],
    duplicate_source_rows[:EXACT_DUPLICATES],
):

    source_record_id = df.loc[
        source_index,
        "_record_id",
    ]

    order_id = df.loc[
        source_index,
        "order_id",
    ]

    error_log.append(
        {
            "record_id": new_record_id,
            "error_type": "Exact duplicate order",
            "rule_id": "DQ003",
            "field_affected": "order_id",
            "original_value": str(order_id),
            "modified_value": str(order_id),
        }
    )


# ------------------------------------------------------------
# 7B. Conflicting duplicates
# ------------------------------------------------------------

conflicting_duplicates = duplicate_rows.iloc[
    EXACT_DUPLICATES:
].copy()

conflicting_duplicates["_record_id"] = np.arange(
    len(df) + 1,
    len(df) + CONFLICTING_DUPLICATES + 1,
)

for position, source_index in enumerate(
    duplicate_source_rows[EXACT_DUPLICATES:]
):

    new_record_id = conflicting_duplicates.iloc[
        position
    ]["_record_id"]

    original_region = conflicting_duplicates.iloc[
        position
    ]["region"]

    alternative_regions = [
        region
        for region in REGIONS
        if region != original_region
    ]

    new_region = random.choice(
        alternative_regions
    )

    conflicting_duplicates.iloc[
        position,
        conflicting_duplicates.columns.get_loc(
            "region"
        ),
    ] = new_region

    error_log.append(
        {
            "record_id": new_record_id,
            "error_type": "Conflicting duplicate order",
            "rule_id": "DQ003",
            "field_affected": "region",
            "original_value": str(original_region),
            "modified_value": str(new_region),
        }
    )


df = pd.concat(
    [df, conflicting_duplicates],
    ignore_index=True,
)


print(
    f"Records after duplicate creation: "
    f"{len(df):,}"
)


# ============================================================
# 8. MISSING VALUES
# ============================================================

print("Injecting missing values...")

MISSING_ERRORS = 300

missing_fields = [
    "customer_id",
    "region",
    "sales_channel",
    "product_category",
    "quantity",
    "unit_price",
    "total_sales",
    "customer_segment",
    "payment_method",
    "order_status",
    "source_system",
]

missing_rule_map = {
    "customer_id": "DQ001",
    "region": "DQ008",
    "sales_channel": "DQ010",
    "product_category": "DQ011",
    "quantity": "DQ012",
    "unit_price": "DQ013",
    "total_sales": "DQ014",
    "customer_segment": "DQ015",
    "payment_method": "DQ016",
    "order_status": "DQ017",
    "source_system": "DQ018",
}

for _ in range(MISSING_ERRORS):

    row_index = random.choice(df.index)
    field = random.choice(missing_fields)

    original_value = df.loc[
        row_index,
        field,
    ]

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    df.loc[
        row_index,
        field,
    ] = np.nan

    log_error(
        record_id,
        "Missing value",
        missing_rule_map[field],
        field,
        original_value,
        np.nan,
    )


# ============================================================
# 9. CATEGORICAL INCONSISTENCIES
# ============================================================

print("Injecting categorical inconsistencies...")

CATEGORICAL_ERRORS = 200

categorical_fields = [
    "region",
    "sales_channel",
    "product_category",
    "customer_segment",
    "payment_method",
    "order_status",
    "source_system",
]


def create_categorical_variant(
    field,
    value,
):

    value = str(value)

    if field == "region":
        return f" {value} "

    if field == "sales_channel":
        return value.lower()

    if field == "product_category":
        return value.upper()

    if field == "customer_segment":
        return value.lower()

    if field == "payment_method":
        return value.lower()

    if field == "order_status":
        return value.upper()

    if field == "source_system":
        return f"{value} "

    return value


successful_categorical_errors = 0

while (
    successful_categorical_errors
    < CATEGORICAL_ERRORS
):

    row_index = random.choice(df.index)
    field = random.choice(categorical_fields)

    original_value = df.loc[
        row_index,
        field,
    ]

    if pd.isna(original_value):
        continue

    modified_value = create_categorical_variant(
        field,
        original_value,
    )

    # Avoid creating an identical value.
    if str(modified_value) == str(
        original_value
    ):
        continue

    df.loc[
        row_index,
        field,
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Categorical inconsistency",
        "DQ019",
        field,
        original_value,
        modified_value,
    )

    successful_categorical_errors += 1


# ============================================================
# 10. INVALID QUANTITIES
# ============================================================

print("Injecting invalid quantities...")

INVALID_QUANTITY_ERRORS = 100

for row_index in choose_rows(
    INVALID_QUANTITY_ERRORS
):

    original_value = df.loc[
        row_index,
        "quantity",
    ]

    modified_value = random.choice(
        [0, -1, -2, -5, -10]
    )

    df.loc[
        row_index,
        "quantity",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Invalid quantity",
        "DQ012",
        "quantity",
        original_value,
        modified_value,
    )


# ============================================================
# 11. INVALID UNIT PRICES
# ============================================================

print("Injecting invalid unit prices...")

INVALID_PRICE_ERRORS = 100

for row_index in choose_rows(
    INVALID_PRICE_ERRORS
):

    original_value = df.loc[
        row_index,
        "unit_price",
    ]

    modified_value = random.choice(
        [0, -10, -100, -500, -1000]
    )

    df.loc[
        row_index,
        "unit_price",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Invalid unit price",
        "DQ013",
        "unit_price",
        original_value,
        modified_value,
    )


# ============================================================
# 12. INCORRECT TOTAL SALES
# ============================================================

print("Injecting incorrect total sales...")

INCORRECT_SALES_ERRORS = 150

successful_sales_errors = 0

while (
    successful_sales_errors
    < INCORRECT_SALES_ERRORS
):

    row_index = random.choice(df.index)

    original_value = df.loc[
        row_index,
        "total_sales",
    ]

    if pd.isna(original_value):
        continue

    modified_value = round(
        float(original_value)
        * random.choice(
            [0.5, 0.8, 1.1, 1.2, 1.5]
        ),
        2,
    )

    df.loc[
        row_index,
        "total_sales",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Incorrect total sales",
        "DQ014",
        "total_sales",
        original_value,
        modified_value,
    )

    successful_sales_errors += 1


# ============================================================
# 13. INVALID DATES
# ============================================================

print("Injecting invalid dates...")

INVALID_DATE_ERRORS = 50

invalid_dates = [
    "2024-12-15",
    "2026-07-15",
    "2027-01-01",
    "not_a_date",
    "2026/99/99",
]

for row_index in choose_rows(
    INVALID_DATE_ERRORS
):

    original_value = df.loc[
        row_index,
        "order_date",
    ]

    modified_value = random.choice(
        invalid_dates
    )

    df.loc[
        row_index,
        "order_date",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Invalid or out-of-range date",
        "DQ006/DQ007",
        "order_date",
        original_value,
        modified_value,
    )


# ============================================================
# 14. INVALID CUSTOMER IDs
# ============================================================

print("Injecting invalid customer IDs...")

INVALID_CUSTOMER_ID_ERRORS = 50

invalid_customer_ids = [
    "CUST123",
    "CUSTOMER00125",
    "CUSTABCDE",
    "12345",
    "CUST-00125",
    "",
]

for row_index in choose_rows(
    INVALID_CUSTOMER_ID_ERRORS
):

    original_value = df.loc[
        row_index,
        "customer_id",
    ]

    modified_value = random.choice(
        invalid_customer_ids
    )

    df.loc[
        row_index,
        "customer_id",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Invalid customer ID",
        "DQ004",
        "customer_id",
        original_value,
        modified_value,
    )


# ============================================================
# 15. INVALID ORDER IDs
# ============================================================

print("Injecting invalid order IDs...")

INVALID_ORDER_ID_ERRORS = 50

invalid_order_ids = [
    "ORD123",
    "ORDER004582",
    "ORDABCDEF",
    "123456",
    "ORD-004582",
    "",
]

for row_index in choose_rows(
    INVALID_ORDER_ID_ERRORS
):

    original_value = df.loc[
        row_index,
        "order_id",
    ]

    modified_value = random.choice(
        invalid_order_ids
    )

    df.loc[
        row_index,
        "order_id",
    ] = modified_value

    record_id = df.loc[
        row_index,
        "_record_id",
    ]

    log_error(
        record_id,
        "Invalid order ID",
        "DQ005",
        "order_id",
        original_value,
        modified_value,
    )


# ============================================================
# 16. PRE-SAVE VALIDATION
# ============================================================

print("\nRunning pre-save validation...")

assert len(df) == FINAL_RECORDS, (
    f"Expected {FINAL_RECORDS:,} records, "
    f"but found {len(df):,}."
)

expected_columns = [
    "customer_id",
    "order_id",
    "order_date",
    "region",
    "sales_channel",
    "product_category",
    "quantity",
    "unit_price",
    "total_sales",
    "customer_segment",
    "payment_method",
    "order_status",
    "source_system",
]

assert list(
    df.drop(columns=["_record_id"]).columns
) == expected_columns

assert len(
    error_log
) > 0


# ============================================================
# 17. SHUFFLE RECORDS
# ============================================================

# The technical record ID allows the error log to continue
# identifying records after this shuffle.

df = df.sample(
    frac=1,
    random_state=SEED,
).reset_index(drop=True)


# ============================================================
# 18. REMOVE TECHNICAL ID FROM RAW DATA
# ============================================================

raw_df = df.drop(
    columns=["_record_id"]
).copy()


# ============================================================
# 19. FORMAT NUMERIC COLUMNS
# ============================================================

raw_df["quantity"] = pd.to_numeric(
    raw_df["quantity"],
    errors="coerce",
)

raw_df["unit_price"] = pd.to_numeric(
    raw_df["unit_price"],
    errors="coerce",
)

raw_df["total_sales"] = pd.to_numeric(
    raw_df["total_sales"],
    errors="coerce",
)


# ============================================================
# 20. SAVE RAW DATASET
# ============================================================

raw_df.to_csv(
    RAW_FILE,
    index=False,
)


# ============================================================
# 21. SAVE GROUND-TRUTH ERROR LOG
# ============================================================

error_log_df = pd.DataFrame(
    error_log
)

error_log_df.to_csv(
    ERROR_LOG_FILE,
    index=False,
)


# ============================================================
# 22. FINAL VALIDATION
# ============================================================

assert RAW_FILE.exists()
assert ERROR_LOG_FILE.exists()

assert len(raw_df) == FINAL_RECORDS

assert list(raw_df.columns) == expected_columns


# ============================================================
# 23. GENERATION SUMMARY
# ============================================================

print("\n==============================================")
print("DATA GENERATION COMPLETED")
print("==============================================")

print(
    f"Final records: "
    f"{len(raw_df):,}"
)

print(
    f"Unique order IDs: "
    f"{raw_df['order_id'].nunique(dropna=True):,}"
)

print(
    f"Unique customers: "
    f"{raw_df['customer_id'].nunique(dropna=True):,}"
)

print(
    f"Ground-truth error events: "
    f"{len(error_log_df):,}"
)

print("\nRaw dataset columns:")
print(
    list(raw_df.columns)
)

print("\nError events by type:")

print(
    error_log_df[
        "error_type"
    ].value_counts()
)

print("\nFiles created:")

print(
    f"1. {RAW_FILE}"
)

print(
    f"2. {ERROR_LOG_FILE}"
)

print("\n==============================================")
