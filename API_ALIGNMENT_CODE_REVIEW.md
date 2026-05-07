# API Alignment Code Review - Critical Data Structure Mismatches

## Executive Summary

**Status**: ❌ CRITICAL MISMATCHES FOUND  
**Date**: 2026-05-07  
**Reviewer**: Code Analysis  
**Focus Areas**: Backend API endpoints vs Frontend expectations, Dashboard UI vs Generated Report

---

## 🔴 CRITICAL ISSUE #1: Statistical Tests Data Structure Mismatch

### Backend Returns (main_simple.py lines 316-325):
```python
stats_results[dataset_name] = {
    "ks_statistic": ks_result.get("ks_statistic", 0),
    "ks_details": ks_result,
    "gini_coefficient": gini_result.get("gini", 0),  # ❌ WRONG KEY
    "gini_details": gini_result,
    "psi": psi_result.get("psi", 0),
    "psi_details": psi_result,
    "csi": csi_result.get("average_csi", 0),
    "csi_details": csi_result
}
```

### Frontend Expects (ValidationResults.jsx lines 196-280):
```javascript
// Frontend looks for:
results.statistical_tests?.train?.ks_statistic  // ✅ MATCHES
results.statistical_tests?.train?.gini_coefficient  // ✅ MATCHES
results.statistical_tests?.train?.psi  // ✅ MATCHES
results.statistical_tests?.train?.csi  // ❌ MISSING - backend has it but not exposed
```

### Problem:
The backend stores `gini_coefficient` correctly, but the `gini_result` from `StatisticalTestsCalculator` returns `"gini"` not `"gini_coefficient"`.

**Impact**: Gini values may not display correctly in UI

---

## 🔴 CRITICAL ISSUE #2: Performance Metrics Not Exposed to Frontend

### Backend Calculates (main_simple.py lines 330-336):
```python
performance_results = performance_validator.validate_performance(
    model_config=model_config,
    train_data=train_data,
    test_data=test_data,
    oot_data=oot_data
)
```

### Backend Stores (main_simple.py lines 368-380):
```python
"results": {
    "statistical_tests": stats_results,  # ✅ Exposed
    "performance": performance_results,   # ❌ NOT properly structured for frontend
    "model_specific": model_specific_results,
    "compliance": compliance_results,
    ...
}
```

### Frontend Expects (ValidationResults.jsx lines 141-148):
```javascript
results.performance?.train?.accuracy  // ❌ MISMATCH
```

### Actual Backend Structure (performance_validator.py):
```python
{
    "train": {
        "accuracy": 0.85,
        "ks_test": {...},  // Nested inside train
        "gini_test": {...}  // Nested inside train
    }
}
```

**Problem**: The `performance_results` object already has the correct structure, but it's not being transformed for frontend compatibility in the results endpoint.

---

## 🔴 CRITICAL ISSUE #3: Missing Data Transformation in Results Endpoint

### Current Implementation (main_simple.py lines 413-468):
```python
@app.get("/api/v1/validate/{validation_id}/results")
async def get_validation_results(validation_id: str):
    results = validation["results"]
    
    # Only creates stability object
    stability = {...}
    
    # Returns raw results + stability
    return {
        **results,  # ❌ Raw results without transformation
        "model_config": model_config,
        "stability": stability,
        "metadata": metadata
    }
```

### What's Missing:
The endpoint does NOT transform the data structure to match frontend expectations. It should:

1. Extract statistical tests from `stats_results` (dataset-level)
2. Extract performance metrics from `performance_results` (dataset-level)
3. Create frontend-compatible structure

---

## 🟡 ISSUE #4: Inconsistent Data Between Dashboard and Report

### Dashboard Data Source:
- API endpoint: `/api/v1/validate/{validation_id}/results`
- Returns: `results.statistical_tests.train.ks_statistic`

### Report Data Source (main_simple.py lines 488-520):
```python
report_content = f"""
KS Statistic: {results.get('summary', {}).get('ks_statistic', 'N/A')}
Gini Coefficient: {results.get('summary', {}).get('gini_coefficient', 'N/A')}
"""
```

### Problem:
- Dashboard uses `results.statistical_tests.train.ks_statistic`
- Report uses `results.summary.ks_statistic`
- These pull from DIFFERENT data sources!

**Impact**: Dashboard and report may show different values

---

## 📊 Data Flow Analysis

### Current Flow (BROKEN):
```
1. Validators calculate metrics
   ↓
2. main_simple.py stores in validation_store
   {
     "statistical_tests": {
       "train": {"ks_statistic": 0.45, ...},
       "test": {...},
       "out_of_time": {...}
     },
     "performance": {
       "train": {"accuracy": 0.85, "ks_test": {...}},  // ❌ Duplicate KS data
       ...
     }
   }
   ↓
3. Results endpoint returns RAW data
   ↓
4. Frontend tries to access:
   - results.statistical_tests.train.ks_statistic ✅
   - results.performance.train.accuracy ❌ (structure mismatch)
```

### Required Flow (FIXED):
```
1. Validators calculate metrics
   ↓
2. main_simple.py stores in validation_store
   ↓
3. Results endpoint TRANSFORMS data:
   - Extracts statistical_tests properly
   - Extracts performance metrics properly
   - Creates unified structure
   ↓
4. Frontend receives consistent structure
```

---

## 🔧 Required Fixes

### Fix #1: Update Results Endpoint (main_simple.py)

**Location**: Lines 413-468

**Current**:
```python
return {
    **results,
    "model_config": model_config,
    "stability": stability,
    "metadata": metadata
}
```

**Should Be**:
```python
# Extract and restructure data
statistical_tests = {
    "train": {
        "ks_statistic": results["statistical_tests"]["train"]["ks_statistic"],
        "ks_details": results["statistical_tests"]["train"]["ks_details"],
        "gini_coefficient": results["statistical_tests"]["train"]["gini_coefficient"],
        "gini_details": results["statistical_tests"]["train"]["gini_details"],
        "psi": results["statistical_tests"]["train"]["psi"],
        "psi_details": results["statistical_tests"]["train"]["psi_details"],
        "csi": results["statistical_tests"]["train"]["csi"],
        "csi_details": results["statistical_tests"]["train"]["csi_details"]
    },
    "test": {...},  // Same structure
    "out_of_time": {...}  // Same structure
}

performance = {
    "train": {
        "accuracy": results["performance"]["train"]["accuracy"],
        "precision": results["performance"]["train"]["precision"],
        "recall": results["performance"]["train"]["recall"],
        "f1_score": results["performance"]["train"]["f1_score"],
        "auc_roc": results["performance"]["train"]["auc_roc"]
    },
    "test": {...},
    "out_of_time": {...}
}

return {
    "statistical_tests": statistical_tests,
    "performance": performance,
    "model_specific": results["model_specific"],
    "compliance": results["compliance"],
    "stability": stability,
    "model_config": model_config,
    "metadata": metadata
}
```

### Fix #2: Ensure Gini Key Consistency

**Location**: backend/validation/statistical_tests.py

**Check**: The `calculate_gini_coefficient` method should return:
```python
{
    "gini_coefficient": gini_value,  // Not "gini"
    "gini": gini_value,  // Keep for backward compatibility
    ...
}
```

### Fix #3: Align Report Generation with Dashboard Data

**Location**: main_simple.py lines 488-520

**Change**: Use the SAME data paths as the dashboard:
```python
# Get data from same source as dashboard
stats_train = results["statistical_tests"]["train"]
perf_train = results["performance"]["train"]

report_content = f"""
KS Statistic: {stats_train.get('ks_statistic', 'N/A')}
Gini Coefficient: {stats_train.get('gini_coefficient', 'N/A')}
Accuracy: {perf_train.get('accuracy', 'N/A')}
"""
```

---

## 📋 Testing Checklist

After applying fixes, verify:

- [ ] Dashboard displays all 4 statistical tests (KS, Gini, PSI, CSI)
- [ ] Dashboard displays performance metrics (Accuracy, Precision, Recall, F1, AUC-ROC)
- [ ] Values in dashboard match values in generated report
- [ ] All 3 datasets (train, test, OOT) display correctly
- [ ] Status chips show correct colors (green/yellow/red)
- [ ] No console errors in browser
- [ ] API response structure matches frontend expectations

---

## 🎯 Priority

**CRITICAL** - These mismatches prevent the UI from displaying validation results correctly, which is the core functionality of the application.

**Estimated Fix Time**: 2-3 hours

**Risk**: Medium - Changes affect data structure but not business logic

---

## 📝 Additional Notes

1. The `validation_orchestrator.py` fix we applied earlier is NOT being used because `main_simple.py` doesn't use the orchestrator
2. Need to decide: Use orchestrator OR fix main_simple.py
3. Consider consolidating duplicate statistical test calculations (currently in both stats_results and performance_results)

---

**Next Steps**:
1. Apply Fix #1 (Results endpoint transformation)
2. Verify Fix #2 (Gini key consistency)
3. Apply Fix #3 (Report alignment)
4. Test end-to-end with sample data
5. Commit changes