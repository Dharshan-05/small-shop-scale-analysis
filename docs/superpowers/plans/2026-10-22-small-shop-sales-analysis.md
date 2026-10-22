# Small Shop Sales Pattern Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-quality, reproducible, runnable full-stack web application for analyzing retail sales patterns in small shops, implementing data ingestion, column mapping, automated data cleaning, exploratory data analysis, interactive dashboard visualization, and automated evidence-based business insights.

**Architecture:** A lightweight local-first architecture consisting of a Python FastAPI backend exposing RESTful endpoints for file parsing, quality auditing, column mapping, and deterministic statistical aggregations, coupled with a responsive React + TypeScript + Vite + Tailwind CSS frontend featuring Recharts for interactive analytics, data filtering, and automated insight generation.

**Tech Stack:**
- Backend: Python 3.11, FastAPI, Pandas, Pydantic v2, Pytest, OpenPyXL, Uvicorn
- Frontend: React 18 / 19, TypeScript, Vite, Tailwind CSS, Recharts, Lucide React
- Testing & Verification: Pytest, Playwright browser tests, Vitest / ESLint

**Spec:** Project report titled "Small Shop Sales Pattern Analysis Using Data Science" (saved at `docs/Small_Shop_Sales_Pattern_Analysis_Report.pdf`) and the Solo Founder Master Execution Prompt.

## Global Constraints
- Preserve original dataset files; never overwrite raw inputs with cleaned data.
- Revenue calculation: If unit price and quantity are provided: `Total Sales = Quantity Sold × Unit Price`. If pre-calculated total sales column exists, map without double-counting.
- Date validation: Derivation of day-of-week must be calculated from validated datetime parsing, correcting any invalid manual calendar annotations (e.g., 01-02-2026 was Sunday, not Monday).
- Local-first architecture: No external cloud dependencies, API keys, or Docker containers required for core operation.
- Clearly differentiate external Kaggle demonstration data, deterministic synthetic demo data, and user-uploaded shop data.

## Review Focus
- Calendar day-of-week discrepancy: When an uploaded dataset has a manual "Day" column that contradicts the parsed "Date", the system must detect and flag the inconsistency and use the verified calendar day.
- Double-counting prevention: When a dataset already has a `Total_Sales` or `Total` column, the parser must not multiply it again by quantity.
- Extreme or dirty inputs: Empty files, non-numeric values in numeric columns, negative quantities, negative prices, and trailing blank rows must be safely caught and reported as data quality issues with row-level transparency.
- Missing optional dimensions: If a dataset lacks `Product_Category` or `Product_Name`, category-level or product-level analyses should gracefully degrade with helpful explanations rather than crashing.
- Export fidelity: CSV exports must reflect filtered or cleaned subsets accurately without data loss.

---

### Task 1: Core Data Models, Schemas, and Column Mapping Layer

**Files:**
- Create: `backend/app/schemas/sales.py`
- Create: `backend/app/core/config.py`
- Test: `backend/tests/test_schemas.py`

**Interfaces:**
- Consumes: None (base models)
- Produces: `SalesRecord`, `DataQualityReport`, `ColumnMappingConfig`, `AnalyticsFilterParams`, `SalesSummaryKPIs`

- [ ] **Step 1: Write the failing test for schemas**
- [ ] **Step 2: Run pytest to verify it fails**
- [ ] **Step 3: Implement data schemas in `backend/app/schemas/sales.py` and settings in `backend/app/core/config.py`**
- [ ] **Step 4: Run pytest to verify it passes**
- [ ] **Step 5: Commit**

---

### Task 2: Data Preprocessing and Quality Audit Engine

**Files:**
- Create: `backend/app/services/preprocessor.py`
- Test: `backend/tests/test_preprocessor.py`

**Interfaces:**
- Consumes: `ColumnMappingConfig`, raw pandas DataFrame or file streams
- Produces: Cleaned `pd.DataFrame`, `DataQualityReport` (tracking missing values, duplicate counts, date corrections, rejected rows)

- [ ] **Step 1: Write failing tests for preprocessor (handling missing, negative, duplicate, date-mismatch records)**
- [ ] **Step 2: Run pytest to verify it fails**
- [ ] **Step 3: Implement `DataPreprocessor` in `backend/app/services/preprocessor.py`**
- [ ] **Step 4: Run pytest to verify it passes**
- [ ] **Step 5: Commit**

---

### Task 3: Deterministic Sales Analytics Engine and Insights Generator

**Files:**
- Create: `backend/app/analytics/engine.py`
- Create: `backend/app/analytics/insights.py`
- Test: `backend/tests/test_analytics.py`

**Interfaces:**
- Consumes: Cleaned `pd.DataFrame`, `AnalyticsFilterParams`
- Produces: `SalesAnalyticsResponse` (KPIs, product rankings, category breakdowns, daily trends, weekday analysis, automated text findings)

- [ ] **Step 1: Write failing tests for analytics (verifying exact report sample totals: Biscuits=200, Tea=75, Chips=375, Coffee=200, total=850)**
- [ ] **Step 2: Run pytest to verify it fails**
- [ ] **Step 3: Implement analytics calculations in `backend/app/analytics/engine.py` and `insights.py`**
- [ ] **Step 4: Run pytest to verify it passes**
- [ ] **Step 5: Commit**

---

### Task 4: FastAPI REST Endpoints and File Ingestion API

**Files:**
- Create: `backend/app/api/endpoints.py`
- Create: `backend/app/main.py`
- Test: `backend/tests/test_api.py`

**Interfaces:**
- Consumes: `DataPreprocessor`, `SalesAnalyticsEngine`
- Produces: Endpoints `/api/health`, `/api/upload`, `/api/preview`, `/api/analyze`, `/api/samples`, `/api/export`

- [ ] **Step 1: Write failing API tests using FastAPI TestClient**
- [ ] **Step 2: Run pytest to verify it fails**
- [ ] **Step 3: Implement API routes and FastAPI application**
- [ ] **Step 4: Run pytest to verify all backend tests pass**
- [ ] **Step 5: Commit**

---

### Task 5: Frontend Application Setup with Tailwind CSS and Component Architecture

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/src/types/api.ts`
- Create: `frontend/src/services/api.ts`
- Create: `frontend/src/components/*`
- Create: `frontend/src/pages/Dashboard.tsx`

**Interfaces:**
- Consumes: Backend REST API
- Produces: Interactive SPA with Dataset Selector, Upload Modal, KPI Cards, Recharts Charts, Filter Bar, Findings Panel, Data Quality Modal, and Table

- [ ] **Step 1: Scaffold Vite + React + TypeScript + Tailwind frontend**
- [ ] **Step 2: Implement API client with typed schemas in `frontend/src/services/api.ts`**
- [ ] **Step 3: Build UI components (KPI cards, charts, filters, data table, quality alert banners, automated findings)**
- [ ] **Step 4: Verify build succeeds with `npm run build`**
- [ ] **Step 5: Commit**

---

### Task 6: End-to-End Testing and Verification with Playwright

**Files:**
- Create: `tests/e2e/dashboard.spec.ts` or playwright test script `scripts/verify_e2e.py`
- Test: Real browser navigation, dataset loading, filter interactions, KPI validation

- [ ] **Step 1: Start backend and frontend services**
- [ ] **Step 2: Run browser tests against sample datasets and verify calculations match expected report figures**
- [ ] **Step 3: Capture verification screenshots**
- [ ] **Step 4: Commit**

---

### Task 7: Comprehensive Documentation and Final Delivery Traceability

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/data-dictionary.md`
- Create: `docs/report-to-implementation-mapping.md`
- Create: `docs/dataset-source-and-license.md`
- Create: `docs/testing.md`
- Create: `README.md`

- [ ] **Step 1: Author detailed architectural, data dictionary, testing, and traceability documents**
- [ ] **Step 2: Review all requirements against Definition of Done**
- [ ] **Step 3: Commit and finalize**
