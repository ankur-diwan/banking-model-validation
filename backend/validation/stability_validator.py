"""
Stability Validator - Enhanced
Comprehensive stability analysis with PSI/CSI integration
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import logging

# Import our statistical tests module for PSI/CSI
try:
    from statistical_tests import StatisticalTestsCalculator
except ImportError:
    from .statistical_tests import StatisticalTestsCalculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StabilityValidator:
    """
    Enhanced stability validator with PSI/CSI integration
    Analyzes population and characteristic stability across datasets
    """
    
    def __init__(self):
        """Initialize the stability validator"""
        self.stats_calculator = StatisticalTestsCalculator()
        logger.info("StabilityValidator initialized with PSI/CSI integration")
    
    def analyze_stability(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        model_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive stability analysis across all datasets
        
        Args:
            train_data: Training dataset
            test_data: Test dataset
            oot_data: Out-of-time dataset
            model_config: Optional model configuration
            
        Returns:
            Complete stability analysis results
        """
        logger.info("Starting comprehensive stability analysis")
        
        try:
            results = {
                "status": "in_progress",
                "train_rows": len(train_data),
                "test_rows": len(test_data),
                "oot_rows": len(oot_data),
            }
            
            # Detect target and score columns
            target_column = self._detect_target_column(train_data)
            score_column = self._detect_score_column(train_data)
            
            if target_column == "unknown" or score_column == "unknown":
                results["status"] = "error"
                results["error"] = f"Could not detect target ({target_column}) or score ({score_column}) columns"
                return results
            
            results["target_column"] = target_column
            results["score_column"] = score_column
            
            # 1. Population Stability Index (PSI) Analysis
            results["psi_analysis"] = self._analyze_psi(
                train_data, test_data, oot_data, target_column, score_column
            )
            
            # 2. Characteristic Stability Index (CSI) Analysis
            results["csi_analysis"] = self._analyze_csi(
                train_data, test_data, oot_data
            )
            
            # 3. Target Rate Stability
            results["target_stability"] = self._analyze_target_stability(
                train_data, test_data, oot_data, target_column
            )
            
            # 4. Score Distribution Stability
            results["score_stability"] = self._analyze_score_stability(
                train_data, test_data, oot_data, score_column
            )
            
            # 5. Feature Stability Analysis
            results["feature_stability"] = self._analyze_feature_stability(
                train_data, test_data, oot_data
            )
            
            # 6. Overall Stability Assessment
            results["overall_assessment"] = self._determine_overall_stability(results)
            results["status"] = results["overall_assessment"]["status"]
            
            logger.info(f"Stability analysis completed with status: {results['status']}")
            return results
            
        except Exception as e:
            logger.error(f"Stability analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _analyze_psi(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        target_column: str,
        score_column: str
    ) -> Dict[str, Any]:
        """
        Analyze Population Stability Index across datasets
        
        PSI measures the shift in population distribution
        Thresholds: <0.1 (stable), 0.1-0.25 (moderate shift), >0.25 (significant shift)
        """
        logger.info("Calculating PSI across datasets")
        
        try:
            # Calculate PSI for target variable
            target_psi_test = self.stats_calculator.calculate_psi(
                train_data[target_column].values,
                test_data[target_column].values,
                "target_train_vs_test"
            )
            
            target_psi_oot = self.stats_calculator.calculate_psi(
                train_data[target_column].values,
                oot_data[target_column].values,
                "target_train_vs_oot"
            )
            
            # Calculate PSI for score variable
            score_psi_test = self.stats_calculator.calculate_psi(
                train_data[score_column].values,
                test_data[score_column].values,
                "score_train_vs_test"
            )
            
            score_psi_oot = self.stats_calculator.calculate_psi(
                train_data[score_column].values,
                oot_data[score_column].values,
                "score_train_vs_oot"
            )
            
            # Determine overall PSI status
            all_psi_values = [
                target_psi_test.get("psi", 0),
                target_psi_oot.get("psi", 0),
                score_psi_test.get("psi", 0),
                score_psi_oot.get("psi", 0)
            ]
            max_psi = max(all_psi_values)
            
            if max_psi < 0.1:
                psi_status = "passed"
                psi_message = "Population is stable across all datasets"
            elif max_psi < 0.25:
                psi_status = "warning"
                psi_message = "Moderate population shift detected"
            else:
                psi_status = "failed"
                psi_message = "Significant population shift detected"
            
            return {
                "target_psi": {
                    "train_vs_test": target_psi_test,
                    "train_vs_oot": target_psi_oot
                },
                "score_psi": {
                    "train_vs_test": score_psi_test,
                    "train_vs_oot": score_psi_oot
                },
                "max_psi": round(max_psi, 4),
                "status": psi_status,
                "message": psi_message
            }
            
        except Exception as e:
            logger.error(f"PSI analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _analyze_csi(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze Characteristic Stability Index for features
        
        CSI measures the shift in feature distributions
        """
        logger.info("Calculating CSI for features")
        
        try:
            # Get numeric features (excluding target and score)
            numeric_features = train_data.select_dtypes(include=[np.number]).columns.tolist()
            exclude_cols = ['default', 'default_next_12m', 'recovered', 'score', 'probability', 'target']
            numeric_features = [f for f in numeric_features if f not in exclude_cols]
            
            if len(numeric_features) == 0:
                return {
                    "status": "warning",
                    "message": "No numeric features found for CSI analysis"
                }
            
            # Calculate CSI for train vs test
            csi_test = self.stats_calculator.calculate_csi(
                train_data[numeric_features],
                test_data[numeric_features],
                "train_vs_test"
            )
            
            # Calculate CSI for train vs OOT
            csi_oot = self.stats_calculator.calculate_csi(
                train_data[numeric_features],
                oot_data[numeric_features],
                "train_vs_oot"
            )
            
            # Determine overall CSI status
            max_csi_test = max([f["csi"] for f in csi_test.get("feature_csi", [])]) if csi_test.get("feature_csi") else 0
            max_csi_oot = max([f["csi"] for f in csi_oot.get("feature_csi", [])]) if csi_oot.get("feature_csi") else 0
            max_csi = max(max_csi_test, max_csi_oot)
            
            if max_csi < 0.1:
                csi_status = "passed"
                csi_message = "Feature distributions are stable"
            elif max_csi < 0.25:
                csi_status = "warning"
                csi_message = "Moderate feature distribution shift detected"
            else:
                csi_status = "failed"
                csi_message = "Significant feature distribution shift detected"
            
            return {
                "train_vs_test": csi_test,
                "train_vs_oot": csi_oot,
                "max_csi": round(max_csi, 4),
                "features_analyzed": len(numeric_features),
                "status": csi_status,
                "message": csi_message
            }
            
        except Exception as e:
            logger.error(f"CSI analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _analyze_target_stability(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        target_column: str
    ) -> Dict[str, Any]:
        """Analyze target rate stability across datasets"""
        try:
            train_rate = float(train_data[target_column].mean())
            test_rate = float(test_data[target_column].mean())
            oot_rate = float(oot_data[target_column].mean())
            
            # Calculate relative changes
            test_change = ((test_rate - train_rate) / train_rate * 100) if train_rate > 0 else 0
            oot_change = ((oot_rate - train_rate) / train_rate * 100) if train_rate > 0 else 0
            
            max_change = max(abs(test_change), abs(oot_change))
            
            if max_change < 10:
                status = "passed"
                message = "Target rate is stable"
            elif max_change < 25:
                status = "warning"
                message = "Moderate target rate shift"
            else:
                status = "failed"
                message = "Significant target rate shift"
            
            return {
                "train_rate": round(train_rate, 4),
                "test_rate": round(test_rate, 4),
                "oot_rate": round(oot_rate, 4),
                "test_change_pct": round(test_change, 2),
                "oot_change_pct": round(oot_change, 2),
                "max_change_pct": round(max_change, 2),
                "status": status,
                "message": message
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _analyze_score_stability(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        score_column: str
    ) -> Dict[str, Any]:
        """Analyze score distribution stability"""
        try:
            train_mean = float(train_data[score_column].mean())
            test_mean = float(test_data[score_column].mean())
            oot_mean = float(oot_data[score_column].mean())
            
            train_std = float(train_data[score_column].std())
            test_std = float(test_data[score_column].std())
            oot_std = float(oot_data[score_column].std())
            
            # Calculate coefficient of variation changes
            test_cv_change = abs((test_std / test_mean) - (train_std / train_mean)) if train_mean > 0 and test_mean > 0 else 0
            oot_cv_change = abs((oot_std / oot_mean) - (train_std / train_mean)) if train_mean > 0 and oot_mean > 0 else 0
            
            max_cv_change = max(test_cv_change, oot_cv_change)
            
            if max_cv_change < 0.1:
                status = "passed"
                message = "Score distribution is stable"
            elif max_cv_change < 0.25:
                status = "warning"
                message = "Moderate score distribution shift"
            else:
                status = "failed"
                message = "Significant score distribution shift"
            
            return {
                "train_mean": round(train_mean, 4),
                "test_mean": round(test_mean, 4),
                "oot_mean": round(oot_mean, 4),
                "train_std": round(train_std, 4),
                "test_std": round(test_std, 4),
                "oot_std": round(oot_std, 4),
                "max_cv_change": round(max_cv_change, 4),
                "status": status,
                "message": message
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _analyze_feature_stability(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """Analyze stability of individual features"""
        try:
            numeric_features = train_data.select_dtypes(include=[np.number]).columns.tolist()
            exclude_cols = ['default', 'default_next_12m', 'recovered', 'score', 'probability', 'target']
            numeric_features = [f for f in numeric_features if f not in exclude_cols]
            
            if len(numeric_features) == 0:
                return {
                    "status": "warning",
                    "message": "No features to analyze"
                }
            
            feature_stats = []
            for feature in numeric_features[:10]:  # Limit to top 10 features
                try:
                    train_mean = float(train_data[feature].mean())
                    test_mean = float(test_data[feature].mean())
                    oot_mean = float(oot_data[feature].mean())
                    
                    test_change = ((test_mean - train_mean) / train_mean * 100) if train_mean != 0 else 0
                    oot_change = ((oot_mean - train_mean) / train_mean * 100) if train_mean != 0 else 0
                    
                    feature_stats.append({
                        "feature": feature,
                        "train_mean": round(train_mean, 4),
                        "test_mean": round(test_mean, 4),
                        "oot_mean": round(oot_mean, 4),
                        "test_change_pct": round(test_change, 2),
                        "oot_change_pct": round(oot_change, 2)
                    })
                except:
                    continue
            
            return {
                "features_analyzed": len(feature_stats),
                "feature_statistics": feature_stats,
                "status": "passed"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _determine_overall_stability(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Determine overall stability status"""
        statuses = []
        
        if "psi_analysis" in results:
            statuses.append(results["psi_analysis"].get("status", "unknown"))
        
        if "csi_analysis" in results:
            statuses.append(results["csi_analysis"].get("status", "unknown"))
        
        if "target_stability" in results:
            statuses.append(results["target_stability"].get("status", "unknown"))
        
        if "score_stability" in results:
            statuses.append(results["score_stability"].get("status", "unknown"))
        
        if "failed" in statuses or "error" in statuses:
            overall_status = "failed"
            message = "Significant stability issues detected"
        elif "warning" in statuses:
            overall_status = "warning"
            message = "Moderate stability concerns detected"
        elif "passed" in statuses:
            overall_status = "passed"
            message = "Model is stable across all datasets"
        else:
            overall_status = "unknown"
            message = "Unable to determine stability"
        
        return {
            "status": overall_status,
            "message": message,
            "checks_performed": len(statuses),
            "passed_checks": statuses.count("passed"),
            "warning_checks": statuses.count("warning"),
            "failed_checks": statuses.count("failed")
        }
    
    def _detect_target_column(self, data: pd.DataFrame) -> str:
        """Detect the target column in the dataset"""
        for col in ['default', 'default_next_12m', 'recovered', 'target', 'label', 'y']:
            if col in data.columns:
                return col
        return "unknown"
    
    def _detect_score_column(self, data: pd.DataFrame) -> str:
        """Detect the score column in the dataset"""
        for col in ['score', 'probability', 'pred_proba', 'prediction', 'y_pred']:
            if col in data.columns:
                return col
        return "unknown"


# Made with Bob - Enhanced Stability Validator
