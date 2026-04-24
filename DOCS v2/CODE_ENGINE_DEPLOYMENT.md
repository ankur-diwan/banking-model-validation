# IBM Cloud Code Engine Deployment Guide for Banking Model Validation

This guide applies only to the copied deployment workspace:

`/Users/ad/workspace/banking-model-validation-code-engine`

Your original repository remains unchanged.

---

# 1. What you are deploying

You will deploy this application as **two separate IBM Cloud Code Engine applications**:

1. **Backend application**
   - FastAPI / Python app
   - Exposes APIs such as `/health` and `/api/v1/validate`
   - Connects to PostgreSQL
   - Connects to IBM watsonx

2. **Frontend application**
   - React/Vite UI
   - Built into static files
   - Served using nginx
   - Calls the backend through the backend public URL

You will also use:

3. **IBM Cloud Databases for PostgreSQL**
   - Managed PostgreSQL database
   - Replaces the local Docker Compose database

4. **IBM Cloud Container Registry**
   - Stores the backend and frontend container images

---

# 2. Architecture overview

Local development used:
- Docker Compose
- local PostgreSQL
- localhost URLs

IBM Cloud Code Engine deployment will use:
- Code Engine app for backend
- Code Engine app for frontend
- managed PostgreSQL
- public backend URL
- frontend built with backend URL embedded through `VITE_API_URL`

---

# 3. Changes already made in the copied workspace

The following changes were made only in the copied workspace:

## Frontend Dockerfile
File:
- `frontend/Dockerfile`

Change:
- converted from Vite development server to a production multi-stage build
- final container serves static files using nginx on port `8080`

## Frontend API base URL handling
Files:
- `frontend/src/services/api.js`
- `frontend/src/App.jsx`

Change:
- removed hardcoded fallback `http://localhost:8000`
- frontend now depends on `VITE_API_URL`

These changes are necessary for Code Engine.

---

# 4. Prerequisites

Before starting, make sure you have all of the following.

## 4.1 IBM Cloud account
You need:
- an IBM Cloud account
- permission to create services and apps
- billing enabled if you are creating paid services

## 4.2 IBM Cloud services you will create
You will need:
- **Code Engine**
- **Container Registry**
- **Databases for PostgreSQL**
- **watsonx.ai project and API key**

Optional but recommended later:
- **Cloud Object Storage** for persistent validation report storage

## 4.3 Software on your laptop
Install the following locally:

### Required
- Docker Desktop
- IBM Cloud CLI

### Recommended
- jq
- curl

### Check installations
Run:
```bash
docker --version
ibmcloud --version
curl --version
```

---

# 5. Install IBM Cloud CLI plugins

You need the Code Engine and Container Registry plugins.

Run:
```bash
ibmcloud plugin install code-engine
ibmcloud plugin install container-registry
```

Verify:
```bash
ibmcloud plugin list
```

You should see plugins similar to:
- `code-engine`
- `container-registry`

---

# 6. Decide your deployment region

You should preferably use a region close to:
- your PostgreSQL deployment
- your watsonx location
- your user base

Because your watsonx endpoint is Toronto, a Canada region alignment is generally easier if available for the services you choose.

To list available regions:
```bash
ibmcloud regions
```

Pick one region and use it consistently in later commands.

Example placeholder used in this guide:
- `<REGION>`

Example values could be:
- `ca-tor`
- `us-south`

Use the exact region supported in your IBM Cloud account and service catalog.

---

# 7. Log in to IBM Cloud

If you use SSO:
```bash
ibmcloud login -sso
```

If you use username/password:
```bash
ibmcloud login
```

After login, target the region:
```bash
ibmcloud target -r <REGION>
```

Check:
```bash
ibmcloud target
```

---

# 8. Select or create a resource group

IBM Cloud resources belong to a resource group.

List resource groups:
```bash
ibmcloud resource groups
```

If you already have one you want to use, select it:
```bash
ibmcloud target -g Default
```

If you want a dedicated one:
```bash
ibmcloud resource group-create banking-validation-rg
ibmcloud target -g banking-validation-rg
```

Verify:
```bash
ibmcloud target
```

---

# 9. Create a Container Registry namespace

Your Docker images must be pushed into IBM Cloud Container Registry.

## 9.1 Set registry region
```bash
ibmcloud cr region-set <REGION>
```

## 9.2 Log in to registry
```bash
ibmcloud cr login
```

## 9.3 Create namespace
Choose a namespace name. Example:
- `bankingvalidation`

Create it:
```bash
ibmcloud cr namespace-add bankingvalidation
```

List namespaces:
```bash
ibmcloud cr namespaces
```

You will use:
- `icr.io/bankingvalidation/...`

If your region uses a regional registry hostname, use the exact value shown by IBM Cloud.

---

# 10. Create a Code Engine project

A Code Engine project is the logical workspace where your apps run.

## 10.1 Create project
```bash
ibmcloud ce project create --name banking-validation-ce
```

## 10.2 Select the project
```bash
ibmcloud ce project select --name banking-validation-ce
```

## 10.3 Verify
```bash
ibmcloud ce project current
```

---

# 11. Provision IBM Cloud Databases for PostgreSQL

This will replace the local postgres container.

## 11.1 Create the service through IBM Cloud UI
If you are new, the UI is easier than CLI.

### Steps in UI
1. Log in to IBM Cloud Console
2. Search for **Databases for PostgreSQL**
3. Click **Create**
4. Choose:
   - the same resource group
   - a supported region
   - an instance name such as `banking-validation-postgres`
5. Choose a plan appropriate for your budget
6. Create the service

## 11.2 Open the service
After provisioning:
1. Go to the PostgreSQL service instance
2. Open **Overview**
3. Open **Connections**
4. Locate the connection information

## 11.3 Get the connection string
You need the PostgreSQL connection string for the backend environment variable:
- `DATABASE_URL`

It will typically look like:
```text
postgresql://username:password@host:port/database?sslmode=require
```

Important:
- use the exact database URL provided by IBM Cloud
- if SSL parameters are included, keep them
- do not use the local compose database URL

Save this value securely. You will use it during backend deployment.

---

# 12. Confirm your watsonx details

You already used watsonx locally, so gather the same details for Code Engine.

You will need:
- `WATSONX_API_KEY`
- `WATSONX_PROJECT_ID`
- `WATSONX_URL`
- optionally `WATSONX_SPACE_ID`

From your current setup, the likely URL is:
```text
https://ca-tor.ml.cloud.ibm.com
```

If your project is using a space, keep `WATSONX_SPACE_ID` available.
If not, deployment can still work with project ID only.

---

# 13. Backend container image build and push

Now build the backend image from the copied workspace.

## 13.1 Go to backend directory
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/backend
```

## 13.2 Build image
Replace `<NAMESPACE>` with your registry namespace.

Example:
```bash
docker build -t icr.io/<NAMESPACE>/banking-validation-backend:ce-v1 .
```

Example with real namespace:
```bash
docker build -t icr.io/bankingvalidation/banking-validation-backend:ce-v1 .
```

## 13.3 Push image
```bash
docker push icr.io/<NAMESPACE>/banking-validation-backend:ce-v1
```

## 13.4 Verify image exists
```bash
ibmcloud cr images
```

You should see the backend image listed.

---

# 14. Deploy backend to Code Engine

## 14.1 Create backend application
Replace placeholders before running:

- `<NAMESPACE>`
- `<POSTGRES_CONNECTION_STRING>`
- `<WATSONX_API_KEY>`
- `<WATSONX_PROJECT_ID>`
- `<WATSONX_SPACE_ID>` if used

Run:
```bash
ibmcloud ce application create \
  --name banking-validation-backend \
  --image icr.io/<NAMESPACE>/banking-validation-backend:ce-v1 \
  --port 8000 \
  --cpu 1 \
  --memory 2G \
  --min-scale 1 \
  --max-scale 2 \
  --env DATABASE_URL='<POSTGRES_CONNECTION_STRING>' \
  --env WATSONX_API_KEY='<WATSONX_API_KEY>' \
  --env WATSONX_PROJECT_ID='<WATSONX_PROJECT_ID>' \
  --env WATSONX_URL='https://ca-tor.ml.cloud.ibm.com' \
  --env WATSONX_SPACE_ID='<WATSONX_SPACE_ID>' \
  --env ENVIRONMENT='production' \
  --env LOG_LEVEL='INFO'
```

## 14.2 If you do not use WATSONX_SPACE_ID
You can omit it:
```bash
ibmcloud ce application create \
  --name banking-validation-backend \
  --image icr.io/<NAMESPACE>/banking-validation-backend:ce-v1 \
  --port 8000 \
  --cpu 1 \
  --memory 2G \
  --min-scale 1 \
  --max-scale 2 \
  --env DATABASE_URL='<POSTGRES_CONNECTION_STRING>' \
  --env WATSONX_API_KEY='<WATSONX_API_KEY>' \
  --env WATSONX_PROJECT_ID='<WATSONX_PROJECT_ID>' \
  --env WATSONX_URL='https://ca-tor.ml.cloud.ibm.com' \
  --env ENVIRONMENT='production' \
  --env LOG_LEVEL='INFO'
```

## 14.3 Wait for deployment
Check status:
```bash
ibmcloud ce application get --name banking-validation-backend
```

You are looking for:
- ready / deployed status
- a public application URL

## 14.4 Save backend URL
It will look something like:
```text
https://banking-validation-backend.<generated-subdomain>.<region>.codeengine.appdomain.cloud
```

You need this exact URL for the frontend build.

---

# 15. Verify backend first before frontend

Always verify the backend before building the frontend.

## 15.1 Health check
```bash
curl https://<BACKEND_URL>/health
```

Expected result:
```json
{
  "status": "healthy",
  ...
}
```

## 15.2 If health fails
Check logs:
```bash
ibmcloud ce application logs --name banking-validation-backend --follow
```

Common issues:
- wrong `DATABASE_URL`
- wrong `WATSONX_API_KEY`
- wrong `WATSONX_PROJECT_ID`
- unsupported region mismatch
- app still starting

---

# 16. Build frontend image with backend URL

The frontend must be built with the deployed backend URL.

## 16.1 Go to frontend directory
```bash
cd /Users/ad/workspace/banking-model-validation-code-engine/frontend
```

## 16.2 Build image
Use the real backend URL from step 14.

Example:
```bash
docker build \
  --build-arg VITE_API_URL=https://<BACKEND_URL> \
  -t icr.io/<NAMESPACE>/banking-validation-frontend:ce-v1 .
```

Example:
```bash
docker build \
  --build-arg VITE_API_URL=https://banking-validation-backend.<generated>.codeengine.appdomain.cloud \
  -t icr.io/bankingvalidation/banking-validation-frontend:ce-v1 .
```

## 16.3 Push image
```bash
docker push icr.io/<NAMESPACE>/banking-validation-frontend:ce-v1
```

## 16.4 Verify image
```bash
ibmcloud cr images
```

You should now see both:
- backend image
- frontend image

---

# 17. Deploy frontend to Code Engine

Create the frontend app:

```bash
ibmcloud ce application create \
  --name banking-validation-frontend \
  --image icr.io/<NAMESPACE>/banking-validation-frontend:ce-v1 \
  --port 8080 \
  --cpu 0.5 \
  --memory 1G \
  --min-scale 1 \
  --max-scale 2
```

Check status:
```bash
ibmcloud ce application get --name banking-validation-frontend
```

Save the frontend public URL.

---

# 18. End-to-end testing after deployment

## 18.1 Open frontend in browser
Open:
```text
https://<FRONTEND_URL>
```

Check:
- page loads
- options are loaded
- no obvious blank screen
- browser console has no API CORS or network failures

## 18.2 Start a test validation from browser
Use sample values:
- Model Name: `demo-scorecard`
- Product Type: `secured`
- Scorecard Type: `application`
- Model Type: `GLM`
- Description: `Code Engine test deployment`

Submit validation and verify:
- validation starts
- progress loads
- results page appears
- document download works

---

# 19. Backend API test using curl

You can also test directly without the frontend.

## 19.1 Start validation
```bash
curl -X POST https://<BACKEND_URL>/api/v1/validate \
  -H 'Content-Type: application/json' \
  -d '{
    "model_config": {
      "model_name": "demo-scorecard",
      "product_type": "secured",
      "scorecard_type": "application",
      "model_type": "GLM",
      "description": "Code Engine validation test"
    },
    "generate_document": true
  }'
```

You should receive:
- `validation_id`
- `status: started`

## 19.2 Check status
```bash
curl https://<BACKEND_URL>/api/v1/validate/<VALIDATION_ID>
```

## 19.3 Fetch results
```bash
curl https://<BACKEND_URL>/api/v1/validate/<VALIDATION_ID>/results
```

## 19.4 Download document
```bash
curl -OJ https://<BACKEND_URL>/api/v1/validate/<VALIDATION_ID>/document
```

---

# 20. Important production note about document storage

The application currently writes generated documents to:
```text
/app/output/documents
```

In Code Engine, local container storage is **ephemeral**.

That means documents may be lost when:
- the container restarts
- the app scales
- the instance is rescheduled

## What this means for you
For an initial deployment and simple testing:
- current behavior may still be acceptable

For production durability:
- you should later store generated reports in **IBM Cloud Object Storage**

This is not required to get the app deployed, but it is recommended.

---

# 21. Recommended resource settings

For initial deployment:

## Backend
- CPU: `1`
- Memory: `2G`
- Min scale: `1`
- Max scale: `2`

## Frontend
- CPU: `0.5`
- Memory: `1G`
- Min scale: `1`
- Max scale: `2`

If cost is a concern, you can reduce these later after observing actual usage.

---

# 22. Use secrets instead of plain environment variables later

For first deployment, using `--env` is simpler.
For better security, later move sensitive values into Code Engine secrets.

Sensitive values include:
- database URL
- watsonx API key

Beginner recommendation:
- first get deployment working
- then convert to secrets

---

# 23. Useful Code Engine commands

## List apps
```bash
ibmcloud ce application list
```

## Get one app
```bash
ibmcloud ce application get --name banking-validation-backend
ibmcloud ce application get --name banking-validation-frontend
```

## View logs
```bash
ibmcloud ce application logs --name banking-validation-backend --follow
ibmcloud ce application logs --name banking-validation-frontend --follow
```

## Update backend image
```bash
ibmcloud ce application update \
  --name banking-validation-backend \
  --image icr.io/<NAMESPACE>/banking-validation-backend:ce-v2
```

## Update frontend image
```bash
ibmcloud ce application update \
  --name banking-validation-frontend \
  --image icr.io/<NAMESPACE>/banking-validation-frontend:ce-v2
```

## Delete an app
```bash
ibmcloud ce application delete --name banking-validation-backend
ibmcloud ce application delete --name banking-validation-frontend
```

---

# 24. Troubleshooting guide

## Problem: backend health endpoint fails
Possible causes:
- invalid database connection string
- watsonx credentials incorrect
- app not fully started yet

Check:
```bash
ibmcloud ce application logs --name banking-validation-backend --follow
```

## Problem: frontend loads but cannot call backend
Possible causes:
- frontend was built with wrong `VITE_API_URL`
- backend URL changed after rebuild
- browser console shows failed network calls

Fix:
- rebuild frontend image with correct backend URL
- push new image
- update frontend Code Engine app

## Problem: validation starts but fails
Possible causes:
- watsonx credentials are wrong
- watsonx project ID is wrong
- backend cannot reach required services

Check backend logs.

## Problem: document download fails
Possible causes:
- validation not completed yet
- file generated on a different instance
- ephemeral filesystem limitations

For durable download behavior, later move report storage to Object Storage.

## Problem: image push fails
Possible causes:
- not logged into Container Registry
- namespace not created
- wrong registry region targeted

Fix:
```bash
ibmcloud cr region-set <REGION>
ibmcloud cr login
ibmcloud cr namespaces
```

---

# 25. Safe deployment sequence summary

Follow this exact order:

1. Log in to IBM Cloud
2. Select region
3. Select resource group
4. Create Container Registry namespace
5. Create Code Engine project
6. Create PostgreSQL service
7. Collect PostgreSQL connection string
8. Collect watsonx credentials
9. Build backend image
10. Push backend image
11. Deploy backend app
12. Verify backend health
13. Build frontend image using backend URL
14. Push frontend image
15. Deploy frontend app
16. Verify UI and validation flow

Do not build the frontend before the backend URL is known.

---

# 26. Files in copied workspace relevant for Code Engine

Modified in copied workspace:
- `frontend/Dockerfile`
- `frontend/src/services/api.js`
- `frontend/src/App.jsx`

Unchanged but used:
- `backend/Dockerfile`
- `backend/main.py`
- `backend/wxo/watsonx_client.py`

Deployment guide:
- `CODE_ENGINE_DEPLOYMENT.md`

---

# 27. Final recommendation

For your first IBM Cloud deployment:
- deploy backend first
- verify `/health`
- then build and deploy frontend
- use managed PostgreSQL
- keep document persistence improvement for a later phase

This keeps the first deployment simpler and reduces moving parts.

---

# 28. What I can do next

Once you are ready, the next best step is:

1. I help you create the backend and frontend images with exact commands using your chosen:
   - region
   - registry namespace
   - backend Code Engine URL

or

2. I help you prepare Code Engine secrets and safer production configuration.

or

3. I help you validate the copied workspace locally before pushing to IBM Cloud.