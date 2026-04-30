"""
Unit Tests for Statistical Tests Module
Tests KS, Gini, PSI, and CSI calculations
"""

import pytest
import numpy as np
import pandas as pd
from statistical_tests import StatisticalTestsCalculator


class TestStatisticalTests:
    """Test suite for statistical tests"""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance"""
        return StatisticalTestsCalculator()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        np.random.seed(42)
        n = 1000
        
        # Create binary target
        y_true = np.random.binomial(1, 0.3, n)
        
        # Create scores with some discrimination power
        y_pred_proba = np.random.beta(2, 5, n)
        y_pred_proba[y_true == 1] += 0.2  # Shift bad customers higher
        y_pred_proba = np.clip(y_pred_proba, 0, 1)
        
        return y_true, y_pred_proba
    
    def test_ks_statistic(self, calculator, sample_data):
        """Test KS statistic calculation"""
        y_true, y_pred_proba = sample_data
        
        result = calculator.calculate_ks_statistic(y_true, y_pred_proba, "test")
        
        assert "ks_statistic" in result
        assert "optimal_cutoff" in result
        assert "status" in result
        assert 0 <= result["ks_statistic"] <= 1
        assert result["test_name"] == "Kolmogorov-Smirnov Test"
        print(f"✓ KS Test: {result['ks_statistic']:.4f} - {result['interpretation']}")
    
    def test_gini_coefficient(self, calculator, sample_data):
        """Test Gini coefficient calculation"""
        y_true, y_pred_proba = sample_data
        
        result = calculator.calculate_gini_coefficient(y_true, y_pred_proba, "test")
        
        assert "gini" in result
        assert "auc" in result
        assert "status" in result
        assert -1 <= result["gini"] <= 1
        assert 0 <= result["auc"] <= 1
        assert result["test_name"] == "Gini Coefficient"
        print(f"✓ Gini Test: {result['gini']:.4f} (AUC: {result['auc']:.4f}) - {result['interpretation']}")
    
    def test_gini_comparison(self, calculator, sample_data):
        """Test Gini comparison across datasets"""
        y_true, y_pred_proba = sample_data
        
        train_result = calculator.calculate_gini_coefficient(y_true, y_pred_proba, "train")
        test_result = calculator.calculate_gini_coefficient(y_true, y_pred_proba, "test")
        
        comparison = calculator.compare_gini_across_datasets(train_result, test_result)
        
        assert "train_gini" in comparison
        assert "test_gini" in comparison
        assert "degradation_pct" in comparison
        assert "status" in comparison
        print(f"✓ Gini Comparison: Degradation {comparison['degradation_pct']:.2f}% - {comparison['interpretation']}")
    
    def test_psi_calculation(self, calculator):
        """Test PSI calculation"""
        np.random.seed(42)
        
        # Create two similar distributions
        expected = np.random.normal(100, 15, 1000)
        actual = np.random.normal(102, 16, 1000)  # Slight shift
        
        result = calculator.calculate_psi(expected, actual, buckets=10, feature_name="test_feature")
        
        assert "psi" in result
        assert "bucket_details" in result
        assert "status" in result
        assert result["test_name"] == "Population Stability Index"
        print(f"✓ PSI Test: {result['psi']:.4f} - {result['interpretation']}")
    
    def test_csi_calculation(self, calculator):
        """Test CSI calculation"""
        np.random.seed(42)
        
        # Create sample dataframes
        expected_df = pd.DataFrame({
            'feature1': np.random.normal(100, 15, 1000),
            'feature2': np.random.normal(50, 10, 1000),
            'feature3': np.random.normal(200, 30, 1000)
        })
        
        actual_df = pd.DataFrame({
            'feature1': np.random.normal(102, 16, 1000),
            'feature2': np.random.normal(51, 11, 1000),
            'feature3': np.random.normal(205, 32, 1000)
        })
        
        result = calculator.calculate_csi(expected_df, actual_df, features=['feature1', 'feature2', 'feature3'])
        
        assert "average_csi" in result
        assert "features_analyzed" in result
        assert "overall_status" in result
        assert result["test_name"] == "Characteristic Stability Index"
        print(f"✓ CSI Test: Avg CSI {result['average_csi']:.4f} - {result['overall_interpretation']}")
    
    def test_run_all_tests(self, calculator):
        """Test running all tests together"""
        np.random.seed(42)
        n = 1000
        
        # Create sample datasets
        train_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.3, n),
            'score': np.random.beta(2, 5, n),
            'feature1': np.random.normal(100, 15, n),
            'feature2': np.random.normal(50, 10, n)
        })
        
        test_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.3, n),
            'score': np.random.beta(2, 5, n),
            'feature1': np.random.normal(102, 16, n),
            'feature2': np.random.normal(51, 11, n)
        })
        
        results = calculator.run_all_tests(
            train_data,
            test_data,
            target_column='default',
            score_column='score',
            features=['feature1', 'feature2']
        )
        
        assert "ks_tests" in results
        assert "gini_tests" in results
        assert "psi_tests" in results
        assert "csi_test" in results
        assert "summary" in results
        
        print(f"✓ All Tests: {results['summary']['tests_completed']} tests completed")
        print(f"  Overall Status: {results['summary']['overall_status']}")


def run_manual_tests():
    """Run tests manually without pytest"""
    print("\n" + "="*60)
    print("Running Statistical Tests Module - Manual Tests")
    print("="*60 + "\n")
    
    calculator = StatisticalTestsCalculator()
    np.random.seed(42)
    
    # Test 1: KS Statistic
    print("Test 1: KS Statistic")
    print("-" * 40)
    n = 1000
    y_true = np.random.binomial(1, 0.3, n)
    y_pred_proba = np.random.beta(2, 5, n)
    y_pred_proba[y_true == 1] += 0.2
    y_pred_proba = np.clip(y_pred_proba, 0, 1)
    
    ks_result = calculator.calculate_ks_statistic(y_true, y_pred_proba, "test")
    print(f"KS Statistic: {ks_result['ks_statistic']:.4f}")
    print(f"Optimal Cutoff: {ks_result['optimal_cutoff']:.4f}")
    print(f"Status: {ks_result['status']}")
    print(f"Interpretation: {ks_result['interpretation']}\n")
    
    # Test 2: Gini Coefficient
    print("Test 2: Gini Coefficient")
    print("-" * 40)
    gini_result = calculator.calculate_gini_coefficient(y_true, y_pred_proba, "test")
    print(f"Gini: {gini_result['gini']:.4f}")
    print(f"AUC: {gini_result['auc']:.4f}")
    print(f"Status: {gini_result['status']}")
    print(f"Interpretation: {gini_result['interpretation']}\n")
    
    # Test 3: PSI
    print("Test 3: Population Stability Index")
    print("-" * 40)
    expected = np.random.normal(100, 15, 1000)
    actual = np.random.normal(102, 16, 1000)
    psi_result = calculator.calculate_psi(expected, actual, feature_name="test_feature")
    print(f"PSI: {psi_result['psi']:.4f}")
    print(f"Status: {psi_result['status']}")
    print(f"Interpretation: {psi_result['interpretation']}\n")
    
    # Test 4: CSI
    print("Test 4: Characteristic Stability Index")
    print("-" * 40)
    expected_df = pd.DataFrame({
        'feature1': np.random.normal(100, 15, 1000),
        'feature2': np.random.normal(50, 10, 1000)
    })
    actual_df = pd.DataFrame({
        'feature1': np.random.normal(102, 16, 1000),
        'feature2': np.random.normal(51, 11, 1000)
    })
    csi_result = calculator.calculate_csi(expected_df, actual_df)
    print(f"Average CSI: {csi_result['average_csi']:.4f}")
    print(f"Features Analyzed: {csi_result['features_analyzed']}")
    print(f"Status: {csi_result['overall_status']}")
    print(f"Interpretation: {csi_result['overall_interpretation']}\n")
    
    print("="*60)
    print("✓ All manual tests completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run manual tests
    run_manual_tests()

# Made with Bob
