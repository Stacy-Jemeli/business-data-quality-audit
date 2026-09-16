# Data Dictionary

## Overview

This data dictionary defines the structure, meaning, expected data type, and business requirements for the synthetic operational sales dataset used in this project.

The dataset contains approximately 10,000 order records and is designed to simulate operational sales data collected from multiple source systems and sales channels.

The data dictionary serves as the reference specification for:

- Synthetic data generation
- Data-quality validation
- SQL analysis
- Python analysis
- Data cleaning
- Data reconciliation
- Final reporting

---

## Dataset Variables

| # | Variable | Data Type | Required | Example | Business Meaning |
|---:|---|---|---|---|---|
| 1 | `customer_id` | String | Yes | `CUST00125` | Identifier assigned to a customer |
| 2 | `order_id` | String | Yes | `ORD004582` | Identifier assigned to an order |
| 3 | `order_date` | Date | Yes | `2026-03-15` | Date on which the order was placed |
| 4 | `region` | Categorical | Yes | `Nairobi` | Geographic region associated with the order |
| 5 | `sales_channel` | Categorical | Yes | `Online` | Channel through which the order was received |
| 6 | `product_category` | Categorical | Yes | `Electronics` | Category of product purchased |
| 7 | `quantity` | Integer | Yes | `4` | Number of units purchased |
| 8 | `unit_price` | Decimal | Yes | `12500.00` | Price of one unit |
| 9 | `total_sales` | Decimal | Yes | `50000.00` | Recorded monetary value of the order |
| 10 | `customer_segment` | Categorical | Yes | `Corporate` | Classification of the customer |
| 11 | `payment_method` | Categorical | Yes | `Card` | Method used to pay for the order |
| 12 | `order_status` | Categorical | Yes | `Completed` | Current status of the order |
| 13 | `source_system` | Categorical | Yes | `ERP` | System from which the record originated |

---

## Variable Specifications

### 1. `customer_id`

**Data type:** String

**Required:** Yes

**Expected format:**

`CUST` followed by five digits.

Examples:

- `CUST00001`
- `CUST00025`
- `CUST01250`

**Business rule:** Customer identifiers should follow the approved format and should not be missing.

A customer may have multiple orders.

---

### 2. `order_id`

**Data type:** String

**Required:** Yes

**Expected format:**

`ORD` followed by six digits.

Examples:

- `ORD000001`
- `ORD000125`
- `ORD004582`

**Business rule:** Order identifiers should follow the approved format and should normally be unique.

---

### 3. `order_date`

**Data type:** Date

**Required:** Yes

**Example:** `2026-03-15`

**Reporting period:**

`2025-01-01` to `2026-06-30`

**Business rule:** The order date must be a valid date and must fall within the defined reporting period.

---

### 4. `region`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Nairobi
- Central
- Eastern
- Coast
- Rift Valley
- Western
- Nyanza
- North Eastern

**Business rule:** Region values should use the approved controlled vocabulary.

---

### 5. `sales_channel`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Online
- Retail Store
- Mobile App
- Sales Representative

**Business rule:** Sales channel values should use the approved controlled vocabulary.

---

### 6. `product_category`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Electronics
- Home & Kitchen
- Clothing
- Beauty
- Groceries
- Office Supplies

**Business rule:** Product category values should use the approved controlled vocabulary.

---

### 7. `quantity`

**Data type:** Integer

**Required:** Yes

**Example:** `4`

**Business rule:**

`quantity > 0`

Zero and negative quantities are considered invalid.

---

### 8. `unit_price`

**Data type:** Decimal

**Required:** Yes

**Example:** `12500.00`

**Business rule:**

`unit_price > 0`

Zero and negative prices are considered invalid.

---

### 9. `total_sales`

**Data type:** Decimal

**Required:** Yes

**Example:** `50000.00`

**Expected calculation:**

`total_sales = quantity × unit_price`

The recorded total sales value should be consistent with the quantity and unit price.

---

### 10. `customer_segment`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Individual
- Small Business
- Corporate
- Government

**Business rule:** Customer segment values should use the approved controlled vocabulary.

---

### 11. `payment_method`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Cash
- Card
- Mobile Money
- Bank Transfer

**Business rule:** Payment method values should use the approved controlled vocabulary.

---

### 12. `order_status`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- Completed
- Pending
- Cancelled
- Returned

**Business rule:** Order status values should use the approved controlled vocabulary.

---

### 13. `source_system`

**Data type:** Categorical

**Required:** Yes

**Approved values:**

- ERP
- CRM
- E-commerce
- Mobile App

**Business rule:** Source system values should use the approved controlled vocabulary.

---

## Identifier Validation Patterns

### Customer ID

Expected pattern:

`^CUST[0-9]{5}$`

### Order ID

Expected pattern:

`^ORD[0-9]{6}$`

These patterns will later be implemented in Python and SQL validation checks where supported.

---

## Numerical Validation Rules

| Variable | Validation |
|---|---|
| `quantity` | Must be greater than 0 |
| `unit_price` | Must be greater than 0 |
| `total_sales` | Should equal `quantity × unit_price` |

---

## Date Validation Rules

| Rule | Requirement |
|---|---|
| Valid date | `order_date` must be a valid date |
| Lower boundary | `order_date >= 2025-01-01` |
| Upper boundary | `order_date <= 2026-06-30` |

---

## Data-Quality Considerations

Although the variables have defined valid values and business rules, the raw synthetic dataset will deliberately contain data-quality problems.

These may include:

- Missing values
- Duplicate order identifiers
- Invalid identifier formats
- Inconsistent categorical values
- Invalid dates
- Zero or negative quantities
- Zero or negative prices
- Incorrect total sales
- Multiple quality problems occurring in the same record

The purpose is to provide a realistic dataset for demonstrating data-quality auditing techniques using SQL and Python.

---

## Source of Truth

This data dictionary represents the approved schema for the project.

Any changes to the dataset structure should be reflected in this document before changes are made to the data-generation or analysis code.
