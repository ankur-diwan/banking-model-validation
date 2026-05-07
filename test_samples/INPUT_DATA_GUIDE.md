# Banking Model Validation System - Input Data Guide

## 📋 Overview

This guide explains what input data is required to run the Banking Model Validation System and how to generate sample data that will demonstrate successful model validation.

---

## 🎯 Required Input Data

### 1. **Model Configuration** (Required)
Provided through the UI form in Step 2:

```json
{
  "model_name": "US_Unsecured_Application_v2",
  "product_type": "unsecured_personal_loans",
  "scorecard_type": "application",
  "model_type": "logistic_regression",
  "description": "Application scorecard for unsecured personal loans",
  "version": "2.1",
  "owner": "Credit Risk Analytics"
}
```

**Available Options:**
- **Product Types**: 
  - `unsecured_personal_loans`
  - `secured_personal_loans`
  - `credit_cards`
  - `auto_loans`
  - `mortgages`

- **Scorecard Types**:
  - `application` - For new customer acquisition
  - `behavioral` - For existing customer risk assessment
  - `collections_early` - For early stage collections (0-90 DPD)
  - `collections_late` - For late stage collections (90+ DPD)

- **Model Types**:
  - `logistic_regression` (GLM)
  - `decision_tree`
  - `random_forest`
  - `xgboost`
  - `neural_network`

### 2. **Training Data CSV** (Required)
Must contain:
- **Features**: Predictor variables (age, income, credit_score, etc.)
- **Target**: Binary outcome variable (0 = good, 1 = bad/default)
- **Score**: Model predictions (0-1000 scale typical for scorecards)

**Minimum Requirements:**
- At least 1,000 rows
- At least 3 features
- Target column with binary values (0/1)
- Score column with numeric predictions

**Example Structure:**
```csv
age,income,credit_score,dti_ratio,delinquencies,target,score
35,75000,720,0.35,0,0,650
42,95000,680,0.42,1,1,520
28,55000,750,0.28,0,0,720
...
```

### 3. **Test Data CSV** (Required)
Same structure as training data, used for out-of-sample validation.

**Minimum Requirements:**
- At least 500 rows
- Same columns as training data
- Different time period or population segment

### 4. **Out-of-Time (OOT) Data CSV** (Required)
Same structure as training/test data, represents most recent performance.

**Minimum Requirements:**
- At least 300 rows
- Same columns as training/test data
- Most recent time period

### 5. **Documentation Files** (Optional but Recommended)
- **Model Documentation** (PDF/DOCX): Model development details, SR 11-7 sections
- **Data Dictionary** (CSV): Variable definitions and business logic
- **Validation Report** (PDF/DOCX): Previous validation findings

---

## ✅ Generating Sample Data for Successful Validation

### Option 1: Use the Built-in Data Generator (Recommended)

The system includes a synthetic data generator that creates realistic data with **good model performance**.

**Run the generator:**
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine
python test_samples/generate_successful_validation_data.py
```

This will create:
- `successful_train.csv` (2,000 rows)
- `successful_test.csv` (1,000 rows)
- `successful_oot.csv` (600 rows)
- `successful_model_documentation.docx`

**Expected Performance Metrics:**
- ✅ KS Statistic: 0.40-0.50 (Excellent)
- ✅ Gini Coefficient: 0.60-0.70 (Good)
- ✅ PSI: < 0.10 (Stable)
- ✅ CSI: < 0.10 (Stable)
- ✅ AUC-ROC: 0.80-0.85 (Excellent)
- ✅ Accuracy: 85-90%

### Option 2: Manual Data Preparation

If you have your own data, ensure it meets these criteria for successful validation:

#### Data Quality Checks:
1. **No Missing Values** in critical columns (target, score)
2. **Balanced Target Distribution**: 5-15% default rate
3. **Score Distribution**: Reasonable spread (not all same values)
4. **Feature Variability**: Features should have meaningful variation

#### Performance Thresholds:
For a model to pass validation:

| Metric | Minimum (Acceptable) | Good | Excellent |
|--------|---------------------|------|-----------|
| KS Statistic | 0.20 | 0.30 | 0.40+ |
| Gini Coefficient | 0.30 | 0.40 | 0.60+ |
| AUC-ROC | 0.65 | 0.75 | 0.80+ |
| PSI (Stability) | < 0.25 | < 0.10 | < 0.05 |
| CSI (Stability) | < 0.25 | < 0.10 | < 0.05 |

#### Creating Good Predictions:
```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Load your data
df = pd.read_csv('your_data.csv')

# Select features
features = ['age', 'income', 'credit_score', 'dti_ratio']
X = df[features]
y = df['target']

# Train a simple model
model = LogisticRegression()
model.fit(X, y)

# Generate predictions (probabilities)
probabilities = model.predict_proba(X)[:, 1]

# Convert to scorecard scale (300-850)
df['score'] = 850 - (probabilities * 550)

# Save
df.to_csv('prepared_data.csv', index=False)
```

---

## 📊 Sample Data Files Included

### 1. **sample_model_documentation.docx**
**Purpose**: Demonstrates proper model documentation with SR 11-7 sections

**Contains:**
- Executive Summary
- Model Overview (name, type, product)
- SR 11-7 Compliance Framework:
  - Conceptual Soundness
  - Data Quality and Integrity
  - Model Performance
  - Model Assumptions
  - Ongoing Monitoring
- Model Variables and Coefficients
- Performance Metrics

**How to Use:**
1. Upload in Step 1 (Document Upload)
2. System will extract model metadata
3. SR 11-7 sections will be detected
4. Compliance score will be enhanced

### 2. **sample_data_dictionary.csv**
**Purpose**: Variable definitions and business logic

**Contains:**
- Variable names
- Data types
- Valid ranges
- Missing value treatment
- Business descriptions

**How to Use:**
1. Upload alongside model documentation
2. Helps with data quality validation
3. Provides context for validators

### 3. **sample_validation_report.docx**
**Purpose**: Previous validation findings

**Contains:**
- Validation methodology
- Performance assessment
- Findings and recommendations
- Approval status

**How to Use:**
1. Upload for historical context
2. System can compare current vs. previous validation
3. Helps track model evolution

---

## 🚀 Step-by-Step Demo Workflow

### Scenario: Successful Application Scorecard Validation

**Step 1: Generate Sample Data**
```bash
cd test_samples
python generate_successful_validation_data.py
```

**Step 2: Access the Application**
- Open browser: http://localhost:3002/
- You'll see the validation wizard

**Step 3: Upload Documents (Optional)**
- Drag and drop `successful_model_documentation.docx`
- Drag and drop `sample_data_dictionary.csv`
- Click "Continue"

**Step 4: Configure Model**
Fill in the form:
- Model Name: `US_Unsecured_Application_v2`
- Product Type: `Unsecured Personal Loans`
- Scorecard Type: `Application`
- Model Type: `Logistic Regression`
- Description: `Application scorecard for unsecured personal loans`
- Version: `2.1`
- Owner: `Credit Risk Analytics`

**Step 5: Upload Data Files**
- Training Data: `successful_train.csv`
- Test Data: `successful_test.csv`
- Out-of-Time Data: `successful_oot.csv`

**Step 6: Start Validation**
- Click "Start Validation"
- Wait 30-60 seconds for processing

**Step 7: View Results**
You should see:
- ✅ **Overall Status**: PASS
- ✅ **KS Statistic**: 0.45 (Excellent)
- ✅ **Gini Coefficient**: 0.65 (Good)
- ✅ **PSI**: 0.05 (Stable)
- ✅ **CSI**: 0.03 (Stable)
- ✅ **SR 11-7 Compliance**: 75%+ (if documents uploaded)

**Step 8: Download Report**
- Click "Download Report" button
- Get a Word document with complete validation results

---

## 🔍 Understanding the Results

### Dashboard Sections:

#### 1. **Validation Summary** (4 Cards)
- **Overall Status**: PASS/FAIL based on all tests
- **Model Type**: Scorecard type and product
- **Stability**: PSI score and status
- **SR 11-7 Score**: Compliance percentage

#### 2. **Statistical Tests** (4 Cards)
- **KS Test**: Measures separation between good/bad
- **Gini Coefficient**: Measures discrimination power
- **PSI**: Population stability over time
- **CSI**: Characteristic stability across features

#### 3. **Performance Metrics** (Table)
Shows metrics across 3 datasets (Train, Test, OOT):
- Accuracy
- Precision
- Recall
- F1 Score
- AUC-ROC

#### 4. **Stability Analysis**
- PSI by dataset
- CSI by feature
- Overall stability assessment

#### 5. **SR 11-7 Compliance**
9 categories with pass/fail status:
- Model Purpose
- Conceptual Soundness
- Data Quality
- Performance Validation
- Stability Analysis
- Assumptions Testing
- Implementation Validation
- Ongoing Monitoring
- Documentation

#### 6. **Model-Specific Validation**
Checks specific to scorecard type:
- Data quality checks
- Target analysis
- Score distribution
- Predictive power
- Behavioral patterns (for behavioral scorecards)
- Collection strategies (for collections scorecards)

---

## ⚠️ Common Issues and Solutions

### Issue 1: Low KS/Gini Scores
**Symptom**: KS < 0.20, Gini < 0.30
**Cause**: Poor model predictions or random scores
**Solution**: 
- Ensure scores are actual model predictions, not random
- Check that target variable is correctly defined
- Verify score scale is appropriate (higher scores = lower risk)

### Issue 2: High PSI/CSI
**Symptom**: PSI > 0.25, CSI > 0.25
**Cause**: Significant population shift between datasets
**Solution**:
- Use data from similar time periods
- Ensure consistent data collection methods
- Check for data quality issues

### Issue 3: Low Compliance Score
**Symptom**: SR 11-7 score < 50%
**Cause**: Missing documentation or incomplete model info
**Solution**:
- Upload model documentation with SR 11-7 sections
- Provide complete model configuration
- Include data dictionary and validation reports

### Issue 4: File Upload Errors
**Symptom**: "Invalid file type" or "File too large"
**Solution**:
- Use only PDF, DOCX, or CSV formats
- Keep files under 10MB
- Ensure CSV files have proper headers

---

## 📞 Support

For issues or questions:
1. Check the console logs (F12 → Console)
2. Review backend logs in terminal
3. Verify all required files are present
4. Ensure data meets minimum requirements

---

## 🎓 Best Practices

1. **Always upload documentation** - Improves compliance score
2. **Use realistic data** - Synthetic data should mimic production
3. **Check data quality first** - Run basic checks before validation
4. **Review all sections** - Don't just look at overall status
5. **Download reports** - Keep validation records for audit
6. **Test multiple scenarios** - Try different model types and products
7. **Monitor trends** - Compare validations over time

---

## 📚 Additional Resources

- **SR 11-7 Guidelines**: Federal Reserve guidance on model risk management
- **Model Validation Best Practices**: Industry standards for credit risk models
- **Statistical Tests Reference**: Detailed explanations of KS, Gini, PSI, CSI
- **Scorecard Development**: Guide to building credit scorecards

---

**Generated by**: Banking Model Validation System  
**Version**: 2.0.0  
**Last Updated**: May 7, 2026