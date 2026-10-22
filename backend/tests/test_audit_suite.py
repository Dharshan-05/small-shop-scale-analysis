import os
import io
import json
import pandas as pd
from openpyxl import Workbook
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_audit_excel_upload_and_analyze():
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Date", "Day", "Category", "Product", "Quantity", "Price"])
    ws.append(["2026-02-01", "Sunday", "Snacks", "Biscuits", 10, 20])
    ws.append(["2026-02-02", "Monday", "Beverages", "Tea", 20, 10])
    
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)
    
    files = {"file": ("test_upload.xlsx", excel_io.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    res_preview = client.post("/api/upload/preview", files=files)
    assert res_preview.status_code == 200
    preview_data = res_preview.json()
    assert preview_data["total_rows"] == 2
    assert "Product" in preview_data["columns"]

    mapping = {
        "date_col": "Date",
        "category_col": "Category",
        "product_col": "Product",
        "quantity_col": "Quantity",
        "price_col": "Price"
    }
    files = {"file": ("test_upload.xlsx", excel_io.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"mapping": json.dumps(mapping)}
    res_analyze = client.post("/api/upload/analyze", files=files, data=data)
    assert res_analyze.status_code == 200
    analyze_data = res_analyze.json()
    assert analyze_data["kpis"]["total_revenue"] == 400.0
    assert analyze_data["kpis"]["total_quantity_sold"] == 30.0

def test_audit_double_counting_protection():
    csv_precalc = (
        "Date,Item,Units,Line_Total\n"
        "2026-02-01,Shirt,5,500.0\n"
        "2026-02-02,Pants,2,1000.0\n"
    ).encode("utf-8")
    mapping_precalc = {
        "date_col": "Date",
        "product_col": "Item",
        "quantity_col": "Units",
        "total_sales_col": "Line_Total"
    }
    files = {"file": ("precalc.csv", io.BytesIO(csv_precalc), "text/csv")}
    data = {"mapping": json.dumps(mapping_precalc)}
    res = client.post("/api/upload/analyze", files=files, data=data)
    assert res.status_code == 200
    data = res.json()
    assert data["kpis"]["total_revenue"] == 1500.0
    assert data["kpis"]["total_quantity_sold"] == 7.0

def test_audit_calendar_reconciliation():
    csv_calendar = (
        "Date,Day,Product,Quantity,Price\n"
        "01-02-2026,Monday,ItemA,1,10\n"
        "02-02-2026,Friday,ItemB,2,15\n"
    ).encode("utf-8")
    files = {"file": ("calendar.csv", io.BytesIO(csv_calendar), "text/csv")}
    res = client.post("/api/upload/analyze", files=files)
    assert res.status_code == 200
    cal_data = res.json()
    assert cal_data["quality_report"]["date_corrections_count"] == 2
    recs = cal_data["records_preview"]
    assert recs[0]["day_of_week"] == "Sunday"
    assert recs[1]["day_of_week"] == "Monday"

def test_audit_dirty_data_rejections():
    csv_dirty = (
        "Date,Product,Quantity,Price\n"
        "01-02-2026,ValidItem,10,10\n"
        "01-02-2026,ValidItem,10,10\n"
        "not-a-date,BadDateItem,5,10\n"
        "02-02-2026,NegQtyItem,-5,10\n"
        "02-02-2026,NegPriceItem,5,-10\n"
        ",NullDateItem,5,10\n"
    ).encode("utf-8")
    files = {"file": ("dirty.csv", io.BytesIO(csv_dirty), "text/csv")}
    res = client.post("/api/upload/analyze", files=files)
    assert res.status_code == 200
    data = res.json()
    q = data["quality_report"]
    assert q["total_raw_rows"] == 6
    assert q["rejected_rows"] == 5
    assert q["duplicate_rows_detected"] == 1
    assert q["duplicate_rows_removed"] == 1
    assert q["accepted_rows"] == 1

def test_audit_screenshot_files_exist_and_valid():
    ss_dir = "docs/screenshots"
    assert os.path.exists(ss_dir)
    screenshots = [
        "01_dashboard_report_sample.png",
        "02_data_quality_audit_modal.png",
        "03_dashboard_realistic_15_days.png",
        "04_upload_modal.png"
    ]
    for ss in screenshots:
        p = os.path.join(ss_dir, ss)
        assert os.path.exists(p)
        assert os.path.getsize(p) > 20000

def test_audit_benchmark_sample_math():
    df_report = pd.read_csv("data/samples/report_sample_transactions.csv")
    calc_totals = df_report["Quantity_Sold"] * df_report["Price"]
    assert list(calc_totals) == [200, 75, 375, 200]
    assert calc_totals.sum() == 850

    df_15d = pd.read_csv("data/samples/small_shop_15_days_realistic.csv")
    assert len(df_15d) == 189
    assert (df_15d["Quantity_Sold"] * df_15d["Price"]).sum() == 104165.0
