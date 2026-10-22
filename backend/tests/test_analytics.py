import pytest
import pandas as pd
from backend.app.analytics.engine import SalesAnalyticsEngine
from backend.app.analytics.insights import generate_sales_insights
from backend.app.schemas.sales import AnalyticsFilterParams

@pytest.fixture
def sample_clean_df():
    data = {
        "date": ["2026-02-01", "2026-02-01", "2026-02-02", "2026-02-02"],
        "day_of_week": ["Sunday", "Sunday", "Monday", "Monday"],
        "product_category": ["Snacks", "Beverages", "Snacks", "Beverages"],
        "product_name": ["Biscuits", "Tea", "Chips", "Coffee"],
        "quantity_sold": [20.0, 15.0, 25.0, 10.0],
        "unit_price": [10.0, 5.0, 15.0, 20.0],
        "total_sales": [200.0, 75.0, 375.0, 200.0]
    }
    return pd.DataFrame(data)

def test_kpi_calculations_exact_report_values(sample_clean_df):
    engine = SalesAnalyticsEngine()
    kpis = engine.calculate_kpis(sample_clean_df)
    
    assert kpis.total_revenue == 850.0
    assert kpis.total_quantity_sold == 70.0
    assert kpis.total_records == 4
    assert kpis.unique_days == 2
    assert kpis.unique_products == 4
    assert kpis.unique_categories == 2
    assert kpis.avg_revenue_per_day == 425.0
    assert kpis.avg_revenue_per_record == 212.5
    
    # Best selling by revenue: Chips (375 INR)
    assert kpis.best_selling_by_revenue.name == "Chips"
    assert kpis.best_selling_by_revenue.value == 375.0
    
    # Best selling by quantity: Chips (25 units)
    assert kpis.best_selling_by_quantity.name == "Chips"
    assert kpis.best_selling_by_quantity.value == 25.0
    
    # Least selling by revenue: Tea (75 INR)
    assert kpis.least_selling_by_revenue.name == "Tea"
    assert kpis.least_selling_by_revenue.value == 75.0

def test_product_and_category_performance(sample_clean_df):
    engine = SalesAnalyticsEngine()
    prod_perf = engine.get_product_performance(sample_clean_df)
    cat_perf = engine.get_category_performance(sample_clean_df)
    
    # Chips should be top ranked by revenue
    assert prod_perf[0].product_name == "Chips"
    assert prod_perf[0].total_revenue == 375.0
    assert prod_perf[0].revenue_share_pct == round((375.0 / 850.0) * 100, 2)
    
    # Category totals: Snacks (200 + 375 = 575), Beverages (75 + 200 = 275)
    snacks = next(c for c in cat_perf if c.product_category == "Snacks")
    beverages = next(c for c in cat_perf if c.product_category == "Beverages")
    assert snacks.total_revenue == 575.0
    assert beverages.total_revenue == 275.0
    assert snacks.total_quantity == 45.0
    assert beverages.total_quantity == 25.0

def test_daily_and_weekday_trends(sample_clean_df):
    engine = SalesAnalyticsEngine()
    daily = engine.get_daily_trends(sample_clean_df)
    weekday = engine.get_day_of_week_performance(sample_clean_df)
    
    assert len(daily) == 2
    assert daily[0].date == "2026-02-01"
    assert daily[0].total_revenue == 275.0 # 200 + 75
    assert daily[1].date == "2026-02-02"
    assert daily[1].total_revenue == 575.0 # 375 + 200
    
    # Weekday check: Sunday and Monday present
    sun = next((w for w in weekday if w.day_of_week == "Sunday"), None)
    mon = next((w for w in weekday if w.day_of_week == "Monday"), None)
    assert sun is not None
    assert mon is not None
    assert sun.total_revenue == 275.0
    assert mon.total_revenue == 575.0

def test_filtering_by_category(sample_clean_df):
    engine = SalesAnalyticsEngine()
    filtered = engine.apply_filters(sample_clean_df, AnalyticsFilterParams(categories=["Snacks"]))
    assert len(filtered) == 2
    assert set(filtered["product_category"].unique()) == {"Snacks"}

def test_insights_generation(sample_clean_df):
    engine = SalesAnalyticsEngine()
    kpis = engine.calculate_kpis(sample_clean_df)
    prod_perf = engine.get_product_performance(sample_clean_df)
    cat_perf = engine.get_category_performance(sample_clean_df)
    daily = engine.get_daily_trends(sample_clean_df)
    weekday = engine.get_day_of_week_performance(sample_clean_df)
    
    insights = generate_sales_insights(kpis, prod_perf, cat_perf, daily, weekday)
    assert len(insights) >= 3
    titles = [i.title for i in insights]
    assert any("Best-Selling Product" in t for t in titles)
    assert any("Top Contributing Category" in t for t in titles)
