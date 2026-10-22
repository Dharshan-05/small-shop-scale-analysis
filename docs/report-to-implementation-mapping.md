# Project Report to Implementation Traceability Mapping

This document provides a comprehensive traceability matrix linking the academic project report titled **“Small Shop Sales Pattern Analysis Using Data Science”** to the actual production implementation delivered in this repository.

---

## Traceability Matrix

| Report Section & Requirement | Report Claim / Specification | Implementation Location | Test / Verification Method | Status | Limitations & Justified Enhancements |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Introduction & 1.1 Org Profile** | Focuses on small daily-consumer retail shop transactions over a 10 to 15 day period. | `data/samples/report_sample_transactions.csv` & `data/samples/small_shop_15_days_realistic.csv` | Pytest + Playwright verification | **Complete** | **Enhancement:** Built both the literal 4-transaction report sample and the realistic 15-day dataset described in text so users can evaluate both. |
| **1.2 System Specification** | Windows 10/11, Python 3.x, Pandas, Matplotlib, Seaborn, Core i3+, 4GB RAM. | Backend in Python 3.11 (`backend/app/`), Frontend in React 18 (`frontend/src/`) | Environment tests, Pytest, Playwright | **Complete** | **Enhancement:** Transformed static script into an interactive web application while maintaining full local execution without cloud servers. |
| **2.2 & 2.2.1 Proposed System Features** | Automated data processing, cleaning, missing value handling, total sales calculation, product/category/day analysis. | `backend/app/services/preprocessor.py`, `backend/app/analytics/engine.py` | `test_preprocessor.py`, `test_analytics.py` | **Complete** | **Enhancement:** Added row-level quality audit reporting, auto-column mapping, and double-counting prevention. |
| **3.1, 3.2, 3.4 File & Input Design** | Tabular structure: `Date, Day, Product_Category, Product_Name, Quantity_Sold, Price, Total_Sales`. | `backend/app/schemas/sales.py`, `frontend/src/types/api.ts` | `test_schemas.py` | **Complete** | **Gap Addressed:** Supports Excel (.xlsx) and CSV with arbitrary user headers via the flexible Column Mapping Modal. |
| **3.3 Output Design & Visualizations** | Bar chart (product sales), Line chart (daily trends), Pie chart (category contribution), KPI summaries. | `frontend/src/components/KPICards.tsx`, `DailySalesChart.tsx`, `ProductPerformanceChart.tsx`, `CategoryPieChart.tsx`, `DayOfWeekChart.tsx` | Playwright browser automated screenshot verification | **Complete** | **Enhancement:** Interactive tooltips, responsive layout, and toggles between Revenue (₹) and Volume (Units). |
| **3.5.1 Description of Modules** | Data Collection, Data Preprocessing, Exploratory Data Analysis, Data Visualization, Insight Generation. | `backend/app/api/endpoints.py`, `backend/app/services/preprocessor.py`, `backend/app/analytics/engine.py`, `backend/app/analytics/insights.py` | Full Pytest suite (16 tests) | **Complete** | Strictly preserves modularity matching Chapter 3.5.1 definitions. |
| **Appendix C: Sample Coding** | Python code calculates `total = quantity * price`, aggregates product sales, and finds best seller. | `backend/app/analytics/engine.py:calculate_kpis` | `test_analytics.py::test_kpi_calculations_exact_report_values` | **Complete** | Exactly reproduces report totals: Biscuits=₹200, Tea=₹75, Chips=₹375, Coffee=₹200 (Total ₹850.00). |
| **Calendar Accuracy Check** | Report code claims `01-02-2026` is `"Monday"`. | `backend/app/services/preprocessor.py:clean` | `test_preprocessor.py::test_preprocess_report_sample_clean` | **Complete** | **Discrepancy Rectified:** The actual calendar shows 1 Feb 2026 was a Sunday. The preprocessor detects this mismatch and reconciles to the true calendar. |
| **Revenue vs Quantity Ranking** | Report sample claims Chips is best-selling, but treats revenue and volume interchangeably. | `backend/app/analytics/engine.py` & `KPICards.tsx` | `test_analytics.py` | **Complete** | **Critical Distinction:** Distinguishes Revenue Leader (₹) from Volume Leader (Units), preventing misleading business conclusions. |

---

## Detailed Analysis of Identified Report Gaps

1. **Discrepancy Between 4-Transaction Code and Described 15-Day Scope:**
   - The report's Appendix C code only includes 4 hardcoded transactions over 2 days (`01-02-2026` and `02-02-2026`), yet Section 1.1 states: *"The project focuses on collecting and analyzing the sales data of the shop over a specific period, typically 10 to 15 days."*
   - **Resolution:** We implemented both datasets. The exact 4-row dataset is available as `report_sample`, and a comprehensive 15-day dataset is available as `realistic_15_days` (189 transactions across 15 days from 01-02-2026 to 15-02-2026).

2. **Calendar Date / Weekday Inconsistency:**
   - In Appendix C, row 1 is `["01-02-2026", "Monday", "Snacks", "Biscuits", 20, 10]`.
   - A standard Gregorian calendar check demonstrates that February 1, 2026 is actually a **Sunday**.
   - **Resolution:** The system automatically validates dates with `pd.to_datetime` and computes the true `.day_name()`. When a discrepancy is detected, it logs a `weekday_calendar_mismatch` warning in the Data Quality Report and uses the verified day for time-series analysis.

3. **Double-Counting Risk in Generic Datasets:**
   - Many external retail datasets (such as Kaggle retail forecasting data) already provide line totals or pre-calculated sales revenue. If a system blindly executes `Quantity × Price` on a dataset that already has line totals, it can distort financial metrics.
   - **Resolution:** Our preprocessing layer provides a dedicated `total_sales_col` mapping option. If pre-calculated revenue exists, it is ingested directly without multiplication.
