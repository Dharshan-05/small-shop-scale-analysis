import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any

from backend.app.schemas.sales import (
    SalesSummaryKPIs,
    TopProductSummary,
    ProductPerformance,
    CategoryPerformance,
    DailySalesTrend,
    DayOfWeekPerformance,
    AnalyticsFilterParams
)

WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

class SalesAnalyticsEngine:
    def __init__(self):
        pass

    def apply_filters(self, df: pd.DataFrame, filters: Optional[AnalyticsFilterParams]) -> pd.DataFrame:
        if df.empty or filters is None:
            return df

        filtered = df.copy()

        if filters.start_date:
            filtered = filtered[filtered["date"] >= filters.start_date]
        if filters.end_date:
            filtered = filtered[filtered["date"] <= filters.end_date]
        if filters.categories and len(filters.categories) > 0:
            filtered = filtered[filtered["product_category"].isin(filters.categories)]
        if filters.products and len(filters.products) > 0:
            filtered = filtered[filtered["product_name"].isin(filters.products)]

        return filtered

    def calculate_kpis(self, df: pd.DataFrame) -> SalesSummaryKPIs:
        if df.empty:
            return SalesSummaryKPIs()

        total_rev = float(df["total_sales"].sum())
        total_qty = float(df["quantity_sold"].sum())
        total_records = len(df)
        unique_days = int(df["date"].nunique())
        unique_products = int(df["product_name"].nunique())
        unique_categories = int(df["product_category"].nunique())

        avg_rev_per_day = round(total_rev / unique_days, 2) if unique_days > 0 else 0.0
        avg_rev_per_record = round(total_rev / total_records, 2) if total_records > 0 else 0.0

        # Best / least selling by revenue
        prod_rev = df.groupby(["product_name", "product_category"])["total_sales"].sum().reset_index()
        prod_qty = df.groupby(["product_name", "product_category"])["quantity_sold"].sum().reset_index()

        best_rev_item = None
        least_rev_item = None
        best_qty_item = None

        if not prod_rev.empty:
            top_rev_row = prod_rev.sort_values(by="total_sales", ascending=False).iloc[0]
            best_rev_item = TopProductSummary(
                name=str(top_rev_row["product_name"]),
                category=str(top_rev_row["product_category"]),
                value=round(float(top_rev_row["total_sales"]), 2),
                unit="INR"
            )

            least_rev_row = prod_rev.sort_values(by="total_sales", ascending=True).iloc[0]
            least_rev_item = TopProductSummary(
                name=str(least_rev_row["product_name"]),
                category=str(least_rev_row["product_category"]),
                value=round(float(least_rev_row["total_sales"]), 2),
                unit="INR"
            )

        if not prod_qty.empty:
            top_qty_row = prod_qty.sort_values(by="quantity_sold", ascending=False).iloc[0]
            best_qty_item = TopProductSummary(
                name=str(top_qty_row["product_name"]),
                category=str(top_qty_row["product_category"]),
                value=round(float(top_qty_row["quantity_sold"]), 2),
                unit="Units"
            )

        return SalesSummaryKPIs(
            total_revenue=round(total_rev, 2),
            total_quantity_sold=round(total_qty, 2),
            total_records=total_records,
            unique_days=unique_days,
            unique_products=unique_products,
            unique_categories=unique_categories,
            avg_revenue_per_day=avg_rev_per_day,
            avg_revenue_per_record=avg_rev_per_record,
            best_selling_by_revenue=best_rev_item,
            best_selling_by_quantity=best_qty_item,
            least_selling_by_revenue=least_rev_item
        )

    def get_product_performance(self, df: pd.DataFrame) -> List[ProductPerformance]:
        if df.empty:
            return []

        total_rev_all = df["total_sales"].sum()

        grouped = df.groupby(["product_name", "product_category"]).agg(
            total_revenue=("total_sales", "sum"),
            total_quantity=("quantity_sold", "sum"),
            record_count=("total_sales", "count"),
            unit_price_avg=("unit_price", lambda s: float(s.dropna().mean()) if s.dropna().size > 0 else 0.0)
        ).reset_index()

        grouped.sort_values(by="total_revenue", ascending=False, inplace=True)

        results = []
        for _, row in grouped.iterrows():
            rev = float(row["total_revenue"])
            share = round((rev / total_rev_all * 100), 2) if total_rev_all > 0 else 0.0
            results.append(ProductPerformance(
                product_name=str(row["product_name"]),
                product_category=str(row["product_category"]),
                total_revenue=round(rev, 2),
                total_quantity=round(float(row["total_quantity"]), 2),
                record_count=int(row["record_count"]),
                unit_price_avg=round(float(row["unit_price_avg"]), 2),
                revenue_share_pct=share
            ))
        return results

    def get_category_performance(self, df: pd.DataFrame) -> List[CategoryPerformance]:
        if df.empty:
            return []

        total_rev_all = df["total_sales"].sum()

        grouped = df.groupby("product_category").agg(
            total_revenue=("total_sales", "sum"),
            total_quantity=("quantity_sold", "sum"),
            product_count=("product_name", "nunique")
        ).reset_index()

        grouped.sort_values(by="total_revenue", ascending=False, inplace=True)

        results = []
        for _, row in grouped.iterrows():
            rev = float(row["total_revenue"])
            share = round((rev / total_rev_all * 100), 2) if total_rev_all > 0 else 0.0
            results.append(CategoryPerformance(
                product_category=str(row["product_category"]),
                total_revenue=round(rev, 2),
                total_quantity=round(float(row["total_quantity"]), 2),
                product_count=int(row["product_count"]),
                revenue_share_pct=share
            ))
        return results

    def get_daily_trends(self, df: pd.DataFrame) -> List[DailySalesTrend]:
        if df.empty:
            return []

        grouped = df.groupby(["date", "day_of_week"]).agg(
            total_revenue=("total_sales", "sum"),
            total_quantity=("quantity_sold", "sum"),
            transaction_count=("total_sales", "count")
        ).reset_index()

        grouped.sort_values(by="date", inplace=True)

        results = []
        for _, row in grouped.iterrows():
            results.append(DailySalesTrend(
                date=str(row["date"]),
                day_of_week=str(row["day_of_week"]),
                total_revenue=round(float(row["total_revenue"]), 2),
                total_quantity=round(float(row["total_quantity"]), 2),
                transaction_count=int(row["transaction_count"])
            ))
        return results

    def get_day_of_week_performance(self, df: pd.DataFrame) -> List[DayOfWeekPerformance]:
        if df.empty:
            return []

        # Distinct days count per day_of_week
        distinct_days_per_dow = df.groupby("day_of_week")["date"].nunique().to_dict()

        grouped = df.groupby("day_of_week").agg(
            total_revenue=("total_sales", "sum"),
            total_quantity=("quantity_sold", "sum"),
            record_count=("total_sales", "count")
        ).reset_index()

        results = []
        for idx, dow in enumerate(WEEKDAY_ORDER):
            match = grouped[grouped["day_of_week"] == dow]
            if not match.empty:
                row = match.iloc[0]
                rev = float(row["total_revenue"])
                unique_occurrences = distinct_days_per_dow.get(dow, 1)
                avg_daily = round(rev / unique_occurrences, 2) if unique_occurrences > 0 else 0.0
                results.append(DayOfWeekPerformance(
                    day_of_week=dow,
                    day_index=idx,
                    total_revenue=round(rev, 2),
                    total_quantity=round(float(row["total_quantity"]), 2),
                    avg_daily_revenue=avg_daily,
                    record_count=int(row["record_count"])
                ))
            else:
                results.append(DayOfWeekPerformance(
                    day_of_week=dow,
                    day_index=idx,
                    total_revenue=0.0,
                    total_quantity=0.0,
                    avg_daily_revenue=0.0,
                    record_count=0
                ))
        return results
