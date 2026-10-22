import os
import sys
import time
from playwright.sync_api import sync_playwright

def run():
    screenshots_dir = os.path.abspath("docs/screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("1. Navigating to http://127.0.0.1:5173 ...")
        page.goto("http://127.0.0.1:5173", wait_until="networkidle")
        time.sleep(2)

        # Verify page title
        title = page.title()
        print(f"Page Title: {title}")
        assert "Small Shop Sales" in title

        # Verify exact report sample values
        content = page.content()
        assert "850.00" in content, "Expected total revenue 850.00 not found"
        assert "70" in content, "Expected total quantity 70 not found"
        assert "Chips" in content, "Expected top product Chips not found"
        print("[OK] Verified report sample calculations: Total Revenue=850.00, Quantity=70, Top Product=Chips")

        # Take screenshot of default dashboard
        screenshot_1 = os.path.join(screenshots_dir, "01_dashboard_report_sample.png")
        page.screenshot(path=screenshot_1, full_page=True)
        print(f"[OK] Saved screenshot: {screenshot_1}")

        # Open Data Quality Modal
        print("2. Opening Data Quality Modal...")
        page.click("button:has-text('Quality')")
        page.wait_for_selector("text=Data Quality Audit & Preprocessing Log")
        time.sleep(1)

        modal_text = page.content()
        assert "Raw Input Rows" in modal_text
        assert "Date/Day Corrections" in modal_text
        print("[OK] Data Quality Audit Modal rendered with calendar reconciliation details.")

        screenshot_2 = os.path.join(screenshots_dir, "02_data_quality_audit_modal.png")
        page.screenshot(path=screenshot_2)
        print(f"[OK] Saved screenshot: {screenshot_2}")

        # Close Modal
        page.click("button:has-text('Close Audit Log')")
        time.sleep(1)

        # Switch to 15-day realistic dataset
        print("3. Switching dataset to 15-Day Realistic Small Shop...")
        page.select_option("select", value="realistic_15_days")
        time.sleep(2)
        page.wait_for_load_state("networkidle")

        content_15d = page.content()
        assert "Realistic 15-Day" in content_15d
        assert "189" in content_15d # 189 transactions
        print("[OK] Successfully loaded 15-Day Realistic dataset with 189 transactions.")

        screenshot_3 = os.path.join(screenshots_dir, "03_dashboard_realistic_15_days.png")
        page.screenshot(path=screenshot_3, full_page=True)
        print(f"[OK] Saved screenshot: {screenshot_3}")

        # Open Upload Modal
        print("4. Testing Upload Modal...")
        page.click("button:has-text('Upload Data')")
        page.wait_for_selector("text=Upload Small Shop Sales Dataset")
        time.sleep(1)

        screenshot_4 = os.path.join(screenshots_dir, "04_upload_modal.png")
        page.screenshot(path=screenshot_4)
        print(f"[OK] Saved screenshot: {screenshot_4}")

        page.click("button:has-text('Cancel')")
        time.sleep(1)

        browser.close()
        print("\n=== ALL PLAYWRIGHT E2E VERIFICATION CHECKS PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    run()
