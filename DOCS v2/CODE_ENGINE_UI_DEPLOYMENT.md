# IBM Cloud Code Engine UI Deployment Guide
# Banking Model Validation Application

This guide shows you how to deploy using the IBM Cloud Console UI instead of CLI commands.

---

## Prerequisites

Before starting, ensure you have:
1. IBM Cloud account with login access
2. Docker Desktop installed locally
3. Your watsonx credentials ready:
   - `WATSONX_API_KEY`
   - `WATSONX_PROJECT_ID`
   - `WATSONX_URL` (e.g., https://ca-tor.ml.cloud.ibm.com)

---

## Part 1: Create PostgreSQL Database

### Step 1: Navigate to Catalog
1. Log in to [IBM Cloud Console](https://cloud.ibm.com)
2. Click **Catalog** in the top menu
3. Search for **"Databases for PostgreSQL"**
4. Click on the service

### Step 2: Configure PostgreSQL
1. **Select a location**: Choose a region (e.g., Dallas, Toronto, etc.)
2. **Pricing plan**: Select appropriate plan (Lite for testing, Standard for production)
3. **Service name**: Enter `banking-validation-postgres`
4. **Resource group**: Select `COE Dev` or your preferred group
5. Click **Create**

### Step 3: Wait for Provisioning
- Wait 5-10 minutes for the database to provision
- Status will change from "Provisioning" to "Active"

### Step 4: Get Connection String
1. Click on your PostgreSQL instance
2. Go to **Service credentials** tab
3. Click **New credential** if none exists
4. Click **View credentials**
5. Copy the entire connection string that looks like:
   ```
   postgresql://ibm_cloud_xxx:password@host:port/ibmclouddb?sslmode=require
   ```
6. **Save this securely** - you'll need it later

---

## Part 2: Build and Push Docker Images

Since you don't have Container Registry permissions, we'll use an alternative approach.

### Option A: Request Container Registry Access (Recommended)

Ask your IBM Cloud administrator to:
1. Grant you **Manager** role on Container Registry
2. Or create a namespace for you and grant **Writer** access

Then follow the CLI steps in the original guide.

### Option B: Use Docker Hub (Alternative)

If you cannot get Container Registry access:

#### Step 1: Create Docker Hub Account
1. Go to [hub.docker.com](https://hub.docker.com)
2. Create a free account
3. Create a repository named `banking-validation-backend`
4. Create a repository named `banking-validation-frontend`

#### Step 2: Build Backend Image
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/backend
docker build -t yourdockerhubusername/banking-validation-backend:v1 .
docker login
docker push yourdockerhubusername/banking-validation-backend:v1
```

#### Step 3: Build Frontend Image (After Backend is Deployed)
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/frontend
docker build --build-arg VITE_API_URL=https://YOUR-BACKEND-URL -t yourdockerhubusername/banking-validation-frontend:v1 .
docker push yourdockerhubusername/banking-validation-frontend:v1
```

---

## Part 3: Create Code Engine Project

### Step 1: Navigate to Code Engine
1. In IBM Cloud Console, click the **Navigation menu** (☰)
2. Go to **Code Engine**
3. Click **Start creating** or **Create project**

### Step 2: Create Project
1. **Project name**: `banking-validation-ce`
2. **Location**: Select same region as your PostgreSQL (or nearby)
3. **Resource group**: Select `COE Dev`
4. Click **Create**

### Step 3: Wait for Project Creation
- Project will be created in 1-2 minutes
- You'll be taken to the project dashboard

---

## Part 4: Deploy Backend Application

### Step 1: Create Application
1. Inside your Code Engine project, click **Applications**
2. Click **Create**
3. Select **Container image**

### Step 2: Configure Backend Application

#### General Settings:
- **Application name**: `banking-validation-backend`
- **Code to run**: Select **Container image**

#### Image Settings:
- **Image reference**: 
  - If using Docker Hub: `docker.io/yourusername/banking-validation-backend:v1`
  - If using IBM Container Registry: `icr.io/namespace/banking-validation-backend:v1`
- **Registry access**: 
  - For Docker Hub: Click **Add registry** → Enter Docker Hub credentials
  - For IBM Container Registry: Select existing or create new

#### Resources:
- **CPU**: `1 vCPU`
- **Memory**: `2 GB`
- **Ephemeral storage**: `0.4 GB` (default)
- **Min instances**: `1`
- **Max instances**: `2`

#### Listening Port:
- **Port**: `8000`

### Step 3: Add Environment Variables
Click **Environment variables** tab and add:

| Name | Value |
|------|-------|
| `DATABASE_URL` | Your PostgreSQL connection string from Part 1 |
| `WATSONX_API_KEY` | Your watsonx API key |
| `WATSONX_PROJECT_ID` | Your watsonx project ID |
| `WATSONX_URL` | `https://ca-tor.ml.cloud.ibm.com` |
| `WATSONX_SPACE_ID` | Your space ID (if applicable) |
| `ENVIRONMENT` | `production` |
| `LOG_LEVEL` | `INFO` |

**Important**: Click the "lock" icon next to sensitive values like `DATABASE_URL` and `WATSONX_API_KEY` to make them secrets.

### Step 4: Create Application
1. Review all settings
2. Click **Create**
3. Wait 2-3 minutes for deployment

### Step 5: Get Backend URL
1. Once status shows **Ready**, click on the application name
2. Find the **Application URL** (looks like: `https://banking-validation-backend.xxx.us-east.codeengine.appdomain.cloud`)
3. **Copy this URL** - you need it for the frontend

### Step 6: Test Backend
1. Open a new browser tab
2. Go to: `https://YOUR-BACKEND-URL/health`
3. You should see:
   ```json
   {
     "status": "healthy",
     ...
   }
   ```

If you see an error, check the logs:
1. Go to your application in Code Engine
2. Click **Logging** tab
3. Review error messages

---

## Part 5: Deploy Frontend Application

### Step 1: Rebuild Frontend with Backend URL

**Important**: You must rebuild the frontend image with the actual backend URL.

```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/frontend

# Replace YOUR-BACKEND-URL with the actual URL from Part 4, Step 5
docker build \
  --build-arg VITE_API_URL=https://YOUR-BACKEND-URL \
  -t yourdockerhubusername/banking-validation-frontend:v1 .

docker push yourdockerhubusername/banking-validation-frontend:v1
```

### Step 2: Create Frontend Application
1. In Code Engine project, click **Applications**
2. Click **Create**
3. Select **Container image**

### Step 3: Configure Frontend Application

#### General Settings:
- **Application name**: `banking-validation-frontend`
- **Code to run**: Select **Container image**

#### Image Settings:
- **Image reference**: `docker.io/yourusername/banking-validation-frontend:v1`
- **Registry access**: Same as backend

#### Resources:
- **CPU**: `0.5 vCPU`
- **Memory**: `1 GB`
- **Min instances**: `1`
- **Max instances**: `2`

#### Listening Port:
- **Port**: `8080`

### Step 4: Create Application
1. Click **Create**
2. Wait 2-3 minutes for deployment

### Step 5: Get Frontend URL
1. Once status shows **Ready**, click on the application name
2. Find the **Application URL**
3. **Open this URL in your browser**

---

## Part 6: Test the Complete Application

### Step 1: Open Frontend
1. Open the frontend URL in your browser
2. You should see the Banking Model Validation interface

### Step 2: Run a Test Validation
1. Fill in the form:
   - **Model Name**: `demo-scorecard`
   - **Product Type**: `secured`
   - **Scorecard Type**: `application`
   - **Model Type**: `GLM`
   - **Description**: `Code Engine UI deployment test`
2. Click **Start Validation**
3. Wait for validation to complete
4. Check results and download document

### Step 3: Verify Everything Works
- ✅ Frontend loads without errors
- ✅ Validation starts successfully
- ✅ Results are displayed
- ✅ Document can be downloaded

---

## Troubleshooting

### Backend Health Check Fails

**Check logs:**
1. Go to Code Engine → Applications → banking-validation-backend
2. Click **Logging** tab
3. Look for errors

**Common issues:**
- Wrong `DATABASE_URL` format
- Invalid watsonx credentials
- Application still starting (wait 2-3 minutes)

### Frontend Cannot Connect to Backend

**Symptoms:**
- Frontend loads but shows errors
- Browser console shows network errors

**Solution:**
1. Verify backend URL is correct
2. Rebuild frontend image with correct `VITE_API_URL`
3. Update frontend application with new image

**To update frontend:**
1. Go to Code Engine → Applications → banking-validation-frontend
2. Click **Configuration** tab
3. Click **Edit and create new revision**
4. Update image reference if needed
5. Click **Save and create**

### Validation Fails

**Check:**
1. Backend logs for watsonx errors
2. Verify watsonx credentials are correct
3. Ensure watsonx project ID is valid
4. Check if watsonx service is accessible

### Permission Errors

If you see "not authorized" errors:
1. Contact your IBM Cloud account administrator
2. Request necessary permissions for:
   - Code Engine (Editor or Writer role)
   - Container Registry (Manager or Writer role)
   - Databases for PostgreSQL (Editor role)

---

## Monitoring and Management

### View Application Logs
1. Go to Code Engine → Applications
2. Click on application name
3. Click **Logging** tab
4. Use filters to find specific logs

### Scale Applications
1. Go to application
2. Click **Configuration** tab
3. Click **Edit and create new revision**
4. Adjust **Min instances** and **Max instances**
5. Click **Save and create**

### Update Application
1. Build new Docker image with updated code
2. Push to registry with new tag (e.g., `:v2`)
3. Go to application in Code Engine
4. Click **Configuration** → **Edit and create new revision**
5. Update image reference to new tag
6. Click **Save and create**

### Delete Resources
To clean up:
1. Delete applications: Code Engine → Applications → Select → Delete
2. Delete project: Code Engine → Projects → Select → Delete
3. Delete PostgreSQL: Resource list → Databases → Select → Delete

---

## Cost Optimization Tips

1. **Use minimum instances**: Set min to 0 for non-production to scale to zero
2. **Right-size resources**: Start small and increase if needed
3. **Use Lite tier**: For PostgreSQL during testing
4. **Monitor usage**: Check Code Engine dashboard for actual resource usage

---

## Security Best Practices

1. **Use secrets**: Always mark sensitive environment variables as secrets
2. **Rotate credentials**: Regularly update watsonx API keys
3. **Limit access**: Use IAM policies to restrict who can modify applications
4. **Enable logging**: Keep logs for audit and troubleshooting
5. **Use HTTPS**: Code Engine provides HTTPS by default

---

## Next Steps

After successful deployment:

1. **Add custom domain**: Configure your own domain name
2. **Set up monitoring**: Use IBM Cloud Monitoring service
3. **Configure alerts**: Set up notifications for failures
4. **Implement CI/CD**: Automate deployments using toolchains
5. **Add Object Storage**: Store validation documents persistently

---

## Summary of URLs You'll Have

After deployment, you'll have:

1. **PostgreSQL**: Connection string (keep secret)
2. **Backend URL**: `https://banking-validation-backend.xxx.codeengine.appdomain.cloud`
3. **Frontend URL**: `https://banking-validation-frontend.xxx.codeengine.appdomain.cloud`

**Share only the frontend URL with users.**

---

## Getting Help

If you encounter issues:

1. Check application logs in Code Engine
2. Review this guide's troubleshooting section
3. Contact your IBM Cloud administrator for permission issues
4. Check IBM Cloud status page for service outages
5. Review IBM Cloud Code Engine documentation

---

## Answer to Your Original Question

**Yes, having watsonx in a different region (Toronto) from Code Engine (us-east) will work perfectly fine.**

The backend application makes HTTPS API calls to watsonx, which works across regions. You may experience slightly higher latency (50-200ms), but functionality is not affected.

Choose your Code Engine region based on:
- Where your users are located
- Where your PostgreSQL database is
- Service availability in your account

**The cross-region setup is fully supported and commonly used.**