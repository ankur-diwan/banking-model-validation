"""
Test suite for Model-Specific Validator
Tests validation logic for all scorecard types
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np

try:
    from model_specific_validator import ModelSpecificValidator
except ImportError:
    from .model_specific_validator import ModelSpecificValidator


class TestModelSpecificValidator:
    """Test suite for ModelSpecificValidator"""
    
    def create_sample_data(self, scorecard_type='application'):
        """Create sample datasets for testing"""
        np.random.seed(42)
        n_samples = 1000
        
        if scorecard_type == 'application':
            # Application scorecard data
            base_data = {
                'age': np.random.randint(18, 70, n_samples),
                'income': np.random.randint(20000, 150000, n_samples),
                'employment_status': np.random.choice(['employed', 'self-employed', 'unemployed'], n_samples),
                'default': np.random.binomial(1, 0.08, n_samples),  # 8% default rate
                'score': np.random.randint(300, 850, n_samples)
            }
        elif scorecard_type == 'behavioral':
            # Behavioral scorecard data
            base_data = {
                'months_on_book': np.random.randint(1, 120, n_samples),
                'utilization': np.random.uniform(0, 1, n_samples),
                'payment_history': np.random.randint(0, 24, n_samples),
                'default': np.random.binomial(1, 0.05, n_samples),  # 5% default rate
                'score': np.random.randint(0, 1000, n_samples)
            }
        elif scorecard_type in ['collections_early', 'collections_late']:
            # Collections scorecard data
            recovery_rate = 0.40 if scorecard_type == 'collections_early' else 0.15
            base_data = {
                'days_past_due': np.random.randint(30, 180, n_samples),
                'outstanding_balance': np.random.uniform(100, 50000, n_samples),
                'contact_attempts': np.random.randint(0, 20, n_samples),
                'previous_collections': np.random.binomial(1, 0.3, n_samples),
                'recovered': np.random.binomial(1, recovery_rate, n_samples),
                'score': np.random.uniform(0, 100, n_samples)
            }
        else:
            base_data = {
                'feature1': np.random.normal(0, 1, n_samples),
                'default': np.random.binomial(1, 0.1, n_samples),
                'score': np.random.uniform(0, 1, n_samples)
            }
        
        train_data = pd.DataFrame(base_data)
        test_data = pd.DataFrame(base_data)  # Simplified - same distribution
        oot_data = pd.DataFrame(base_data)   # Simplified - same distribution
        
        return train_data, test_data, oot_data
    
    def test_validator_initialization(self):
        """Test validator initializes correctly"""
        validator = ModelSpecificValidator()
        assert validator is not None
        assert len(validator.scorecard_validators) == 4
        assert 'application' in validator.scorecard_validators
        assert 'behavioral' in validator.scorecard_validators
        assert 'collections_early' in validator.scorecard_validators
        assert 'collections_late' in validator.scorecard_validators
        print("✓ Validator initialized successfully")
    
    def test_application_scorecard_validation(self):
        """Test Application Scorecard validation"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('application')
        
        model_config = {
            'model_name': 'Test Application Scorecard',
            'scorecard_type': 'application'
        }
        
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        # Check structure
        assert 'status' in results
        assert 'scorecard_type' in results
        assert results['scorecard_type'] == 'application'
        assert 'validation_type' in results
        assert 'use_case' in results
        assert 'checks' in results
        
        # Check all required checks are present
        assert 'data_quality' in results['checks']
        assert 'target_analysis' in results['checks']
        assert 'score_distribution' in results['checks']
        assert 'predictive_power' in results['checks']
        assert 'stability' in results['checks']
        assert 'regulatory' in results['checks']
        
        print("✓ Application Scorecard validation working correctly")
        print(f"  - Status: {results['status']}")
        print(f"  - Use Case: {results['use_case']}")
        print(f"  - Checks Performed: {len(results['checks'])}")
    
    def test_behavioral_scorecard_validation(self):
        """Test Behavioral Scorecard validation"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('behavioral')
        
        model_config = {
            'model_name': 'Test Behavioral Scorecard',
            'scorecard_type': 'behavioral'
        }
        
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        # Check structure
        assert results['scorecard_type'] == 'behavioral'
        assert 'behavioral_patterns' in results['checks']
        
        # Check behavioral-specific requirements
        assert results['checks']['predictive_power']['requirements']['min_gini'] == 0.35
        assert results['checks']['stability']['requirements']['max_psi'] == 0.20
        
        print("✓ Behavioral Scorecard validation working correctly")
        print(f"  - Status: {results['status']}")
        print(f"  - Min Gini Required: {results['checks']['predictive_power']['requirements']['min_gini']}")
    
    def test_collections_early_validation(self):
        """Test Early Stage Collections validation"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('collections_early')
        
        model_config = {
            'model_name': 'Test Collections Early',
            'scorecard_type': 'collections_early'
        }
        
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        # Check structure
        assert results['scorecard_type'] == 'collections_early'
        assert 'collections_metrics' in results['checks']
        
        # Check target is 'recovered' not 'default'
        assert results['checks']['target_analysis']['target_name'] == 'recovered'
        
        print("✓ Collections Early Stage validation working correctly")
        print(f"  - Status: {results['status']}")
        print(f"  - Use Case: {results['use_case']}")
    
    def test_collections_late_validation(self):
        """Test Late Stage Collections validation"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('collections_late')
        
        model_config = {
            'model_name': 'Test Collections Late',
            'scorecard_type': 'collections_late'
        }
        
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        # Check structure
        assert results['scorecard_type'] == 'collections_late'
        
        # Check more lenient requirements for late stage
        assert results['checks']['predictive_power']['requirements']['min_gini'] == 0.20
        assert results['checks']['stability']['requirements']['max_psi'] == 0.35
        
        print("✓ Collections Late Stage validation working correctly")
        print(f"  - Status: {results['status']}")
        print(f"  - Min Gini Required: {results['checks']['predictive_power']['requirements']['min_gini']}")
    
    def test_unknown_scorecard_type(self):
        """Test handling of unknown scorecard type"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data()
        
        model_config = {
            'model_name': 'Test Unknown',
            'scorecard_type': 'unknown_type'
        }
        
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        assert results['status'] == 'error'
        assert 'error' in results
        assert 'supported_types' in results
        
        print("✓ Unknown scorecard type handling working correctly")
    
    def test_data_quality_checks(self):
        """Test data quality checking"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('application')
        
        # Test with missing features
        incomplete_data = train_data.drop(columns=['age'])
        
        model_config = {'scorecard_type': 'application'}
        results = validator.validate(model_config, incomplete_data, test_data, oot_data)
        
        # Should detect missing features
        assert 'data_quality' in results['checks']
        train_quality = results['checks']['data_quality']['train']
        assert 'age' in train_quality['missing_features']
        
        print("✓ Data quality checks working correctly")
        print(f"  - Missing features detected: {train_quality['missing_features']}")
    
    def test_target_analysis(self):
        """Test target variable analysis"""
        validator = ModelSpecificValidator()
        train_data, test_data, oot_data = self.create_sample_data('application')
        
        model_config = {'scorecard_type': 'application'}
        results = validator.validate(model_config, train_data, test_data, oot_data)
        
        target_analysis = results['checks']['target_analysis']
        
        assert 'train_rate' in target_analysis
        assert 'test_rate' in target_analysis
        assert 'oot_rate' in target_analysis
        assert 'expected_range' in target_analysis
        
        print("✓ Target analysis working correctly")
        print(f"  - Train Rate: {target_analysis['train_rate']}")
        print(f"  - Expected Range: {target_analysis['expected_range']}")
    
    def test_all_scorecard_types(self):
        """Test all scorecard types in sequence"""
        validator = ModelSpecificValidator()
        
        scorecard_types = ['application', 'behavioral', 'collections_early', 'collections_late']
        
        for scorecard_type in scorecard_types:
            train_data, test_data, oot_data = self.create_sample_data(scorecard_type)
            model_config = {'scorecard_type': scorecard_type}
            
            results = validator.validate(model_config, train_data, test_data, oot_data)
            
            assert results['scorecard_type'] == scorecard_type
            assert 'status' in results
            assert 'checks' in results
        
        print(f"✓ All {len(scorecard_types)} scorecard types validated successfully")


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*70)
    print("MODEL-SPECIFIC VALIDATOR TEST SUITE")
    print("="*70 + "\n")
    
    test_instance = TestModelSpecificValidator()
    
    try:
        print("Test 1: Validator Initialization")
        test_instance.test_validator_initialization()
        print()
        
        print("Test 2: Application Scorecard Validation")
        test_instance.test_application_scorecard_validation()
        print()
        
        print("Test 3: Behavioral Scorecard Validation")
        test_instance.test_behavioral_scorecard_validation()
        print()
        
        print("Test 4: Collections Early Stage Validation")
        test_instance.test_collections_early_validation()
        print()
        
        print("Test 5: Collections Late Stage Validation")
        test_instance.test_collections_late_validation()
        print()
        
        print("Test 6: Unknown Scorecard Type Handling")
        test_instance.test_unknown_scorecard_type()
        print()
        
        print("Test 7: Data Quality Checks")
        test_instance.test_data_quality_checks()
        print()
        
        print("Test 8: Target Analysis")
        test_instance.test_target_analysis()
        print()
        
        print("Test 9: All Scorecard Types")
        test_instance.test_all_scorecard_types()
        print()
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED! ✓")
        print("="*70)
        print("\nModel-Specific Validator is ready for integration!")
        print("Scorecard types supported:")
        print("  ✓ Application Scorecards (Credit Origination)")
        print("  ✓ Behavioral Scorecards (Existing Customer Risk)")
        print("  ✓ Collections Early Stage (30-90 DPD)")
        print("  ✓ Collections Late Stage (90+ DPD)")
        print("\nValidation checks implemented:")
        print("  ✓ Data quality assessment")
        print("  ✓ Target variable analysis")
        print("  ✓ Score distribution checks")
        print("  ✓ Predictive power requirements")
        print("  ✓ Stability requirements")
        print("  ✓ Regulatory compliance checks")
        print("  ✓ Model-specific pattern analysis")
        
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
