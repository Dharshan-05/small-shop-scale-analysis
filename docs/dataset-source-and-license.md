# Dataset Provenance, Licensing & External Kaggle Documentation

## 1. Overview of Data Sources

This application supports three distinct tiers of data:
1. **Academic Report Sample Data (`report_sample`):**
   - **Source:** Literal reproduction of the 4 transactions documented in Appendix C of the college project report.
   - **Records:** 4 rows (Biscuits, Tea, Chips, Coffee across 01-02-2026 and 02-02-2026).
   - **Purpose:** Direct unit verification against the calculations and figures shown in the report.
2. **Deterministic 15-Day Small Shop Demonstration Data (`realistic_15_days`):**
   - **Source:** Deterministic synthetic dataset generated to fulfill Section 1.1 of the report ("collecting and analyzing sales data... typically 10 to 15 days").
   - **Records:** 189 transactions across 14 grocery and household products from 01-02-2026 to 15-02-2026.
   - **Purpose:** Full demonstration of multi-day time-series patterns, category distributions, and weekend surges.
   - **Labeling:** Clearly designated as synthetic demonstration data; never represented as proprietary small shop records.
3. **User Uploads & External Kaggle Data (`user_upload`):**
   - **Source:** User-provided `.csv` or `.xlsx` files uploaded through the web application interface.

---

## 2. Kaggle Dataset Inspection & Status

### Requested Kaggle Dataset
- **URL:** `https://www.kaggle.com/datasets/svizor/retail-sales-forecasting-data`
- **Host User:** `svizor`
- **Topic:** Retail Sales Forecasting Data (Store demand & weekly department forecasting)

### Verification & Access Blocker Findings
During automated inspection of the requested URL:
- Direct HTTP requests to `https://www.kaggle.com/datasets/svizor/retail-sales-forecasting-data` returned **`HTTP 404: Not Found`**.
- Kaggle dataset slugs may be made private, modified by the author, or restricted behind Kaggle user authentication protocols requiring API key tokens (`kaggle.json`).

### Schema Comparison with Report Schema

| Report Example Schema | Typical Kaggle Retail Schema (`svizor` / Walmart format) | Mapping & Handling Strategy |
| :--- | :--- | :--- |
| **`Date`** | `date` / `Date` | Mapped directly via `date_col`. |
| **`Day`** | *(Usually absent)* | Automatically derived from Gregorian calendar date. |
| **`Product_Category`** | `department` / `store_type` | Mapped to `category_col`. |
| **`Product_Name`** | `sku` / `department` | Mapped to `product_col` (if missing, defaults to "Item"). |
| **`Quantity_Sold`** | `venda` / `units` | Mapped to `quantity_col` (if missing, defaults to 1 per record). |
| **`Price`** | `preco` | Mapped to `price_col`. |
| **`Total_Sales`** | `weekly_sales` / `amount` | Mapped to `total_sales_col` (prevents double-counting). |

---

## 3. Step-by-Step Kaggle Dataset Recovery Instructions

If you have acquired a Kaggle retail dataset (e.g., Walmart Sales Forecasting or Brazilian Retail Sales):

1. **Obtain the file:** Download the dataset CSV file to your local computer (e.g. `sales.csv`).
2. **Store locally:** Place a copy in `data/kaggle/sales.csv` for local reference.
3. **Open the Web Application:** Open `http://localhost:5173` in any modern web browser.
4. **Click "Upload Data":**
   - Drag or browse to your downloaded CSV file.
   - The preview window will display detected columns.
5. **Set Column Mappings:**
   - Map Date column to `date`.
   - Map Product column to `sku` or `department`.
   - Map Quantity to `venda` or units.
   - If pre-calculated revenue exists (such as `weekly_sales`), assign it to **"Pre-Calculated Total Sales Column"**.
6. **Click "Analyze Dataset":**
   - The application will process, clean, and display complete interactive analytics without modifying your source files.
