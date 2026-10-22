import pytest
import io
import json
import pandas as pd
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import Settings

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"

def test_get_samples_list():
    res = client.get("/api/samples")
    assert res.status_code == 200
    samples = res.json()
    assert len(samples) >= 3
    sample_ids = [s["id"] for s in samples]
    assert "report_sample" in sample_ids
    assert "realistic_15_days" in sample_ids

def test_analyze_report_sample_endpoint():
    res = client.get("/api/samples/report_sample/analyze")
    assert res.status_code == 200
    data = res.json()
    assert data["dataset_source"] == "report_sample"
    assert data["kpis"]["total_revenue"] == 850.0
    assert data["kpis"]["total_quantity_sold"] == 70.0
    assert len(data["product_performance"]) == 4
    assert len(data["category_performance"]) == 2
    assert len(data["insights"]) > 0

def test_export_sample_full_rows_over_100():
    # The realistic_15_days sample has 189 records.
    # While preview is capped at 100, the export endpoint must export ALL 189 records!
    res = client.get("/api/samples/realistic_15_days/export")
    assert res.status_code == 200
    assert "attachment; filename=cleaned_realistic_15_days_full_export.csv" in res.headers["content-disposition"]
    
    csv_text = res.text
    lines = [line.strip() for line in csv_text.strip().split("\n") if line.strip()]
    header = lines[0]
    data_rows = lines[1:]
    
    assert "date" in header
    assert "total_sales" in header
    assert len(data_rows) == 189, f"Expected 189 exported rows, got {len(data_rows)}"
    
    # Calculate sum of total_sales column from exported CSV
    df = pd.read_csv(io.StringIO(csv_text))
    assert len(df) == 189
    assert df["total_sales"].sum() == 104165.0

def test_export_sample_with_category_filter():
    # Export realistic_15_days filtered to Snacks category only
    res = client.get("/api/samples/realistic_15_days/export?categories=Snacks")
    assert res.status_code == 200
    df = pd.read_csv(io.StringIO(res.text))
    assert len(df) > 0
    assert set(df["product_category"].unique()) == {"Snacks"}

def test_upload_and_export_full_uploaded_dataset():
    # Generate 120 distinct custom transactions
    rows = ["Date,Product_Name,Quantity_Sold,Price"]
    for i in range(120):
        rows.append(f"2026-02-01,Unique_Item_{i},2,10.0")
    csv_bytes = "\n".join(rows).encode("utf-8")
    
    mapping = {
        "date_col": "Date",
        "product_col": "Product_Name",
        "quantity_col": "Quantity_Sold",
        "price_col": "Price"
    }
    files = {"file": ("bulk_test.csv", io.BytesIO(csv_bytes), "text/csv")}
    data = {"mapping": json.dumps(mapping)}
    
    res = client.post("/api/upload/export", files=files, data=data)
    assert res.status_code == 200
    df = pd.read_csv(io.StringIO(res.text))
    # All 120 rows must be exported without truncation
    assert len(df) == 120
    assert df["total_sales"].sum() == 120 * 20.0

def test_cors_production_validation():
    # In production mode, wildcard CORS origin must be rejected with ValueError
    import os
    os.environ["ENVIRONMENT"] = "production"
    os.environ["CORS_ORIGINS"] = "http://localhost:5173,*"
    with pytest.raises(ValueError, match="Wildcard CORS origin"):
        Settings()
    
    # In development mode, safe default origins are populated without wildcard
    os.environ["ENVIRONMENT"] = "development"
    os.environ.pop("CORS_ORIGINS", None)
    s = Settings()
    assert "*" not in s.CORS_ORIGINS
    assert "http://localhost:5173" in s.CORS_ORIGINS

def test_upload_preview_csv():
    csv_content = b"Date,Product_Name,Quantity_Sold,Price\n2026-02-01,Biscuits,10,20\n2026-02-02,Tea,5,10\n"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    res = client.post("/api/upload/preview", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["total_rows"] == 2
    assert "Product_Name" in data["columns"]
    assert data["suggested_mapping"]["date_col"] == "Date"
    assert data["suggested_mapping"]["product_col"] == "Product_Name"

def test_upload_and_analyze_with_mapping():
    csv_content = b"TxDate,Item,Volume,UnitRate\n2026-02-01,Biscuits,10,20\n2026-02-02,Tea,5,10\n"
    mapping = {
        "date_col": "TxDate",
        "product_col": "Item",
        "quantity_col": "Volume",
        "price_col": "UnitRate"
    }
    files = {"file": ("custom.csv", io.BytesIO(csv_content), "text/csv")}
    data = {"mapping": json.dumps(mapping)}
    res = client.post("/api/upload/analyze", files=files, data=data)
    assert res.status_code == 200
    resp_data = res.json()
    assert resp_data["kpis"]["total_revenue"] == 250.0
    assert resp_data["kpis"]["total_quantity_sold"] == 15.0
    assert resp_data["total_cleaned_records"] == 2
