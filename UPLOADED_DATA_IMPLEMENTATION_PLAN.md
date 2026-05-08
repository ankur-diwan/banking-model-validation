# Uploaded Data Integration - Implementation Plan

**Date**: May 7, 2026  
**Status**: READY TO IMPLEMENT  
**Estimated Time**: 2-3 hours

---

## 🎯 Implementation Strategy

We'll implement this in 3 phases with testing after each phase:

1. **Phase 1**: Backend - Update upload endpoint to return structured file paths
2. **Phase 2**: Backend - Update validation endpoint to load CSV files
3. **Phase 3**: Frontend - Pass file paths to validation endpoint

---

## 📋 Phase 1: Update Upload Endpoint (30 minutes)

### File: `backend/main_simple.py`
### Function: `upload_documents()` (Lines 965-996)

### Current Behavior:
- Saves files to uploads/ directory
- Returns list of uploaded files
- Doesn't map files to dataset types

### Required Changes:
```python
@app.post("/api/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload model documentation and CSV data files
    Returns structured file paths mapped to dataset types
    """
    try:
        uploaded_files = {
            'documents': [],
            'datasets': {}  # ← NEW: Map dataset types to file paths
        }
        
        for file in files:
            # Save file logic (existing)
            file_path = f"uploads/{file.filename}"
            
            # Determine file type
            if file.filename.endswith('.csv'):
                # Map to dataset type based on filename
                if 'train' in file.filename.lower():
                    uploaded_files['datasets']['train'] = file_path
                elif 'test' in file.filename.lower():
                    uploaded_files['datasets']['test'] = file_path
                elif 'oot' in file.filename.lower() or 'out_of_time' in file.filename.lower():
                    uploaded_files['datasets']['oot'] = file_path
            else:
                # PDF/DOCX documents
                uploaded_files['documents'].append({
                    'filename': file.filename,
                    'path': file_path
                })
        
        return {
            "message": "Files uploaded successfully",
            "files": uploaded_files  # ← Return structured data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Testing Phase 1:
```bash
# Test upload endpoint
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@train.csv" \
  -F "files=@test.csv" \
  -F "files=@oot.csv"

# Expected response:
{
  "message": "Files uploaded successfully",
  "files": {
    "documents": [],
    "datasets": {
      "train": "uploads/train.csv",
      "test": "uploads/test.csv",
      "oot": "uploads/oot.csv"
    }
  }
}
```

---

## 📋 Phase 2: Update Validation Endpoint (1-1.5 hours)

### File: `backend/main_simple.py`
### Function: `start_validation_v1()` (Lines 224-393)

### Current Code (Lines 273-275):
```python
# Generate sample data
train_data = generate_sample_data(1000, backend_model_type)
test_data = generate_sample_data(500, backend_model_type)
oot_data = generate_sample_data(300, backend_model_type)
```

### Required Changes:
```python
import pandas as pd
import os

# Get uploaded file paths from request
uploaded_files = request.get("uploaded_files", {})
datasets_paths = uploaded_files.get("datasets", {})

# Load data from uploaded CSV files or generate sample data
try:
    if datasets_paths and all(k in datasets_paths for k in ['train', 'test', 'oot']):
        # ✅ Load uploaded CSV files
        print(f"\n📂 Loading uploaded CSV files...")
        
        train_data = pd.read_csv(datasets_paths['train'])
        test_data = pd.read_csv(datasets_paths['test'])
        oot_data = pd.read_csv(datasets_paths['oot'])
        
        print(f"✅ Loaded uploaded data:")
        print(f"   Train: {len(train_data)} rows, {len(train_data.columns)} columns")
        print(f"   Test: {len(test_data)} rows, {len(test_data.columns)} columns")
        print(f"   OOT: {len(oot_data)} rows, {len(oot_data.columns)} columns")
        
        # Validate required columns
        required_columns = ['score', 'age', 'income', 'target', 'prediction']
        for dataset_name, data in [('train', train_data), ('test', test_data), ('oot', oot_data)]:
            missing_cols = [col for col in required_columns if col not in data.columns]
            if missing_cols:
                raise ValueError(f"{dataset_name} dataset missing columns: {missing_cols}")
        
        print(f"✅ All required columns present in uploaded data\n")
        
    else:
        # ⚠️  Fallback to sample data
        print(f"\n⚠️  No uploaded files found or incomplete dataset")
        print(f"   Using generated sample data for testing\n")
        
        train_data = generate_sample_data(1000, backend_model_type)
        test_data = generate_sample_data(500, backend_model_type)
        oot_data = generate_sample_data(300, backend_model_type)
        
except FileNotFoundError as e:
    print(f"\n❌ Error: Uploaded file not found: {str(e)}")
    print(f"   Falling back to sample data\n")
    
    train_data = generate_sample_data(1000, backend_model_type)
    test_data = generate_sample_data(500, backend_model_type)
    oot_data = generate_sample_data(300, backend_model_type)
    
except ValueError as e:
    print(f"\n❌ Error: Invalid CSV format: {str(e)}")
    print(f"   Falling back to sample data\n")
    
    train_data = generate_sample_data(1000, backend_model_type)
    test_data = generate_sample_data(500, backend_model_type)
    oot_data = generate_sample_data(300, backend_model_type)
    
except Exception as e:
    print(f"\n❌ Unexpected error loading uploaded files: {str(e)}")
    print(f"   Falling back to sample data\n")
    
    train_data = generate_sample_data(1000, backend_model_type)
    test_data = generate_sample_data(500, backend_model_type)
    oot_data = generate_sample_data(300, backend_model_type)
```

### Testing Phase 2:
```bash
# Test validation with uploaded files
curl -X POST http://localhost:8000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "model_config": {
      "model_name": "Test_Model",
      "scorecard_type": "application"
    },
    "uploaded_files": {
      "datasets": {
        "train": "uploads/train.csv",
        "test": "uploads/test.csv",
        "oot": "uploads/oot.csv"
      }
    }
  }'

# Check backend logs for:
# ✅ "Loading uploaded CSV files..."
# ✅ "Loaded uploaded data: Train: X rows..."
```

---

## 📋 Phase 3: Update Frontend (30-45 minutes)

### File: `frontend/src/App.jsx`
### Function: `handleStartValidation()`

### Current Code:
```javascript
const response = await axios.post(`${API_BASE_URL}/api/v1/validate`, {
  model_config: modelConfig,
  generate_document: true,
  register_governance: true
});
```

### Required Changes:
```javascript
const handleStartValidation = async () => {
  try {
    setLoading(true);
    setError(null);
    
    // Check if CSV files are uploaded
    const trainFile = uploadedDocuments.find(d => 
      d.name.toLowerCase().includes('train') && d.name.endsWith('.csv')
    );
    const testFile = uploadedDocuments.find(d => 
      d.name.toLowerCase().includes('test') && d.name.endsWith('.csv')
    );
    const ootFile = uploadedDocuments.find(d => 
      (d.name.toLowerCase().includes('oot') || d.name.toLowerCase().includes('out_of_time')) 
      && d.name.endsWith('.csv')
    );
    
    // Build uploaded_files object
    const uploaded_files = {};
    if (trainFile && testFile && ootFile) {
      uploaded_files.datasets = {
        train: `uploads/${trainFile.name}`,
        test: `uploads/${testFile.name}`,
        oot: `uploads/${ootFile.name}`
      };
      console.log('✅ Using uploaded CSV files:', uploaded_files.datasets);
    } else {
      console.log('⚠️  CSV files not found, backend will use sample data');
    }
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/validate`, {
      model_config: modelConfig,
      uploaded_files: uploaded_files,  // ← NEW
      generate_document: true,
      register_governance: true
    });
    
    console.log('Validation started:', response.data);
    setValidationId(response.data.validation_id);
    handleNext();
  } catch (err) {
    console.error('Validation start error:', err);
    setError(err.response?.data?.detail || err.message || 'Failed to start validation');
  } finally {
    setLoading(false);
  }
};
```

### Testing Phase 3:
1. Upload 3 CSV files (train.csv, test.csv, oot.csv)
2. Configure model settings
3. Start validation
4. Check browser console for: "✅ Using uploaded CSV files"
5. Check backend logs for: "✅ Loaded uploaded data"
6. Verify results are based on actual data

---

## 📊 CSV File Format Requirements

### Required Columns:
```csv
score,age,income,target,prediction
650,35,50000,0,0.2
720,42,75000,1,0.8
580,28,35000,0,0.3
```

### Column Descriptions:
- **score**: Model score (numeric, typically 300-850)
- **age**: Customer age (numeric, typically 18-100)
- **income**: Customer income (numeric, positive)
- **target**: Actual outcome (0 or 1, binary)
- **prediction**: Model prediction probability (0.0 to 1.0)

### Validation Rules:
- All 3 files must be present (train, test, oot)
- Files must be CSV format with header row
- Must contain all 5 required columns
- No missing values in required columns
- target must be binary (0 or 1)
- prediction must be between 0 and 1

---

## 🧪 Complete Testing Workflow

### Test 1: With Uploaded Files
```
1. Upload train.csv, test.csv, oot.csv
2. Configure model (Application Scorecard)
3. Start validation
4. Expected: Backend logs "✅ Loaded uploaded data"
5. Expected: Results based on actual CSV data
6. Verify: Dashboard shows correct metrics
7. Verify: Report matches dashboard
```

### Test 2: Without Uploaded Files
```
1. Don't upload any CSV files
2. Configure model
3. Start validation
4. Expected: Backend logs "⚠️  Using generated sample data"
5. Expected: Results based on sample data
6. Verify: System still works (fallback)
```

### Test 3: With Invalid CSV
```
1. Upload CSV with missing columns
2. Start validation
3. Expected: Backend logs "❌ Error: Invalid CSV format"
4. Expected: Falls back to sample data
5. Verify: System handles error gracefully
```

### Test 4: With Partial Upload
```
1. Upload only train.csv and test.csv (missing oot.csv)
2. Start validation
3. Expected: Backend logs "⚠️  Incomplete dataset"
4. Expected: Falls back to sample data
5. Verify: System requires all 3 files
```

---

## 🔄 Rollback Plan

If issues occur:
1. Revert backend changes: `git checkout backend/main_simple.py`
2. Revert frontend changes: `git checkout frontend/src/App.jsx`
3. System will work with sample data as before
4. No data loss or corruption

---

## ✅ Success Criteria

After implementation:
- [ ] Upload endpoint returns structured file paths
- [ ] Validation endpoint loads CSV files when available
- [ ] Validation falls back to sample data if files missing
- [ ] Frontend passes file paths to backend
- [ ] Results based on actual uploaded data
- [ ] Error handling works for all edge cases
- [ ] Backend logs clearly indicate data source
- [ ] All existing functionality still works

---

## 📝 Implementation Checklist

### Backend Phase 1:
- [ ] Update `upload_documents()` function
- [ ] Add dataset type mapping logic
- [ ] Return structured file paths
- [ ] Test upload endpoint

### Backend Phase 2:
- [ ] Add pandas import (already present)
- [ ] Extract uploaded_files from request
- [ ] Add CSV loading logic with try/except
- [ ] Add column validation
- [ ] Add fallback to sample data
- [ ] Add comprehensive logging
- [ ] Test validation endpoint

### Frontend Phase 3:
- [ ] Update `handleStartValidation()` function
- [ ] Find uploaded CSV files from state
- [ ] Build uploaded_files object
- [ ] Pass to validation endpoint
- [ ] Add console logging
- [ ] Test end-to-end workflow

### Testing:
- [ ] Test with valid CSV files
- [ ] Test without CSV files
- [ ] Test with invalid CSV
- [ ] Test with partial upload
- [ ] Verify results accuracy
- [ ] Check error handling

### Documentation:
- [ ] Update API documentation
- [ ] Document CSV format requirements
- [ ] Add user guide section
- [ ] Update README

---

**Ready to implement**: Yes  
**Estimated time**: 2-3 hours  
**Risk level**: Low (has fallback to sample data)  
**Breaking changes**: None (backward compatible)