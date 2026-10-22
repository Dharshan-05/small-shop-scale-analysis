import pytest
import pandas as pd
from backend.app.services.preprocessor import DataPreprocessor
from backend.app.schemas.sales import ColumnMappingConfig

def test_preprocess_report_sample_clean():
    data = {
        "Date": ["01-02-2026", "01-02-2026", "02-02-2026", "02-02-2026"],
        "Day": ["Monday", "Monday", "Tuesday", "Tuesday"],
        "Product_Category": ["Snacks", "Beverages", "Snacks", "Beverages"],
        "Product_Name": ["Biscuits", "Tea", "Chips", "Coffee"],
        "Quantity_Sold": [20, 15, 25, 10],
        "Price": [10, 5, 15, 20]
    }
    df = pd.DataFrame(data)
    preprocessor = DataPreprocessor()
    clean_df, report = preprocessor.clean(df, ColumnMappingConfig())
    
    assert report.total_raw_rows == 4
    assert report.accepted_rows == 4
    assert report.rejected_rows == 0
    assert len(clean_df) == 4
    
    # Check calendar correction: 01-02-2026 is actually Sunday, not Monday
    assert clean_df.iloc[0]["day_of_week"] == "Sunday"
    assert clean_df.iloc[2]["day_of_week"] == "Monday"
    assert report.date_corrections_count > 0
    
    # Check total sales computation
    assert clean_df.iloc[0]["total_sales"] == 200.0
    assert clean_df.iloc[1]["total_sales"] == 75.0
    assert clean_df.iloc[2]["total_sales"] == 375.0
    assert clean_df.iloc[3]["total_sales"] == 200.0

def test_duplicate_policy_remove_exact():
    data = {
        "Date": ["01-02-2026", "01-02-2026", "02-02-2026"],
        "Product_Name": ["Biscuits", "Biscuits", "Biscuits"],
        "Quantity_Sold": [10, 10, 10],
        "Price": [20, 20, 20]
    }
    # Rows 0 and 1 are exact duplicates (same date, same product, same qty, same price)
    # Row 2 is on a different date (02-02-2026), so it is a distinct, legitimate transaction
    df = pd.DataFrame(data)
    preprocessor = DataPreprocessor()
    
    mapping = ColumnMappingConfig(
        date_col="Date",
        product_col="Product_Name",
        quantity_col="Quantity_Sold",
        price_col="Price",
        duplicate_policy="remove_exact"
    )
    clean_df, report = preprocessor.clean(df, mapping)
    
    assert report.total_raw_rows == 3
    assert report.duplicate_rows_detected == 1
    assert report.duplicate_rows_removed == 1
    assert report.accepted_rows == 2
    assert len(clean_df) == 2
    # Ensure total sales is 2 * (10 * 20) = 400.0, NOT inflated to 600.0
    assert clean_df["total_sales"].sum() == 400.0

def test_duplicate_policy_keep_all():
    data = {
        "Date": ["01-02-2026", "01-02-2026"],
        "Product_Name": ["Biscuits", "Biscuits"],
        "Quantity_Sold": [10, 10],
        "Price": [20, 20]
    }
    df = pd.DataFrame(data)
    preprocessor = DataPreprocessor()
    
    mapping = ColumnMappingConfig(
        date_col="Date",
        product_col="Product_Name",
        quantity_col="Quantity_Sold",
        price_col="Price",
        duplicate_policy="keep_all"
    )
    clean_df, report = preprocessor.clean(df, mapping)
    
    assert report.duplicate_rows_detected == 1
    assert report.duplicate_rows_removed == 0
    assert report.accepted_rows == 2
    assert len(clean_df) == 2

def test_non_duplicate_same_product_different_attributes():
    # Transactions of the same product with different quantity or different price are NOT duplicates
    data = {
        "Date": ["01-02-2026", "01-02-2026", "01-02-2026"],
        "Product_Name": ["Tea", "Tea", "Tea"],
        "Quantity_Sold": [1, 2, 1],
        "Price": [10, 10, 15]
    }
    df = pd.DataFrame(data)
    preprocessor = DataPreprocessor()
    clean_df, report = preprocessor.clean(df, ColumnMappingConfig(
        date_col="Date",
        product_col="Product_Name",
        quantity_col="Quantity_Sold",
        price_col="Price"
    ))
    
    assert report.duplicate_rows_detected == 0
    assert report.duplicate_rows_removed == 0
    assert len(clean_df) == 3

def test_precalculated_total_sales_no_double_counting():
    data = {
        "Date": ["2026-02-01", "2026-02-02"],
        "Product_Name": ["Shirt", "Shoes"],
        "Quantity_Sold": [2, 1],
        "Total_Sales": [500.0, 1200.0]
    }
    df = pd.DataFrame(data)
    mapping = ColumnMappingConfig(
        date_col="Date",
        product_col="Product_Name",
        quantity_col="Quantity_Sold",
        price_col="",
        total_sales_col="Total_Sales"
    )
    preprocessor = DataPreprocessor()
    clean_df, report = preprocessor.clean(df, mapping)
    
    assert len(clean_df) == 2
    assert clean_df.iloc[0]["total_sales"] == 500.0
    assert clean_df.iloc[1]["total_sales"] == 1200.0
