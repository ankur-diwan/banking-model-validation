"""
Statistical Tests Module
Implements core statistical tests for model validation:
- KS (Kolmogorov-Smirnov) Test
- Gini Coefficient
- PSI (Population Stability Index)
- CSI (Characteristic Stability Index)
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve
import warnings

warnings.filterwarnings('ignore')


class StatisticalTestsCalculator:
    """
    Calculator for statistical tests used in model validation
    """
    
    def __init__(self):
        """Initialize the calculator"""
        self.results = {}
    
    def calculate_ks_statistic(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray,
        dataset_name: str = "dataset"
    ) -> Dict[str, Any]:
        """
        Calculate Kolmogorov-Smirnov (KS) statistic
        
        The KS statistic measures the maximum separation between the cumulative
        distribution functions of good and bad customers.
        
        Args:
            y_true: True binary labels (0 or 1)
            y_pred_proba: Predicted probabilities
            dataset_name: Name of the dataset for reporting
            
        Returns:
            Dictionary containing KS statistic, optimal cutoff, and interpretation
        """
        try:
            # Separate scores for good (0) and bad (1) customers
            scores_good = y_pred_proba[y_true == 0]
            scores_bad = y_pred_proba[y_true == 1]
            
            # Calculate KS statistic
            ks_statistic, p_value = stats.ks_2samp(scores_bad, scores_good)
            
            # Find optimal cutoff (point of maximum separation)
            fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
            ks_values = tpr - fpr
            optimal_idx = np.argmax(ks_values)
            optimal_cutoff = thresholds[optimal_idx]
            max_ks = ks_values[optimal_idx]
            
            # Interpretation
            if ks_statistic >= 0.4:
                interpretation = "Excellent discrimination"
                status = "passed"
            elif ks_statistic >= 0.3:
                interpretation = "Good discrimination"
                status = "passed"
            elif ks_statistic >= 0.2:
                interpretation = "Acceptable discrimination"
                status = "warning"
            else:
                interpretation = "Poor discrimination"
                status = "failed"
            
            result = {
                "test_name": "Kolmogorov-Smirnov Test",
                "dataset": dataset_name,
                "ks_statistic": round(float(ks_statistic), 4),
                "max_ks": round(float(max_ks), 4),
                "optimal_cutoff": round(float(optimal_cutoff), 4),
                "p_value": round(float(p_value), 6),
                "interpretation": interpretation,
                "status": status,
                "threshold": {
                    "excellent": 0.4,
                    "good": 0.3,
                    "acceptable": 0.2
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "test_name": "Kolmogorov-Smirnov Test",
                "dataset": dataset_name,
                "status": "error",
                "error": str(e)
            }
    
    def calculate_gini_coefficient(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray,
        dataset_name: str = "dataset"
    ) -> Dict[str, Any]:
        """
        Calculate Gini Coefficient
        
        Gini = 2 * AUC - 1
        Measures the model's ability to discriminate between good and bad customers.
        
        Args:
            y_true: True binary labels
            y_pred_proba: Predicted probabilities
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary containing Gini coefficient, AUC, and interpretation
        """
        try:
            # Calculate AUC
            auc = roc_auc_score(y_true, y_pred_proba)
            
            # Calculate Gini
            gini = 2 * auc - 1
            
            # Interpretation
            if gini >= 0.6:
                interpretation = "Excellent model performance"
                status = "passed"
            elif gini >= 0.4:
                interpretation = "Good model performance"
                status = "passed"
            elif gini >= 0.3:
                interpretation = "Acceptable model performance"
                status = "warning"
            else:
                interpretation = "Poor model performance"
                status = "failed"
            
            result = {
                "test_name": "Gini Coefficient",
                "dataset": dataset_name,
                "gini": round(float(gini), 4),
                "auc": round(float(auc), 4),
                "interpretation": interpretation,
                "status": status,
                "threshold": {
                    "excellent": 0.6,
                    "good": 0.4,
                    "acceptable": 0.3
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "test_name": "Gini Coefficient",
                "dataset": dataset_name,
                "status": "error",
                "error": str(e)
            }
    
    def compare_gini_across_datasets(
        self,
        train_result: Dict[str, Any],
        test_result: Dict[str, Any],
        oot_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compare Gini coefficients across datasets to detect degradation
        
        Args:
            train_result: Gini result from training data
            test_result: Gini result from test data
            oot_result: Gini result from out-of-time data (optional)
            
        Returns:
            Comparison results with degradation analysis
        """
        try:
            train_gini = train_result.get("gini", 0)
            test_gini = test_result.get("gini", 0)
            
            # Calculate degradation
            degradation_test = ((train_gini - test_gini) / train_gini) * 100 if train_gini > 0 else 0
            
            comparison = {
                "train_gini": round(train_gini, 4),
                "test_gini": round(test_gini, 4),
                "degradation_pct": round(degradation_test, 2),
                "datasets_compared": ["train", "test"]
            }
            
            if oot_result:
                oot_gini = oot_result.get("gini", 0)
                degradation_oot = ((train_gini - oot_gini) / train_gini) * 100 if train_gini > 0 else 0
                comparison["oot_gini"] = round(oot_gini, 4)
                comparison["degradation_oot_pct"] = round(degradation_oot, 2)
                comparison["datasets_compared"].append("oot")
            
            # Interpretation
            max_degradation = max(abs(degradation_test), 
                                 abs(comparison.get("degradation_oot_pct", 0)))
            
            if max_degradation < 10:
                comparison["interpretation"] = "Stable performance across datasets"
                comparison["status"] = "passed"
            elif max_degradation < 20:
                comparison["interpretation"] = "Moderate degradation detected"
                comparison["status"] = "warning"
            else:
                comparison["interpretation"] = "Significant degradation detected"
                comparison["status"] = "failed"
            
            return comparison
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def calculate_psi(
        self,
        expected: np.ndarray,
        actual: np.ndarray,
        buckets: int = 10,
        feature_name: str = "feature"
    ) -> Dict[str, Any]:
        """
        Calculate Population Stability Index (PSI)
        
        PSI measures the shift in population distribution between two datasets.
        PSI = sum((actual% - expected%) * ln(actual% / expected%))
        
        Args:
            expected: Expected distribution (e.g., training data)
            actual: Actual distribution (e.g., test/OOT data)
            buckets: Number of buckets for binning
            feature_name: Name of the feature
            
        Returns:
            Dictionary containing PSI value, bucket details, and interpretation
        """
        try:
            # Remove NaN values
            expected = expected[~np.isnan(expected)]
            actual = actual[~np.isnan(actual)]
            
            # Create bins based on expected distribution
            breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
            breakpoints = np.unique(breakpoints)  # Remove duplicates
            
            # If we have fewer unique breakpoints than requested buckets
            if len(breakpoints) < buckets + 1:
                buckets = len(breakpoints) - 1
            
            # Bin the data
            expected_bins = np.digitize(expected, breakpoints[1:-1])
            actual_bins = np.digitize(actual, breakpoints[1:-1])
            
            # Calculate percentages
            expected_percents = np.array([(expected_bins == i).sum() / len(expected) 
                                         for i in range(buckets)])
            actual_percents = np.array([(actual_bins == i).sum() / len(actual) 
                                       for i in range(buckets)])
            
            # Avoid division by zero
            expected_percents = np.where(expected_percents == 0, 0.0001, expected_percents)
            actual_percents = np.where(actual_percents == 0, 0.0001, actual_percents)
            
            # Calculate PSI
            psi_values = (actual_percents - expected_percents) * np.log(actual_percents / expected_percents)
            psi = np.sum(psi_values)
            
            # Interpretation
            if psi < 0.1:
                interpretation = "No significant population shift"
                status = "passed"
            elif psi < 0.25:
                interpretation = "Moderate population shift"
                status = "warning"
            else:
                interpretation = "Significant population shift"
                status = "failed"
            
            result = {
                "test_name": "Population Stability Index",
                "feature": feature_name,
                "psi": round(float(psi), 4),
                "buckets": int(buckets),
                "interpretation": interpretation,
                "status": status,
                "threshold": {
                    "stable": 0.1,
                    "moderate": 0.25
                },
                "bucket_details": [
                    {
                        "bucket": i,
                        "expected_pct": round(float(expected_percents[i]) * 100, 2),
                        "actual_pct": round(float(actual_percents[i]) * 100, 2),
                        "psi_contribution": round(float(psi_values[i]), 4)
                    }
                    for i in range(buckets)
                ]
            }
            
            return result
            
        except Exception as e:
            return {
                "test_name": "Population Stability Index",
                "feature": feature_name,
                "status": "error",
                "error": str(e)
            }
    
    def calculate_csi(
        self,
        expected_df: pd.DataFrame,
        actual_df: pd.DataFrame,
        features: Optional[List[str]] = None,
        buckets: int = 10
    ) -> Dict[str, Any]:
        """
        Calculate Characteristic Stability Index (CSI) for multiple features
        
        CSI is similar to PSI but applied to individual features/characteristics.
        
        Args:
            expected_df: Expected dataset (e.g., training data)
            actual_df: Actual dataset (e.g., test/OOT data)
            features: List of features to analyze (if None, use all numeric features)
            buckets: Number of buckets for binning
            
        Returns:
            Dictionary containing CSI for each feature and overall stability
        """
        try:
            # Select features
            if features is None:
                features = expected_df.select_dtypes(include=[np.number]).columns.tolist()
            
            # Calculate CSI for each feature
            feature_csi = {}
            unstable_features = []
            
            for feature in features:
                if feature in expected_df.columns and feature in actual_df.columns:
                    psi_result = self.calculate_psi(
                        expected_df[feature].values,
                        actual_df[feature].values,
                        buckets=buckets,
                        feature_name=feature
                    )
                    
                    feature_csi[feature] = psi_result
                    
                    if psi_result.get("status") in ["warning", "failed"]:
                        unstable_features.append({
                            "feature": feature,
                            "csi": psi_result.get("psi", 0),
                            "status": psi_result.get("status")
                        })
            
            # Overall assessment
            avg_csi = np.mean([result.get("psi", 0) for result in feature_csi.values()])
            
            if avg_csi < 0.1:
                overall_status = "passed"
                overall_interpretation = "All features are stable"
            elif avg_csi < 0.25:
                overall_status = "warning"
                overall_interpretation = f"{len(unstable_features)} features show moderate instability"
            else:
                overall_status = "failed"
                overall_interpretation = f"{len(unstable_features)} features show significant instability"
            
            result = {
                "test_name": "Characteristic Stability Index",
                "features_analyzed": len(features),
                "average_csi": round(float(avg_csi), 4),
                "unstable_features_count": len(unstable_features),
                "unstable_features": unstable_features,
                "overall_status": overall_status,
                "overall_interpretation": overall_interpretation,
                "feature_details": feature_csi
            }
            
            return result
            
        except Exception as e:
            return {
                "test_name": "Characteristic Stability Index",
                "status": "error",
                "error": str(e)
            }
    
    def run_all_tests(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: Optional[pd.DataFrame] = None,
        target_column: str = "default",
        score_column: str = "score",
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run all statistical tests on the provided datasets
        
        Args:
            train_data: Training dataset
            test_data: Test dataset
            oot_data: Out-of-time dataset (optional)
            target_column: Name of the target column
            score_column: Name of the score/probability column
            features: List of features for CSI analysis
            
        Returns:
            Complete results from all statistical tests
        """
        results = {
            "ks_tests": {},
            "gini_tests": {},
            "gini_comparison": {},
            "psi_tests": {},
            "csi_test": {}
        }
        
        try:
            # KS and Gini for train
            if target_column in train_data.columns and score_column in train_data.columns:
                results["ks_tests"]["train"] = self.calculate_ks_statistic(
                    train_data[target_column].values,
                    train_data[score_column].values,
                    "train"
                )
                results["gini_tests"]["train"] = self.calculate_gini_coefficient(
                    train_data[target_column].values,
                    train_data[score_column].values,
                    "train"
                )
            
            # KS and Gini for test
            if target_column in test_data.columns and score_column in test_data.columns:
                results["ks_tests"]["test"] = self.calculate_ks_statistic(
                    test_data[target_column].values,
                    test_data[score_column].values,
                    "test"
                )
                results["gini_tests"]["test"] = self.calculate_gini_coefficient(
                    test_data[target_column].values,
                    test_data[score_column].values,
                    "test"
                )
            
            # KS and Gini for OOT
            if oot_data is not None and target_column in oot_data.columns and score_column in oot_data.columns:
                results["ks_tests"]["oot"] = self.calculate_ks_statistic(
                    oot_data[target_column].values,
                    oot_data[score_column].values,
                    "oot"
                )
                results["gini_tests"]["oot"] = self.calculate_gini_coefficient(
                    oot_data[target_column].values,
                    oot_data[score_column].values,
                    "oot"
                )
            
            # Gini comparison
            if "train" in results["gini_tests"] and "test" in results["gini_tests"]:
                results["gini_comparison"] = self.compare_gini_across_datasets(
                    results["gini_tests"]["train"],
                    results["gini_tests"]["test"],
                    results["gini_tests"].get("oot")
                )
            
            # PSI for score
            if score_column in train_data.columns and score_column in test_data.columns:
                results["psi_tests"]["score_test"] = self.calculate_psi(
                    train_data[score_column].values,
                    test_data[score_column].values,
                    feature_name=score_column
                )
                
                if oot_data is not None and score_column in oot_data.columns:
                    results["psi_tests"]["score_oot"] = self.calculate_psi(
                        train_data[score_column].values,
                        oot_data[score_column].values,
                        feature_name=score_column
                    )
            
            # CSI for features
            if features:
                results["csi_test"]["test"] = self.calculate_csi(
                    train_data,
                    test_data,
                    features=features
                )
                
                if oot_data is not None:
                    results["csi_test"]["oot"] = self.calculate_csi(
                        train_data,
                        oot_data,
                        features=features
                    )
            
            # Overall summary
            results["summary"] = {
                "tests_completed": sum([
                    len(results["ks_tests"]),
                    len(results["gini_tests"]),
                    len(results["psi_tests"]),
                    1 if results["csi_test"] else 0
                ]),
                "overall_status": self._determine_overall_status(results)
            }
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["status"] = "error"
            return results
    
    def _determine_overall_status(self, results: Dict[str, Any]) -> str:
        """Determine overall status from all test results"""
        statuses = []
        
        # Collect all statuses
        for test_category in ["ks_tests", "gini_tests", "psi_tests"]:
            for test_result in results.get(test_category, {}).values():
                if isinstance(test_result, dict):
                    statuses.append(test_result.get("status", "unknown"))
        
        # Check CSI
        for csi_result in results.get("csi_test", {}).values():
            if isinstance(csi_result, dict):
                statuses.append(csi_result.get("overall_status", "unknown"))
        
        # Determine overall
        if "failed" in statuses or "error" in statuses:
            return "failed"
        elif "warning" in statuses:
            return "warning"
        elif "passed" in statuses:
            return "passed"
        else:
            return "unknown"


# Made with Bob - Statistical Tests Module for Model Validation