import pytest
from backend.app.schemas.sales import (
    ColumnMappingConfig,
    DataQualityReport,
    SalesRecord,
    SalesSummaryKPIs,
    TopProductSummary
)

def test_column_mapping_defaults():
    mapping = ColumnMappingConfig()
    assert mapping.date_col == "Date"
    assert mapping.quantity_col == "Quantity_Sold"
    assert mapping.price_col == "Price"

def test_sales_record_model():
    rec = SalesRecord(
        date="2026-02-01",
        day_of_week="Sunday",
        product_category="Snacks",
        product_name="Biscuits",
        quantity_sold=20,
        unit_price=10.0,
        total_sales=200.0
    )
    assert rec.total_sales == 200.0
    assert rec.day_of_week == "Sunday"

def test_kpi_model_summary():
    top = TopProductSummary(
        name="Chips",
        category="Snacks",
        value=375.0,
        unit="INR"
    )
    kpis = SalesSummaryKPIs(
        total_revenue=850.0,
        total_quantity_sold=70.0,
        total_records=4,
        unique_days=2,
        unique_products=4,
        unique_categories=2,
        avg_revenue_per_day=425.0,
        avg_revenue_per_record=212.5,
        best_selling_by_revenue=top
    )
    assert kpis.total_revenue == 850.0
    assert kpis.best_selling_by_revenue.name == "Chips"
