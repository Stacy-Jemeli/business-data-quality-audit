# Data Quality Rules

## Overview

This document defines the data-quality rules that will be applied to the synthetic operational sales dataset.

The rules provide a formal framework for identifying, classifying, and quantifying data-quality problems before the data is used for management reporting or decision-making.

The rules will be implemented using SQL and Python during the data-quality audit.

---

## Data Quality Dimensions

The audit will evaluate the following dimensions:

1. Completeness
2. Uniqueness
3. Validity
4. Consistency
5. Accuracy and plausibility

---

## Data Quality Rule Catalogue

| Rule ID | Dimension | Variable(s) | Rule | Failure Condition |
|---|---|---|---|---|
| DQ001 | Completeness | `customer_id` | Customer ID must be populated | `customer_id` is missing |
| DQ002 | Completeness | `order_id` | Order ID must be populated | `order_id` is missing |
| DQ003 | Uniqueness | `order_id` | Order ID should be unique | An order ID occurs more than once |
| DQ004 | Validity | `customer_id` | Customer ID must follow the approved format | ID does not match `CUST#####` |
| DQ005 | Validity | `order_id` | Order ID must follow the approved format | ID does not match `ORD######` |
| DQ006 | Validity | `order_date` | Order date must be valid | Invalid or unparseable date |
| DQ007 | Validity | `order_date` | Order date must fall within reporting period | Date is before 2025-01-01 or after 2026-06-30 |
| DQ008 | Completeness | `region` | Region should be populated | Region is missing |
| DQ009 | Validity | `region` | Region must use approved vocabulary | Value is not an approved region |
| DQ010 | Validity | `sales_channel` | Sales channel must use approved vocabulary | Value is not an approved sales channel |
| DQ011 | Validity | `product_category` | Product category must use approved vocabulary | Value is not an approved category |
| DQ012 | Validity | `quantity` | Quantity must be greater than zero | Quantity is zero or negative |
| DQ013 | Validity | `unit_price` | Unit price must be greater than zero | Unit price is zero or negative |
| DQ014 | Consistency | `quantity`, `unit_price`, `total_sales` | Total sales must equal quantity × unit price | Recorded total differs from expected total |
| DQ015 | Validity | `customer_segment` | Customer segment must use approved vocabulary | Value is not an approved segment |
| DQ016 | Validity | `payment_method` | Payment method must use approved vocabulary | Value is not an approved payment method |
| DQ017 | Validity | `order_status` | Order status must use approved vocabulary | Value is not an approved status |
| DQ018 | Validity | `source_system` | Source system must use approved vocabulary | Value is not an approved source system |
| DQ019 | Consistency | Categorical variables | Categorical values should be standardised | Case or whitespace variant is detected |
| DQ020 | Completeness | All required fields | Required operational fields should be populated | One or more required fields are missing |

---

## Rule Details

### DQ001 — Customer ID Completeness

**Dimension:** Completeness

`customer_id` must not be missing.

A record fails this rule when the customer identifier is NULL, blank, or otherwise absent.

---

### DQ002 — Order ID Completeness

**Dimension:** Completeness

`order_id` must not be missing.

A record fails this rule when the order identifier is NULL, blank, or otherwise absent.

---

### DQ003 — Order ID Uniqueness

**Dimension:** Uniqueness

Each order should have a unique `order_id`.

A repeated order identifier will be flagged for investigation.

Duplicate records will not automatically be deleted because repeated identifiers may represent either:

- Exact duplicate records, or
- Conflicting records requiring investigation.

---

### DQ004 — Customer ID Format

**Dimension:** Validity

Customer IDs should follow the pattern:

`CUST` followed by five digits.

Expected pattern:

`^CUST[0-9]{5}$`

Example of a valid value:

`CUST00125`

Examples of invalid values:

- `CUST125`
- `cust00125`
- `CUSTOMER00125`
- `CUST-00125`

---

### DQ005 — Order ID Format

**Dimension:** Validity

Order IDs should follow the pattern:

`ORD` followed by six digits.

Expected pattern:

`^ORD[0-9]{6}$`

Example of a valid value:

`ORD004582`

Examples of invalid values:

- `ORD4582`
- `order004582`
- `ORD-004582`

---

### DQ006 — Order Date Validity

**Dimension:** Validity

Every `order_date` should represent a valid calendar date.

Unparseable or malformed dates should be flagged.

---

### DQ007 — Order Date Range

**Dimension:** Validity

The defined reporting period is:

`2025-01-01` to `2026-06-30`

Therefore:

`order_date >= 2025-01-01`

and

`order_date <= 2026-06-30`

Dates outside this range should be flagged.

---

### DQ008 — Region Completeness

**Dimension:** Completeness

The `region` field should be populated for every operational order.

Missing region values will be flagged.

---

### DQ009 — Region Validity

**Dimension:** Validity

The approved region vocabulary is:

- Nairobi
- Central
- Eastern
- Coast
- Rift Valley
- Western
- Nyanza
- North Eastern

Values outside this vocabulary will be flagged.

---

### DQ010 — Sales Channel Validity

**Dimension:** Validity

The approved sales channels are:

- Online
- Retail Store
- Mobile App
- Sales Representative

Other values will be flagged.

---

### DQ011 — Product Category Validity

**Dimension:** Validity

The approved product categories are:

- Electronics
- Home & Kitchen
- Clothing
- Beauty
- Groceries
- Office Supplies

Other values will be flagged.

---

### DQ012 — Quantity Validity

**Dimension:** Validity

The quantity must be greater than zero.

Valid:

`1, 2, 3, 4, ...`

Invalid:

`0`

`-1`

`-2`

---

### DQ013 — Unit Price Validity

**Dimension:** Validity

The unit price must be greater than zero.

Valid:

`100`

`2500`

`12500`

Invalid:

`0`

`-100`

`-1500`

---

### DQ014 — Total Sales Consistency

**Dimension:** Consistency

The expected sales value is calculated as:

`Expected Total Sales = Quantity × Unit Price`

A record fails the rule when:

`Recorded Total Sales != Expected Total Sales`

Example:

Quantity = `4`

Unit Price = `12500`

Expected Total Sales = `50000`

If recorded total sales is `47000`, the record fails DQ014.

---

### DQ015 — Customer Segment Validity

**Dimension:** Validity

Approved customer segments:

- Individual
- Small Business
- Corporate
- Government

Other values will be flagged.

---

### DQ016 — Payment Method Validity

**Dimension:** Validity

Approved payment methods:

- Cash
- Card
- Mobile Money
- Bank Transfer

Other values will be flagged.

---

### DQ017 — Order Status Validity

**Dimension:** Validity

Approved order statuses:

- Completed
- Pending
- Cancelled
- Returned

Other values will be flagged.

---

### DQ018 — Source System Validity

**Dimension:** Validity

Approved source systems:

- ERP
- CRM
- E-commerce
- Mobile App

Other values will be flagged.

---

### DQ019 — Categorical Standardisation

**Dimension:** Consistency

Categorical values should be standardised.

Potential variants include:

- `Online`
- `online`
- `ONLINE`
- `Online `

These may represent the same intended category and should be identified during the audit.

The original raw value will be retained until the cleaning stage.

---

### DQ020 — Overall Completeness

**Dimension:** Completeness

The following fields are considered required operational fields:

- `customer_id`
- `order_id`
- `order_date`
- `region`
- `sales_channel`
- `product_category`
- `quantity`
- `unit_price`
- `total_sales`
- `customer_segment`
- `payment_method`
- `order_status`
- `source_system`

A record with one or more missing required fields will be classified as incomplete.

---

# Quality-Failure Measurement

The audit will distinguish between two measures.

## Rule Violations

A rule violation represents an individual failure of a specific data-quality rule.

For example, one record could fail:

- DQ008
- DQ012
- DQ013

This represents three rule violations.

## Affected Records

An affected record is a unique row that fails at least one quality rule.

Therefore, the number of affected records may be lower than the total number of rule violations.

This distinction will be maintained throughout the analysis.

---

# Overlapping Quality Problems

The synthetic dataset will deliberately allow multiple quality problems to occur within the same record.

For example, one record may contain:

- A missing customer ID
- An invalid region
- A negative quantity
- An invalid unit price
- An incorrect total sales value

Such a record will be counted once when calculating the number of affected records, but each applicable quality-rule failure will be recorded separately.

---

# Audit Output

For each quality rule, the analysis will calculate:

- Number of records tested
- Number of records failing the rule
- Percentage of records failing the rule
- Affected variable
- Quality dimension
- Severity or business relevance where appropriate

The final audit will also calculate the overall number and percentage of unique records affected by one or more data-quality problems.

---

# Implementation

The rules defined in this document will subsequently be implemented using:

- SQL
- Python
- Pandas

The SQL and Python implementations will be independently compared to ensure that the audit results are reproducible and consistent.

---

# Governance Principle

The data-quality rules are defined before the analysis is performed.

This prevents the quality criteria from being changed simply to fit the observed results.

Any modification to the rules should be documented and reflected in this file.
