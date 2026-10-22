import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any, Optional
from datetime import datetime

from backend.app.schemas.sales import (
    ColumnMappingConfig,
    DataQualityReport,
    DataQualityIssue
)

class DataPreprocessor:
    def __init__(self):
        pass

    def auto_detect_mapping(self, df: pd.DataFrame) -> ColumnMappingConfig:
        """Heuristically detect columns if standard names aren't matched exactly."""
        cols = {c.lower().strip().replace(" ", "_"): c for c in df.columns}
        
        def find_exact_or_substring(candidates: List[str], exclude: Optional[List[str]] = None) -> Optional[str]:
            exclude = exclude or []
            # 1. Exact match check
            for cand in candidates:
                for norm_c, orig_c in cols.items():
                    if norm_c == cand and not any(ex in norm_c for ex in exclude):
                        return orig_c
            # 2. Substring match check
            for cand in candidates:
                for norm_c, orig_c in cols.items():
                    if cand in norm_c and not any(ex in norm_c for ex in exclude):
                        return orig_c
            return None

        date_col = find_exact_or_substring(["date", "dt", "trans_date", "invoice_date", "day_date"]) or "Date"
        day_col = find_exact_or_substring(["day_of_week", "day_name", "weekday", "day"], exclude=["date"])
        cat_col = find_exact_or_substring(["product_category", "category", "dept", "department", "cat"])
        prod_col = find_exact_or_substring(["product_name", "product", "item_name", "item", "sku", "description", "desc"], exclude=["category"])
        qty_col = find_exact_or_substring(["quantity_sold", "quantity", "qty", "units", "venda", "count"])
        price_col = find_exact_or_substring(["unit_price", "price", "rate", "cost", "preco"])
        total_col = find_exact_or_substring(["total_sales", "total_revenue", "weekly_sales", "amount", "total", "net_amount"])

        return ColumnMappingConfig(
            date_col=date_col if date_col in df.columns else (df.columns[0] if len(df.columns) > 0 else "Date"),
            day_col=day_col if day_col in df.columns else None,
            category_col=cat_col if cat_col in df.columns else None,
            product_col=prod_col if prod_col in df.columns else None,
            quantity_col=qty_col if qty_col in df.columns else None,
            price_col=price_col if price_col in df.columns else None,
            total_sales_col=total_col if total_col in df.columns else None
        )

    def clean(self, raw_df: pd.DataFrame, mapping: Optional[ColumnMappingConfig] = None) -> Tuple[pd.DataFrame, DataQualityReport]:
        df = raw_df.copy()
        report = DataQualityReport(total_raw_rows=len(df))

        if df.empty:
            report.warnings.append("The uploaded dataset is empty.")
            return pd.DataFrame(), report

        if mapping is None:
            mapping = self.auto_detect_mapping(df)

        issues: List[DataQualityIssue] = []
        missing_counts: Dict[str, int] = {}

        # 1. Check duplicate rows
        duplicates_mask = df.duplicated()
        dup_count = int(duplicates_mask.sum())
        report.duplicate_rows_detected = dup_count
        if dup_count > 0:
            report.warnings.append(f"Detected {dup_count} duplicate row(s) in source dataset.")
            for idx in df[duplicates_mask].index[:10]: # report up to 10 instances
                issues.append(DataQualityIssue(
                    row_index=int(idx),
                    column="ALL",
                    issue_type="duplicate_row",
                    original_value="Duplicate Row Record",
                    action_taken="flagged",
                    severity="warning"
                ))

        # 2. Date parsing
        date_col = mapping.date_col
        if date_col not in df.columns:
            # Fallback search
            found = False
            for col in df.columns:
                if "date" in col.lower():
                    date_col = col
                    found = True
                    break
            if not found:
                report.rejected_rows = len(df)
                report.warnings.append(f"Required date column '{mapping.date_col}' not found in dataset.")
                report.issues = issues
                return pd.DataFrame(), report

        # Track missing dates
        null_dates = df[date_col].isna()
        if null_dates.sum() > 0:
            missing_counts["date"] = int(null_dates.sum())
            for idx in df[null_dates].index:
                issues.append(DataQualityIssue(
                    row_index=int(idx),
                    column=date_col,
                    issue_type="missing_date",
                    original_value=None,
                    action_taken="dropped",
                    severity="error"
                ))

        # Parse date with multiple format handling
        parsed_dates = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        # For values that failed with dayfirst=True, try without dayfirst
        if parsed_dates.isna().sum() > null_dates.sum():
            failed_mask = parsed_dates.isna() & (~null_dates)
            fallback_parsed = pd.to_datetime(df.loc[failed_mask, date_col], errors="coerce")
            parsed_dates.update(fallback_parsed)

        invalid_date_mask = parsed_dates.isna()
        for idx in df[invalid_date_mask & (~null_dates)].index:
            issues.append(DataQualityIssue(
                row_index=int(idx),
                column=date_col,
                issue_type="invalid_date_format",
                original_value=str(df.loc[idx, date_col]),
                action_taken="dropped",
                severity="error"
            ))

        df["_parsed_date"] = parsed_dates
        df["date"] = parsed_dates.dt.strftime("%Y-%m-%d")
        df["day_of_week"] = parsed_dates.dt.day_name()

        # 3. Calendar verification against user-provided Day column
        date_corrections = 0
        if mapping.day_col and mapping.day_col in df.columns:
            for idx, row in df.iterrows():
                if pd.notna(row["_parsed_date"]) and pd.notna(row[mapping.day_col]):
                    given_day = str(row[mapping.day_col]).strip().capitalize()
                    actual_day = row["day_of_week"]
                    if given_day != actual_day:
                        date_corrections += 1
                        issues.append(DataQualityIssue(
                            row_index=int(idx),
                            column=mapping.day_col,
                            issue_type="weekday_calendar_mismatch",
                            original_value=given_day,
                            action_taken=f"corrected to {actual_day}",
                            severity="warning",
                            details=f"Date {row['date']} fell on a {actual_day}, but was annotated as {given_day}."
                        ))
        report.date_corrections_count = date_corrections
        if date_corrections > 0:
            report.warnings.append(
                f"Corrected {date_corrections} weekday annotation(s) where manual label contradicted verified calendar."
            )

        # 4. Product Name and Category handling
        if mapping.product_col and mapping.product_col in df.columns:
            df["product_name"] = df[mapping.product_col].fillna("Unknown Item").astype(str).str.strip()
            # check missing
            null_prod = df[mapping.product_col].isna() | (df[mapping.product_col].astype(str).str.strip() == "")
            if null_prod.sum() > 0:
                missing_counts["product_name"] = int(null_prod.sum())
                for idx in df[null_prod].index:
                    issues.append(DataQualityIssue(
                        row_index=int(idx),
                        column=mapping.product_col,
                        issue_type="missing_product_name",
                        original_value=None,
                        action_taken="imputed 'Unknown Item'",
                        severity="warning"
                    ))
        else:
            df["product_name"] = "Item"

        if mapping.category_col and mapping.category_col in df.columns:
            df["product_category"] = df[mapping.category_col].fillna("General").astype(str).str.strip()
            null_cat = df[mapping.category_col].isna() | (df[mapping.category_col].astype(str).str.strip() == "")
            if null_cat.sum() > 0:
                missing_counts["product_category"] = int(null_cat.sum())
                for idx in df[null_cat].index:
                    issues.append(DataQualityIssue(
                        row_index=int(idx),
                        column=mapping.category_col,
                        issue_type="missing_category",
                        original_value=None,
                        action_taken="imputed 'General'",
                        severity="warning"
                    ))
        else:
            df["product_category"] = "General"

        # 5. Quantity and Price / Total Sales numeric processing
        # Quantity
        if mapping.quantity_col and mapping.quantity_col in df.columns:
            raw_qty = pd.to_numeric(df[mapping.quantity_col], errors="coerce")
            null_qty = raw_qty.isna()
            neg_qty = raw_qty < 0
            if null_qty.sum() > 0:
                missing_counts["quantity"] = int(null_qty.sum())
                for idx in df[null_qty].index:
                    issues.append(DataQualityIssue(
                        row_index=int(idx),
                        column=mapping.quantity_col,
                        issue_type="invalid_or_missing_quantity",
                        original_value=str(df.loc[idx, mapping.quantity_col]),
                        action_taken="dropped",
                        severity="error"
                    ))
            for idx in df[neg_qty].index:
                issues.append(DataQualityIssue(
                    row_index=int(idx),
                    column=mapping.quantity_col,
                    issue_type="negative_quantity",
                    original_value=float(raw_qty.loc[idx]),
                    action_taken="dropped",
                    severity="error"
                ))
            df["quantity_sold"] = raw_qty
        else:
            # Default to 1 unit if total sales is present
            df["quantity_sold"] = 1.0

        # Price
        if mapping.price_col and mapping.price_col in df.columns:
            raw_price = pd.to_numeric(df[mapping.price_col], errors="coerce")
            neg_price = raw_price < 0
            null_price = raw_price.isna()
            if null_price.sum() > 0:
                missing_counts["price"] = int(null_price.sum())
            for idx in df[neg_price].index:
                issues.append(DataQualityIssue(
                    row_index=int(idx),
                    column=mapping.price_col,
                    issue_type="negative_price",
                    original_value=float(raw_price.loc[idx]),
                    action_taken="dropped",
                    severity="error"
                ))
            df["unit_price"] = raw_price
        else:
            df["unit_price"] = None

        # Total Sales: Check precalculated or calculate from Quantity * Price
        has_precalc_total = False
        if mapping.total_sales_col and mapping.total_sales_col in df.columns:
            raw_total = pd.to_numeric(df[mapping.total_sales_col], errors="coerce")
            if raw_total.notna().sum() > 0:
                has_precalc_total = True
                df["total_sales"] = raw_total
                neg_total = raw_total < 0
                for idx in df[neg_total].index:
                    issues.append(DataQualityIssue(
                        row_index=int(idx),
                        column=mapping.total_sales_col,
                        issue_type="negative_total_sales",
                        original_value=float(raw_total.loc[idx]),
                        action_taken="dropped",
                        severity="error"
                    ))

        if not has_precalc_total:
            # Calculate Total Sales = Quantity Sold * Unit Price
            if "unit_price" in df.columns and df["unit_price"].notna().any():
                df["total_sales"] = df["quantity_sold"] * df["unit_price"]
            else:
                # If neither price nor total sales exists, quantity is total units
                df["total_sales"] = df["quantity_sold"]

        # 6. Filter valid rows
        valid_mask = (
            df["_parsed_date"].notna() &
            df["quantity_sold"].notna() &
            (df["quantity_sold"] >= 0) &
            df["total_sales"].notna() &
            (df["total_sales"] >= 0)
        )
        if "unit_price" in df.columns and df["unit_price"].notna().any():
            valid_mask = valid_mask & ((df["unit_price"].isna()) | (df["unit_price"] >= 0))

        clean_df = df[valid_mask].copy()
        
        report.accepted_rows = len(clean_df)
        report.rejected_rows = report.total_raw_rows - report.accepted_rows
        report.missing_values_count = missing_counts
        report.issues = issues

        # Keep clean output columns
        cols_to_keep = [
            "date",
            "day_of_week",
            "product_category",
            "product_name",
            "quantity_sold",
            "unit_price",
            "total_sales"
        ]
        clean_df = clean_df[[c for c in cols_to_keep if c in clean_df.columns]]
        clean_df.sort_values(by="date", inplace=True)
        clean_df.reset_index(drop=True, inplace=True)

        return clean_df, report
