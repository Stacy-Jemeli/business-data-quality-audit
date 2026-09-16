# Business Scenario

## Project Overview

This project simulates a data-quality audit for a commercial organisation that receives customer orders through multiple sales channels.

Management has identified potential problems in its operational sales data, including duplicate records, missing customer information, inconsistent categorical values, unusual or invalid dates, inconsistent sales values, and incomplete records originating from different source systems.

Before the data is used for management reporting and decision-making, the organisation requires a systematic assessment of its quality.

## Business Question

> How reliable is the company's operational sales data, and what data-quality issues could affect management reporting and decision-making?

## Business Objective

The objective of this project is to assess the quality and reliability of operational sales data by identifying, quantifying, and documenting data-quality issues that may affect analysis and management reporting.

The audit will examine dimensions including:

- Completeness
- Uniqueness
- Validity
- Consistency
- Accuracy and plausibility

## Dataset

The project will use a synthetic operational sales dataset containing approximately 10,000 order records.

The dataset will contain information relating to:

- Customers
- Orders
- Order dates
- Geographic regions
- Sales channels
- Product categories
- Quantities
- Unit prices
- Total sales
- Customer segments
- Payment methods
- Order statuses
- Source systems

## Data-Quality Problems

The synthetic dataset will deliberately contain realistic data-quality problems for analytical testing.

These may include:

- Missing values
- Duplicate order records
- Invalid customer or order identifiers
- Inconsistent categorical values
- Invalid dates
- Zero or negative quantities
- Zero or negative unit prices
- Incorrect total sales calculations
- Incomplete records
- Cross-field inconsistencies

The problems will be deliberately introduced using a reproducible data-generation process.

## Analytical Approach

The project will follow a structured data-quality workflow:

1. Generate the synthetic operational dataset.
2. Profile the raw dataset.
3. Define and apply data-quality rules.
4. Identify data-quality violations using SQL.
5. Perform independent data-quality analysis using Python.
6. Quantify affected records and rule violations.
7. Investigate patterns of poor data quality across regions, channels, and source systems.
8. Clean and standardise the affected data where appropriate.
9. Validate the cleaned dataset.
10. Produce a final data-quality audit report.

## Business Value

The audit is intended to demonstrate how a data analyst can identify problems in operational data before that data is used for management reporting.

The findings will help illustrate:

- The extent of data-quality problems.
- Which data fields are most affected.
- Which quality dimensions require attention.
- Whether particular source systems or operational segments have higher rates of data-quality issues.
- Which data-quality controls could reduce future reporting problems.

## Synthetic Data Disclaimer

This project uses entirely synthetic data created for portfolio and educational purposes.

The dataset does not represent the actual operational data of a real company, organisation, customer, or individual.

Any business findings generated from the dataset are therefore illustrative and should not be interpreted as findings from a real organisation.
