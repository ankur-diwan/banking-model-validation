# Testing Guide: Uploaded Data Integration

## ✅ Servers Running Successfully!

**Backend**: http://localhost:8000 (PID: 26786)
**Frontend**: http://localhost:3002 (PID: 26838)

---

## 🧪 Test Procedure

### Step 1: Open Application
1. Open your browser
2. Navigate to: **http://localhost:3002**
3. **Hard refresh** the page: **Cmd+Shift+R** (Mac) or **Ctrl+Shift+R** (Windows)
   - This ensures you get the latest JavaScript code

### Step 2: Open Browser DevTools
1. Press **F12** or **Cmd+Option+I** (Mac)
2. Click on the **Console** tab
3. Keep this open during testing to see log messages

### Step 3: Upload Test Files
1. In the application, go to the **"Upload Model Documentation"** step
2. Upload these 3 files from `test_samples/set1_successful/`:
   - `train.csv` (87 KB, 2000 rows)
   - `test.csv` (44 KB, 1000 rows)
   - `oot.csv` (26 KB, 600 rows)

### Step 4: Check Console Logs (CRITICAL!)
After uploading, you should see in the Console:

```
Documents uploaded: (3) [{…}, {…}, {…}]
Datasets mapped: {train: "/tmp/train.csv", test: "/tmp/test.csv", oot: "/tmp/oot.csv"}
```

**✅ If you see this**: The upload is working correctly!
**❌ If you don't see this**: The frontend code isn't loaded. Try:
- Hard refresh again (Cmd+Shift+R)
- Clear browser cache
- Restart frontend server

### Step 5: Configure Model
1. Fill in the model configuration:
   - **Model Name**: Test Application Scorecard
   - **Product Type**: Unsecured Personal Loans
   - **Scorecard Type**: Application
   - **Model Type**: Logistic Regression

### Step 6: Start Validation
1. Click **"Start Validation"** button
2. **Check Console immediately** - you should see:

```
Starting validation with config: {…}
Uploaded datasets: {train: "/tmp/train.csv", test: "/tmp/test.csv", oot: "/tmp/oot.csv"}
Including uploaded datasets in validation request: {train: "/tmp/train.csv", test: "/tmp/test.csv", oot: "/tmp/oot.csv"}
```

**✅ If you see "Including uploaded datasets"**: Frontend is sending the data!
**❌ If you see "No uploaded datasets found"**: State issue - check if datasets were captured in Step 4

### Step 7: Check Backend Logs
Open a new terminal and run:
```bash
tail -f backend.log
```

You should see:
```
DEBUG: uploaded_files = {'datasets': {'train': '/tmp/train.csv', 'test': '/tmp/test.csv', 'oot': '/tmp/oot.csv'}}
DEBUG: datasets_paths = {'train': '/tmp/train.csv', 'test': '/tmp/test.csv', 'oot': '/tmp/oot.csv'}
DEBUG: Has all required keys? True
Loading uploaded CSV files...
Successfully loaded uploaded CSV files
Train data shape: (2000, X)
Test data shape: (1000, X)
OOT data shape: (600, X)
```

**✅ If you see "Loading uploaded CSV files"**: Backend is using your data!
**❌ If you see "Generating sample data"**: Backend didn't receive the file paths

### Step 8: Verify Results
Wait for validation to complete (2-3 minutes). Check the results:

**Expected Results with Set 1 (Successful) Data:**
- ✅ **KS Statistic**: 0.40 - 0.50 (currently shows 0.0596 with sample data)
- ✅ **Gini Coefficient**: 0.60 - 0.70 (currently shows 0.0117 with sample data)
- ✅ **PSI**: < 0.10 (stable)
- ✅ **Overall Status**: **PASS**

**If you still see poor metrics (KS < 0.10, Gini < 0.05):**
- The system is still using generated sample data
- Check Console and backend logs to see where the data flow broke

---

## 🔍 Troubleshooting

### Issue 1: Console is Blank
**Problem**: No log messages appear in Console
**Solution**:
```bash
# Restart frontend
lsof -ti:3002 | xargs kill -9
cd frontend && npm run dev
```
Then hard refresh browser (Cmd+Shift+R)

### Issue 2: "Datasets mapped: null"
**Problem**: Backend not returning datasets in upload response
**Solution**: Backend needs restart with updated code
```bash
lsof -ti:8000 | xargs kill -9
cd backend && python main_simple.py
```

### Issue 3: "No uploaded datasets found"
**Problem**: Frontend state not capturing datasets
**Check**:
1. Did you see "Datasets mapped: {...}" in Step 4?
2. If not, backend upload response is missing datasets
3. If yes, state is being reset - check for component remounting

### Issue 4: Backend Still Generates Sample Data
**Problem**: Backend not receiving uploaded_files in request
**Check**:
1. Browser Network tab → Find POST to `/api/v1/validate`
2. Click on it → Check "Payload" tab
3. Look for `uploaded_files` object
4. If missing, frontend isn't sending it (check Console logs)

---

## 📊 Test Data Sets

### Set 1: Successful Validation (`test_samples/set1_successful/`)
**Purpose**: Designed to PASS validation
**Characteristics**:
- Strong discrimination (KS 0.40-0.50, Gini 0.60-0.70)
- Stable populations (PSI < 0.10)
- Consistent default rates (10-11%)
- Good model performance

**Use this to verify**: Uploaded data integration is working

### Set 2: Failed Validation (`test_samples/set2_failed/`)
**Purpose**: Designed to FAIL validation
**Characteristics**:
- Weak discrimination (KS < 0.20, Gini < 0.30)
- Unstable populations (PSI > 0.25)
- Varying default rates (9-16%)
- Poor model performance

**Use this to verify**: System correctly identifies bad models

---

## ✅ Success Criteria Checklist

- [ ] Console shows "Documents uploaded" with 3 files
- [ ] Console shows "Datasets mapped" with file paths
- [ ] Console shows "Including uploaded datasets in validation request"
- [ ] Backend logs show "Loading uploaded CSV files..."
- [ ] Backend logs show correct row counts (2000/1000/600)
- [ ] Validation results show KS > 0.40
- [ ] Validation results show Gini > 0.60
- [ ] Overall status shows PASS

---

## 🎯 Quick Test Commands

### Test Upload Endpoint Directly
```bash
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set1_successful/train.csv" \
  -F "files=@test_samples/set1_successful/test.csv" \
  -F "files=@test_samples/set1_successful/oot.csv"
```

**Expected Response**:
```json
{
  "status": "success",
  "files_uploaded": 3,
  "documents": [...],
  "datasets": {
    "train": "/tmp/train.csv",
    "test": "/tmp/test.csv",
    "oot": "/tmp/oot.csv"
  }
}
```

### Test Validation with Explicit Paths
```bash
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

---

## 📝 What to Report

If the test fails, please provide:

1. **Console screenshot** showing log messages (or lack thereof)
2. **Network tab screenshot** showing the validation request payload
3. **Backend log excerpt** showing what the backend received
4. **Validation results** showing the metrics

This will help identify exactly where the data flow is breaking.

---

## 🎉 Expected Outcome

When everything works correctly:

1. ✅ Upload shows 3 files with "Uploaded" status
2. ✅ Console shows datasets with file paths
3. ✅ Validation request includes uploaded_files
4. ✅ Backend loads CSV files (not generates sample data)
5. ✅ Results show excellent metrics (KS 0.45, Gini 0.65)
6. ✅ Overall status: **PASS** ✨

**This proves the uploaded data integration is working!**

---

## 🔄 To Stop Servers

```bash
kill 26786 26838
```

Or use the startup script again - it will kill old processes automatically.

---

**Ready to test! Follow the steps above and let me know what you see in the Console.** 🚀