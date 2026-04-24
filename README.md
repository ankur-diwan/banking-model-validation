# Banking Model Validation System

A comprehensive, AI-powered model validation platform for banking and financial institutions, built with IBM watsonx.ai, watsonx.governance, and FastAPI.

## 🎯 Overview

This system automates the validation of banking models (credit risk, fraud detection, etc.) according to regulatory frameworks like SR 11-7, ensuring compliance, accuracy, and reliability.

### Key Features

- ✅ **Automated Model Validation** - Comprehensive validation across multiple dimensions
- 🤖 **AI-Powered Analysis** - Uses IBM watsonx.ai for intelligent document review
- 📊 **MLOps Integration** - Full model lifecycle management with watsonx.governance
- 🔄 **Workflow Orchestration** - Automated approval workflows with watsonx Orchestrate
- 📈 **Real-time Monitoring** - Continuous model performance tracking
- 📝 **Automated Documentation** - SR 11-7 compliant validation reports
- 🎨 **Modern UI** - React-based frontend with real-time updates

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  React + Vite
│   (Port 5173)   │
└────────┬────────┘
         │
┌────────▼────────┐
│   Backend API   │  FastAPI + Python
│   (Port 8080)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│ DB   │  │watsonx│
│ PG   │  │ AI    │
└──────┘  └───────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- IBM Cloud account with watsonx.ai access
- Docker (optional, for containerized deployment)

### Environment Variables

Create a `.env` file in the root directory:

```bash
# IBM watsonx Configuration
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/banking_validation

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access the application at `http://localhost:5173`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individual containers
docker build -t banking-validation-backend ./backend
docker build -t banking-validation-frontend ./frontend
```

## ☁️ IBM Cloud Code Engine Deployment

### Prerequisites

- IBM Cloud CLI installed
- Code Engine plugin installed
- IBM Cloud account with Code Engine and watsonx access

### Deploy Backend

```bash
# Login to IBM Cloud
ibmcloud login --sso

# Target Code Engine project
ibmcloud ce project select --name your-project

# Create application from source
ibmcloud ce application create \
  --name banking-validation-backend \
  --build-source https://github.com/YOUR_USERNAME/YOUR_REPO \
  --build-context-dir backend \
  --port 8080 \
  --min-scale 1 \
  --max-scale 2 \
  --cpu 1 \
  --memory 2G \
  --env WATSONX_API_KEY=your_api_key \
  --env WATSONX_PROJECT_ID=your_project_id \
  --env WATSONX_URL=https://us-south.ml.cloud.ibm.com \
  --env DATABASE_URL=your_database_url \
  --env ENVIRONMENT=production \
  --env LOG_LEVEL=INFO
```

### Deploy Frontend

```bash
ibmcloud ce application create \
  --name banking-validation-frontend \
  --build-source https://github.com/YOUR_USERNAME/YOUR_REPO \
  --build-context-dir frontend \
  --port 8080 \
  --env VITE_API_URL=https://your-backend-url.appdomain.cloud
```

## 📚 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

### Key Endpoints

- `POST /api/v1/validate` - Start model validation
- `GET /api/v1/validate/{id}` - Get validation status
- `GET /api/v1/validate/{id}/results` - Get validation results
- `GET /api/v1/validate/{id}/document` - Download validation report
- `POST /api/v1/mlops/register-model` - Register new model
- `GET /api/v1/governance/models` - List all models

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Code Engine Deployment](CODE_ENGINE_DEPLOYMENT.md)
- [SR 11-7 Framework](docs/SR-11-7-FRAMEWORK.md)
- [Supported Models](docs/SUPPORTED_MODELS.md)
- [MCP Integration](docs/MCP_INTEGRATION.md)

## 🔒 Security

- API key authentication for watsonx services
- Role-based access control (RBAC)
- Encrypted database connections
- Secure environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM watsonx.ai for AI capabilities
- IBM watsonx.governance for model lifecycle management
- FastAPI for the excellent web framework
- React and Vite for the frontend

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: your-email@example.com

## 🗺️ Roadmap

- [ ] Additional model types support
- [ ] Enhanced stress testing scenarios
- [ ] Integration with more data sources
- [ ] Advanced visualization dashboards
- [ ] Multi-language support

---

**Built with ❤️ using IBM watsonx and FastAPI**# bnk-ad-ce
