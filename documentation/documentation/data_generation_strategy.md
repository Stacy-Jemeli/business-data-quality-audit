# Synthetic Data Generation Strategy

## Overview

This document defines the methodology used to generate the synthetic operational sales dataset for the data-quality audit project.

The purpose of the generation process is to create a realistic operational dataset containing valid records as well as controlled, reproducible data-quality problems.

The dataset is synthetic and does not represent data from a real organisation.

---

## Dataset Size

The target dataset will contain approximately:

**10,000 order records**

The dataset will represent approximately:

**3,000–4,000 unique customers**

Each customer may have multiple orders.

This creates a realistic one-to-many relationship between customers and orders.

---

## Generation Approach

The dataset will be generated in two major phases:

### Phase 1 — Generate Valid Operational Data

First, a clean baseline dataset will be generated.

At this stage:

- Customer IDs will follow the approved format.
- Order IDs will follow the approved format.
- Order dates will fall within the reporting period.
- Categorical variables will use approved values.
- Quantities will be positive.
- Unit prices will be positive.
- Total sales will equal quantity multiplied by unit price.
- Required fields will be populated.

This clean baseline provides the reference from which controlled data-quality problems can be introduced.

### Phase 2 — Introduce Controlled Data-Quality Problems

After generating valid records, selected records will be deliberately modified to simulate common operational data-quality problems.

The modifications will be reproducible and documented.

---

## Reporting Period

The synthetic dataset will use the following reporting period:

**1 January 2025 – 30 June 2026**

Valid order dates must fall within this period.

---

## Reproducibility

A fixed random seed will be used during data generation.

The initial implementation will use:

```python
random_state = 42
