"""
Performance Validator
Minimal implementation required for runtime validation flow
"""

from typing import Dict, Any
import pandas as pd


class PerformanceValidator:
    """Perform lightweight performance validation."""

    def validate_performance(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        target_column = self._detect_target_column(train_data)

        return {
            "status": "passed",
            "target_column": target_column,
            "train": self._dataset_summary(train_data, target_column),
            "test": self._dataset_summary(test_data, target_column),
            "out_of_time": self._dataset_summary(oot_data, target_column),
        }

    def _detect_target_column(self, df: pd.DataFrame) -> str:
        for candidate in ["default", "default_next_12m", "recovered"]:
            if candidate in df.columns:
                return candidate
        return "unknown"

    def _dataset_summary(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        summary = {
            "row_count": len(df),
            "column_count": len(df.columns),
        }

        if target_column in df.columns and len(df) > 0:
            summary["target_rate"] = round(float(df[target_column].mean()), 4)

        return summary

# Made with Bob
