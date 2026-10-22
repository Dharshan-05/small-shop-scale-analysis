# Small Shop Sales Pattern Analysis Using Data Science

A full-stack, local-first retail analytics platform built to operationalize the university project report **“Small Shop Sales Pattern Analysis Using Data Science.”**

This application enables small shop owners and business analysts to transform raw manual daily sales transaction logs into verified data science insights, interactive time-series visualizations, product rankings, and automated findings.

---

## Key Features

- **Automated Data Cleaning & Quality Audit:** Detects missing entries, negative values, and duplicate records. Provides a row-level audit log and summary metrics.
- **Calendar Day-of-Week Reconciliation:** Parses transaction dates and calculates genuine Gregorian weekdays using datetime libraries, catching and correcting human clerical errors (such as `01-02-2026` erroneously annotated as Monday instead of Sunday).
- **Flexible Column Mapping Layer:** Supports any CSV or Excel (`.xlsx`) file with custom headers, allowing easy migration from legacy shop spreadsheets.
- **Double-Counting Guard:** Distinguishes unit-based calculations (`Quantity × Unit Price`) from pre-calculated line totals (`Total_Sales`), preventing inflated revenue metrics.
- **Deterministic Analytics Engine:** Computes Total Revenue, Units Sold, Daily Averages, Average Order Value, Product/Category rankings, and Weekday vs Weekend velocity.
- **Interactive Visual Dashboard:** Built with React 18, Tailwind CSS, and Recharts, featuring daily time-series line charts, product ranking bars, category distribution donut charts, and weekday comparison bar charts.
- **Evidence-Based Findings Generator:** Synthesizes actionable observations and inventory warnings strictly from computed metrics without data hallucination.
- **Clean Table Export:** Filterable, sortable transaction table with direct one-click CSV export.

---

## System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit)
- **Processor:** Intel Core i3 or equivalent (Core i5 recommended)
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** Minimum 500MB free disk space
- **Runtimes:** Python 3.11+, Node.js 18+ (or Bun 1.x)

---

## Repository Structure

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

## Quickstart Guide (Windows)

### 1. Start the Backend API

In a PowerShell terminal:

```powershell
# Navigate to project root
cd "d:\PROJECT\small shop scale analysis"

# Run FastAPI backend with Uvicorn
py -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend API will start at `http://127.0.0.1:8000`. Interactive Swagger API documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Start the Frontend Dashboard

In a second PowerShell terminal:

```powershell
cd "d:\PROJECT\small shop scale analysis\frontend"

# Install dependencies (if not already installed)
bun install  # or npm install

# Start Vite dev server
bun run dev -- --host 127.0.0.1 --port 5173
```

Open your web browser and navigate to:
**`http://127.0.0.1:5173`**

---

## Running the Automated Test Suite

### Backend Unit & Integration Tests (16 Tests)
```powershell
py -m pytest backend/tests/ -v
```

### Frontend Production Build Verification
```powershell
cd frontend
bun run build  # or npm run build
```

### End-to-End Browser Verification (Playwright)
Ensure both backend and frontend are running, then run:
```powershell
py scripts/verify_e2e.py
```
This automated script tests dashboard rendering, verifies calculations against report figures, exercises the data quality audit modal, switches datasets, and saves screenshot proofs into `docs/screenshots/`.

---

## Kaggle External Dataset Instructions

If you wish to test with an external Kaggle retail dataset:
1. Refer to `docs/dataset-source-and-license.md` for background and schema comparison.
2. Download your retail CSV file (e.g. `sales.csv`).
3. In the application interface, click **Upload Data**.
4. In the Column Mapping dialog, assign the Date, Product, and Sales columns.
5. If the external dataset already includes line totals (e.g., `weekly_sales`), map it to **"Pre-Calculated Total Sales Column"** to prevent double multiplication.

---

## License & Attribution

- Built as an engineering expansion of the student academic report **“Small Shop Sales Pattern Analysis Using Data Science.”**
- Licensed under the MIT License for educational and small business analytics use.
