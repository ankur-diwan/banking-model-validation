"""
Performance Validator - Enhanced
Comprehensive performance validation with statistical tests integration
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)
import logging

# Import our statistical tests module
try:
    from statistical_tests import StatisticalTestsCalculator
except ImportError:
    from .statistical_tests import StatisticalTestsCalculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceValidator:
    """
    Enhanced performance validator with comprehensive metrics
    Integrates statistical tests (KS, Gini) and classification metrics
    """
    
    def __init__(self):
        """Initialize the performance validator"""
        self.stats_calculator = StatisticalTestsCalculator()
        logger.info("PerformanceValidator initialized with statistical tests integration")

    def validate_performance(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Comprehensive performance validation across all datasets
        
        Args:
            model_config: Model configuration
            train_data: Training dataset
            test_data: Test dataset
            oot_data: Out-of-time dataset
            
        Returns:
            Complete performance validation results
        """
        logger.info(f"Starting performance validation for model: {model_config.get('model_name', 'unknown')}")
        
        try:
            # Detect target and score columns
            target_column = self._detect_target_column(train_data)
            score_column = self._detect_score_column(train_data)
            
            logger.info(f"Detected target column: {target_column}, score column: {score_column}")
            
            results = {
                "status": "in_progress",
                "target_column": target_column,
                "score_column": score_column,
                "model_type": model_config.get("model_type", "unknown"),
                "scorecard_type": model_config.get("scorecard_type", "unknown"),
            }
            
            # Validate each dataset
            if target_column != "unknown" and score_column != "unknown":
                # Train dataset metrics
                results["train"] = self._calculate_dataset_metrics(
                    train_data, target_column, score_column, "train"
                )
                
                # Test dataset metrics
                results["test"] = self._calculate_dataset_metrics(
                    test_data, target_column, score_column, "test"
                )
                
                # OOT dataset metrics
                results["out_of_time"] = self._calculate_dataset_metrics(
                    oot_data, target_column, score_column, "out_of_time"
                )
                
                # Performance comparison across datasets
                results["comparison"] = self._compare_performance(
                    results["train"],
                    results["test"],
                    results.get("out_of_time")
                )
                
                # Overall status
                results["status"] = self._determine_overall_status(results)
                
            else:
                results["status"] = "error"
                results["error"] = f"Could not detect target ({target_column}) or score ({score_column}) columns"
                logger.error(results["error"])
            
            logger.info(f"Performance validation completed with status: {results['status']}")
            return results
            
        except Exception as e:
            logger.error(f"Performance validation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _calculate_dataset_metrics(
        self,
        data: pd.DataFrame,
        target_column: str,
        score_column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive metrics for a single dataset
        
        Args:
            data: Dataset to analyze
            target_column: Name of target column
            score_column: Name of score/probability column
            dataset_name: Name for reporting
            
        Returns:
            Dictionary with all performance metrics
        """
        try:
            metrics = {
                "dataset_name": dataset_name,
                "row_count": len(data),
                "column_count": len(data.columns),
            }
            
            if len(data) == 0:
                metrics["status"] = "error"
                metrics["error"] = "Empty dataset"
                return metrics
            
            # Basic statistics
            y_true = data[target_column].values
            y_scores_raw = data[score_column].values
            
            metrics["target_rate"] = round(float(y_true.mean()), 4)
            metrics["score_mean"] = round(float(y_scores_raw.mean()), 4)
            metrics["score_std"] = round(float(y_scores_raw.std()), 4)
            
            # Normalize scores to 0-1 range and invert
            # Higher credit score = lower risk = lower probability of default
            # So we need to invert: high score -> low probability of being bad (target=1)
            score_min = y_scores_raw.min()
            score_max = y_scores_raw.max()
            
            if score_max > score_min:
                # Normalize to 0-1
                y_scores_normalized = (y_scores_raw - score_min) / (score_max - score_min)
                # Invert: high score -> low probability of default
                y_pred_proba = 1 - y_scores_normalized
            else:
                # All scores are the same, use 0.5
                y_pred_proba = np.full_like(y_scores_raw, 0.5)
            
            # Binary classification metrics (using 0.5 threshold on probability)
            y_pred_binary = (y_pred_proba >= 0.5).astype(int)
            
            # Confusion Matrix
            cm = confusion_matrix(y_true, y_pred_binary)
            metrics["confusion_matrix"] = {
                "true_negative": int(cm[0, 0]),
                "false_positive": int(cm[0, 1]),
                "false_negative": int(cm[1, 0]),
                "true_positive": int(cm[1, 1])
            }
            
            # Classification Metrics
            metrics["accuracy"] = round(float(accuracy_score(y_true, y_pred_binary)), 4)
            metrics["precision"] = round(float(precision_score(y_true, y_pred_binary, zero_division=0)), 4)
            metrics["recall"] = round(float(recall_score(y_true, y_pred_binary, zero_division=0)), 4)
            metrics["f1_score"] = round(float(f1_score(y_true, y_pred_binary, zero_division=0)), 4)
            
            # AUC-ROC
            try:
                metrics["auc_roc"] = round(float(roc_auc_score(y_true, y_pred_proba)), 4)
            except Exception as e:
                metrics["auc_roc"] = None
                logger.warning(f"Could not calculate AUC-ROC for {dataset_name}: {str(e)}")
            
            # Statistical Tests (KS and Gini)
            ks_result = self.stats_calculator.calculate_ks_statistic(
                y_true, y_pred_proba, dataset_name
            )
            metrics["ks_test"] = ks_result
            
            gini_result = self.stats_calculator.calculate_gini_coefficient(
                y_true, y_pred_proba, dataset_name
            )
            metrics["gini_test"] = gini_result
            
            # Determine status based on metrics
            if (metrics.get("auc_roc", 0) >= 0.7 and
                ks_result.get("status") == "passed" and
                gini_result.get("status") == "passed"):
                metrics["status"] = "passed"
            elif (metrics.get("auc_roc", 0) >= 0.6 or
                  ks_result.get("status") in ["passed", "warning"]):
                metrics["status"] = "warning"
            else:
                metrics["status"] = "failed"
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics for {dataset_name}: {str(e)}")
            return {
                "dataset_name": dataset_name,
                "status": "error",
                "error": str(e)
            }

    def _compare_performance(
        self,
        train_metrics: Dict[str, Any],
        test_metrics: Dict[str, Any],
        oot_metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compare performance across datasets to detect degradation
        
        Args:
            train_metrics: Training dataset metrics
            test_metrics: Test dataset metrics
            oot_metrics: Out-of-time dataset metrics (optional)
            
        Returns:
            Comparison results with degradation analysis
        """
        try:
            comparison = {
                "datasets_compared": ["train", "test"]
            }
            
            # Compare key metrics
            metrics_to_compare = ["accuracy", "precision", "recall", "f1_score", "auc_roc"]
            
            for metric in metrics_to_compare:
                train_val = train_metrics.get(metric, 0)
                test_val = test_metrics.get(metric, 0)
                
                if train_val and test_val:
                    degradation = ((train_val - test_val) / train_val) * 100 if train_val > 0 else 0
                    comparison[f"{metric}_degradation_pct"] = round(degradation, 2)
            
            # Compare Gini coefficients
            train_gini = train_metrics.get("gini_test", {}).get("gini", 0)
            test_gini = test_metrics.get("gini_test", {}).get("gini", 0)
            
            gini_comparison = self.stats_calculator.compare_gini_across_datasets(
                train_metrics.get("gini_test", {}),
                test_metrics.get("gini_test", {}),
                oot_metrics.get("gini_test", {}) if oot_metrics else None
            )
            comparison["gini_comparison"] = gini_comparison
            
            # OOT comparison if available
            if oot_metrics:
                comparison["datasets_compared"].append("out_of_time")
                for metric in metrics_to_compare:
                    train_val = train_metrics.get(metric, 0)
                    oot_val = oot_metrics.get(metric, 0)
                    
                    if train_val and oot_val:
                        degradation = ((train_val - oot_val) / train_val) * 100 if train_val > 0 else 0
                        comparison[f"{metric}_oot_degradation_pct"] = round(degradation, 2)
            
            # Overall assessment
            max_degradation = max([
                abs(comparison.get(f"{m}_degradation_pct", 0))
                for m in metrics_to_compare
            ])
            
            if max_degradation < 10:
                comparison["overall_assessment"] = "Stable performance across datasets"
                comparison["status"] = "passed"
            elif max_degradation < 20:
                comparison["overall_assessment"] = "Moderate performance degradation detected"
                comparison["status"] = "warning"
            else:
                comparison["overall_assessment"] = "Significant performance degradation detected"
                comparison["status"] = "failed"
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing performance: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _determine_overall_status(self, results: Dict[str, Any]) -> str:
        """Determine overall validation status"""
        statuses = []
        
        for dataset in ["train", "test", "out_of_time"]:
            if dataset in results:
                statuses.append(results[dataset].get("status", "unknown"))
        
        if "comparison" in results:
            statuses.append(results["comparison"].get("status", "unknown"))
        
        if "failed" in statuses or "error" in statuses:
            return "failed"
        elif "warning" in statuses:
            return "warning"
        elif "passed" in statuses:
            return "passed"
        else:
            return "unknown"

    def _detect_target_column(self, df: pd.DataFrame) -> str:
        """Detect the target column in the dataset"""
        for candidate in ["default", "default_next_12m", "recovered", "target", "label", "y"]:
            if candidate in df.columns:
                return candidate
        return "unknown"
    
    def _detect_score_column(self, df: pd.DataFrame) -> str:
        """Detect the score/probability column in the dataset"""
        for candidate in ["score", "probability", "pred_proba", "prediction", "y_pred"]:
            if candidate in df.columns:
                return candidate
        return "unknown"

    def _dataset_summary(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Legacy method for backward compatibility"""
        summary = {
            "row_count": len(df),
            "column_count": len(df.columns),
        }

        if target_column in df.columns and len(df) > 0:
            summary["target_rate"] = round(float(df[target_column].mean()), 4)

        return summary


# Made with Bob - Enhanced Performance Validator
