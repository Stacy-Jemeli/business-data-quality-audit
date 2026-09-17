
# ============================================================
# 03 QUALITY AUDIT
# Business Data Quality Audit
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "operational_sales_raw.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "metadata"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

df = pd.read_csv(RAW_FILE)

print("=" * 70)
print("BUSINESS DATA QUALITY AUDIT")
print("=" * 70)

print(f"Records: {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# ============================================================
# 3. APPROVED VOCABULARIES
# ============================================================

valid_regions = {
    "Nairobi",
    "Central",
    "Eastern",
    "Coast",
    "Rift Valley",
    "Western",
    "Nyanza",
    "North Eastern"
}

valid_channels = {
    "Online",
    "Retail Store",
    "Mobile App",
    "Sales Representative"
}

valid_categories = {
    "Electronics",
    "Home & Kitchen",
    "Clothing",
    "Beauty",
    "Groceries",
    "Office Supplies"
}

valid_segments = {
    "Individual",
    "Small Business",
    "Corporate",
    "Government"
}

valid_payment_methods = {
    "Cash",
    "Card",
    "Mobile Money",
    "Bank Transfer"
}

valid_statuses = {
    "Completed",
    "Pending",
    "Cancelled",
    "Returned"
}

valid_sources = {
    "ERP",
    "CRM",
    "E-commerce",
    "Mobile App"
}


# ============================================================
# 4. PREPARE AUDIT DATA
# ============================================================

audit = pd.DataFrame(index=df.index)


# ============================================================
# DQ001 — CUSTOMER ID REQUIRED
# ============================================================

audit["DQ001"] = df["customer_id"].isna()


# ============================================================
# DQ002 — ORDER ID REQUIRED
# ============================================================

audit["DQ002"] = df["order_id"].isna()


# ============================================================
# DQ003 — NON-MISSING ORDER IDs SHOULD BE UNIQUE
# ============================================================

audit["DQ003"] = (
    df["order_id"].notna()
    & df["order_id"].duplicated(keep=False)
)


# ============================================================
# DQ004 — CUSTOMER ID FORMAT
# ============================================================

audit["DQ004"] = (
    df["customer_id"].notna()
    & ~df["customer_id"].astype(str).str.fullmatch(
        r"CUST[0-9]{5}"
    )
)


# ============================================================
# DQ005 — ORDER ID FORMAT
# ============================================================

audit["DQ005"] = (
    df["order_id"].notna()
    & ~df["order_id"].astype(str).str.fullmatch(
        r"ORD[0-9]{6}"
    )
)


# ============================================================
# 5. DATE VALIDATION
# ============================================================

parsed_dates = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

report_start = pd.Timestamp("2025-01-01")
report_end = pd.Timestamp("2026-06-30")


# ============================================================
# DQ006 — ORDER DATE MUST BE VALID
# ============================================================

audit["DQ006"] = (
    df["order_date"].notna()
    & parsed_dates.isna()
)


# ============================================================
# DQ007 — ORDER DATE WITHIN REPORTING PERIOD
# ============================================================

audit["DQ007"] = (
    parsed_dates.notna()
    & (
        (parsed_dates < report_start)
        | (parsed_dates > report_end)
    )
)


# ============================================================
# DQ008 — REGION REQUIRED
# ============================================================

audit["DQ008"] = df["region"].isna()


# ============================================================
# DQ009 — REGION APPROVED VOCABULARY
# ============================================================

audit["DQ009"] = (
    df["region"].notna()
    & ~df["region"].isin(valid_regions)
)


# ============================================================
# DQ010 — SALES CHANNEL APPROVED VOCABULARY
# ============================================================

audit["DQ010"] = (
    df["sales_channel"].notna()
    & ~df["sales_channel"].isin(valid_channels)
)


# ============================================================
# DQ011 — PRODUCT CATEGORY APPROVED VOCABULARY
# ============================================================

audit["DQ011"] = (
    df["product_category"].notna()
    & ~df["product_category"].isin(valid_categories)
)


# ============================================================
# DQ012 — QUANTITY MUST BE GREATER THAN ZERO
# ============================================================

audit["DQ012"] = (
    df["quantity"].notna()
    & (df["quantity"] <= 0)
)


# ============================================================
# DQ013 — UNIT PRICE MUST BE GREATER THAN ZERO
# ============================================================

audit["DQ013"] = (
    df["unit_price"].notna()
    & (df["unit_price"] <= 0)
)


# ============================================================
# DQ014 — TOTAL SALES MUST EQUAL
# QUANTITY × UNIT PRICE
# ============================================================

complete_sales = (
    df["quantity"].notna()
    & df["unit_price"].notna()
    & df["total_sales"].notna()
)

expected_total = (
    df["quantity"] * df["unit_price"]
)

audit["DQ014"] = (
    complete_sales
    & ~np.isclose(
        df["total_sales"],
        expected_total,
        rtol=1e-9,
        atol=0.01
    )
)


# ============================================================
# DQ015 — CUSTOMER SEGMENT APPROVED VOCABULARY
# ============================================================

audit["DQ015"] = (
    df["customer_segment"].notna()
    & ~df["customer_segment"].isin(valid_segments)
)


# ============================================================
# DQ016 — PAYMENT METHOD APPROVED VOCABULARY
# ============================================================

audit["DQ016"] = (
    df["payment_method"].notna()
    & ~df["payment_method"].isin(valid_payment_methods)
)


# ============================================================
# DQ017 — ORDER STATUS APPROVED VOCABULARY
# ============================================================

audit["DQ017"] = (
    df["order_status"].notna()
    & ~df["order_status"].isin(valid_statuses)
)


# ============================================================
# DQ018 — SOURCE SYSTEM APPROVED VOCABULARY
# ============================================================

audit["DQ018"] = (
    df["source_system"].notna()
    & ~df["source_system"].isin(valid_sources)
)


# ============================================================
# DQ019 — CATEGORICAL STANDARDISATION
# ============================================================

audit["DQ019"] = False

categorical_rules = {
    "region": valid_regions,
    "sales_channel": valid_channels,
    "product_category": valid_categories,
    "customer_segment": valid_segments,
    "payment_method": valid_payment_methods,
    "order_status": valid_statuses,
    "source_system": valid_sources
}

for column, standard_values in categorical_rules.items():

    canonical_values = {
        str(value).strip().lower()
        for value in standard_values
    }

    normalised_values = (
        df[column]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    standardisation_issue = (
        df[column].notna()
        & ~df[column].isin(standard_values)
        & normalised_values.isin(canonical_values)
    )

    audit["DQ019"] |= standardisation_issue


# ============================================================
# DQ020 — REQUIRED OPERATIONAL FIELDS COMPLETE
# ============================================================

required_columns = [
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
    "source_system"
]

audit["DQ020"] = (
    df[required_columns]
    .isna()
    .any(axis=1)
)


# ============================================================
# 6. AUDIT SUMMARY
# ============================================================

audit_summary = pd.DataFrame({
    "dq_rule": audit.columns,
    "violations": [
        int(audit[column].sum())
        for column in audit.columns
    ]
})

audit_summary["violation_rate_pct"] = (
    audit_summary["violations"]
    / len(df)
    * 100
)

audit_summary = audit_summary.sort_values(
    "violations",
    ascending=False
)


# ============================================================
# 7. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY AUDIT RESULTS")
print("=" * 70)

display(audit_summary)


# ============================================================
# 8. OVERALL RECORD-LEVEL QUALITY
# ============================================================

any_violation = audit.any(axis=1)

records_with_quality_issue = int(any_violation.sum())
records_without_quality_issue = int((~any_violation).sum())

print("\n" + "=" * 70)
print("RECORD-LEVEL QUALITY SUMMARY")
print("=" * 70)

print(
    f"Records with at least one DQ violation: "
    f"{records_with_quality_issue:,}"
)

print(
    f"Records with no DQ violation: "
    f"{records_without_quality_issue:,}"
)

print(
    f"Overall records with a quality issue: "
    f"{records_with_quality_issue / len(df) * 100:.2f}%"
)


# ============================================================
# 9. SAVE AUDIT OUTPUTS
# ============================================================

audit_summary_file = (
    OUTPUT_DIR / "data_quality_audit_summary.csv"
)

audit_record_file = (
    OUTPUT_DIR / "data_quality_record_flags.csv"
)

audit_summary.to_csv(
    audit_summary_file,
    index=False
)

audit.to_csv(
    audit_record_file,
    index=False
)

print("\nAudit outputs saved:")
print(audit_summary_file)
print(audit_record_file)
