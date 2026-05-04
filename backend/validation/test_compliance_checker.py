"""
Test Suite for SR 11-7 Compliance Checker
Tests comprehensive regulatory compliance validation
"""

import pytest
from compliance_checker import ComplianceChecker


class TestComplianceChecker:
    """Test suite for ComplianceChecker class."""
    
    @pytest.fixture
    def checker(self):
        """Create a ComplianceChecker instance."""
        return ComplianceChecker()
    
    @pytest.fixture
    def fully_compliant_results(self):
        """Create fully compliant validation results."""
        return {
            "model_info": {
                "model_type": "Application Scorecard",
                "model_name": "Credit Risk Model v2.0"
            },
            "data_quality": {
                "completeness_score": 0.95,
                "quality_score": 0.92,
                "sample_size_adequate": True,
                "missing_values": 0.05
            },
            "conceptual_soundness": {
                "overall_status": "passed",
                "theory_sound": True,
                "methodology_appropriate": True
            },
            "performance": {
                "gini": 0.45,
                "ks_statistic": 0.35,
                "accuracy": 0.82,
                "auc_roc": 0.78,
                "precision": 0.75,
                "recall": 0.80
            },
            "stability": {
                "overall_stability": "passed",
                "psi_analysis": {
                    "target_psi": 0.08,
                    "score_psi": 0.06
                },
                "csi_analysis": {
                    "feature_1": 0.05,
                    "feature_2": 0.07
                }
            },
            "assumptions": {
                "overall_status": "passed",
                "assumptions_tested": True,
                "sensitivity_analysis": {
                    "performed": True
                }
            },
            "implementation": {
                "production_ready": True,
                "rollback_plan_exists": True,
                "implementation_verified": True
            },
            "monitoring_plan": {
                "defined": True,
                "frequency": "monthly"
            },
            "revalidation_schedule": {
                "next_validation": "2026-12-31"
            },
            "recommendations": [
                "Model approved for production use"
            ],
            "timestamp": "2026-05-04T09:00:00Z"
        }
    
    @pytest.fixture
    def partially_compliant_results(self):
        """Create partially compliant validation results."""
        return {
            "model_info": {
                "model_type": "Behavioral Scorecard"
            },
            "data_quality": {
                "completeness_score": 0.70,
                "quality_score": 0.65,
                "sample_size_adequate": False
            },
            "performance": {
                "gini": 0.25,
                "ks_statistic": 0.15
            },
            "stability": {
                "overall_stability": "warning"
            },
            "recommendations": [
                "Improve data quality before production"
            ]
        }
    
    @pytest.fixture
    def non_compliant_results(self):
        """Create non-compliant validation results."""
        return {
            "model_info": {
                "model_type": "Collections Scorecard"
            },
            "data_quality": {
                "completeness_score": 0.50,
                "quality_score": 0.45,
                "sample_size_adequate": False
            }
        }
    
    def test_checker_initialization(self, checker):
        """Test ComplianceChecker initialization."""
        assert checker is not None
        assert checker.total_weight == 100
        assert len(checker.SR_11_7_REQUIREMENTS) == 9
    
    def test_fully_compliant_validation(self, checker, fully_compliant_results):
        """Test validation with fully compliant results."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        # Check overall compliance
        assert result["sr_11_7_compliant"] is True
        assert result["compliance_score"] >= 90.0
        assert result["overall_status"] == "Fully Compliant"
        
        # Check structure
        assert "detailed_checks" in result
        assert "gaps_identified" in result
        assert "recommendations" in result
        assert "summary" in result
        
        # Check summary
        assert result["summary"]["ready_for_production"] is True
        
        print("\n✅ Fully Compliant Validation:")
        print(f"   Score: {result['compliance_score']}%")
        print(f"   Status: {result['overall_status']}")
        print(f"   Requirements Passed: {result['summary']['requirements_passed']}")
    
    def test_partially_compliant_validation(self, checker, partially_compliant_results):
        """Test validation with partially compliant results."""
        result = checker.check_sr_11_7_compliance(partially_compliant_results)
        
        # Check overall compliance
        assert result["sr_11_7_compliant"] is False
        # Partially compliant data has limited sections, so score will be lower
        assert result["compliance_score"] < 90.0
        assert result["overall_status"] in ["Partially Compliant", "Substantially Compliant", "Non-Compliant"]
        
        # Check gaps identified
        assert len(result["gaps_identified"]) > 0
        assert len(result["recommendations"]) > 0
        
        print("\n⚠️  Partially Compliant Validation:")
        print(f"   Score: {result['compliance_score']}%")
        print(f"   Status: {result['overall_status']}")
        print(f"   Gaps: {len(result['gaps_identified'])}")
        print(f"   Recommendations: {len(result['recommendations'])}")
    
    def test_non_compliant_validation(self, checker, non_compliant_results):
        """Test validation with non-compliant results."""
        result = checker.check_sr_11_7_compliance(non_compliant_results)
        
        # Check overall compliance
        assert result["sr_11_7_compliant"] is False
        assert result["compliance_score"] < 75.0
        
        # Check gaps identified
        assert len(result["gaps_identified"]) > 5
        assert len(result["recommendations"]) > 5
        
        # Check summary
        assert result["summary"]["ready_for_production"] is False
        
        print("\n❌ Non-Compliant Validation:")
        print(f"   Score: {result['compliance_score']}%")
        print(f"   Status: {result['overall_status']}")
        print(f"   Gaps: {len(result['gaps_identified'])}")
    
    def test_model_purpose_check(self, checker, fully_compliant_results):
        """Test model purpose requirement check."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        model_purpose = result["detailed_checks"]["model_purpose"]
        assert model_purpose["status"] == "Passed"
        assert model_purpose["checks_passed"] == model_purpose["total_checks"]
        assert model_purpose["weight"] == 8
        
        print("\n✅ Model Purpose Check:")
        print(f"   Status: {model_purpose['status']}")
        print(f"   Checks: {model_purpose['checks_passed']}/{model_purpose['total_checks']}")
    
    def test_conceptual_soundness_check(self, checker, fully_compliant_results):
        """Test conceptual soundness requirement check."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        conceptual = result["detailed_checks"]["conceptual_soundness"]
        assert conceptual["status"] == "Passed"
        assert conceptual["weight"] == 15
        
        print("\n✅ Conceptual Soundness Check:")
        print(f"   Status: {conceptual['status']}")
        print(f"   Score: {conceptual['score']}")
    
    def test_data_quality_check(self, checker, fully_compliant_results):
        """Test data quality requirement check."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        data_quality = result["detailed_checks"]["data_quality"]
        assert data_quality["status"] == "Passed"
        assert data_quality["weight"] == 12
        
        print("\n✅ Data Quality Check:")
        print(f"   Status: {data_quality['status']}")
        print(f"   Checks: {data_quality['checks_passed']}/{data_quality['total_checks']}")
    
    def test_performance_validation_check(self, checker, fully_compliant_results):
        """Test performance validation requirement check."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        performance = result["detailed_checks"]["performance_validation"]
        assert performance["status"] == "Passed"
        assert performance["weight"] == 15
        
        print("\n✅ Performance Validation Check:")
        print(f"   Status: {performance['status']}")
        print(f"   Score: {performance['score']}")
    
    def test_stability_analysis_check(self, checker, fully_compliant_results):
        """Test stability analysis requirement check."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        stability = result["detailed_checks"]["stability_analysis"]
        assert stability["status"] == "Passed"
        assert stability["weight"] == 12
        
        print("\n✅ Stability Analysis Check:")
        print(f"   Status: {stability['status']}")
        print(f"   Checks: {stability['checks_passed']}/{stability['total_checks']}")
    
    def test_compliance_score_calculation(self, checker, fully_compliant_results):
        """Test compliance score calculation."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        # Score should be between 0 and 100
        assert 0 <= result["compliance_score"] <= 100
        
        # Check that score matches sum of requirement scores
        total_score = sum(
            req["score"] for req in result["detailed_checks"].values()
        )
        assert abs(result["compliance_score"] - total_score) < 0.01
        
        print("\n📊 Compliance Score Calculation:")
        print(f"   Total Score: {result['compliance_score']}%")
        print(f"   Calculated: {total_score}%")
    
    def test_gap_identification(self, checker, partially_compliant_results):
        """Test gap identification."""
        result = checker.check_sr_11_7_compliance(partially_compliant_results)
        
        gaps = result["gaps_identified"]
        assert len(gaps) > 0
        
        # Check gap structure
        for gap in gaps:
            assert "requirement" in gap
            assert "description" in gap
            assert "status" in gap
            assert "weight" in gap
            assert "failed_checks" in gap
        
        # Gaps should be sorted by weight (descending)
        weights = [gap["weight"] for gap in gaps]
        assert weights == sorted(weights, reverse=True)
        
        print("\n🔍 Gap Identification:")
        print(f"   Total Gaps: {len(gaps)}")
        for gap in gaps[:3]:  # Show top 3
            print(f"   - {gap['requirement']}: {gap['status']} (weight: {gap['weight']})")
    
    def test_recommendations_generation(self, checker, partially_compliant_results):
        """Test recommendations generation."""
        result = checker.check_sr_11_7_compliance(partially_compliant_results)
        
        recommendations = result["recommendations"]
        assert len(recommendations) > 0
        
        # Each recommendation should be a string
        for rec in recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 0
        
        print("\n💡 Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")
    
    def test_compliance_status_determination(self, checker):
        """Test compliance status determination logic."""
        # Test different score ranges
        test_cases = [
            (95.0, "Fully Compliant"),
            (85.0, "Substantially Compliant"),
            (70.0, "Partially Compliant"),
            (50.0, "Non-Compliant")
        ]
        
        for score, expected_status in test_cases:
            status = checker._determine_compliance_status(score)
            assert status == expected_status
            print(f"   Score {score}% → {status}")
    
    def test_empty_results(self, checker):
        """Test compliance check with empty results."""
        result = checker.check_sr_11_7_compliance({})
        
        # Should still return valid structure
        assert "compliance_score" in result
        assert "overall_status" in result
        assert result["sr_11_7_compliant"] is False
        
        # Score should be very low
        assert result["compliance_score"] < 30.0
        
        print("\n⚠️  Empty Results:")
        print(f"   Score: {result['compliance_score']}%")
        print(f"   Status: {result['overall_status']}")
    
    def test_summary_generation(self, checker, fully_compliant_results):
        """Test summary generation."""
        result = checker.check_sr_11_7_compliance(fully_compliant_results)
        
        summary = result["summary"]
        assert "score" in summary
        assert "status" in summary
        assert "requirements_passed" in summary
        assert "total_checks_passed" in summary
        assert "total_checks" in summary
        assert "ready_for_production" in summary
        
        print("\n📋 Summary:")
        print(f"   Score: {summary['score']}%")
        print(f"   Status: {summary['status']}")
        print(f"   Requirements: {summary['requirements_passed']}")
        print(f"   Checks: {summary['total_checks_passed']}/{summary['total_checks']}")
        print(f"   Production Ready: {summary['ready_for_production']}")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])

# Made with Bob
