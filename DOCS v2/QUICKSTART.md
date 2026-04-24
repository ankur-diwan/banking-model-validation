# Quick Start Guide

Get the Banking Model Validation System running in 5 minutes!

## Prerequisites

- Docker Desktop installed and running
- IBM watsonx API key (get from https://cloud.ibm.com)

## Steps

### 1. Clone and Configure (2 minutes)

```bash
# Clone repository
git clone <repository-url>
cd banking-model-validation

# Copy environment template
cp .env.example .env

# Edit with your watsonx credentials
nano .env
```

Add your credentials:
```env
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
```

### 2. Start Services (2 minutes)

```bash
# Build and start all services
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
docker-compose ps
```

### 3. Access Application (1 minute)

Open your browser to: **http://localhost:3000**

## First Validation

1. **Enter Model Details:**
   - Model Name: `Test_Application_Scorecard_v1`
   - Product Type: `Unsecured Loans`
   - Scorecard Type: `Application Scorecard`
   - Model Type: `XGBoost`

2. **Click "Next"** to review

3. **Click "Start Validation"**

4. **Wait 2-3 minutes** for validation to complete

5. **Download Report** - Get your comprehensive SR 11-7 validation document!

## What You Get

✅ Automated data quality assessment  
✅ Model performance validation  
✅ SR 11-7 compliance checking  
✅ Professional Word document report  
✅ watsonx.governance integration  

## Troubleshooting

**Services won't start?**
```bash
docker-compose down
docker-compose up -d
```

**Can't access UI?**
- Check http://localhost:3000
- Verify Docker is running
- Check logs: `docker-compose logs frontend`

**Validation fails?**
- Verify watsonx API key in .env
- Check backend logs: `docker-compose logs backend`

## Next Steps

- Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed information
- Review [SR-11-7-FRAMEWORK.md](docs/SR-11-7-FRAMEWORK.md) for validation details
- Explore API at http://localhost:8000/docs

## Support

- Documentation: See README.md
- API Docs: http://localhost:8000/docs
- IBM watsonx: https://cloud.ibm.com/docs/watsonx

---

**Ready to validate your banking models with AI-powered automation!** 🚀