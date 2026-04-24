# Banking Model Validation System - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Banking Model Validation System, an agentic AI application built with IBM watsonx for automating SR 11-7 compliance validation.

## Prerequisites

### Required Software
- Docker Desktop (v20.10+)
- Docker Compose (v2.0+)
- Git
- IBM Cloud Account with watsonx.ai access

### IBM watsonx Setup

1. **Create IBM Cloud Account**
   - Visit https://cloud.ibm.com
   - Sign up or log in

2. **Provision watsonx.ai**
   - Navigate to Catalog > AI/Machine Learning
   - Select "watsonx.ai"
   - Create a new instance

3. **Get API Credentials**
   - Go to watsonx.ai dashboard
   - Navigate to Profile & Settings > API Keys
   - Create a new API key
   - Note down:
     - API Key
     - Project ID
     - Service URL

4. **Set Up watsonx.governance** (Optional but Recommended)
   - Navigate to watsonx.governance
   - Create a governance workspace
   - Note the workspace ID

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd banking-model-validation
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update the following variables:
```env
WATSONX_API_KEY=your_actual_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_SPACE_ID=your_space_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 3. Build and Start Services

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

Expected output:
```
NAME                          STATUS    PORTS
banking-validation-backend    Up        0.0.0.0:8000->8000/tcp
banking-validation-frontend   Up        0.0.0.0:3000->3000/tcp
banking-validation-db         Up        0.0.0.0:5432->5432/tcp
```

### 4. Verify Installation

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
open http://localhost:3000
```

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (React)                   │
│                    http://localhost:3000                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend Service                     │
│                    http://localhost:8000                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Validation Orchestrator Agent                 │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  • Data Quality Agent                          │  │  │
│  │  │  • Performance Validation Agent                │  │  │
│  │  │  • Assumptions Testing Agent                   │  │  │
│  │  │  • Stability Analysis Agent                    │  │  │
│  │  │  • Compliance Checker Agent                    │  │  │
│  │  │  • Documentation Generator Agent               │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
                   ▼                  ▼
         ┌─────────────────┐  ┌──────────────────┐
         │   PostgreSQL    │  │  IBM watsonx.ai  │
         │    Database     │  │  watsonx.gov     │
         └─────────────────┘  └──────────────────┘
```

### Data Flow

1. **User Input** → Frontend collects model configuration
2. **API Request** → Backend receives validation request
3. **Agent Orchestration** → Validation orchestrator coordinates agents
4. **Data Generation** → Synthetic data generator creates test datasets
5. **Validation Execution** → Multiple agents perform parallel validation
6. **watsonx Integration** → AI-powered analysis and governance tracking
7. **Document Generation** → Word document with comprehensive report
8. **Results Delivery** → User downloads validation report

## Usage Guide

### Starting a Validation

1. **Access the UI**
   - Open browser to http://localhost:3000

2. **Configure Model**
   - Enter model name (e.g., "US_Unsecured_Application_v1")
   - Select product type (Secured/Unsecured/Revolving)
   - Select scorecard type (Application/Behavioral/Collections)
   - Select model type (GLM/XGBoost/RandomForest/etc.)
   - Add description and metadata

3. **Review Configuration**
   - Verify all selections
   - Review validation scope

4. **Start Validation**
   - Click "Start Validation"
   - Monitor progress (typically 2-5 minutes)

5. **Download Report**
   - Once complete, download Word document
   - Review comprehensive validation report

### API Usage

#### Start Validation
```bash
curl -X POST http://localhost:8000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "model_config": {
      "model_name": "Test_Application_Scorecard",
      "product_type": "unsecured",
      "scorecard_type": "application",
      "model_type": "XGBoost",
      "description": "Test scorecard",
      "version": "1.0"
    },
    "generate_document": true,
    "register_governance": true
  }'
```

#### Check Status
```bash
curl http://localhost:8000/api/v1/validate/{validation_id}
```

#### Get Results
```bash
curl http://localhost:8000/api/v1/validate/{validation_id}/results
```

#### Download Document
```bash
curl -O http://localhost:8000/api/v1/validate/{validation_id}/document
```

## Validation Components

### 1. Data Quality Assessment
- Completeness checks
- Accuracy validation
- Consistency verification
- Timeliness assessment
- Representativeness analysis

### 2. Model Performance Validation
- Discriminatory power (Gini, KS, AUC)
- Calibration analysis
- Stability metrics (PSI, CSI)
- Benchmarking

### 3. Assumptions Testing
- Statistical assumption validation
- Sensitivity analysis
- Stress testing
- Scenario analysis

### 4. SR 11-7 Compliance
- Model purpose documentation
- Data quality standards
- Model specification review
- Performance validation
- Implementation verification
- Monitoring plan assessment

### 5. Document Generation
- Executive summary
- Technical specifications
- Validation results
- Compliance summary
- Recommendations

## Monitoring and Maintenance

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Database logs
docker-compose logs -f postgres
```

### Database Access

```bash
# Connect to database
docker-compose exec postgres psql -U validation_user -d banking_validation

# View models
SELECT * FROM models;

# View validations
SELECT * FROM validations ORDER BY created_at DESC LIMIT 10;
```

### Backup Data

```bash
# Backup database
docker-compose exec postgres pg_dump -U validation_user banking_validation > backup.sql

# Backup validation documents
docker cp banking-validation-backend:/app/output ./backup_output
```

## Troubleshooting

### Common Issues

#### 1. watsonx Connection Failed
```
Error: WATSONX_API_KEY must be provided
```
**Solution:** Verify .env file has correct API key

#### 2. Database Connection Error
```
Error: could not connect to server
```
**Solution:** 
```bash
docker-compose restart postgres
docker-compose logs postgres
```

#### 3. Frontend Can't Reach Backend
```
Error: Network Error
```
**Solution:** Check VITE_API_URL in .env matches backend URL

#### 4. Document Generation Failed
```
Error: Failed to generate document
```
**Solution:** Ensure output directory exists and has write permissions

### Health Checks

```bash
# Check all services
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Test database
docker-compose exec postgres pg_isready

# Check disk space
docker system df
```

## Production Deployment

### Security Considerations

1. **Environment Variables**
   - Use secrets management (AWS Secrets Manager, Azure Key Vault)
   - Never commit .env files
   - Rotate API keys regularly

2. **Network Security**
   - Use HTTPS/TLS
   - Configure firewall rules
   - Implement rate limiting

3. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups
   - Implement access controls

4. **Authentication**
   - Add OAuth2/OIDC
   - Implement RBAC
   - Audit logging

### Scaling

#### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
    # Add load balancer
```

#### Performance Optimization
- Enable caching (Redis)
- Use CDN for frontend
- Database connection pooling
- Async processing for long validations

### Monitoring

#### Prometheus Metrics
```python
# Add to backend
from prometheus_client import Counter, Histogram

validation_counter = Counter('validations_total', 'Total validations')
validation_duration = Histogram('validation_duration_seconds', 'Validation duration')
```

#### Logging
- Centralized logging (ELK Stack)
- Log aggregation
- Alert configuration

## Maintenance

### Regular Tasks

**Daily:**
- Monitor validation queue
- Check error logs
- Verify disk space

**Weekly:**
- Review validation metrics
- Update documentation
- Check for updates

**Monthly:**
- Database maintenance
- Security updates
- Performance review
- Backup verification

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d

# Verify
docker-compose ps
```

## Support

### Getting Help

1. **Documentation**: Review this guide and README.md
2. **Logs**: Check application logs for errors
3. **IBM watsonx Support**: https://cloud.ibm.com/docs/watsonx
4. **Community**: IBM watsonx community forums

### Reporting Issues

Include:
- Error messages
- Log excerpts
- Steps to reproduce
- Environment details
- watsonx configuration (without credentials)

## Appendix

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| WATSONX_API_KEY | IBM Cloud API key | Yes | - |
| WATSONX_PROJECT_ID | watsonx.ai project ID | Yes | - |
| WATSONX_SPACE_ID | watsonx.ai space ID | No | - |
| WATSONX_URL | watsonx service URL | No | us-south |
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| VITE_API_URL | Backend API URL | Yes | localhost:8000 |

### Port Reference

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Web UI |
| Backend | 8000 | REST API |
| PostgreSQL | 5432 | Database |

### File Structure

```
banking-model-validation/
├── backend/
│   ├── agents/              # Validation agents
│   ├── models/              # Data models
│   ├── validation/          # Validation modules
│   ├── wxo/                 # watsonx integration
│   ├── data_generators/     # Synthetic data
│   └── main.py              # FastAPI app
├── frontend/
│   └── src/
│       ├── components/      # React components
│       └── App.jsx          # Main app
├── database/
│   └── init.sql             # Database schema
├── docs/                    # Documentation
├── docker-compose.yml       # Container orchestration
└── .env                     # Configuration
```

## Conclusion

The Banking Model Validation System provides automated, comprehensive SR 11-7 compliance validation powered by IBM watsonx. Follow this guide for successful deployment and operation.

For questions or support, refer to the documentation or contact your IBM watsonx representative.