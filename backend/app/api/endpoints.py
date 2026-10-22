import os
import io
import json
import pandas as pd
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import StreamingResponse

from backend.app.schemas.sales import (
    ColumnMappingConfig,
    AnalyticsFilterParams,
    SalesAnalyticsResponse
)
from backend.app.services.preprocessor import DataPreprocessor
from backend.app.analytics.engine import SalesAnalyticsEngine
from backend.app.analytics.insights import generate_sales_insights
from backend.app.core.config import settings

router = APIRouter()
preprocessor = DataPreprocessor()
analytics_engine = SalesAnalyticsEngine()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLES_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "samples")

SAMPLE_CONFIGS = {
    "report_sample": {
        "id": "report_sample",
        "title": "Report Sample Dataset (Exact 4 Transactions)",
        "description": "The exact four example transactions documented in the college project report code (Biscuits, Tea, Chips, Coffee).",
        "filename": "report_sample_transactions.csv",
        "source_type": "report_sample"
    },
    "realistic_15_days": {
        "id": "realistic_15_days",
        "title": "Realistic 15-Day Small Shop Dataset (189 Transactions)",
        "description": "Representative 15-day daily transactions for a neighbourhood shop across Groceries, Snacks, Beverages, and Household necessities.",
        "filename": "small_shop_15_days_realistic.csv",
        "source_type": "realistic_15_days"
    },
    "dirty_test": {
        "id": "dirty_test",
        "title": "Quality Audit Benchmark (Dirty Test Data)",
        "description": "Demonstrates data cleaning resilience: handles missing categories, negative quantities, calendar weekday discrepancies, and duplicates.",
        "filename": "small_shop_dirty_test.csv",
        "source_type": "dirty_test"
    }
}

async def read_upload_with_limit(file: UploadFile, max_bytes: int) -> bytes:
    chunks = []
    total_bytes = 0
    chunk_size = 1024 * 1024
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total_bytes += len(chunk)
        if total_bytes > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum allowed size of {max_bytes // (1024 * 1024)}MB."
            )
        chunks.append(chunk)
    return b"".join(chunks)

def load_file_to_df(filename: str, content_bytes: bytes) -> pd.DataFrame:
    ext = os.path.splitext(filename or "")[1].lower()
    if ext in [".xlsx", ".xls"]:
        try:
            return pd.read_excel(io.BytesIO(content_bytes))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse Excel file: {str(e)}")
    elif ext in [".csv", ".txt", ".tsv", ""]:
        try:
            return pd.read_csv(io.BytesIO(content_bytes), encoding="utf-8")
        except UnicodeDecodeError:
            try:
                return pd.read_csv(io.BytesIO(content_bytes), encoding="latin-1")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{ext}'. Please upload .csv or .xlsx")

def process_and_build_response(
    df: pd.DataFrame,
    mapping: Optional[ColumnMappingConfig],
    filters: Optional[AnalyticsFilterParams],
    dataset_name: str,
    dataset_source: str
) -> SalesAnalyticsResponse:
    clean_df, quality_report = preprocessor.clean(df, mapping)
    
    min_date = str(clean_df["date"].min()) if not clean_df.empty else None
    max_date = str(clean_df["date"].max()) if not clean_df.empty else None
    available_cats = sorted(clean_df["product_category"].dropna().unique().tolist()) if not clean_df.empty else []
    available_prods = sorted(clean_df["product_name"].dropna().unique().tolist()) if not clean_df.empty else []

    filtered_df = analytics_engine.apply_filters(clean_df, filters)

    kpis = analytics_engine.calculate_kpis(filtered_df)
    prod_perf = analytics_engine.get_product_performance(filtered_df)
    cat_perf = analytics_engine.get_category_performance(filtered_df)
    daily_trends = analytics_engine.get_daily_trends(filtered_df)
    dow_perf = analytics_engine.get_day_of_week_performance(filtered_df)
    insights = generate_sales_insights(kpis, prod_perf, cat_perf, daily_trends, dow_perf)

    preview_records = filtered_df.head(100).to_dict(orient="records") if not filtered_df.empty else []

    return SalesAnalyticsResponse(
        dataset_name=dataset_name,
        dataset_source=dataset_source,
        quality_report=quality_report,
        kpis=kpis,
        product_performance=prod_perf,
        category_performance=cat_perf,
        daily_trends=daily_trends,
        day_of_week_performance=dow_perf,
        insights=insights,
        records_preview=preview_records,
        total_cleaned_records=len(filtered_df),
        available_categories=available_cats,
        available_products=available_prods,
        min_date=min_date,
        max_date=max_date
    )

@router.get("/health")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": settings.VERSION}

@router.get("/samples")
def list_samples():
    return list(SAMPLE_CONFIGS.values())

@router.get("/samples/{sample_id}/analyze", response_model=SalesAnalyticsResponse)
def analyze_sample(
    sample_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    products: Optional[List[str]] = Query(None)
):
    if sample_id not in SAMPLE_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Sample '{sample_id}' not found.")
    
    cfg = SAMPLE_CONFIGS[sample_id]
    file_path = os.path.join(SAMPLES_DIR, cfg["filename"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Sample file '{cfg['filename']}' not found on server.")

    raw_df = pd.read_csv(file_path)
    filters = AnalyticsFilterParams(
        start_date=start_date,
        end_date=end_date,
        categories=categories,
        products=products
    )
    mapping = preprocessor.auto_detect_mapping(raw_df)
    return process_and_build_response(
        raw_df,
        mapping,
        filters,
        dataset_name=cfg["title"],
        dataset_source=cfg["source_type"]
    )

@router.post("/upload/preview")
async def upload_preview(file: UploadFile = File(...)):
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    contents = await read_upload_with_limit(file, max_bytes)
    
    df = load_file_to_df(file.filename, contents)
    mapping = preprocessor.auto_detect_mapping(df)
    preview_rows = df.head(5).fillna("").to_dict(orient="records")
    
    return {
        "filename": file.filename,
        "total_rows": len(df),
        "columns": list(df.columns),
        "preview": preview_rows,
        "suggested_mapping": mapping.model_dump()
    }

@router.post("/upload/analyze", response_model=SalesAnalyticsResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    mapping: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
    products: Optional[str] = Form(None)
):
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    contents = await read_upload_with_limit(file, max_bytes)
    
    df = load_file_to_df(file.filename, contents)
    
    mapping_obj = None
    if mapping:
        try:
            m_dict = json.loads(mapping)
            mapping_obj = ColumnMappingConfig(**m_dict)
        except Exception:
            mapping_obj = preprocessor.auto_detect_mapping(df)
    else:
        mapping_obj = preprocessor.auto_detect_mapping(df)

    cat_list = json.loads(categories) if categories else None
    prod_list = json.loads(products) if products else None

    filters = AnalyticsFilterParams(
        start_date=start_date,
        end_date=end_date,
        categories=cat_list,
        products=prod_list
    )

    return process_and_build_response(
        df,
        mapping_obj,
        filters,
        dataset_name=file.filename,
        dataset_source="user_upload"
    )

@router.get("/samples/{sample_id}/export")
def export_sample_clean_csv(
    sample_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    products: Optional[List[str]] = Query(None)
):
    if sample_id not in SAMPLE_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Sample '{sample_id}' not found.")
    cfg = SAMPLE_CONFIGS[sample_id]
    file_path = os.path.join(SAMPLES_DIR, cfg["filename"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Sample file not found.")
        
    raw_df = pd.read_csv(file_path)
    clean_df, _ = preprocessor.clean(raw_df)
    
    filters = AnalyticsFilterParams(
        start_date=start_date,
        end_date=end_date,
        categories=categories,
        products=products
    )
    filtered_df = analytics_engine.apply_filters(clean_df, filters)
    
    stream = io.StringIO()
    filtered_df.to_csv(stream, index=False)
    stream.seek(0)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=cleaned_{sample_id}_full_export.csv"
    return response

@router.post("/upload/export")
async def export_upload_clean_csv(
    file: UploadFile = File(...),
    mapping: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
    products: Optional[str] = Form(None)
):
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    contents = await read_upload_with_limit(file, max_bytes)
    df = load_file_to_df(file.filename, contents)
    
    mapping_obj = None
    if mapping:
        try:
            m_dict = json.loads(mapping)
            mapping_obj = ColumnMappingConfig(**m_dict)
        except Exception:
            mapping_obj = preprocessor.auto_detect_mapping(df)
    else:
        mapping_obj = preprocessor.auto_detect_mapping(df)

    cat_list = json.loads(categories) if categories else None
    prod_list = json.loads(products) if products else None

    filters = AnalyticsFilterParams(
        start_date=start_date,
        end_date=end_date,
        categories=cat_list,
        products=prod_list
    )

    clean_df, _ = preprocessor.clean(df, mapping_obj)
    filtered_df = analytics_engine.apply_filters(clean_df, filters)

    stream = io.StringIO()
    filtered_df.to_csv(stream, index=False)
    stream.seek(0)

    safe_name = os.path.splitext(file.filename or "upload")[0]
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=cleaned_{safe_name}_full_export.csv"
    return response
