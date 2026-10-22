# Small Shop Sales Pattern Analysis Using Data Science

A full-stack, local-first retail analytics platform built to operationalize the university project report **“Small Shop Sales Pattern Analysis Using Data Science.”**

This application enables small shop owners, business analysts, and students to transform raw daily sales transaction records into verified data science insights, interactive time-series visualizations, product rankings, and automated findings.

---

## 1. Key Features

- **Automated Data Cleaning & Quality Audit:** Detects missing entries, negative values, and duplicate records. Provides a row-level audit log and summary metrics.
- **Calendar Day-of-Week Reconciliation:** Parses transaction dates and calculates genuine Gregorian weekdays using datetime libraries, catching and correcting human clerical errors (such as `01-02-2026` erroneously annotated as Monday instead of Sunday).
- **Flexible Column Mapping Layer:** Supports any CSV or Excel (`.xlsx`) file with custom headers, allowing easy migration from legacy shop spreadsheets.
- **Double-Counting Guard:** Distinguishes unit-based calculations (`Quantity × Unit Price`) from pre-calculated line totals (`Total_Sales`), preventing inflated revenue metrics.
- **Deterministic Analytics Engine:** Computes Total Revenue, Units Sold, Daily Averages, Average Order Value, Product/Category rankings, and Weekday vs Weekend velocity.
- **Interactive Visual Dashboard:** Built with React 18, Tailwind CSS, and Recharts, featuring daily time-series line charts, product ranking bars, category distribution donut charts, and weekday comparison bar charts.
- **Evidence-Based Findings Generator:** Synthesizes actionable observations and inventory warnings strictly from computed metrics without data hallucination.
- **Clean Table Export:** Filterable, sortable transaction table with direct one-click CSV export.

---

## 2. System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit)
- **Processor:** Intel Core i3 or higher (Core i5 recommended)
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** Minimum 500MB free disk space
- **Runtimes:** Python 3.11+, Node.js 18+ (or Bun 1.x), Git

---

## 3. Repository Structure

```text
small-shop-sales-analysis/
├── backend/
│   ├── app/
│   │   ├── analytics/        # Deterministic aggregations & automated insights
│   │   ├── api/              # FastAPI endpoints (upload, preview, analyze, export)
│   │   ├── core/             # Configuration & environment settings
│   │   ├── schemas/          # Pydantic v2 data models & quality reports
│   │   ├── services/         # Data preprocessor, auto-mapping & calendar auditor
│   │   └── main.py           # FastAPI entrypoint
│   ├── tests/                # 16 unit & integration tests (100% pass)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # UI components (KPIs, Charts, Modals, Table, FilterBar)
│   │   ├── services/         # Typed REST API client
│   │   ├── types/            # TypeScript interfaces
│   │   ├── App.tsx           # Master dashboard state & layout
│   │   └── main.tsx          # React DOM entrypoint
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docs/
│   ├── Small_Shop_Sales_Pattern_Analysis_Report.pdf  # Original reference report
│   ├── architecture.md                              # System architecture & data flow
│   ├── data-dictionary.md                           # Schema definitions & quality codes
│   ├── report-to-implementation-mapping.md          # Full traceability matrix & gap analysis
│   ├── dataset-source-and-license.md                # Provenance & Kaggle setup guide
│   ├── testing.md                                   # Verification results & test logs
│   └── screenshots/                                 # Playwright verification captures
├── data/
│   ├── samples/              # Built-in demo datasets (report sample, 15-day, dirty test)
│   └── kaggle/               # Directory for user-provided Kaggle datasets
├── scripts/
│   └── verify_e2e.py         # Automated Playwright browser verification suite
├── .env.example
├── .gitignore
└── README.md
```

---

## 4. Dataset Provenance & Labelling

The application ships with three built-in datasets in `data/samples/`, clearly distinguished by source:

1. **`report_sample_transactions.csv` (Academic Reference Benchmark):**
   - **Type:** Exact reproduction of the 4 transactions documented in Appendix C of the college project report.
   - **Metrics:** Biscuits (₹200), Tea (₹75), Chips (₹375), Coffee (₹200). Total Revenue = **₹850.00**, Units = **70**.
2. **`small_shop_15_days_realistic.csv` (Synthetic Demonstration Dataset):**
   - **Type:** Deterministic synthetic dataset generated to satisfy Chapter 1.1 of the report ("sales data... over 10 to 15 days").
   - **Metrics:** 189 transactions across 15 trading days (01-02-2026 to 15-02-2026) covering 14 grocery and household products. Total Sales = **₹104,165.00**.
   - **Labeling:** Strictly labelled as synthetic demonstration data; not real proprietary records.
3. **`small_shop_dirty_test.csv` (Quality Audit Benchmark):**
   - **Type:** Synthetic test dataset with intentional flaws: missing category, negative quantities, negative prices, unparseable dates, and duplicate rows. Demonstrates audit and cleaning resilience.
4. **External Kaggle Datasets (`data/kaggle/`):**
   - The requested Kaggle URL (`https://www.kaggle.com/datasets/svizor/retail-sales-forecasting-data`) returned an HTTP 404 on Kaggle.
   - Any external retail forecasting CSV can be placed in `data/kaggle/` and analyzed using the built-in column mapping layer.

---

## 5. API Endpoints Reference

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Health check & system version | None | `{"status": "ok", "app": "...", "version": "1.0.0"}` |
| `GET` | `/api/samples` | List available built-in datasets | None | Array of `SampleDatasetMeta` objects |
| `GET` | `/api/samples/{id}/analyze` | Compute sales analytics on a sample | Query params (date filters, categories) | `SalesAnalyticsResponse` JSON |
| `POST` | `/api/upload/preview` | Inspect and auto-map uploaded file | `file` (Multipart form-data: CSV or Excel) | Column list, row count, preview, suggested mapping |
| `POST` | `/api/upload/analyze` | Clean, audit, and analyze user dataset | `file`, `mapping` JSON, optional filters | `SalesAnalyticsResponse` JSON |
| `GET` | `/api/samples/{id}/export` | Export cleaned sample to CSV | None | CSV file attachment stream |
| `GET` | `/docs` | Interactive Swagger API documentation | None | OpenAPI Swagger UI |

---

## 6. Windows Clean-Machine Setup & Execution Guide

### Step 1: Clone or Navigate to the Workspace
```powershell
cd "d:\PROJECT\small shop scale analysis"
```

### Step 2: Install Python Backend Dependencies
Ensure Python 3.11+ is installed (`py --version`).
```powershell
py -m pip install -r backend/requirements.txt
```
*(Required packages: `fastapi`, `uvicorn`, `pydantic`, `pandas`, `openpyxl`, `python-multipart`, `pytest`, `httpx`)*

### Step 3: Install Frontend Dependencies
Ensure Node.js or Bun is installed (`node --version` or `bun --version`).
```powershell
cd frontend
bun install
# Or if using standard npm:
# npm install
cd ..
```

---

## 7. Running the Application

### Terminal 1: Launch Backend API Server
```powershell
cd "d:\PROJECT\small shop scale analysis"
py -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend runs on `http://127.0.0.1:8000`. API docs available at `http://127.0.0.1:8000/docs`.*

### Terminal 2: Launch Frontend Web Dashboard
```powershell
cd "d:\PROJECT\small shop scale analysis\frontend"
bun run dev -- --host 127.0.0.1 --port 5173
# Or if using npm:
# npm run dev -- --host 127.0.0.1 --port 5173
```
*Frontend runs on `http://127.0.0.1:5173`.*

---

## 8. Running Automated Tests & Verification

### Run Backend Unit & Integration Tests (16 Tests)
```powershell
cd "d:\PROJECT\small shop scale analysis"
py -m pytest backend/tests/ -v
```

### Run Frontend Production Build & TypeScript Check
```powershell
cd "d:\PROJECT\small shop scale analysis\frontend"
bun run --bun tsc --noEmit
bun run build
cd ..
```

### Run Playwright Browser End-to-End Verification
Make sure both servers are running, then execute:
```powershell
cd "d:\PROJECT\small shop scale analysis"
py scripts/verify_e2e.py
```
This automated browser test executes live assertions against the interface and updates the screenshot proofs in `docs/screenshots/`.

---

## 9. Troubleshooting Guide

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **Port 8000 already in use** | Another Uvicorn process is listening on port 8000. | Check processes with `Get-NetTCPConnection -LocalPort 8000` and stop the conflicting PID, or run on an alternate port with `--port 8001`. |
| **Port 5173 already in use** | Another Vite dev server is running. | Vite will automatically suggest port 5174, or specify `--port 5174`. Update `frontend/vite.config.ts` proxy if needed. |
| **Excel (.xlsx) upload fails** | Missing `openpyxl` dependency. | Run `py -m pip install openpyxl`. |
| **Playwright Chromium error** | Chromium browser binaries not installed for Playwright. | Run `py -m playwright install chromium`. |
| **CORS errors in browser console** | Accessing from an unwhitelisted port. | Check `.env.example` / `backend/app/core/config.py`. Port 5173 and 3000 are whitelisted by default. |
| **File encoding error during upload** | Legacy CSV saved in ANSI / Windows-1252. | The backend automatically falls back to `latin-1` if UTF-8 decoding fails. If problem persists, re-save CSV as UTF-8 in Excel. |

---

## 10. License & Attribution

- Built as an engineering expansion of the academic project report **“Small Shop Sales Pattern Analysis Using Data Science.”**
- Released for educational, demonstration, and small business analytics use under the MIT License.
