from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ColumnMappingConfig(BaseModel):
    date_col: str = Field(default="Date", description="Column for transaction date")
    day_col: Optional[str] = Field(default="Day", description="Optional column for weekday name")
    category_col: Optional[str] = Field(default="Product_Category", description="Column for product category")
    product_col: Optional[str] = Field(default="Product_Name", description="Column for product name")
    quantity_col: Optional[str] = Field(default="Quantity_Sold", description="Column for quantity sold")
    price_col: Optional[str] = Field(default="Price", description="Column for unit price")
    total_sales_col: Optional[str] = Field(default="Total_Sales", description="Column for pre-calculated total sales")
    duplicate_policy: str = Field(default="remove_exact", description="Policy for duplicate rows: 'remove_exact' or 'keep_all'")

class DataQualityIssue(BaseModel):
    row_index: int
    column: str
    issue_type: str
    original_value: Any = None
    action_taken: str
    severity: str = "warning"
    details: Optional[str] = None

class DataQualityReport(BaseModel):
    total_raw_rows: int = 0
    accepted_rows: int = 0
    rejected_rows: int = 0
    duplicate_rows_detected: int = 0
    duplicate_rows_removed: int = 0
    duplicate_policy: str = "remove_exact"
    missing_values_count: Dict[str, int] = Field(default_factory=dict)
    date_corrections_count: int = 0
    issues: List[DataQualityIssue] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class SalesRecord(BaseModel):
    date: str
    day_of_week: str
    product_category: str = "General"
    product_name: str = "Item"
    quantity_sold: float = 0.0
    unit_price: Optional[float] = None
    total_sales: float = 0.0

class TopProductSummary(BaseModel):
    name: str
    category: str
    value: float
    unit: str

class SalesSummaryKPIs(BaseModel):
    total_revenue: float = 0.0
    total_quantity_sold: float = 0.0
    total_records: int = 0
    unique_days: int = 0
    unique_products: int = 0
    unique_categories: int = 0
    avg_revenue_per_day: float = 0.0
    avg_revenue_per_record: float = 0.0
    best_selling_by_revenue: Optional[TopProductSummary] = None
    best_selling_by_quantity: Optional[TopProductSummary] = None
    least_selling_by_revenue: Optional[TopProductSummary] = None

class ProductPerformance(BaseModel):
    product_name: str
    product_category: str
    total_revenue: float
    total_quantity: float
    record_count: int
    unit_price_avg: float
    revenue_share_pct: float

class CategoryPerformance(BaseModel):
    product_category: str
    total_revenue: float
    total_quantity: float
    product_count: int
    revenue_share_pct: float

class DailySalesTrend(BaseModel):
    date: str
    day_of_week: str
    total_revenue: float
    total_quantity: float
    transaction_count: int

class DayOfWeekPerformance(BaseModel):
    day_of_week: str
    day_index: int
    total_revenue: float
    total_quantity: float
    avg_daily_revenue: float
    record_count: int

class InsightItem(BaseModel):
    category: str
    title: str
    description: str
    metric_value: Optional[str] = None
    importance: str = "medium"

class AnalyticsFilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    categories: Optional[List[str]] = None
    products: Optional[List[str]] = None

class SalesAnalyticsResponse(BaseModel):
    dataset_name: str
    dataset_source: str
    quality_report: DataQualityReport
    kpis: SalesSummaryKPIs
    product_performance: List[ProductPerformance]
    category_performance: List[CategoryPerformance]
    daily_trends: List[DailySalesTrend]
    day_of_week_performance: List[DayOfWeekPerformance]
    insights: List[InsightItem]
    records_preview: List[Dict[str, Any]]
    total_cleaned_records: int = 0
    available_categories: List[str]
    available_products: List[str]
    min_date: Optional[str] = None
    max_date: Optional[str] = None
