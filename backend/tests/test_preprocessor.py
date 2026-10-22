import pytest
import pandas as pd
from backend.app.services.preprocessor import DataPreprocessor
from backend.app.schemas.sales import ColumnMappingConfig

def test_preprocess_report_sample_clean():
    # 4 rows from report
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
    assert clean_df.iloc[2]["day_of_week"] == "Monday" # 02-02-2026 is Monday
    assert report.date_corrections_count > 0
    
    # Check total sales computation
    assert clean_df.iloc[0]["total_sales"] == 200.0
    assert clean_df.iloc[1]["total_sales"] == 75.0
    assert clean_df.iloc[2]["total_sales"] == 375.0
    assert clean_df.iloc[3]["total_sales"] == 200.0

def test_preprocess_dirty_dataset():
    data = {
        "Date": ["01-02-2026", "01-02-2026", "02-02-2026", "03-02-2026", "not_a_date"],
        "Day": ["Sunday", "Sunday", "Monday", "Tuesday", "Wednesday"],
        "Product_Category": ["Snacks", "Snacks", None, "Grocery", "Household"],
        "Product_Name": ["Biscuits", "Biscuits", "Chips", "Rice", "Soap"],
        "Quantity_Sold": [10, 10, -5, "invalid", 5],
        "Price": [10, 10, 20, 50, -10]
    }
    df = pd.DataFrame(data)
    preprocessor = DataPreprocessor()
    clean_df, report = preprocessor.clean(df, ColumnMappingConfig())
    
    # Duplicate row detected
    assert report.duplicate_rows_detected >= 1
    # Invalid date and negative values rejected
    assert report.rejected_rows >= 2
    # Missing category imputed
    valid_accepted = clean_df[clean_df["product_name"] == "Chips"]
    if len(valid_accepted) > 0:
        assert valid_accepted.iloc[0]["product_category"] in ["General", "Uncategorized"]

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
    # Must equal 500.0 and 1200.0, NOT 500 * 2 = 1000
    assert clean_df.iloc[0]["total_sales"] == 500.0
    assert clean_df.iloc[1]["total_sales"] == 1200.0
