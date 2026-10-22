from typing import List
from backend.app.schemas.sales import (
    SalesSummaryKPIs,
    ProductPerformance,
    CategoryPerformance,
    DailySalesTrend,
    DayOfWeekPerformance,
    InsightItem
)

def generate_sales_insights(
    kpis: SalesSummaryKPIs,
    product_perf: List[ProductPerformance],
    category_perf: List[CategoryPerformance],
    daily_trends: List[DailySalesTrend],
    dow_perf: List[DayOfWeekPerformance]
) -> List[InsightItem]:
    insights: List[InsightItem] = []

    if kpis.total_records == 0:
        return [
            InsightItem(
                category="overview",
                title="No Data Available",
                description="Upload a sales dataset or choose a demo to view automated business insights.",
                importance="low"
            )
        ]

    # 1. Best Selling Product by Revenue
    if kpis.best_selling_by_revenue:
        top_prod = kpis.best_selling_by_revenue
        match_prod = next((p for p in product_perf if p.product_name == top_prod.name), None)
        share_str = f" ({match_prod.revenue_share_pct}% of total sales)" if match_prod else ""
        insights.append(
            InsightItem(
                category="best_seller",
                title="Best-Selling Product by Revenue",
                description=f"'{top_prod.name}' ({top_prod.category}) generates the highest revenue at {top_prod.value:,.2f} INR{share_str}. Ensure reliable supplier replenishment to avoid stockouts.",
                metric_value=f"{top_prod.value:,.2f} INR",
                importance="high"
            )
        )

    # 2. Volume vs Revenue Divergence
    if kpis.best_selling_by_quantity and kpis.best_selling_by_revenue:
        if kpis.best_selling_by_quantity.name != kpis.best_selling_by_revenue.name:
            top_qty = kpis.best_selling_by_quantity
            insights.append(
                InsightItem(
                    category="volume_divergence",
                    title="Volume Leader vs Revenue Leader",
                    description=f"While '{kpis.best_selling_by_revenue.name}' leads in gross revenue, '{top_qty.name}' had the highest unit volume ({top_qty.value:,.0f} units sold). High unit movement requires shelf-space prioritization.",
                    metric_value=f"{top_qty.value:,.0f} units",
                    importance="medium"
                )
            )

    # 3. Category Concentration
    if category_perf:
        top_cat = category_perf[0]
        insights.append(
            InsightItem(
                category="category_distribution",
                title="Top Contributing Category",
                description=f"The '{top_cat.product_category}' category accounts for {top_cat.revenue_share_pct}% of shop turnover ({top_cat.total_revenue:,.2f} INR across {top_cat.product_count} products).",
                metric_value=f"{top_cat.revenue_share_pct}% share",
                importance="high"
            )
        )

    # 4. Daily Sales Peaks and Volatility
    if daily_trends:
        sorted_daily = sorted(daily_trends, key=lambda d: d.total_revenue, reverse=True)
        peak_day = sorted_daily[0]
        trough_day = sorted_daily[-1]
        
        diff = peak_day.total_revenue - trough_day.total_revenue
        insights.append(
            InsightItem(
                category="revenue_peak",
                title=f"Peak Sales Day: {peak_day.day_of_week} ({peak_day.date})",
                description=f"Highest single-day sales occurred on {peak_day.date} ({peak_day.day_of_week}) reaching {peak_day.total_revenue:,.2f} INR, compared to {trough_day.total_revenue:,.2f} INR on the lowest day ({trough_day.date}).",
                metric_value=f"{peak_day.total_revenue:,.2f} INR",
                importance="medium"
            )
        )

    # 5. Weekend vs Weekday Dynamic
    active_dows = [d for d in dow_perf if d.record_count > 0]
    weekend_rev = sum(d.total_revenue for d in active_dows if d.day_of_week in ["Saturday", "Sunday"])
    weekend_days = sum(1 for d in active_dows if d.day_of_week in ["Saturday", "Sunday"])
    weekday_rev = sum(d.total_revenue for d in active_dows if d.day_of_week not in ["Saturday", "Sunday"])
    weekday_days = sum(1 for d in active_dows if d.day_of_week not in ["Saturday", "Sunday"])

    avg_weekend = (weekend_rev / weekend_days) if weekend_days > 0 else 0.0
    avg_weekday = (weekday_rev / weekday_days) if weekday_days > 0 else 0.0

    if avg_weekend > 0 and avg_weekday > 0:
        pct_diff = round(((avg_weekend - avg_weekday) / avg_weekday) * 100, 1)
        direction = "higher" if pct_diff > 0 else "lower"
        insights.append(
            InsightItem(
                category="weekend_comparison",
                title="Weekend vs Weekday Pattern",
                description=f"Average daily revenue on weekend days ({avg_weekend:,.2f} INR) is {abs(pct_diff)}% {direction} than weekdays ({avg_weekday:,.2f} INR). Staffing and perishable stock should be tuned accordingly.",
                metric_value=f"{abs(pct_diff)}% {direction}",
                importance="medium"
            )
        )

    # 6. Least Performing Product
    if kpis.least_selling_by_revenue and len(product_perf) > 2:
        least = kpis.least_selling_by_revenue
        insights.append(
            InsightItem(
                category="inventory_risk",
                title="Lowest Revenue Contributor",
                description=f"'{least.name}' contributed the lowest revenue ({least.value:,.2f} INR). Review pricing, shelf placement, or bundle with faster-moving items.",
                metric_value=f"{least.value:,.2f} INR",
                importance="low"
            )
        )

    return insights
