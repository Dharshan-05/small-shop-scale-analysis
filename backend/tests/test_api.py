import pytest
import io
import json
from fastapi.testclient import TestClient
from backend.app.main import app

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
    assert resp_data["kpis"]["total_revenue"] == 250.0 # 200 + 50
    assert resp_data["kpis"]["total_quantity_sold"] == 15.0
