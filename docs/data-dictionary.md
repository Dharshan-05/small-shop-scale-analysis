# Data Dictionary & Schema Definitions

## Standard Project Report Schema

| Field Name | Data Type | Nullable | Description | Example Values |
| :--- | :--- | :--- | :--- | :--- |
| **`Date`** | String / Datetime | No | Calendar date of transaction formatted as `DD-MM-YYYY` or `YYYY-MM-DD`. | `01-02-2026`, `2026-02-01` |
| **`Day`** | String | Yes | Day of the week. Note: verified by backend calendar logic rather than trusting raw entry. | `Sunday`, `Monday` |
| **`Product_Category`** | String | Yes | Merchandise grouping or retail department. | `Snacks`, `Beverages`, `Grocery` |
| **`Product_Name`** | String | No | Stock-keeping unit (SKU) or product description. | `Biscuits`, `Tea`, `Chips`, `Coffee` |
| **`Quantity_Sold`** | Integer / Float | No | Non-negative count of units sold in transaction. | `20`, `15`, `25` |
| **`Price`** | Float | Optional | Unit price in Indian Rupees (₹ / INR). | `10.0`, `5.0`, `15.0` |
| **`Total_Sales`** | Float | Derived / Mapped | Total line revenue. Computed as `Quantity_Sold × Price` unless pre-calculated total column exists. | `200.0`, `75.0`, `375.0` |

---

## Preprocessing & Quality Audit Schema

### Data Quality Issues
- **`missing_date`** (Severity: Error): Row lacks a transaction date and cannot be attributed to a timeline; dropped.
- **`invalid_date_format`** (Severity: Error): Date string could not be parsed into a valid Gregorian date; dropped.
- **`weekday_calendar_mismatch`** (Severity: Warning): Input labeled day (e.g., `Monday`) contradicts Gregorian calendar (e.g., `Sunday`); corrected to actual calendar day.
- **`negative_quantity`** (Severity: Error): Units sold < 0; dropped.
- **`negative_price`** (Severity: Error): Unit price < 0; dropped.
- **`duplicate_row`** (Severity: Warning): Exact duplicate record detected in file; flagged for audit.
- **`missing_category`** (Severity: Warning): Category was null or empty; imputed as `'General'`.
- **`missing_product_name`** (Severity: Warning): Product name was null or empty; imputed as `'Unknown Item'`.
