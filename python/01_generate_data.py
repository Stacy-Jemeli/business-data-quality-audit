# ============================================================
# Business Data Quality Audit
# File: 01_generate_data.py
# Purpose: Generate a reproducible synthetic operational sales
# dataset and a ground-truth error injection log.
# Random seed: 42
# ============================================================

import os
import random
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------

SEED = 42
FINAL_RECORDS = 10_000
BASE_RECORDS = 9_850
N_CUSTOMERS = 3_500

REPORT_START = pd.Timestamp("2025-01-01")
REPORT_END = pd.Timestamp("2026-06-30")

random.seed(SEED)
np.random.seed(SEED)

# Output folders
RAW_DIR = "../data/raw"
METADATA_DIR = "../data/metadata"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

RAW_FILE = os.path.join(RAW_DIR, "operational_sales_raw.csv")
ERROR_LOG_FILE = os.path.join(
    METADATA_DIR,
    "error_injection_log.csv"
)

# ------------------------------------------------------------
# 2. Approved vocabularies
# ------------------------------------------------------------

REGIONS = [
    "Nairobi",
    "Central",
    "Eastern",
    "Coast",
    "Rift Valley",
    "Western",
    "Nyanza",
    "North Eastern"
]

SALES_CHANNELS = [
    "Online",
    "Retail Store",
    "Mobile App",
    "Sales Representative"
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Home & Kitchen",
    "Clothing",
    "Beauty",
    "Groceries",
    "Office Supplies"
]

CUSTOMER_SEGMENTS = [
    "Individual",
    "Small Business",
    "Corporate",
    "Government"
]

PAYMENT_METHODS = [
    "Cash",
    "Card",
    "Mobile Money",
    "Bank Transfer"
]

ORDER_STATUSES = [
    "Completed",
    "Pending",
    "Cancelled",
    "Returned"
]

SOURCE_SYSTEMS = [
    "ERP",
    "CRM",
    "E-commerce",
    "Mobile App"
]

# ------------------------------------------------------------
# 3. Generate clean baseline data
# ------------------------------------------------------------

print("Generating clean baseline dataset...")

customer_ids = [
    f"CUST{i:05d}"
    for i in range(1, N_CUSTOMERS + 1)
]

order_ids = [
    f"ORD{i:06d}"
    for i in range(1, BASE_RECORDS + 1)
]

# Customer-level attributes
customer_segment_map = {
    customer_id: np.random.choice(
        CUSTOMER_SEGMENTS,
        p=[0.60, 0.20, 0.15, 0.05]
    )
    for customer_id in customer_ids
}

records = []

for i in range(BASE_RECORDS):

    customer_id = random.choice(customer_ids)

    order_date = (
        REPORT_START
        + pd.Timedelta(
            days=random.randint(
                0,
                (REPORT_END - REPORT_START).days
            )
        )
    )

    region = np.random.choice(
        REGIONS,
        p=[0.35, 0.10, 0.10, 0.08,
           0.15, 0.08, 0.10, 0.04]
    )

    sales_channel = np.random.choice(
        SALES_CHANNELS,
        p=[0.30, 0.30, 0.20, 0.20]
    )

    product_category = np.random.choice(
        PRODUCT_CATEGORIES,
        p=[0.20, 0.18, 0.18, 0.12, 0.20, 0.12]
    )

    quantity = random.randint(1, 10)

    # Category-specific realistic price ranges
    price_ranges = {
        "Electronics": (1000, 150000),
        "Home & Kitchen": (500, 50000),
        "Clothing": (300, 20000),
        "Beauty": (200, 15000),
        "Groceries": (50, 10000),
        "Office Supplies": (100, 20000)
    }

    min_price, max_price = price_ranges[product_category]

    unit_price = round(
        random.uniform(min_price, max_price),
        2
    )

    total_sales = round(
        quantity * unit_price,
        2
    )

    customer_segment = customer_segment_map[customer_id]

    payment_method = np.random.choice(
        PAYMENT_METHODS,
        p=[0.15, 0.30, 0.40, 0.15]
    )

    order_status = np.random.choice(
        ORDER_STATUSES,
        p=[0.75, 0.10, 0.10, 0.05]
    )

    source_system = np.random.choice(
        SOURCE_SYSTEMS,
        p=[0.35, 0.20, 0.30, 0.15]
    )

    records.append({
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
        "source_system": source_system
    })

df = pd.DataFrame(records)

print(f"Clean baseline records: {len(df):,}")

# ------------------------------------------------------------
# 4. Error logging structure
# ------------------------------------------------------------

error_log = []

def log_error(
    row_index,
    error_type,
    rule_id,
    field,
    original_value,
    modified_value
):
    error_log.append({
        "row_id": row_index + 1,
        "order_id_at_logging": str(
            df.loc[row_index, "order_id"]
        ),
        "error_type": error_type,
        "rule_id": rule_id,
        "field_affected": field,
        "original_value": str(original_value),
        "modified_value": str(modified_value)
    })


def choose_rows(n):
    return np.random.choice(
        df.index,
        size=n,
        replace=False
    )


# ------------------------------------------------------------
# 5. Create space for duplicate records
# ------------------------------------------------------------

# We want exactly 10,000 final records.
# Therefore 150 records will be duplicates of existing records.

duplicate_count = 150

duplicate_source_rows = np.random.choice(
    df.index,
    size=duplicate_count,
    replace=False
)

duplicate_rows = df.loc[
    duplicate_source_rows
].copy()

# Half exact duplicates
exact_duplicate_count = duplicate_count // 2

# Remaining duplicates will have conflicting information
conflicting_duplicate_count = (
    duplicate_count - exact_duplicate_count
)

# Add exact duplicates
df = pd.concat(
    [
        df,
        duplicate_rows.iloc[:exact_duplicate_count]
    ],
    ignore_index=True
)

# ------------------------------------------------------------
# 6. Conflicting duplicate records
# ------------------------------------------------------------

conflicting_rows = duplicate_rows.iloc[
    exact_duplicate_count:
].copy()

df = pd.concat(
    [
        df,
        conflicting_rows
    ],
    ignore_index=True
)

print(f"Records after duplicate creation: {len(df):,}")

# Log duplicate errors
for source_idx, duplicated_row in zip(
    duplicate_source_rows[:exact_duplicate_count],
    range(BASE_RECORDS, BASE_RECORDS + exact_duplicate_count)
):
    error_log.append({
        "row_id": duplicated_row + 1,
        "order_id_at_logging": df.loc[
            duplicated_row,
            "order_id"
        ],
        "error_type": "Exact duplicate order",
        "rule_id": "DQ003",
        "field_affected": "order_id",
        "original_value": df.loc[
            duplicated_row,
            "order_id"
        ],
        "modified_value": df.loc[
            duplicated_row,
            "order_id"
        ]
    })

# Conflicting duplicates
conflict_start = (
    BASE_RECORDS + exact_duplicate_count
)

for source_idx, new_idx in zip(
    duplicate_source_rows[exact_duplicate_count:],
    range(
        conflict_start,
        conflict_start + conflicting_duplicate_count
    )
):

    # Change one non-key field while retaining the same order ID.
    original_region = df.loc[new_idx, "region"]

    alternative_regions = [
        r for r in REGIONS
        if r != original_region
    ]

    new_region = random.choice(
        alternative_regions
    )

    df.loc[new_idx, "region"] = new_region

    error_log.append({
        "row_id": new_idx + 1,
        "order_id_at_logging": df.loc[
            new_idx,
            "order_id"
        ],
        "error_type": "Conflicting duplicate order",
        "rule_id": "DQ003",
        "field_affected": "region",
        "original_value": original_region,
        "modified_value": new_region
    })

# ------------------------------------------------------------
# 7. Missing values
# ------------------------------------------------------------

missing_count = 300

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
    "source_system"
]

for _ in range(missing_count):

    row_index = random.choice(df.index)
    field = random.choice(missing_fields)

    original_value = df.loc[row_index, field]

    df.loc[row_index, field] = np.nan

    rule_id = {
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
        "source_system": "DQ018"
    }[field]

    log_error(
        row_index,
        "Missing value",
        rule_id,
        field,
        original_value,
        np.nan
    )

# ------------------------------------------------------------
# 8. Categorical inconsistencies
# ------------------------------------------------------------

categorical_fields = [
    "region",
    "sales_channel",
    "product_category",
    "customer_segment",
    "payment_method",
    "order_status",
    "source_system"
]

categorical_variants = {
    "region": lambda x: f" {x} ",
    "sales_channel": lambda x: x.lower(),
    "product_category": lambda x: x.upper(),
    "customer_segment": lambda x: f" {x.lower()}",
    "payment_method": lambda x: x.lower(),
    "order_status": lambda x: x.upper(),
    "source_system": lambda x: f"{x} "
}

categorical_error_count = 200

for _ in range(categorical_error_count):

    row_index = random.choice(df.index)
    field = random.choice(categorical_fields)

    original_value = df.loc[row_index, field]

    if pd.isna(original_value):
        continue

    modified_value = categorical_variants[field](
        str(original_value)
    )

    df.loc[row_index, field] = modified_value

    log_error(
        row_index,
        "Categorical inconsistency",
        "DQ019",
        field,
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 9. Invalid quantities
# ------------------------------------------------------------

quantity_error_count = 100

for row_index in choose_rows(quantity_error_count):

    original_value = df.loc[row_index, "quantity"]

    modified_value = random.choice(
        [0, -1, -2, -5, -10]
    )

    df.loc[row_index, "quantity"] = modified_value

    log_error(
        row_index,
        "Invalid quantity",
        "DQ012",
        "quantity",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 10. Invalid unit prices
# ------------------------------------------------------------

price_error_count = 100

for row_index in choose_rows(price_error_count):

    original_value = df.loc[row_index, "unit_price"]

    modified_value = random.choice(
        [0, -10, -100, -500, -1000]
    )

    df.loc[row_index, "unit_price"] = modified_value

    log_error(
        row_index,
        "Invalid unit price",
        "DQ013",
        "unit_price",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 11. Incorrect total sales
# ------------------------------------------------------------

sales_error_count = 150

for row_index in choose_rows(sales_error_count):

    original_value = df.loc[
        row_index,
        "total_sales"
    ]

    if pd.isna(original_value):
        continue

    modified_value = round(
        float(original_value)
        * random.choice(
            [0.5, 0.8, 1.1, 1.2, 1.5]
        ),
        2
    )

    df.loc[
        row_index,
        "total_sales"
    ] = modified_value

    log_error(
        row_index,
        "Incorrect total sales",
        "DQ014",
        "total_sales",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 12. Invalid dates
# ------------------------------------------------------------

date_error_count = 50

invalid_dates = [
    "2024-12-15",
    "2026-07-15",
    "2027-01-01",
    "not_a_date",
    "2026/99/99"
]

for row_index in choose_rows(date_error_count):

    original_value = df.loc[
        row_index,
        "order_date"
    ]

    modified_value = random.choice(
        invalid_dates
    )

    df.loc[
        row_index,
        "order_date"
    ] = modified_value

    log_error(
        row_index,
        "Invalid or out-of-range date",
        "DQ006/DQ007",
        "order_date",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 13. Invalid customer IDs
# ------------------------------------------------------------

customer_id_error_count = 50

invalid_customer_ids = [
    "CUST123",
    "CUSTOMER00125",
    "CUSTABCDE",
    "12345",
    "CUST-00125",
    ""
]

for row_index in choose_rows(
    customer_id_error_count
):

    original_value = df.loc[
        row_index,
        "customer_id"
    ]

    modified_value = random.choice(
        invalid_customer_ids
    )

    df.loc[
        row_index,
        "customer_id"
    ] = modified_value

    log_error(
        row_index,
        "Invalid customer ID",
        "DQ004",
        "customer_id",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 14. Invalid order IDs
# ------------------------------------------------------------

order_id_error_count = 50

invalid_order_ids = [
    "ORD123",
    "ORDER004582",
    "ORDABCDEF",
    "123456",
    "ORD-004582",
    ""
]

for row_index in choose_rows(
    order_id_error_count
):

    original_value = df.loc[
        row_index,
        "order_id"
    ]

    modified_value = random.choice(
        invalid_order_ids
    )

    df.loc[
        row_index,
        "order_id"
    ] = modified_value

    log_error(
        row_index,
        "Invalid order ID",
        "DQ005",
        "order_id",
        original_value,
        modified_value
    )

# ------------------------------------------------------------
# 15. Final formatting
# ------------------------------------------------------------

# Ensure numeric columns remain numeric.
df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)

df["total_sales"] = pd.to_numeric(
    df["total_sales"],
    errors="coerce"
)

# Shuffle records so errors are not concentrated at the end.
df = df.sample(
    frac=1,
    random_state=SEED
).reset_index(drop=True)

# ------------------------------------------------------------
# 16. Save raw dataset
# ------------------------------------------------------------

df.to_csv(
    RAW_FILE,
    index=False
)

# ------------------------------------------------------------
# 17. Save ground-truth error log
# ------------------------------------------------------------

error_log_df = pd.DataFrame(error_log)

error_log_df.to_csv(
    ERROR_LOG_FILE,
    index=False
)

# ------------------------------------------------------------
# 18. Generation summary
# ------------------------------------------------------------

print("\n==============================================")
print("DATA GENERATION COMPLETED")
print("==============================================")

print(f"Final records: {len(df):,}")
print(
    f"Unique order IDs: "
    f"{df['order_id'].nunique(dropna=True):,}"
)
print(
    f"Unique customers: "
    f"{df['customer_id'].nunique(dropna=True):,}"
)
print(
    f"Ground-truth error events: "
    f"{len(error_log_df):,}"
)

print("\nFiles created:")
print(f"1. {RAW_FILE}")
print(f"2. {ERROR_LOG_FILE}")

print("\nError events by type:")
print(
    error_log_df["error_type"]
    .value_counts()
)

print("\n==============================================")
