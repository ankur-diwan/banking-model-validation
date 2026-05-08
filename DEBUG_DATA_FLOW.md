# Data Flow Debugging Guide

## Problem
Uploaded CSV files are not being used for validation - system still generates sample data.

## Systematic Debugging Approach

### Step 1: Verify Frontend is Sending Data

Open browser console (F12) and check the network tab when you click "Start Validation":

1. Find the POST request to `/api/v1/validate`
2. Click on it and check the "Payload" or "Request" tab
3. **Look for**: `uploaded_files` object with `datasets` containing file paths

**Expected**:
```json
{
  "model_config": {...},
  "uploaded_files": {
    "datasets": {
      "train": "/tmp/train.csv",
      "test": "/tmp/test.csv",
      "oot": "/tmp/oot.csv"
    }
  }
}
```

**If missing**: Frontend is not passing the data
**If present**: Backend is not using the data

### Step 2: Check Backend Logs

Look at the terminal where backend is running. Search for:

```
DEBUG: uploaded_files = 
DEBUG: datasets_paths = 
DEBUG: Has all required keys?
```

**What to check**:
- Is `uploaded_files` empty `{}`?
- Is `datasets_paths` empty `{}`?
- Is "Has all required keys?" False?

### Step 3: Manual API Test

Test the upload endpoint directly:

```bash
# Upload files
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set1_successful/train.csv" \
  -F "files=@test_samples/set1_successful/test.csv" \
  -F "files=@test_samples/set1_successful/oot.csv"
```

**Check response** - should include:
```json
{
  "documents": [...],
  "datasets": {
    "train": "/tmp/train.csv",
    "test": "/tmp/test.csv",
    "oot": "/tmp/oot.csv"
  }
}
```

### Step 4: Manual Validation Test

```bash
# Test validation with explicit file paths
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

**Check backend logs** for:
- "Loading uploaded CSV files..."
- "Successfully loaded uploaded CSV files"
- Row counts (2000/1000/600)

## Likely Issues & Solutions

### Issue 1: Frontend Not Refreshed
**Symptom**: Browser still has old code
**Solution**: Hard refresh (Cmd+Shift+R) or clear cache

### Issue 2: Wrong Backend Running
**Symptom**: Changes not reflected
**Solution**: 
```bash
ps aux | grep python | grep main_simple
# Kill the process
kill -9 <PID>
# Restart
cd backend && python main_simple.py
```

### Issue 3: Frontend State Not Updated
**Symptom**: uploadedDatasets is null/empty
**Solution**: Check DocumentUpload callback is being called

### Issue 4: File Paths Don't Exist
**Symptom**: Files uploaded but paths invalid
**Solution**: Check /tmp/ directory has the files

## Quick Diagnostic Commands

```bash
# 1. Check if files exist in /tmp
ls -la /tmp/*.csv

# 2. Check backend process
ps aux | grep main_simple

# 3. Check backend port
lsof -i :8000

# 4. Test health endpoint
curl http://localhost:8000/api/health

# 5. Check frontend build
cd frontend && npm run build
```

## Next Steps Based on Findings

### If Frontend Issue:
1. Verify App.jsx has uploadedDatasets state
2. Verify handleDocumentsUploaded receives datasets
3. Verify handleSubmit includes uploaded_files in request
4. Check browser console for errors

### If Backend Issue:
1. Verify main_simple.py has debug logging
2. Verify upload endpoint returns "documents" not "files"
3. Verify validation endpoint checks uploaded_files.datasets
4. Check backend terminal for errors

### If Data Flow Issue:
1. Files upload successfully but paths not passed
2. Paths passed but backend can't read files
3. Files read but not used in validation
4. Validation uses files but metrics still wrong

## Contact Points for Help

1. **Frontend State**: Check `App.jsx` lines 45, 209-214
2. **Upload Response**: Check `DocumentUpload.jsx` line 180
3. **Backend Upload**: Check `main_simple.py` lines 1025-1081
4. **Backend Validation**: Check `main_simple.py` lines 277-335

## Success Criteria

✅ Browser network tab shows uploaded_files in request
✅ Backend logs show "Loading uploaded CSV files..."
✅ Backend logs show correct row counts (2000/1000/600)
✅ Validation results show KS > 0.40, Gini > 0.60
✅ Overall status shows PASS