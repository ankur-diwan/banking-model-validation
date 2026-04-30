"""
Test suite for Enhanced Performance Validator
Tests confusion matrix, classification metrics, AUC-ROC, and statistical tests integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import pandas as pd
import numpy as np

# Import with absolute path handling
try:
    from performance_validator import PerformanceValidator
except ImportError:
    # Try relative import for package context
    from .performance_validator import PerformanceValidator


class TestPerformanceValidator:
    """Test suite for PerformanceValidator"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance"""
        return PerformanceValidator()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample datasets for testing"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic data with good separation
        train_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.3, n_samples),
            'score': np.random.beta(2, 5, n_samples),
            'feature1': np.random.normal(0, 1, n_samples),
            'feature2': np.random.normal(0, 1, n_samples)
        })
        
        # Test data with similar distribution
        test_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.32, n_samples),
            'score': np.random.beta(2, 5, n_samples),
            'feature1': np.random.normal(0, 1, n_samples),
            'feature2': np.random.normal(0, 1, n_samples)
        })
        
        # OOT data with slight drift
        oot_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.35, n_samples),
            'score': np.random.beta(2.2, 5, n_samples),
            'feature1': np.random.normal(0.1, 1, n_samples),
            'feature2': np.random.normal(0, 1.1, n_samples)
        })
        
        return train_data, test_data, oot_data
    
    @pytest.fixture
    def model_config(self):
        """Sample model configuration"""
        return {
            'model_name': 'Test Application Scorecard',
            'model_type': 'logistic_regression',
            'scorecard_type': 'application'
        }
    
    def test_validator_initialization(self, validator):
        """Test validator initializes correctly"""
        assert validator is not None
        assert validator.stats_calculator is not None
        print("✓ Validator initialized successfully")
    
    def test_detect_target_column(self, validator):
        """Test target column detection"""
        df1 = pd.DataFrame({'default': [0, 1], 'score': [0.3, 0.7]})
        assert validator._detect_target_column(df1) == 'default'
        
        df2 = pd.DataFrame({'target': [0, 1], 'score': [0.3, 0.7]})
        assert validator._detect_target_column(df2) == 'target'
        
        df3 = pd.DataFrame({'unknown_col': [0, 1], 'score': [0.3, 0.7]})
        assert validator._detect_target_column(df3) == 'unknown'
        
        print("✓ Target column detection working correctly")
    
    def test_detect_score_column(self, validator):
        """Test score column detection"""
        df1 = pd.DataFrame({'default': [0, 1], 'score': [0.3, 0.7]})
        assert validator._detect_score_column(df1) == 'score'
        
        df2 = pd.DataFrame({'default': [0, 1], 'probability': [0.3, 0.7]})
        assert validator._detect_score_column(df2) == 'probability'
        
        df3 = pd.DataFrame({'default': [0, 1], 'unknown_col': [0.3, 0.7]})
        assert validator._detect_score_column(df3) == 'unknown'
        
        print("✓ Score column detection working correctly")
    
    def test_calculate_dataset_metrics(self, validator, sample_data):
        """Test comprehensive metrics calculation for a single dataset"""
        train_data, _, _ = sample_data
        
        metrics = validator._calculate_dataset_metrics(
            train_data, 'default', 'score', 'train'
        )
        
        # Check basic fields
        assert metrics['dataset_name'] == 'train'
        assert metrics['row_count'] == 1000
        assert metrics['column_count'] == 4
        assert 'target_rate' in metrics
        assert 'score_mean' in metrics
        assert 'score_std' in metrics
        
        # Check confusion matrix
        assert 'confusion_matrix' in metrics
        cm = metrics['confusion_matrix']
        assert 'true_negative' in cm
        assert 'false_positive' in cm
        assert 'false_negative' in cm
        assert 'true_positive' in cm
        assert cm['true_negative'] + cm['false_positive'] + cm['false_negative'] + cm['true_positive'] == 1000
        
        # Check classification metrics
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['precision'] <= 1
        assert 0 <= metrics['recall'] <= 1
        assert 0 <= metrics['f1_score'] <= 1
        
        # Check AUC-ROC
        assert 'auc_roc' in metrics
        if metrics['auc_roc'] is not None:
            assert 0 <= metrics['auc_roc'] <= 1
        
        # Check statistical tests
        assert 'ks_test' in metrics
        assert 'gini_test' in metrics
        assert metrics['ks_test']['status'] in ['passed', 'warning', 'failed']
        assert metrics['gini_test']['status'] in ['passed', 'warning', 'failed']
        
        # Check overall status
        assert 'status' in metrics
        assert metrics['status'] in ['passed', 'warning', 'failed', 'error']
        
        print("✓ Dataset metrics calculation working correctly")
        print(f"  - Accuracy: {metrics['accuracy']}")
        print(f"  - AUC-ROC: {metrics.get('auc_roc', 'N/A')}")
        print(f"  - KS Statistic: {metrics['ks_test'].get('ks_statistic', 'N/A')}")
        print(f"  - Gini: {metrics['gini_test'].get('gini', 'N/A')}")
    
    def test_compare_performance(self, validator, sample_data):
        """Test performance comparison across datasets"""
        train_data, test_data, oot_data = sample_data
        
        train_metrics = validator._calculate_dataset_metrics(
            train_data, 'default', 'score', 'train'
        )
        test_metrics = validator._calculate_dataset_metrics(
            test_data, 'default', 'score', 'test'
        )
        oot_metrics = validator._calculate_dataset_metrics(
            oot_data, 'default', 'score', 'out_of_time'
        )
        
        comparison = validator._compare_performance(
            train_metrics, test_metrics, oot_metrics
        )
        
        # Check comparison structure
        assert 'datasets_compared' in comparison
        assert 'train' in comparison['datasets_compared']
        assert 'test' in comparison['datasets_compared']
        assert 'out_of_time' in comparison['datasets_compared']
        
        # Check degradation metrics
        assert 'accuracy_degradation_pct' in comparison
        assert 'precision_degradation_pct' in comparison
        assert 'recall_degradation_pct' in comparison
        assert 'f1_score_degradation_pct' in comparison
        
        # Check OOT degradation
        assert 'accuracy_oot_degradation_pct' in comparison
        
        # Check Gini comparison
        assert 'gini_comparison' in comparison
        
        # Check overall assessment
        assert 'overall_assessment' in comparison
        assert 'status' in comparison
        assert comparison['status'] in ['passed', 'warning', 'failed', 'error']
        
        print("✓ Performance comparison working correctly")
        print(f"  - Overall Status: {comparison['status']}")
        print(f"  - Assessment: {comparison['overall_assessment']}")
        print(f"  - Accuracy Degradation: {comparison.get('accuracy_degradation_pct', 0)}%")
    
    def test_validate_performance_complete(self, validator, sample_data, model_config):
        """Test complete performance validation workflow"""
        train_data, test_data, oot_data = sample_data
        
        results = validator.validate_performance(
            model_config, train_data, test_data, oot_data
        )
        
        # Check top-level structure
        assert 'status' in results
        assert results['status'] in ['passed', 'warning', 'failed', 'error']
        assert 'target_column' in results
        assert 'score_column' in results
        assert 'model_type' in results
        assert 'scorecard_type' in results
        
        # Check dataset results
        assert 'train' in results
        assert 'test' in results
        assert 'out_of_time' in results
        
        # Check comparison
        assert 'comparison' in results
        
        print("✓ Complete performance validation working correctly")
        print(f"  - Overall Status: {results['status']}")
        print(f"  - Model Type: {results['model_type']}")
        print(f"  - Scorecard Type: {results['scorecard_type']}")
        print(f"  - Train Status: {results['train']['status']}")
        print(f"  - Test Status: {results['test']['status']}")
        print(f"  - OOT Status: {results['out_of_time']['status']}")
    
    def test_empty_dataset_handling(self, validator, model_config):
        """Test handling of empty datasets"""
        empty_df = pd.DataFrame()
        train_data = pd.DataFrame({'default': [0, 1], 'score': [0.3, 0.7]})
        
        results = validator.validate_performance(
            model_config, train_data, empty_df, empty_df
        )
        
        assert results['test']['status'] == 'error'
        assert 'error' in results['test']
        
        print("✓ Empty dataset handling working correctly")
    
    def test_missing_columns_handling(self, validator, model_config):
        """Test handling of missing target/score columns"""
        bad_data = pd.DataFrame({
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6]
        })
        
        results = validator.validate_performance(
            model_config, bad_data, bad_data, bad_data
        )
        
        assert results['status'] == 'error'
        assert 'error' in results
        
        print("✓ Missing columns handling working correctly")
    
    def test_performance_with_perfect_model(self, validator, model_config):
        """Test with a perfect model (100% accuracy)"""
        perfect_data = pd.DataFrame({
            'default': [0, 0, 1, 1, 0, 1],
            'score': [0.1, 0.2, 0.9, 0.8, 0.3, 0.95]
        })
        
        metrics = validator._calculate_dataset_metrics(
            perfect_data, 'default', 'score', 'perfect'
        )
        
        assert metrics['accuracy'] == 1.0
        assert metrics['precision'] == 1.0
        assert metrics['recall'] == 1.0
        assert metrics['f1_score'] == 1.0
        
        print("✓ Perfect model handling working correctly")
    
    def test_performance_with_poor_model(self, validator, model_config):
        """Test with a poor model (random predictions)"""
        np.random.seed(42)
        poor_data = pd.DataFrame({
            'default': np.random.binomial(1, 0.5, 100),
            'score': np.random.uniform(0, 1, 100)
        })
        
        metrics = validator._calculate_dataset_metrics(
            poor_data, 'default', 'score', 'poor'
        )
        
        # Poor model should have low metrics
        assert metrics['status'] in ['warning', 'failed']
        
        print("✓ Poor model detection working correctly")
        print(f"  - Status: {metrics['status']}")
        print(f"  - Accuracy: {metrics['accuracy']}")


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*70)
    print("ENHANCED PERFORMANCE VALIDATOR TEST SUITE")
    print("="*70 + "\n")
    
    validator = PerformanceValidator()
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    train_data = pd.DataFrame({
        'default': np.random.binomial(1, 0.3, n_samples),
        'score': np.random.beta(2, 5, n_samples),
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples)
    })
    
    test_data = pd.DataFrame({
        'default': np.random.binomial(1, 0.32, n_samples),
        'score': np.random.beta(2, 5, n_samples),
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples)
    })
    
    oot_data = pd.DataFrame({
        'default': np.random.binomial(1, 0.35, n_samples),
        'score': np.random.beta(2.2, 5, n_samples),
        'feature1': np.random.normal(0.1, 1, n_samples),
        'feature2': np.random.normal(0, 1.1, n_samples)
    })
    
    model_config = {
        'model_name': 'Test Application Scorecard',
        'model_type': 'logistic_regression',
        'scorecard_type': 'application'
    }
    
    # Run tests
    test_instance = TestPerformanceValidator()
    
    try:
        print("Test 1: Validator Initialization")
        test_instance.test_validator_initialization(validator)
        print()
        
        print("Test 2: Target Column Detection")
        test_instance.test_detect_target_column(validator)
        print()
        
        print("Test 3: Score Column Detection")
        test_instance.test_detect_score_column(validator)
        print()
        
        print("Test 4: Dataset Metrics Calculation")
        test_instance.test_calculate_dataset_metrics(validator, (train_data, test_data, oot_data))
        print()
        
        print("Test 5: Performance Comparison")
        test_instance.test_compare_performance(validator, (train_data, test_data, oot_data))
        print()
        
        print("Test 6: Complete Validation Workflow")
        test_instance.test_validate_performance_complete(validator, (train_data, test_data, oot_data), model_config)
        print()
        
        print("Test 7: Empty Dataset Handling")
        test_instance.test_empty_dataset_handling(validator, model_config)
        print()
        
        print("Test 8: Missing Columns Handling")
        test_instance.test_missing_columns_handling(validator, model_config)
        print()
        
        print("Test 9: Perfect Model Handling")
        test_instance.test_performance_with_perfect_model(validator, model_config)
        print()
        
        print("Test 10: Poor Model Detection")
        test_instance.test_performance_with_poor_model(validator, model_config)
        print()
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED! ✓")
        print("="*70)
        print("\nEnhanced Performance Validator is ready for integration!")
        print("Features validated:")
        print("  ✓ Confusion Matrix calculation")
        print("  ✓ Classification metrics (Accuracy, Precision, Recall, F1)")
        print("  ✓ AUC-ROC calculation")
        print("  ✓ KS and Gini integration from statistical_tests")
        print("  ✓ Performance comparison across datasets")
        print("  ✓ Degradation detection")
        print("  ✓ Error handling for edge cases")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

# Made with Bob
