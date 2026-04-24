"""
Data Quality Validator
Provides lightweight dataset quality checks for validation workflows
"""

from typing import Dict, Any
import pandas as pd


class DataQualityValidator:
    """Validate basic dataset quality metrics."""

    def validate_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        row_count = len(df)
        column_count = len(df.columns)

        if row_count == 0 or column_count == 0:
            return {
                "row_count": row_count,
                "column_count": column_count,
                "missing_percentage": 100.0,
                "duplicate_rows": 0,
                "overall_score": 0.0,
                "status": "failed",
                "checks": {
                    "non_empty": False,
                    "has_columns": column_count > 0,
                    "duplicate_rate_ok": False,
                    "missing_rate_ok": False,
                },
            }

        total_cells = row_count * column_count
        missing_cells = int(df.isna().sum().sum())
        missing_percentage = round((missing_cells / total_cells) * 100, 2) if total_cells else 0.0

        duplicate_rows = int(df.duplicated().sum())
        duplicate_percentage = round((duplicate_rows / row_count) * 100, 2) if row_count else 0.0

        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

        checks = {
            "non_empty": row_count > 0,
            "has_columns": column_count > 0,
            "duplicate_rate_ok": duplicate_percentage <= 5.0,
            "missing_rate_ok": missing_percentage <= 10.0,
        }

        passed_checks = sum(1 for passed in checks.values() if passed)
        overall_score = round((passed_checks / len(checks)) * 100, 2)

        return {
            "row_count": row_count,
            "column_count": column_count,
            "numeric_columns": len(numeric_columns),
            "categorical_columns": len(categorical_columns),
            "missing_percentage": missing_percentage,
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": duplicate_percentage,
            "overall_score": overall_score,
            "status": "passed" if overall_score >= 75 else "warning",
            "checks": checks,
        }

# Made with Bob
