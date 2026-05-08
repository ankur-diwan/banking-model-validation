# Test Data Sets Guide

## Overview

This directory contains **two complete test data sets** designed for comprehensive testing of the Banking Model Validation System. Each set includes train, test, and out-of-time (OOT) datasets that demonstrate different validation outcomes.

---

## 📁 Directory Structure

```
test_samples/
├── set1_successful/          # ✅ Data for SUCCESSFUL validation
│   ├── train.csv            # 2000 rows, ~10.7% default rate
│   ├── test.csv             # 1000 rows, ~10.4% default rate
│   ├── oot.csv              # 600 rows, ~10.0% default rate
│   └── README.md            # Detailed documentation
│
├── set2_failed/              # ❌ Data for FAILED validation
│   ├── train.csv            # 2000 rows, ~9.2% default rate
│   ├── test.csv             # 1000 rows, ~13.6% default rate
│   ├── oot.csv              # 600 rows, ~15.5% default rate
│   └── README.md            # Detailed documentation
│
├── generate_test_sets.py     # Generator script
└── TEST_DATA_SETS_GUIDE.md   # This file
```

---

## 🎯 Set 1: Successful Validation

### Purpose
Demonstrates a **well-performing model** that passes all validation checks with excellent metrics.

### Expected Results
- ✅ **Overall Status**: PASS
- ✅ **KS Statistic**: 0.40-0.50 (Excellent discrimination)
- ✅ **Gini Coefficient**: 0.60-0.70 (Good performance)
- ✅ **PSI**: < 0.10 (Stable population)
- ✅ **CSI**: < 0.10 (Stable characteristics)
- ✅ **Accuracy**: 85-90%
- ✅ **AUC-ROC**: 0.80-0.85

### Key Characteristics
1. **Strong Predictive Power**: Clear separation between good and bad customers
2. **Stable Distributions**: Minimal population shift across train/test/OOT
3. **Consistent Performance**: Model performs well across all datasets
4. **Good Calibration**: Scores align well with actual default rates
5. **Production Ready**: Suitable for deployment

### Use Cases
- ✅ Demonstrate successful model validation workflow
- ✅ Training and onboarding new users
- ✅ Testing system functionality
- ✅ Validating new features
- ✅ Creating demo presentations

---

## ❌ Set 2: Failed Validation

### Purpose
Demonstrates a **poorly-performing model** that fails validation checks with weak metrics and instability.

### Expected Results
- ❌ **Overall Status**: FAIL
- ❌ **KS Statistic**: < 0.20 (Poor discrimination)
- ❌ **Gini Coefficient**: < 0.30 (Weak performance)
- ❌ **PSI**: > 0.25 (Unstable population)
- ❌ **CSI**: > 0.25 (Unstable characteristics)
- ❌ **Accuracy**: < 70%
- ❌ **AUC-ROC**: < 0.65

### Key Characteristics
1. **Weak Predictive Power**: Poor separation between good and bad customers
2. **Unstable Distributions**: Significant population shift across datasets
3. **Degrading Performance**: Model performance deteriorates on OOT data
4. **Poor Calibration**: Scores don't align with actual default rates
5. **Not Production Ready**: Model requires redevelopment

### Issues Identified
1. Model has weak predictive power (low KS/Gini)
2. Significant population shift between train/test/OOT (high PSI)
3. Feature distributions are unstable (high CSI)
4. Poor discrimination between good and bad customers
5. Model performance degrades significantly on OOT data
6. Not suitable for production deployment

### Use Cases
- ❌ Demonstrate failed model validation workflow
- ❌ Test error handling and validation logic
- ❌ Show importance of model monitoring
- ❌ Demonstrate drift detection capabilities
- ❌ Training on identifying model issues

---

## 📊 Data Structure

All CSV files contain the following columns:

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `age` | int | 18-80 | Customer age |
| `income` | float | 25,000-300,000 | Annual income ($) |
| `credit_score` | int | 300-850 | FICO credit score |
| `dti_ratio` | float | 0.05-0.65 | Debt-to-income ratio |
| `delinquencies` | int | 0-10 | Number of past delinquencies |
| `employment_months` | int | 0-360 | Employment length (months) |
| `utilization` | float | 0-1 | Credit utilization ratio |
| `num_credit_lines` | int | 1-25 | Number of credit lines |
| `inquiries_6m` | int | 0-10 | Credit inquiries (last 6 months) |
| `target` | int | 0 or 1 | Default indicator (0=good, 1=bad) |
| `score` | int | 300-850 | Model prediction score (higher=lower risk) |

---

## 🚀 How to Use

### Step 1: Navigate to the App
Open the Banking Model Validation System in your browser (typically http://localhost:3000)

### Step 2: Configure Model
Fill in the model configuration:
- **Model Name**: Test_Model_Set1 (or Set2)
- **Product Type**: Unsecured Personal Loans
- **Scorecard Type**: Application
- **Model Type**: Logistic Regression
- **Model Technique**: GLM

### Step 3: Upload Documents (Optional)
Upload any model documentation (PDF/DOCX) if available

### Step 4: Upload Data Files
1. Click "Upload Documents" or navigate to the upload section
2. Upload the three CSV files from either set1_successful or set2_failed:
   - train.csv
   - test.csv
   - oot.csv
3. Verify files are uploaded successfully

### Step 5: Start Validation
1. Click "Start Validation"
2. Wait for validation to complete (typically 2-5 minutes)
3. Review the comprehensive validation results

### Step 6: Compare Results
- Use Set 1 to see a **successful validation** with excellent metrics
- Use Set 2 to see a **failed validation** with poor metrics and issues
- Compare the differences in statistical tests, performance metrics, and compliance scores

---

## 🔄 Regenerating Test Data

If you need to regenerate the test data sets:

```bash
cd test_samples
python generate_test_sets.py
```

This will:
1. Create fresh train/test/oot CSV files for both sets
2. Generate README.md files with expected results
3. Ensure data quality and consistency

---

## 📈 Expected Validation Metrics Comparison

| Metric | Set 1 (Success) | Set 2 (Failed) | Threshold |
|--------|----------------|----------------|-----------|
| **KS Statistic** | 0.40-0.50 ✅ | < 0.20 ❌ | > 0.30 |
| **Gini Coefficient** | 0.60-0.70 ✅ | < 0.30 ❌ | > 0.40 |
| **PSI** | < 0.10 ✅ | > 0.25 ❌ | < 0.15 |
| **CSI** | < 0.10 ✅ | > 0.25 ❌ | < 0.15 |
| **Accuracy** | 85-90% ✅ | < 70% ❌ | > 75% |
| **Precision** | 40-50% ✅ | < 30% ❌ | > 35% |
| **Recall** | 60-70% ✅ | < 50% ❌ | > 55% |
| **F1 Score** | 0.50-0.60 ✅ | < 0.35 ❌ | > 0.40 |
| **AUC-ROC** | 0.80-0.85 ✅ | < 0.65 ❌ | > 0.70 |
| **Compliance Score** | 70-80% ✅ | 30-40% ❌ | > 60% |

---

## 🎓 Training Scenarios

### Scenario 1: Successful Model Validation
**Objective**: Learn the complete validation workflow with a good model

1. Upload Set 1 data files
2. Configure model settings
3. Start validation
4. Review all validation results:
   - Statistical tests (KS, Gini, PSI, CSI)
   - Performance metrics (Accuracy, Precision, Recall, F1, AUC)
   - Model-specific validation results
   - Compliance score and gaps
5. Understand what makes a model production-ready

### Scenario 2: Failed Model Validation
**Objective**: Learn to identify and diagnose model issues

1. Upload Set 2 data files
2. Configure model settings
3. Start validation
4. Review validation failures:
   - Identify low KS/Gini (poor discrimination)
   - Identify high PSI/CSI (instability)
   - Identify poor performance metrics
   - Review compliance gaps
5. Understand why the model is not production-ready

### Scenario 3: Comparative Analysis
**Objective**: Compare good vs poor models side-by-side

1. Run validation with Set 1 (save results)
2. Run validation with Set 2 (save results)
3. Compare metrics side-by-side
4. Understand the differences
5. Learn validation thresholds and criteria

---

## 🔍 Troubleshooting

### Issue: Files Not Uploading
**Solution**: 
- Ensure files are in CSV format
- Check file size (should be < 10MB)
- Verify file names contain 'train', 'test', or 'oot'

### Issue: Validation Fails to Start
**Solution**:
- Verify all three files (train, test, oot) are uploaded
- Check model configuration is complete
- Review browser console for errors

### Issue: Unexpected Results
**Solution**:
- Regenerate test data using `generate_test_sets.py`
- Clear browser cache
- Restart backend server
- Check backend logs for errors

---

## 📝 Notes

1. **Data Quality**: Both sets use realistic banking data distributions
2. **Reproducibility**: Random seeds ensure consistent results
3. **Scalability**: Data sizes are optimized for quick validation
4. **Realism**: Metrics align with real-world banking models
5. **Educational**: Designed for training and demonstration

---

## 🤝 Contributing

To add new test data sets:

1. Create a new directory under `test_samples/`
2. Generate train.csv, test.csv, oot.csv
3. Create a README.md with expected results
4. Update this guide with the new set
5. Test thoroughly before committing

---

## 📞 Support

For questions or issues:
- Review the README.md in each set directory
- Check the main project documentation
- Contact the development team
- Submit an issue on GitHub

---

**Generated by**: Banking Model Validation System  
**Version**: 2.0.0  
**Last Updated**: May 7, 2026