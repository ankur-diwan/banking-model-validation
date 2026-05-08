# Uploaded Data Integration - Debug Status

## Current Situation (May 8, 2026 - 11:37 AM IST)

### Problem
Uploaded CSV files are NOT being used for validation. System generates sample data instead, resulting in poor metrics (KS: 0.0596, Gini: 0.0117) even when uploading high-quality test data.

### Root Cause Identified
Through systematic debugging using browser DevTools, we discovered:
1. **Upload response missing `datasets` field** - Backend was returning files array but not the structured datasets object
2. **Frontend state `uploadedDatasets` is null** - Because backend wasn't returning datasets
3. **Validation request missing `uploaded_files`** - Because uploadedDatasets state was null

### Fixes Applied

#### Backend Fix (main_simple.py)
✅ **Line 1081**: Added `"datasets": datasets` to upload endpoint response
```python
return {
    "status": "success",
    "files_uploaded": len(uploaded_files),
    "documents": uploaded_files,
    "datasets": datasets  # ← ADDED THIS
}
```

#### Frontend Code (Already Correct)
✅ **App.jsx lines 209-214**: Callback to receive datasets
✅ **App.jsx lines 147-165**: Logic to include uploaded_files in validation request
✅ **DocumentUpload.jsx line 180**: Passes datasets to callback

### Current Server Status

**Frontend**: ✅ Running (2 npm processes detected)
- Process 7913: Started at 7:12 PM
- Process 37126: Started at 11:46 AM
- **Action Needed**: Kill old process, keep only one

**Backend**: ❌ NOT Running
- No Python process found
- **Action Needed**: Start backend with updated code

### Next Steps

#### Step 1: Clean Up Frontend Processes
```bash
# Kill all npm dev processes
lsof -ti:3002 | xargs kill -9

# Start fresh
cd /Users/ad/workspace/banking-model-validation-code-engine/frontend
npm run dev
```

#### Step 2: Start Backend
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/backend
python main_simple.py
```

#### Step 3: Test Upload Workflow
1. Open browser: http://localhost:3002
2. **Hard refresh**: Cmd+Shift+R
3. Upload 3 CSV files from `test_samples/set1_successful/`
4. **Check Console** (F12 → Console tab):
   - Should see: "Documents uploaded: [...]"
   - Should see: "Datasets mapped: {train: '...', test: '...', oot: '...'}"
5. Click "Start Validation"
6. **Check Console again**:
   - Should see: "Uploaded datasets: {train: '...', test: '...', oot: '...'}"
   - Should see: "Including uploaded datasets in validation request..."

#### Step 4: Verify Backend Logs
Backend terminal should show:
```
DEBUG: uploaded_files = {'datasets': {'train': '/tmp/train.csv', ...}}
DEBUG: datasets_paths = {'train': '/tmp/train.csv', ...}
DEBUG: Has all required keys? True
Loading uploaded CSV files...
Successfully loaded uploaded CSV files
Train data shape: (2000, X)
Test data shape: (1000, X)
OOT data shape: (600, X)
```

#### Step 5: Verify Results
Validation results should show:
- **KS Statistic**: > 0.40 (currently 0.0596)
- **Gini Coefficient**: > 0.60 (currently 0.0117)
- **Overall Status**: PASS (currently FAIL)

### Test Data Available

**Set 1 - Successful** (`test_samples/set1_successful/`)
- Designed to PASS validation
- Expected: KS 0.40-0.50, Gini 0.60-0.70, PSI < 0.10

**Set 2 - Failed** (`test_samples/set2_failed/`)
- Designed to FAIL validation
- Expected: KS < 0.20, Gini < 0.30, PSI > 0.25

### Success Criteria

✅ Browser Console shows datasets being captured
✅ Browser Network tab shows uploaded_files in validation request
✅ Backend logs show "Loading uploaded CSV files..."
✅ Backend logs show correct row counts (2000/1000/600)
✅ Validation results show KS > 0.40, Gini > 0.60
✅ Overall status shows PASS

### Files Modified

1. `backend/main_simple.py` - Line 1081 (datasets in response)
2. `frontend/src/App.jsx` - Lines 209-214 (callback), 147-165 (validation request)
3. `frontend/src/components/DocumentUpload.jsx` - Line 180 (pass datasets)

### Documentation Created

1. `DEBUG_DATA_FLOW.md` - Systematic debugging guide
2. `test_samples/TEST_DATA_SETS_GUIDE.md` - Test data usage guide
3. `test_samples/INPUT_DATA_GUIDE.md` - Input data format guide
4. This file - Current status and action plan

### Manual Testing Commands

```bash
# Test upload endpoint
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set1_successful/train.csv" \
  -F "files=@test_samples/set1_successful/test.csv" \
  -F "files=@test_samples/set1_successful/oot.csv"

# Should return datasets object with file paths

# Test validation endpoint
curl -X POST http://localhost:8000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "model_config": {
      "model_name": "Test",
      "product_type": "unsecured_personal_loans",
      "scorecard_type": "application",
      "model_type": "logistic_regression"
    },
    "uploaded_files": {
      "datasets": {
        "train": "/tmp/train.csv",
        "test": "/tmp/test.csv",
        "oot": "/tmp/oot.csv"
      }
    }
  }'
```

### Timeline

- **May 7, 2026 6:30 PM**: Issue discovered
- **May 7, 2026 7:00 PM**: Root cause identified via browser DevTools
- **May 7, 2026 7:15 PM**: Backend fix applied
- **May 7, 2026 7:30 PM**: Backend restarted
- **May 7, 2026 7:40 PM**: Frontend cache issue identified
- **May 7, 2026 7:45 PM**: Frontend dev server stopped
- **May 8, 2026 11:37 AM**: Session resumed - servers need restart

### Ready to Test

All code fixes are in place. Just need to:
1. Clean up duplicate frontend processes
2. Start backend server
3. Test the complete workflow

The uploaded data integration should work once servers are properly restarted with the updated code.