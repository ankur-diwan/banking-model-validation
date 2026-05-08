#!/usr/bin/env python3
"""
Generate Test Data Sets for Model Validation
Set 1: Data that will pass validation (good model performance)
Set 2: Data that will fail validation (poor model performance)
"""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_successful_data(n_train=2000, n_test=1000, n_oot=600, seed=42):
    """
    Generate data with GOOD model performance that will PASS validation
    - High KS (0.40-0.50)
    - High Gini (0.60-0.70)
    - Low PSI (< 0.10)
    - Low CSI (< 0.10)
    - Good accuracy (85-90%)
    """
    np.random.seed(seed)
    
    def create_dataset(n_samples, default_rate=0.08, seed_offset=0):
        np.random.seed(seed + seed_offset)
        
        # Generate features with realistic distributions
        age = np.random.normal(45, 15, n_samples).clip(18, 80).astype(int)
        income = np.random.lognormal(10.8, 0.6, n_samples).clip(25000, 300000).round(2)
        credit_score = np.random.normal(700, 80, n_samples).clip(300, 850).astype(int)
        dti_ratio = np.random.beta(3, 7, n_samples).clip(0.05, 0.65).round(4)
        delinquencies = np.random.poisson(0.5, n_samples).clip(0, 10).astype(int)
        employment_months = np.random.exponential(60, n_samples).clip(0, 360).astype(int)
        utilization = np.random.beta(2, 5, n_samples).clip(0, 1).round(4)
        num_credit_lines = np.random.poisson(5, n_samples).clip(1, 25).astype(int)
        inquiries_6m = np.random.poisson(1, n_samples).clip(0, 10).astype(int)
        
        # Create STRONG predictive relationship (good model)
        risk_score = (
            -0.02 * (credit_score - 700) +      # Strong negative relationship
            2.5 * dti_ratio +                    # Strong positive relationship
            0.3 * delinquencies +                # Moderate positive
            -0.005 * (income / 1000) +           # Weak negative
            0.15 * inquiries_6m +                # Moderate positive
            0.5 * utilization +                  # Moderate positive
            -0.01 * (employment_months / 12)     # Weak negative
        )
        
        # Add small noise (good signal-to-noise ratio)
        risk_score += np.random.normal(0, 0.5, n_samples)
        
        # Convert to probability
        probability = 1 / (1 + np.exp(-risk_score))
        
        # Adjust to target default rate
        threshold = np.percentile(probability, (1 - default_rate) * 100)
        adjusted_prob = probability / threshold * default_rate * 2
        adjusted_prob = np.clip(adjusted_prob, 0.001, 0.999)
        
        # Generate target with STRONG relationship to features
        target = (np.random.random(n_samples) < adjusted_prob).astype(int)
        
        # Generate scores with GOOD discrimination
        score = (850 - (adjusted_prob * 550)).round(0).astype(int)
        
        # Enhance separation between good and bad
        score[target == 0] = score[target == 0] + np.random.randint(-20, 50, sum(target == 0))
        score[target == 1] = score[target == 1] + np.random.randint(-50, 20, sum(target == 1))
        score = score.clip(300, 850)
        
        return pd.DataFrame({
            'age': age,
            'income': income,
            'credit_score': credit_score,
            'dti_ratio': dti_ratio,
            'delinquencies': delinquencies,
            'employment_months': employment_months,
            'utilization': utilization,
            'num_credit_lines': num_credit_lines,
            'inquiries_6m': inquiries_6m,
            'target': target,
            'score': score
        })
    
    # Generate datasets with similar distributions (low PSI/CSI)
    train_df = create_dataset(n_train, default_rate=0.08, seed_offset=0)
    test_df = create_dataset(n_test, default_rate=0.08, seed_offset=100)
    oot_df = create_dataset(n_oot, default_rate=0.09, seed_offset=200)  # Slight shift
    
    return train_df, test_df, oot_df


def generate_failed_data(n_train=2000, n_test=1000, n_oot=600, seed=99):
    """
    Generate data with POOR model performance that will FAIL validation
    - Low KS (< 0.20)
    - Low Gini (< 0.30)
    - High PSI (> 0.25)
    - High CSI (> 0.25)
    - Poor accuracy (< 70%)
    """
    np.random.seed(seed)
    
    def create_dataset(n_samples, default_rate=0.08, seed_offset=0, distribution_shift=0):
        np.random.seed(seed + seed_offset)
        
        # Generate features with DIFFERENT distributions (high PSI/CSI)
        shift = distribution_shift
        age = np.random.normal(45 + shift*10, 15, n_samples).clip(18, 80).astype(int)
        income = np.random.lognormal(10.8 + shift*0.3, 0.6, n_samples).clip(25000, 300000).round(2)
        credit_score = np.random.normal(700 - shift*50, 80, n_samples).clip(300, 850).astype(int)
        dti_ratio = np.random.beta(3 + shift, 7 - shift, n_samples).clip(0.05, 0.65).round(4)
        delinquencies = np.random.poisson(0.5 + shift, n_samples).clip(0, 10).astype(int)
        employment_months = np.random.exponential(60 - shift*20, n_samples).clip(0, 360).astype(int)
        utilization = np.random.beta(2 + shift, 5 - shift, n_samples).clip(0, 1).round(4)
        num_credit_lines = np.random.poisson(5 + shift, n_samples).clip(1, 25).astype(int)
        inquiries_6m = np.random.poisson(1 + shift, n_samples).clip(0, 10).astype(int)
        
        # Create WEAK predictive relationship (poor model)
        risk_score = (
            -0.005 * (credit_score - 700) +     # Very weak relationship
            0.3 * dti_ratio +                    # Weak relationship
            0.05 * delinquencies +               # Very weak
            -0.0005 * (income / 1000) +          # Almost no relationship
            0.02 * inquiries_6m +                # Very weak
            0.1 * utilization +                  # Weak
            -0.001 * (employment_months / 12)    # Almost no relationship
        )
        
        # Add LARGE noise (poor signal-to-noise ratio)
        risk_score += np.random.normal(0, 2.0, n_samples)
        
        # Convert to probability
        probability = 1 / (1 + np.exp(-risk_score))
        
        # Adjust to target default rate
        threshold = np.percentile(probability, (1 - default_rate) * 100)
        adjusted_prob = probability / threshold * default_rate * 2
        adjusted_prob = np.clip(adjusted_prob, 0.001, 0.999)
        
        # Generate target with WEAK relationship to features
        target = (np.random.random(n_samples) < adjusted_prob).astype(int)
        
        # Generate scores with POOR discrimination (almost random)
        score = (850 - (adjusted_prob * 550)).round(0).astype(int)
        
        # Add random noise to reduce separation
        score = score + np.random.randint(-100, 100, n_samples)
        score = score.clip(300, 850)
        
        return pd.DataFrame({
            'age': age,
            'income': income,
            'credit_score': credit_score,
            'dti_ratio': dti_ratio,
            'delinquencies': delinquencies,
            'employment_months': employment_months,
            'utilization': utilization,
            'num_credit_lines': num_credit_lines,
            'inquiries_6m': inquiries_6m,
            'target': target,
            'score': score
        })
    
    # Generate datasets with DIFFERENT distributions (high PSI/CSI)
    train_df = create_dataset(n_train, default_rate=0.08, seed_offset=0, distribution_shift=0)
    test_df = create_dataset(n_test, default_rate=0.12, seed_offset=100, distribution_shift=0.5)  # Shift
    oot_df = create_dataset(n_oot, default_rate=0.15, seed_offset=200, distribution_shift=1.0)  # Large shift
    
    return train_df, test_df, oot_df


def create_readme(folder_name, description, expected_results):
    """Create README file for test set"""
    content = f"""# {folder_name}

## Description
{description}

## Files Included
- `train.csv` - Training dataset
- `test.csv` - Test dataset  
- `oot.csv` - Out-of-time dataset

## Expected Validation Results
{expected_results}

## How to Use
1. Navigate to the Model Validation app
2. Upload model documentation (optional)
3. Configure model:
   - Model Name: Test_Model
   - Product Type: Unsecured Personal Loans
   - Scorecard Type: Application
   - Model Type: Logistic Regression
4. Upload these three CSV files
5. Start validation
6. Review results

## Data Structure
All CSV files contain the following columns:
- `age`: Customer age (18-80)
- `income`: Annual income ($25,000-$300,000)
- `credit_score`: FICO score (300-850)
- `dti_ratio`: Debt-to-income ratio (0.05-0.65)
- `delinquencies`: Number of past delinquencies (0-10)
- `employment_months`: Employment length in months (0-360)
- `utilization`: Credit utilization ratio (0-1)
- `num_credit_lines`: Number of credit lines (1-25)
- `inquiries_6m`: Credit inquiries in last 6 months (0-10)
- `target`: Default indicator (0=good, 1=bad)
- `score`: Model prediction score (300-850, higher=lower risk)

## Generated By
Banking Model Validation System - Test Data Generator
"""
    return content


def main():
    print("=" * 70)
    print("Generating Test Data Sets for Model Validation")
    print("=" * 70)
    print()
    
    # Create output directories
    base_dir = Path(__file__).parent
    set1_dir = base_dir / "set1_successful"
    set2_dir = base_dir / "set2_failed"
    
    set1_dir.mkdir(exist_ok=True)
    set2_dir.mkdir(exist_ok=True)
    
    # Generate Set 1: Successful Validation
    print("📊 Generating Set 1: Successful Validation Data...")
    train1, test1, oot1 = generate_successful_data()
    
    train1.to_csv(set1_dir / "train.csv", index=False)
    test1.to_csv(set1_dir / "test.csv", index=False)
    oot1.to_csv(set1_dir / "oot.csv", index=False)
    
    print(f"✅ Set 1 - train.csv: {len(train1)} rows, {train1['target'].mean():.2%} default rate")
    print(f"✅ Set 1 - test.csv: {len(test1)} rows, {test1['target'].mean():.2%} default rate")
    print(f"✅ Set 1 - oot.csv: {len(oot1)} rows, {oot1['target'].mean():.2%} default rate")
    print()
    
    # Create README for Set 1
    readme1 = create_readme(
        "Set 1: Successful Validation",
        "This dataset is designed to PASS model validation with excellent performance metrics.",
        """
✅ **Overall Status**: PASS

**Statistical Tests:**
- KS Statistic: 0.40-0.50 (Excellent discrimination)
- Gini Coefficient: 0.60-0.70 (Good model performance)
- PSI: < 0.10 (Stable population)
- CSI: < 0.10 (Stable characteristics)

**Performance Metrics:**
- Accuracy: 85-90%
- Precision: 40-50%
- Recall: 60-70%
- F1 Score: 0.50-0.60
- AUC-ROC: 0.80-0.85

**Model-Specific Validation:**
- ✅ Data quality checks pass
- ✅ Target distribution appropriate
- ✅ Score distribution good
- ✅ Strong predictive power
- ✅ Good separation between good/bad customers

**SR 11-7 Compliance:**
- Score: 70-80% (Good compliance)
"""
    )
    
    with open(set1_dir / "README.md", "w") as f:
        f.write(readme1)
    
    print("✅ Set 1 README.md created")
    print()
    
    # Generate Set 2: Failed Validation
    print("📊 Generating Set 2: Failed Validation Data...")
    train2, test2, oot2 = generate_failed_data()
    
    train2.to_csv(set2_dir / "train.csv", index=False)
    test2.to_csv(set2_dir / "test.csv", index=False)
    oot2.to_csv(set2_dir / "oot.csv", index=False)
    
    print(f"✅ Set 2 - train.csv: {len(train2)} rows, {train2['target'].mean():.2%} default rate")
    print(f"✅ Set 2 - test.csv: {len(test2)} rows, {test2['target'].mean():.2%} default rate")
    print(f"✅ Set 2 - oot.csv: {len(oot2)} rows, {oot2['target'].mean():.2%} default rate")
    print()
    
    # Create README for Set 2
    readme2 = create_readme(
        "Set 2: Failed Validation",
        "This dataset is designed to FAIL model validation with poor performance metrics and instability.",
        """
❌ **Overall Status**: FAIL

**Statistical Tests:**
- KS Statistic: < 0.20 (Poor discrimination) ❌
- Gini Coefficient: < 0.30 (Weak model performance) ❌
- PSI: > 0.25 (Unstable population) ❌
- CSI: > 0.25 (Unstable characteristics) ❌

**Performance Metrics:**
- Accuracy: < 70% ❌
- Precision: < 30% ❌
- Recall: < 50% ❌
- F1 Score: < 0.35 ❌
- AUC-ROC: < 0.65 ❌

**Model-Specific Validation:**
- ❌ Weak predictive power
- ❌ Poor separation between good/bad customers
- ❌ High population shift between datasets
- ❌ Significant characteristic instability
- ❌ Model not suitable for production

**SR 11-7 Compliance:**
- Score: 30-40% (Poor compliance) ❌

**Issues Identified:**
1. Model has weak predictive power (low KS/Gini)
2. Significant population shift between train/test/OOT (high PSI)
3. Feature distributions are unstable (high CSI)
4. Poor discrimination between good and bad customers
5. Model performance degrades significantly on OOT data
6. Not suitable for production deployment
"""
    )
    
    with open(set2_dir / "README.md", "w") as f:
        f.write(readme2)
    
    print("✅ Set 2 README.md created")
    print()
    
    # Summary
    print("=" * 70)
    print("✅ Test Data Generation Complete!")
    print("=" * 70)
    print()
    print("📁 Files created:")
    print(f"   Set 1 (Successful): {set1_dir}/")
    print("      - train.csv (2000 rows)")
    print("      - test.csv (1000 rows)")
    print("      - oot.csv (600 rows)")
    print("      - README.md")
    print()
    print(f"   Set 2 (Failed): {set2_dir}/")
    print("      - train.csv (2000 rows)")
    print("      - test.csv (1000 rows)")
    print("      - oot.csv (600 rows)")
    print("      - README.md")
    print()
    print("🎯 Usage:")
    print("   1. Use Set 1 to demonstrate successful model validation")
    print("   2. Use Set 2 to demonstrate failed model validation")
    print("   3. Upload files in the Model Validation app")
    print("   4. Compare validation results between the two sets")
    print()


if __name__ == "__main__":
    main()

# Made with Bob
