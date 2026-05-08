# Uploaded Data Integration Gap Analysis

**Date**: May 7, 2026  
**Priority**: HIGH  
**Status**: ⚠️ IDENTIFIED - NOT YET IMPLEMENTED

---

## 🎯 Issue Summary

**Current Behavior**: The system generates synthetic sample data for validation instead of using uploaded CSV files.

**Expected Behavior**: The system should use the actual CSV files uploaded by the user (train, test, OOT datasets).

**Impact**: 
- ❌ Validation results are based on fake data, not real model data
- ❌ User uploads are not being utilized
- ❌ Cannot validate actual production models

---

## 🔍 Current Implementation Analysis

### What Happens Now (Lines 273-275 in main_simple.py):

```python
@app.post("/api/v1/validate")
async def start_validation_v1(request: Dict[str, Any]):
    # ... model config setup ...
    
    # ❌ PROBLEM: Generates fake data instead of using uploads
    train_data = generate_sample_data(1000, backend_model_type)
    test_data = generate_sample_data(500, backend_model_type)
    oot_data = generate_sample_data(300, backend_model_type)
    
    # Then runs validation on this fake data
    datasets = {
        "train": train_data,
        "test": test_data,
        "out_of_time": oot_data
    }
```

### What Should Happen:

```python
@app.post("/api/v1/validate")
async def start_validation_v1(request: Dict[str, Any]):
    # ... model config setup ...
    
    # ✅ CORRECT: Load uploaded CSV files
    train_data = pd.read_csv(f"uploads/{validation_id}/train.csv")
    test_data = pd.read_csv(f"uploads/{validation_id}/test.csv")
    oot_data = pd.read_csv(f"uploads/{validation_id}/oot.csv")
    
    # Then run validation on actual data
    datasets = {
        "train": train_data,
        "test": test_data,
        "out_of_time": oot_data
    }
```

---

## 📊 Current Data Flow (INCORRECT)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Uploads CSV Files                                   │
│    - train.csv, test.csv, oot.csv                          │
│    - Stored in uploads/ directory                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. User Starts Validation                                   │
│    POST /api/v1/validate                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Backend IGNORES Uploaded Files ❌                        │
│    - Generates synthetic data instead                       │
│    - train_data = generate_sample_data(1000)               │
│    - test_data = generate_sample_data(500)                 │
│    - oot_data = generate_sample_data(300)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Validation Runs on FAKE Data ❌                          │
│    - Statistical tests on synthetic data                    │
│    - Performance metrics on synthetic data                  │
│    - Results don't reflect actual model                     │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Required Data Flow (CORRECT)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Uploads CSV Files                                   │
│    - train.csv, test.csv, oot.csv                          │
│    - Stored in uploads/{validation_id}/ directory          │
│    - File paths stored in validation_store                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. User Starts Validation                                   │
│    POST /api/v1/validate                                    │
│    Body: { validation_id, model_config }                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Backend LOADS Uploaded Files ✅                          │
│    - Retrieves file paths from validation_store            │
│    - train_data = pd.read_csv(train_file_path)            │
│    - test_data = pd.read_csv(test_file_path)              │
│    - oot_data = pd.read_csv(oot_file_path)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Validation Runs on ACTUAL Data ✅                        │
│    - Statistical tests on real model data                   │
│    - Performance metrics on real model data                 │
│    - Results reflect actual model performance               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Required Changes

### Change #1: Update Validation Request Structure

**File**: `backend/main_simple.py`  
**Function**: `start_validation_v1()` (Lines 224-393)

**Current**:
```python
@app.post("/api/v1/validate")
async def start_validation_v1(request: Dict[str, Any]):
    model_config = request.get("model_config", {})
    validation_id = f"val_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
```

**Required**:
```python
@app.post("/api/v1/validate")
async def start_validation_v1(request: Dict[str, Any]):
    model_config = request.get("model_config", {})
    uploaded_files = request.get("uploaded_files", {})  # ← NEW
    validation_id = f"val_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
```

### Change #2: Load Uploaded CSV Files

**Current (Lines 273-275)**:
```python
# Generate sample data
train_data = generate_sample_data(1000, backend_model_type)
test_data = generate_sample_data(500, backend_model_type)
oot_data = generate_sample_data(300, backend_model_type)
```

**Required**:
```python
import pandas as pd
import os

# Load uploaded CSV files
try:
    if uploaded_files and all(k in uploaded_files for k in ['train', 'test', 'oot']):
        # Use uploaded files
        train_data = pd.read_csv(uploaded_files['train'])
        test_data = pd.read_csv(uploaded_files['test'])
        oot_data = pd.read_csv(uploaded_files['oot'])
        
        print(f"✅ Loaded uploaded data:")
        print(f"   Train: {len(train_data)} rows")
        print(f"   Test: {len(test_data)} rows")
        print(f"   OOT: {len(oot_data)} rows")
    else:
        # Fallback to sample data for testing
        print("⚠️  No uploaded files found, using sample data")
        train_data = generate_sample_data(1000, backend_model_type)
        test_data = generate_sample_data(500, backend_model_type)
        oot_data = generate_sample_data(300, backend_model_type)
        
except Exception as e:
    print(f"❌ Error loading uploaded files: {str(e)}")
    print("⚠️  Falling back to sample data")
    train_data = generate_sample_data(1000, backend_model_type)
    test_data = generate_sample_data(500, backend_model_type)
    oot_data = generate_sample_data(300, backend_model_type)
```

### Change #3: Update Frontend to Pass File Paths

**File**: `frontend/src/App.jsx`  
**Function**: `handleStartValidation()`

**Current**:
```javascript
const response = await axios.post(`${API_BASE_URL}/api/v1/validate`, {
  model_config: modelConfig,
  generate_document: true,
  register_governance: true
});
```

**Required**:
```javascript
const response = await axios.post(`${API_BASE_URL}/api/v1/validate`, {
  model_config: modelConfig,
  uploaded_files: {
    train: uploadedDocuments.find(d => d.type === 'train')?.path,
    test: uploadedDocuments.find(d => d.type === 'test')?.path,
    oot: uploadedDocuments.find(d => d.type === 'oot')?.path
  },
  generate_document: true,
  register_governance: true
});
```

### Change #4: Update Document Upload to Store File Paths

**File**: `backend/main_simple.py`  
**Function**: `upload_documents()` (Lines 965-996)

**Current**: Stores files but doesn't return paths in a structured way

**Required**: Return file paths mapped to dataset types
```python
@app.post("/api/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    uploaded_files = {}
    
    for file in files:
        # ... save file logic ...
        
        # Determine dataset type from filename
        if 'train' in file.filename.lower():
            uploaded_files['train'] = file_path
        elif 'test' in file.filename.lower():
            uploaded_files['test'] = file_path
        elif 'oot' in file.filename.lower() or 'out_of_time' in file.filename.lower():
            uploaded_files['oot'] = file_path
    
    return {
        "message": "Files uploaded successfully",
        "files": uploaded_files  # ← Return structured paths
    }
```

---

## 📋 Implementation Checklist

### Phase 1: Backend Changes (2-3 hours)
- [ ] Update `start_validation_v1()` to accept `uploaded_files` parameter
- [ ] Add CSV file loading logic with error handling
- [ ] Add fallback to sample data for testing
- [ ] Update `upload_documents()` to return structured file paths
- [ ] Add file path validation
- [ ] Test with actual CSV files

### Phase 2: Frontend Changes (1-2 hours)
- [ ] Update `handleStartValidation()` to pass file paths
- [ ] Ensure `uploadedDocuments` state includes file paths
- [ ] Add validation to ensure all 3 files uploaded before validation
- [ ] Update UI to show which files will be used
- [ ] Test end-to-end workflow

### Phase 3: Testing (2 hours)
- [ ] Test with sample CSV files
- [ ] Test with missing files (should use sample data)
- [ ] Test with invalid CSV format
- [ ] Test with different file sizes
- [ ] Verify validation results match actual data

### Phase 4: Documentation (1 hour)
- [ ] Update API documentation
- [ ] Update user guide
- [ ] Add CSV format requirements
- [ ] Document fallback behavior

**Total Estimated Time**: 6-8 hours

---

## 🎯 Priority Assessment

### Why This is Important:
1. **Core Functionality**: Users expect to validate their actual models
2. **Data Accuracy**: Results must reflect real model performance
3. **User Trust**: Fake data undermines system credibility
4. **Production Readiness**: Cannot deploy without this feature

### Current Workaround:
- System works for demonstration purposes with sample data
- Can show UI/UX and data flow
- Cannot validate real production models

### Recommendation:
**Implement in Phase 2** (Week 2) as a high-priority enhancement

**Rationale**:
- Week 1 focused on core validation logic and data consistency fixes
- All critical data mismatch issues are now resolved
- System is stable and ready for this enhancement
- Better to implement properly with full testing than rush it

---

## 📝 Expected CSV File Format

### Required Columns:
```csv
# train.csv, test.csv, oot.csv
score,age,income,target,prediction
650,35,50000,0,0.2
720,42,75000,1,0.8
580,28,35000,0,0.3
...
```

### Column Descriptions:
- **score**: Model score (numeric)
- **age**: Customer age (numeric)
- **income**: Customer income (numeric)
- **target**: Actual outcome (0 or 1)
- **prediction**: Model prediction probability (0-1)

### Validation Rules:
- All 3 files must be present (train, test, oot)
- Files must be CSV format
- Must contain required columns
- No missing values in key columns
- target must be binary (0 or 1)
- prediction must be between 0 and 1

---

## 🔄 Migration Path

### Option 1: Immediate Implementation (Recommended for Week 2)
1. Implement all changes in one go
2. Test thoroughly
3. Deploy as v2.1.0

### Option 2: Gradual Migration
1. Add file loading logic with fallback
2. Test in parallel with sample data
3. Gradually phase out sample data generation

### Option 3: Feature Flag
1. Add configuration flag: `USE_UPLOADED_DATA`
2. Allow switching between modes
3. Useful for testing and demos

**Recommendation**: Option 1 for clean implementation

---

## 📊 Impact Analysis

### What Works Now:
- ✅ UI for file upload
- ✅ File storage on backend
- ✅ Validation logic (on sample data)
- ✅ Results display
- ✅ Report generation
- ✅ Data consistency across components

### What Needs Work:
- ❌ Loading uploaded CSV files
- ❌ Passing file paths from frontend
- ❌ CSV format validation
- ❌ Error handling for bad data
- ❌ Documentation for CSV requirements

### Risk Assessment:
- **Low Risk**: Changes are isolated to data loading
- **High Value**: Enables actual model validation
- **Clear Path**: Well-defined requirements and implementation

---

## ✅ Success Criteria

After implementation, the system should:
1. ✅ Load and validate uploaded CSV files
2. ✅ Run validation on actual model data
3. ✅ Display results based on real data
4. ✅ Generate reports with actual metrics
5. ✅ Handle errors gracefully
6. ✅ Fall back to sample data if needed
7. ✅ Provide clear feedback to users

---

## 📝 Next Steps

### Immediate (This Session):
1. ✅ Document the gap (this file)
2. ✅ Add to issues tracker
3. ✅ Prioritize for Week 2

### Week 2 (Phase 2):
1. Implement backend CSV loading
2. Update frontend to pass file paths
3. Add comprehensive testing
4. Update documentation
5. Deploy as v2.1.0

### Testing Plan:
1. Create sample CSV files with known values
2. Upload and validate
3. Verify results match expected values
4. Test edge cases (missing files, bad format, etc.)
5. Performance testing with large files

---

**Status**: ⚠️ GAP IDENTIFIED - Scheduled for Week 2 Implementation

**Priority**: HIGH - Core functionality for production use

**Estimated Effort**: 6-8 hours (1 day)

**Dependencies**: None - can be implemented independently

**Blocker**: No - system works with sample data for now