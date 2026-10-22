# Kaggle Dataset Integration & Provenance

## Source Reference
- **URL Requested:** https://www.kaggle.com/datasets/svizor/retail-sales-forecasting-data
- **Designation:** External Kaggle demonstration data (NOT actual proprietary sales records from a specific shop)

## Access Status & Blocker Documentation
- Direct automated retrieval returned `HTTP 404: Not Found` from the Kaggle dataset endpoint.
- On Kaggle, dataset slugs may be modified, made private, or require user-authenticated sessions via Kaggle API tokens (`kaggle.json`).

## How to Supply External Kaggle Data
If you download a retail forecasting dataset from Kaggle (such as store sales forecasting datasets or TEVEC retail demand datasets):
1. Download the archive from Kaggle.
2. Place the CSV file(s) into this directory (`data/kaggle/`), e.g., `sales.csv`.
3. Open the Small Shop Sales Analysis web application.
4. Navigate to **Upload Dataset**, select the CSV file, and use the built-in **Column Mapping** feature to map:
   - Date column (e.g., `date` or `data` -> `Date`)
   - Product / Department (e.g., `department` or `sku` -> `Product_Name`)
   - Quantity / Volume (e.g., `venda` or `units` -> `Quantity_Sold`)
   - Price / Total (e.g., `preco` -> `Price` or `weekly_sales` -> `Total_Sales`)

The application supports both unit-based (`Quantity * Price`) and pre-calculated total revenue datasets without double-counting!
