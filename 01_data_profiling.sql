-- ============================================================
-- BUSINESS DATA QUALITY AUDIT
-- SQL DATA PROFILING
-- ============================================================
-- Purpose:
-- Profile the raw operational sales dataset before applying
-- formal data-quality rules.
--
-- Dataset:
-- operational_sales_raw.csv
--
-- SQL dialect:
-- DuckDB
-- ============================================================


-- ------------------------------------------------------------
-- 1. Load the raw dataset
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE operational_sales_raw AS
SELECT *
FROM read_csv_auto(
    'data/raw/operational_sales_raw.csv',
    HEADER = TRUE
);


-- ------------------------------------------------------------
-- 2. Confirm the number of records
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS total_records
FROM operational_sales_raw;
