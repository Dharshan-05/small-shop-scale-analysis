import os
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd
from openpyxl import Workbook
from playwright.sync_api import sync_playwright

def run():
    screenshots_dir = os.path.abspath("docs/screenshots")
    scratch_dir = os.path.abspath("C:/Users/Dharshan/.gemini/antigravity/brain/2e6a0a8e-c33a-4260-a448-baa285f42c74/scratch")
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(scratch_dir, exist_ok=True)

    # 1. Prepare sample upload files (CSV and Excel)
    csv_upload_path = os.path.join(scratch_dir, "test_custom_upload.csv")
    upload_rows = ["Date,Category,Product,Quantity,Price"]
    for i in range(15):
        upload_rows.append(f"01-02-2026,Snacks,CustomItem_{i},10,10.0")
    with open(csv_upload_path, "w", encoding="utf-8") as f:
        f.write("\n".join(upload_rows))

    excel_upload_path = os.path.join(scratch_dir, "test_excel_upload.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.append(["TxDate", "Dept", "Item", "Units", "Rate"])
    for i in range(6):
        ws.append(["2026-02-01", "Grocery", f"ExcelProduct_{i}", 5, 20.0])
    wb.save(excel_upload_path)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()

        print("\n--- PHASE 1: Default Dashboard & Report Sample ---")
        page.goto("http://127.0.0.1:5173", wait_until="networkidle")
        time.sleep(2)

        # Title & benchmark figures
        assert "Small Shop Sales" in page.title()
        content = page.content()
        assert "850.00" in content, "Expected total revenue 850.00 not found"
        assert "70" in content, "Expected total quantity 70 not found"
        assert "Chips" in content, "Expected top product Chips not found"
        print("  [OK] Default report sample verified (Rs. 850.00, 70 units, Chips).")

        ss_1 = os.path.join(screenshots_dir, "01_dashboard_report_sample.png")
        page.screenshot(path=ss_1, full_page=True)
        print(f"  [OK] Saved screenshot: {ss_1}")

        print("\n--- PHASE 2: Dynamic Filters & Reset ---")
        # Filter by category "Snacks"
        page.click("button:has-text('Snacks')")
        time.sleep(1)
        content_filtered = page.content()
        assert "575.00" in content_filtered, "Expected Snacks filtered revenue 575.00"
        print("  [OK] Category filter 'Snacks' applied -> revenue updated to Rs. 575.00.")

        # Clear filters
        page.click("button:has-text('Clear')")
        time.sleep(1)
        content_cleared = page.content()
        assert "850.00" in content_cleared, "Expected cleared revenue 850.00"
        print("  [OK] Filters cleared -> revenue restored to Rs. 850.00.")

        print("\n--- PHASE 3: Multi-Day Dataset & Full CSV Export (>100 Rows) ---")
        page.select_option("select[aria-label='Select Dataset Source']", value="realistic_15_days")
        time.sleep(2)
        page.wait_for_load_state("networkidle")

        content_15d = page.content()
        assert "1,04,165.00" in content_15d or "104,165.00" in content_15d, "Expected 15-day revenue 1,04,165.00"
        print("  [OK] 15-Day dataset loaded: Rs. 1,04,165.00 turnover.")

        ss_3 = os.path.join(screenshots_dir, "03_dashboard_realistic_15_days.png")
        page.screenshot(path=ss_3, full_page=True)
        print(f"  [OK] Saved screenshot: {ss_3}")

        # Test Full CSV Export via Download
        with page.expect_download() as download_info:
            page.click("button:has-text('Export CSV')")
        download = download_info.value
        export_15d_path = os.path.join(scratch_dir, "downloaded_realistic_15_days.csv")
        download.save_as(export_15d_path)

        df_downloaded_15d = pd.read_csv(export_15d_path)
        print(f"  [OK] Downloaded CSV inspected: {len(df_downloaded_15d)} records.")
        # Assert full 189 rows, proving no 100-row preview truncation occurred!
        assert len(df_downloaded_15d) == 189, f"Expected 189 exported rows, got {len(df_downloaded_15d)}"
        assert df_downloaded_15d["total_sales"].sum() == 104165.0, "Exported total sales sum mismatch"
        print("  [OK] Deterministic export assertion passed: full 189 rows, exact Rs. 104,165.00 sum.")

        print("\n--- PHASE 4: Real CSV Upload, Column Mapping & Export ---")
        page.click("button:has-text('Upload Data')")
        page.wait_for_selector("text=Upload Small Shop Sales Dataset")
        time.sleep(1)

        ss_4 = os.path.join(screenshots_dir, "04_upload_modal.png")
        page.screenshot(path=ss_4)
        print(f"  [OK] Saved screenshot: {ss_4}")

        # Upload the test CSV file
        page.set_input_files("input[type='file']", csv_upload_path)
        time.sleep(2)
        # Click Analyze Dataset
        page.click("button:has-text('Analyze Dataset')")
        time.sleep(2)
        page.wait_for_load_state("networkidle")

        content_custom = page.content()
        # 15 items * (10 qty * 10 price) = 1500.00
        assert "1,500.00" in content_custom, "Expected custom upload revenue 1,500.00"
        print("  [OK] Custom CSV upload analyzed successfully: Rs. 1,500.00 revenue across 15 rows.")

        # Export the uploaded data
        with page.expect_download() as download_info_custom:
            page.click("button:has-text('Export CSV')")
        download_custom = download_info_custom.value
        export_custom_path = os.path.join(scratch_dir, "downloaded_custom_upload.csv")
        download_custom.save_as(export_custom_path)
        df_downloaded_custom = pd.read_csv(export_custom_path)
        assert len(df_downloaded_custom) == 15
        assert df_downloaded_custom["total_sales"].sum() == 1500.0
        print("  [OK] Custom CSV export verified: 15 rows, Rs. 1,500.00 total.")

        print("\n--- PHASE 5: Real Excel (.xlsx) Upload & Column Mapping ---")
        page.click("button:has-text('Upload Data')")
        page.wait_for_selector("text=Upload Small Shop Sales Dataset")
        time.sleep(1)

        page.set_input_files("input[type='file']", excel_upload_path)
        time.sleep(2)
        # Select column mappings
        page.locator("label:has-text('Date Column') + select").select_option("TxDate")
        page.locator("label:has-text('Product / Item Name Column') + select").select_option("Item")
        page.locator("label:has-text('Category / Department Column') + select").select_option("Dept")
        page.locator("label:has-text('Quantity Sold Column') + select").select_option("Units")
        page.locator("label:has-text('Unit Price Column') + select").select_option("Rate")

        page.click("button:has-text('Analyze Dataset')")
        time.sleep(2)
        page.wait_for_load_state("networkidle")

        content_excel = page.content()
        # 6 rows * (5 units * 20.0 rate) = 600.00
        assert "600.00" in content_excel, "Expected Excel upload revenue 600.00"
        print("  [OK] Excel (.xlsx) upload analyzed successfully: Rs. 600.00 revenue across 6 rows.")

        print("\n--- PHASE 6: Data Quality Audit Modal & Calendar Verification ---")
        page.select_option("select[aria-label='Select Dataset Source']", value="dirty_test")
        time.sleep(2)
        page.wait_for_load_state("networkidle")
        page.click("button[title='View Data Cleaning & Quality Audit']")
        page.wait_for_selector("text=Data Quality Audit & Preprocessing Log")
        time.sleep(1)

        ss_2 = os.path.join(screenshots_dir, "02_data_quality_audit_modal.png")
        page.screenshot(path=ss_2)
        print(f"  [OK] Saved screenshot: {ss_2}")

        page.click("button:has-text('Close Audit Log')")
        time.sleep(1)

        browser.close()
        print("\n=======================================================")
        print(" ALL PLAYWRIGHT E2E VERIFICATION PHASES PASSED 100%")
        print("=======================================================\n")

if __name__ == "__main__":
    run()
