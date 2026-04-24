# Banking Model Validation System - Deployment & Testing Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Testing Guide](#testing-guide)
6. [Production Deployment](#production-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space
- **Network**: Stable internet connection for watsonx API calls

### Software Requirements
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9+
- **Node.js**: 18+
- **npm**: 9+

### IBM watsonx Requirements
- IBM Cloud account
- watsonx.ai API key
- watsonx.governance access
- watsonx Orchestrate workspace (optional)

## Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd banking-model-validation
```

### 2. Create Environment Files

#### Backend Environment (.env)
```bash
# Create .env file in project root
cat > .env << EOF
# watsonx Configuration
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_SPACE_ID=your_space_id_here
WATSONX_GOVERNANCE_URL=https://api.dataplatform.cloud.ibm.com
WATSONX_ORCHESTRATE_URL=https://api.orchestrate.ibm.com
WATSONX_ORCHESTRATE_WORKSPACE_ID=your_workspace_id_here

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@database:5432/banking_validation
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=banking_validation

# Redis Configuration (optional)
REDIS_URL=redis://redis:6379/0

# Application Configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Security
SECRET_KEY=your_secret_key_here_change_in_production
JWT_SECRET=your_jwt_secret_here_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# API Configuration
API_RATE_LIMIT=100
API_RATE_LIMIT_PERIOD=60
EOF
```

#### Frontend Environment (.env)
```bash
# Create .env file in frontend directory
cat > frontend/.env << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENVIRONMENT=development
EOF
```

### 3. Install Dependencies

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

## Backend Deployment

### Development Mode

#### Option 1: Direct Python
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: Docker
```bash
# Build backend image
docker build -t banking-validation-backend ./backend

# Run backend container
docker run -p 8000:8000 \
  --env-file .env \
  banking-validation-backend
```

### Verify Backend
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

## Frontend Deployment

### Development Mode

#### Option 1: Vite Dev Server
```bash
cd frontend
npm run dev
# Access at http://localhost:5173
```

#### Option 2: Docker
```bash
# Build frontend image
docker build -t banking-validation-frontend ./frontend

# Run frontend container
docker run -p 3000:80 banking-validation-frontend
```

### Verify Frontend
```bash
# Open browser
open http://localhost:5173  # or http://localhost:3000 if using Docker
```

## Docker Compose Deployment

### Full Stack Deployment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Services
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: localhost:5432
- **Redis**: localhost:6379 (if configured)

### Verify All Services
```bash
# Check service status
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Test database
docker-compose exec database psql -U postgres -d banking_validation -c "SELECT 1;"
```

## Testing Guide

### Backend Testing

#### 1. Unit Tests
```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

#### 2. Integration Tests
```bash
# Test API endpoints
pytest tests/test_api.py -v

# Test agents
pytest tests/test_agents.py -v

# Test governance
pytest tests/test_governance.py -v
```

#### 3. Load Testing
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8000
```

#### 4. API Testing with curl

**Test MLOps Endpoints:**
```bash
# Onboard use case
curl -X POST http://localhost:8000/api/v1/mlops/onboard-use-case \
  -H "Content-Type: application/json" \
  -d '{
    "product_type": "unsecured",
    "scorecard_type": "application",
    "business_objective": "Credit risk assessment for personal loans",
    "risk_level": "high"
  }'

# Check existing models
curl "http://localhost:8000/api/v1/mlops/check-existing-models?product_type=unsecured&scorecard_type=application"

# Register model
curl -X POST http://localhost:8000/api/v1/mlops/register-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Test_Model_v1",
    "use_case_id": "UC_123",
    "model_type": "XGBoost",
    "product_type": "unsecured",
    "scorecard_type": "application",
    "features": ["credit_score", "income", "debt_ratio"],
    "data_version": "1.0",
    "performance_metrics": {"AUC": 0.75, "KS": 0.35},
    "validation_results": {"status": "passed"}
  }'
```

**Test Governance Endpoints:**
```bash
# List use cases
curl http://localhost:8000/api/v1/governance/use-cases

# List models
curl http://localhost:8000/api/v1/governance/models

# Get model details
curl http://localhost:8000/api/v1/governance/models/MDL_123

# Get model card
curl http://localhost:8000/api/v1/governance/models/MDL_123/card
```

**Test Orchestrate Endpoints:**
```bash
# List workflows
curl http://localhost:8000/api/v1/orchestrate/workflows

# List tasks
curl http://localhost:8000/api/v1/orchestrate/tasks

# Approve task
curl -X POST http://localhost:8000/api/v1/orchestrate/tasks/action \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK_123",
    "approver": "validator@bank.com",
    "action": "approve",
    "comments": "Approved after review"
  }'
```

### Frontend Testing

#### 1. Unit Tests
```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

#### 2. Component Tests
```bash
# Run Storybook (if configured)
npm run storybook
```

#### 3. E2E Tests
```bash
# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npx playwright test

# Run with UI
npx playwright test --ui
```

#### 4. Manual Testing Checklist

**Dashboard:**
- [ ] Dashboard loads without errors
- [ ] All metrics display correctly
- [ ] Charts render properly
- [ ] Filters work as expected

**Model Management:**
- [ ] Can create new use case
- [ ] Can check existing models
- [ ] Can register new model
- [ ] Model details display correctly

**Monitoring:**
- [ ] Monitoring dashboard loads
- [ ] Metrics update in real-time
- [ ] Alerts display correctly
- [ ] Drift detection works

**Validation:**
- [ ] Can start validation
- [ ] Progress updates in real-time
- [ ] Results display correctly
- [ ] Can download report

**Workflows:**
- [ ] Workflows list correctly
- [ ] Can view workflow details
- [ ] Can approve/reject tasks
- [ ] Notifications work

### Integration Testing

#### End-to-End Workflow Test
```bash
# 1. Start all services
docker-compose up -d

# 2. Wait for services to be ready
sleep 10

# 3. Run integration test script
python tests/integration/test_full_workflow.py

# Expected output:
# ✓ Use case onboarded
# ✓ Existing models checked
# ✓ Model registered
# ✓ Validation started
# ✓ Monitoring configured
# ✓ Deployment workflow created
# ✓ All tests passed
```

## Production Deployment

### 1. Build Production Images

#### Backend
```bash
docker build -t banking-validation-backend:prod \
  --build-arg ENVIRONMENT=production \
  ./backend
```

#### Frontend
```bash
cd frontend
npm run build
docker build -t banking-validation-frontend:prod .
```

### 2. Production Environment Variables

```bash
# Update .env for production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Use strong secrets
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

# Update CORS for production domain
CORS_ORIGINS=https://your-domain.com

# Use production database
DATABASE_URL=postgresql://user:password@prod-db:5432/banking_validation
```

### 3. Deploy to Cloud

#### AWS ECS
```bash
# Push images to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag banking-validation-backend:prod <account-id>.dkr.ecr.us-east-1.amazonaws.com/banking-validation-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/banking-validation-backend:latest

# Deploy using ECS task definition
aws ecs update-service --cluster banking-validation --service backend --force-new-deployment
```

#### Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n banking-validation
kubectl get services -n banking-validation
```

### 4. SSL/TLS Configuration

```bash
# Using Let's Encrypt with Certbot
certbot --nginx -d your-domain.com -d www.your-domain.com

# Or use AWS Certificate Manager for AWS deployments
```

### 5. Database Migration

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Or in production
kubectl exec -it <backend-pod> -- alembic upgrade head
```

## Monitoring & Maintenance

### Application Monitoring

#### Prometheus Metrics
```bash
# Access Prometheus metrics
curl http://localhost:8000/metrics

# Key metrics to monitor:
# - http_requests_total
# - http_request_duration_seconds
# - validation_duration_seconds
# - model_registrations_total
# - monitoring_alerts_total
```

#### Logging
```bash
# View application logs
docker-compose logs -f backend

# Filter by level
docker-compose logs backend | grep ERROR

# Export logs
docker-compose logs backend > backend.log
```

#### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker-compose exec database pg_isready

# Redis health (if configured)
docker-compose exec redis redis-cli ping
```

### Database Maintenance

#### Backup
```bash
# Backup database
docker-compose exec database pg_dump -U postgres banking_validation > backup_$(date +%Y%m%d).sql

# Automated daily backups
0 2 * * * docker-compose exec database pg_dump -U postgres banking_validation > /backups/backup_$(date +\%Y\%m\%d).sql
```

#### Restore
```bash
# Restore from backup
docker-compose exec -T database psql -U postgres banking_validation < backup_20260422.sql
```

### Performance Optimization

#### Database Indexing
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_models_product_type ON models(product_type);
CREATE INDEX idx_models_scorecard_type ON models(scorecard_type);
CREATE INDEX idx_validations_status ON validations(status);
CREATE INDEX idx_monitoring_timestamp ON monitoring_metrics(timestamp);
```

#### Caching
```python
# Enable Redis caching for frequently accessed data
# Already configured in the application
```

## Troubleshooting

### Common Issues

#### 1. Backend Won't Start
```bash
# Check logs
docker-compose logs backend

# Common causes:
# - Missing environment variables
# - Database connection issues
# - Port already in use

# Solutions:
# - Verify .env file
# - Check database is running: docker-compose ps
# - Change port in docker-compose.yml
```

#### 2. Frontend Can't Connect to Backend
```bash
# Check CORS settings
# Verify VITE_API_URL in frontend/.env
# Check network connectivity

# Test backend directly
curl http://localhost:8000/health

# Check browser console for CORS errors
```

#### 3. Database Connection Errors
```bash
# Check database is running
docker-compose ps database

# Test connection
docker-compose exec database psql -U postgres -d banking_validation -c "SELECT 1;"

# Check DATABASE_URL in .env
# Verify credentials
```

#### 4. watsonx API Errors
```bash
# Verify API key
echo $WATSONX_API_KEY

# Test API connection
curl -H "Authorization: Bearer $WATSONX_API_KEY" \
  https://api.dataplatform.cloud.ibm.com/v2/projects

# Check API quota and limits
```

#### 5. Memory Issues
```bash
# Check container memory usage
docker stats

# Increase memory limits in docker-compose.yml
services:
  backend:
    mem_limit: 2g
    mem_reservation: 1g
```

### Debug Mode

#### Enable Debug Logging
```bash
# Update .env
DEBUG=true
LOG_LEVEL=DEBUG

# Restart services
docker-compose restart backend
```

#### Access Container Shell
```bash
# Backend
docker-compose exec backend bash

# Database
docker-compose exec database psql -U postgres banking_validation

# Check Python environment
docker-compose exec backend python -c "import sys; print(sys.path)"
```

### Performance Issues

#### Slow API Responses
```bash
# Check database query performance
docker-compose exec database psql -U postgres banking_validation

# Enable query logging
ALTER DATABASE banking_validation SET log_statement = 'all';

# Analyze slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;
```

#### High Memory Usage
```bash
# Profile Python application
pip install memory_profiler
python -m memory_profiler backend/main.py

# Check for memory leaks
docker stats --no-stream
```

## Security Checklist

### Pre-Production
- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and JWT_SECRET
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable CORS only for trusted domains
- [ ] Implement authentication and authorization
- [ ] Scan for vulnerabilities (OWASP ZAP)
- [ ] Review and update dependencies
- [ ] Enable audit logging

### Production
- [ ] Regular security updates
- [ ] Monitor for suspicious activity
- [ ] Regular backups
- [ ] Disaster recovery plan
- [ ] Incident response plan
- [ ] Regular penetration testing
- [ ] Compliance audits (SOC 2, ISO 27001)

## Support & Resources

### Documentation
- API Documentation: http://localhost:8000/docs
- User Guide: See USER_GUIDE.md
- Architecture: See ENHANCEMENT_SUMMARY.md

### Getting Help
- GitHub Issues: <repository-url>/issues
- Email: support@your-domain.com
- Slack: #banking-validation

### Useful Commands

```bash
# Quick start
docker-compose up -d

# View logs
docker-compose logs -f

# Restart service
docker-compose restart backend

# Stop all
docker-compose down

# Clean everything
docker-compose down -v
docker system prune -a

# Database backup
docker-compose exec database pg_dump -U postgres banking_validation > backup.sql

# Check service health
curl http://localhost:8000/health

# Run tests
docker-compose exec backend pytest

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec database psql -U postgres banking_validation
```

---

Made with ❤️ by Bob