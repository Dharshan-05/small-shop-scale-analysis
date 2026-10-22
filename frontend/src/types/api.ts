export interface ColumnMappingConfig {
  date_col: string;
  day_col?: string | null;
  category_col?: string | null;
  product_col?: string | null;
  quantity_col?: string | null;
  price_col?: string | null;
  total_sales_col?: string | null;
  duplicate_policy?: 'remove_exact' | 'keep_all';
}

export interface DataQualityIssue {
  row_index: number;
  column: string;
  issue_type: string;
  original_value?: any;
  action_taken: string;
  severity: string;
  details?: string | null;
}

export interface DataQualityReport {
  total_raw_rows: number;
  accepted_rows: number;
  rejected_rows: number;
  duplicate_rows_detected: number;
  duplicate_rows_removed: number;
  duplicate_policy: string;
  missing_values_count: Record<string, number>;
  date_corrections_count: number;
  issues: DataQualityIssue[];
  warnings: string[];
}

export interface TopProductSummary {
  name: string;
  category: string;
  value: number;
  unit: string;
}

export interface SalesSummaryKPIs {
  total_revenue: number;
  total_quantity_sold: number;
  total_records: number;
  unique_days: number;
  unique_products: number;
  unique_categories: number;
  avg_revenue_per_day: number;
  avg_revenue_per_record: number;
  best_selling_by_revenue?: TopProductSummary | null;
  best_selling_by_quantity?: TopProductSummary | null;
  least_selling_by_revenue?: TopProductSummary | null;
}

export interface ProductPerformance {
  product_name: string;
  product_category: string;
  total_revenue: number;
  total_quantity: number;
  record_count: number;
  unit_price_avg: number;
  revenue_share_pct: number;
}

export interface CategoryPerformance {
  product_category: string;
  total_revenue: number;
  total_quantity: number;
  product_count: number;
  revenue_share_pct: number;
}

export interface DailySalesTrend {
  date: string;
  day_of_week: string;
  total_revenue: number;
  total_quantity: number;
  transaction_count: number;
}

export interface DayOfWeekPerformance {
  day_of_week: string;
  day_index: number;
  total_revenue: number;
  total_quantity: number;
  avg_daily_revenue: number;
  record_count: number;
}

export interface InsightItem {
  category: string;
  title: string;
  description: string;
  metric_value?: string | null;
  importance: 'high' | 'medium' | 'low';
}

export interface SalesAnalyticsResponse {
  dataset_name: string;
  dataset_source: string;
  quality_report: DataQualityReport;
  kpis: SalesSummaryKPIs;
  product_performance: ProductPerformance[];
  category_performance: CategoryPerformance[];
  daily_trends: DailySalesTrend[];
  day_of_week_performance: DayOfWeekPerformance[];
  insights: InsightItem[];
  records_preview: Record<string, any>[];
  total_cleaned_records: number;
  available_categories: string[];
  available_products: string[];
  min_date?: string | null;
  max_date?: string | null;
}

export interface SampleDatasetMeta {
  id: string;
  title: string;
  description: string;
  filename: string;
  source_type: string;
}

export interface UploadPreviewResponse {
  filename: string;
  total_rows: number;
  columns: string[];
  preview: Record<string, any>[];
  suggested_mapping: ColumnMappingConfig;
}
