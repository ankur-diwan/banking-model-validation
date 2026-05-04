# UI Testing Guide - Banking Model Validation System

## 🎯 Overview
This guide will help you test the newly enhanced Banking Model Validation System with the 5-step workflow including document upload and enhanced results display.

---

## ✅ Pre-Testing Checklist

### 1. Verify Services are Running

#### Backend (Port 8000)
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/backend
python main.py
# OR if using uvicorn
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Frontend (Port 3000 or 5173)
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/frontend
npm run dev
```

**Expected Output**:
```
VITE v4.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 2. Verify API Health
Open browser: `http://localhost:8000/docs`
- Should see Swagger UI with all API endpoints
- Test `/api/health` endpoint - should return `{"status": "healthy"}`

### 3. Access Frontend
Open browser: `http://localhost:5173` (or 3000)
- Should see "Banking Model Validation System" header
- Should see 5-step stepper at top

---

## 🧪 Test Scenarios

### Test Scenario 1: Complete Workflow (No Document Upload)

#### Step 0: Upload Documents (Optional)
1. **Action**: Click "Next" without uploading any documents
2. **Expected**: Should proceed to Step 1 (document upload is optional)
3. **Status**: ✅ Pass / ❌ Fail

#### Step 1: Select Model Configuration
1. **Fill in the form**:
   - Model Name: `US_Credit_Card_Application_v1`
   - Product Type: Select `unsecured`
   - Scorecard Type: Select `application`
   - Model Type: Select `GLM` (or any available)
   - Description: `Test application scorecard for credit cards`
   - Version: `1.0` (default)
   - Owner: `Model Risk Management` (default)

2. **Action**: Click "Next"
3. **Expected**: Should proceed to Step 2 (Review & Submit)
4. **Status**: ✅ Pass / ❌ Fail

#### Step 2: Review & Submit
1. **Verify**: All entered information is displayed correctly
2. **Action**: Click "Start Validation"
3. **Expected**: 
   - Button shows loading spinner
   - Proceeds to Step 3 (Validation Progress)
4. **Status**: ✅ Pass / ❌ Fail

#### Step 3: Validation Progress
1. **Expected**:
   - Progress bar animating
   - Status shows "in_progress" or "running"
   - List of validation steps displayed
   - Polling every 3 seconds for status updates
2. **Wait**: 2-5 minutes for validation to complete
3. **Expected**: Automatically proceeds to Step 4 when complete
4. **Status**: ✅ Pass / ❌ Fail

#### Step 4: Results
1. **Verify Overall Summary Cards**:
   - Overall Status card (with icon and chip)
   - Performance card
   - Stability card
   - Compliance card with score percentage

2. **Verify Statistical Tests Section** (Accordion):
   - KS Test card with:
     - KS Statistic value
     - Interpretation text
     - Status chip (passed/warning/failed)
   - Gini Coefficient card with:
     - Gini score
     - Interpretation text
     - Status chip

3. **Verify Performance Metrics Section** (Accordion):
   - Table with Train/Test/OOT columns
   - Metrics: Accuracy, Precision, Recall, F1, AUC-ROC
   - Status chips for each metric

4. **Verify Stability Analysis Section** (Accordion):
   - PSI card with:
     - PSI score
     - Interpretation
     - Progress bar
     - Status chip
   - CSI card with:
     - Average CSI
     - Interpretation
     - Progress bar
     - Status chip

5. **Verify SR 11-7 Compliance Section** (Accordion):
   - Overall compliance score with progress bar
   - Status chip
   - Category table with scores and weights
   - Gap analysis (if score < 80%)

6. **Verify Model-Specific Section** (Accordion):
   - Model type displayed
   - Checks table with results and status

7. **Verify Download Button**:
   - "Download Validation Report" button visible
   - Click button
   - Expected: DOCX file downloads

8. **Action**: Click "Start New Validation"
9. **Expected**: Returns to Step 0
10. **Status**: ✅ Pass / ❌ Fail

---

### Test Scenario 2: With Document Upload

#### Step 0: Upload Documents
1. **Prepare Test Files**:
   - Create a test PDF file (any PDF)
   - Create a test DOCX file (any Word document)
   - Create a test CSV file (any CSV)

2. **Test Drag-and-Drop**:
   - Drag a PDF file into the upload zone
   - **Expected**: 
     - File appears in the list
     - Status shows "Pending"
     - File icon matches type (red for PDF)
   - **Status**: ✅ Pass / ❌ Fail

3. **Test File Selection**:
   - Click the upload zone
   - Select a DOCX file from file picker
   - **Expected**: File added to list
   - **Status**: ✅ Pass / ❌ Fail

4. **Test File Validation**:
   - Try uploading a file > 10MB
   - **Expected**: Error message displayed
   - Try uploading an unsupported file type (.txt, .jpg)
   - **Expected**: Error message displayed
   - **Status**: ✅ Pass / ❌ Fail

5. **Test File Management**:
   - Click delete icon on a file
   - **Expected**: File removed from list
   - Add multiple files
   - Click "Clear All"
   - **Expected**: All files removed
   - **Status**: ✅ Pass / ❌ Fail

6. **Test Upload**:
   - Add 2-3 valid files
   - Click "Upload Files" button
   - **Expected**:
     - Progress bar shows upload progress
     - Files status changes to "Uploaded" with green chip
     - Success message displayed
   - **Status**: ✅ Pass / ❌ Fail

7. **Verify Summary Cards**:
   - Total Files card shows correct count
   - Uploaded card shows correct count
   - Total Size card shows correct size
   - **Status**: ✅ Pass / ❌ Fail

8. **Action**: Click "Next"
9. **Expected**: Proceeds to Step 1
10. **Status**: ✅ Pass / ❌ Fail

#### Continue with Steps 1-4 as in Scenario 1

---

### Test Scenario 3: Different Model Types

Test each scorecard type to verify model-specific validation:

#### A. Application Scorecard
- Product Type: `unsecured`
- Scorecard Type: `application`
- **Verify**: Application-specific checks in results

#### B. Behavioral Scorecard
- Product Type: `revolving`
- Scorecard Type: `behavioral`
- **Verify**: Behavioral-specific checks in results

#### C. Collections Early Stage
- Product Type: `unsecured`
- Scorecard Type: `collections_early`
- **Verify**: Collections early-stage checks in results

#### D. Collections Late Stage
- Product Type: `secured`
- Scorecard Type: `collections_late`
- **Verify**: Collections late-stage checks in results

---

## 🐛 Common Issues & Solutions

### Issue 1: Frontend Not Loading
**Symptoms**: Blank page or "Cannot GET /" error
**Solutions**:
1. Check if frontend dev server is running
2. Verify port (usually 5173 or 3000)
3. Check browser console for errors
4. Try clearing browser cache

### Issue 2: API Connection Failed
**Symptoms**: "Failed to load options" or network errors
**Solutions**:
1. Verify backend is running on port 8000
2. Check CORS configuration in backend
3. Verify `VITE_API_URL` in frontend `.env` file
4. Check browser network tab for failed requests

### Issue 3: Validation Stuck in Progress
**Symptoms**: Step 3 never completes
**Solutions**:
1. Check backend console for errors
2. Verify validation_orchestrator is working
3. Check if watsonx credentials are configured
4. Look for Python errors in backend logs

### Issue 4: Results Not Displaying
**Symptoms**: Step 4 shows "No validation results available"
**Solutions**:
1. Check if validation completed successfully
2. Verify API response structure matches component expectations
3. Check browser console for JavaScript errors
4. Verify ValidationResults component is receiving data

### Issue 5: Document Upload Fails
**Symptoms**: Upload button doesn't work or shows error
**Solutions**:
1. Verify `/api/upload-documents` endpoint exists
2. Check file size (must be < 10MB)
3. Check file type (PDF, DOCX, CSV only)
4. Verify backend has write permissions for uploads directory

---

## 📊 Test Results Template

### Test Execution Summary

| Test Scenario | Status | Notes |
|--------------|--------|-------|
| Scenario 1: Complete Workflow (No Upload) | ⏳ | |
| - Step 0: Skip Upload | ⏳ | |
| - Step 1: Model Config | ⏳ | |
| - Step 2: Review & Submit | ⏳ | |
| - Step 3: Validation Progress | ⏳ | |
| - Step 4: Results Display | ⏳ | |
| Scenario 2: With Document Upload | ⏳ | |
| - Drag-and-Drop | ⏳ | |
| - File Validation | ⏳ | |
| - File Management | ⏳ | |
| - Upload Process | ⏳ | |
| Scenario 3: Different Model Types | ⏳ | |
| - Application Scorecard | ⏳ | |
| - Behavioral Scorecard | ⏳ | |
| - Collections Early | ⏳ | |
| - Collections Late | ⏳ | |

### Component Testing

| Component | Feature | Status | Notes |
|-----------|---------|--------|-------|
| DocumentUpload | Drag-and-drop | ⏳ | |
| DocumentUpload | File validation | ⏳ | |
| DocumentUpload | Upload progress | ⏳ | |
| DocumentUpload | File management | ⏳ | |
| ValidationResults | Overall summary | ⏳ | |
| ValidationResults | Statistical tests | ⏳ | |
| ValidationResults | Performance metrics | ⏳ | |
| ValidationResults | Stability analysis | ⏳ | |
| ValidationResults | Compliance display | ⏳ | |
| ValidationResults | Model-specific | ⏳ | |
| App | 5-step navigation | ⏳ | |
| App | State management | ⏳ | |
| App | Error handling | ⏳ | |

---

## 🎬 Next Steps After Testing

### If All Tests Pass ✅
1. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Days 5-6: Backend integration and frontend enhancements complete"
   ```

2. **Create Summary Document**:
   - Document any issues found and fixed
   - Take screenshots of working features
   - Note performance metrics

3. **Proceed to Day 7 Tasks**:
   - Update API documentation
   - Create user guide
   - Prepare for deployment

### If Tests Fail ❌
1. **Document Issues**:
   - Screenshot of error
   - Browser console logs
   - Backend error logs
   - Steps to reproduce

2. **Debug and Fix**:
   - Identify root cause
   - Apply fixes
   - Re-test

3. **Update Code**:
   - Commit fixes
   - Update documentation

---

## 📝 Testing Checklist

### Before Starting
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173/3000
- [ ] API health check passes
- [ ] Browser console open for debugging
- [ ] Test files prepared (PDF, DOCX, CSV)

### During Testing
- [ ] Test each step sequentially
- [ ] Document any errors immediately
- [ ] Take screenshots of key features
- [ ] Note performance issues
- [ ] Test edge cases

### After Testing
- [ ] Fill out test results template
- [ ] Document all issues found
- [ ] Create bug reports if needed
- [ ] Update TODO list
- [ ] Prepare for next phase

---

## 🚀 Ready to Test!

**Current Status**: 
- ✅ Backend: All validators integrated
- ✅ Frontend: All components created
- ✅ Integration: Orchestrator updated
- ⏳ Testing: Ready to begin

**What to Test**:
1. Start with Scenario 1 (no upload) - simplest path
2. Then test Scenario 2 (with upload) - full features
3. Finally test Scenario 3 (different models) - comprehensive

**Expected Duration**: 30-45 minutes for complete testing

**Support**: If you encounter issues, check the "Common Issues & Solutions" section first.

---

**Happy Testing! 🎉**

*Made with ❤️ by Bob*