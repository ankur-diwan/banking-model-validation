# Banking Model Validation App Docker Deployment Guide

## Overview

This guide explains how to deploy the Banking Model Validation app on a single machine using Docker for developer and demo environments.

## 1. Pre-requisites

### Hardware
- Minimum 4 vCPU
- Minimum 8 GB RAM
- At least 20 GB free disk space
- Reliable internet connectivity for Docker image pulls and IBM watsonx access

### Operating System
- macOS
- Linux
- Windows with Docker Desktop

### Required Software
- Git
- Docker Desktop 20.10+ or Docker Engine equivalent
- Docker Compose v2+
- Modern web browser

### Required Accounts and External Services
- IBM Cloud account
- watsonx.ai enabled account or project
- Valid watsonx API credentials:
  - `WATSONX_API_KEY`
  - `WATSONX_PROJECT_ID`
  - `WATSONX_URL`

### Optional Services
- `WATSONX_SPACE_ID`
- watsonx.governance workspace
- watsonx Orchestrate access

## 2. Application Components and Dependencies

The deployment uses three main containers defined in `docker-compose.yml`:
- `postgres` for PostgreSQL 15
- `backend` for the FastAPI API service
- `frontend` for the React and Vite UI

### Exposed Ports
- `3000` for the frontend
- `8000` for the backend API and Swagger docs
- `5432` for PostgreSQL

### Core Runtime Dependencies
- Backend Python image based on `python:3.11-slim`
- Frontend Node image based on `node:20-alpine`
- PostgreSQL 15 Alpine image
- IBM watsonx connectivity initialized during backend startup
- Health endpoint available at `/health`

## 3. Required Configuration

Copy `.env.example` to `.env` and set the required values.

Minimum recommended values:

```env
WATSONX_API_KEY=your_actual_api_key
WATSONX_PROJECT_ID=your_actual_project_id
WATSONX_SPACE_ID=your_space_id_if_used
WATSONX_URL=https://us-south.ml.cloud.ibm.com
DATABASE_URL=postgresql://validation_user:validation_pass@localhost:5432/banking_validation
ENVIRONMENT=development
LOG_LEVEL=INFO
VITE_API_URL=http://localhost:8000
```

### Notes
- The backend container overrides its database connection internally using the Docker network.
- `DATABASE_URL` in `.env` is mainly useful for non-container local runs.
- `VITE_API_URL` should remain `http://localhost:8000` for single-machine demo deployment.

## 4. Deployment Steps

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd banking-model-validation
```

### Step 2: Confirm Docker is available

```bash
docker --version
docker compose version
```

If Docker is not running, start Docker Desktop first.

### Step 3: Create the environment file

```bash
cp .env.example .env
```

Open `.env` and update the watsonx credentials.

### Step 4: Use the startup script or deploy manually

You can use the helper script in `start.sh`, which:
- verifies Docker is running
- creates `.env` if missing
- builds and starts the containers
- checks frontend, backend, and database reachability

Optional command:

```bash
bash start.sh
```

### Step 5: Build the containers manually

If you do not use the script, run:

```bash
docker-compose build
```

This builds:
- the backend image from `backend/Dockerfile`
- the frontend image from `frontend/Dockerfile`

### Step 6: Start all services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- FastAPI backend
- React frontend

### Step 7: Confirm containers are healthy

```bash
docker-compose ps
```

Expected active services:
- `banking-validation-db`
- `banking-validation-backend`
- `banking-validation-frontend`

### Step 8: Verify backend health

```bash
curl http://localhost:8000/health
```

Expected result:
- overall `status` should be `healthy`
- service flags indicate whether watsonx-related clients initialized successfully

### Step 9: Verify frontend access

Open:
- `http://localhost:3000`

### Step 10: Verify API documentation

Open:
- `http://localhost:8000/docs`

## 5. Post-Deployment Validation

After deployment, validate these checkpoints:
- frontend page loads on port `3000`
- backend health endpoint responds on port `8000`
- Swagger docs are visible on `/docs`
- PostgreSQL container is running
- watsonx-dependent services in the health response are initialized if valid credentials were supplied

## 6. Operational Commands

### View logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop the application

```bash
docker-compose down
```

### Restart services

```bash
docker-compose restart
```

### Rebuild after code changes

```bash
docker-compose up -d --build
```

## 7. Troubleshooting

### Frontend not loading
- confirm port `3000` is free
- inspect frontend logs
- verify `npm run dev` is starting correctly inside the container

### Backend not healthy
- inspect backend logs
- confirm watsonx credentials in `.env`
- verify the backend startup path in `backend/main.py`
- confirm port `8000` is available

### Database issues
- confirm port `5432` is not already in use
- inspect PostgreSQL logs
- verify the initialization script mount from `./database/init.sql`

### watsonx features unavailable
- the app may still start, but startup logs can show failed initialization
- verify IBM Cloud credentials and network connectivity

## 8. Common Port Conflicts and Resolution

The app binds these local host ports from `docker-compose.yml`:
- `3000` for frontend
- `8000` for backend
- `5432` for PostgreSQL

If one of these ports is already in use, the corresponding container may fail to start.

### How to identify a conflict

On macOS or Linux:

```bash
lsof -i :3000
lsof -i :8000
lsof -i :5432
```

### Common causes
- another React or Vite app already using `3000`
- another FastAPI, Node, or Python service already using `8000`
- a local PostgreSQL instance already using `5432`

### Resolution options
1. Stop the conflicting local service.
2. Change the published Docker port in `docker-compose.yml`.
3. Update client references if you change ports.

Example adjustments:
- change frontend from `3000:3000` to `3001:3000`
- change backend from `8000:8000` to `8001:8000`
- change database from `5432:5432` to `5433:5432`

If you change frontend or backend ports, also update:
- `VITE_API_URL` in `.env.example` or your local `.env`
- any URLs used for health checks or browser access

## 9. Summary Deployment Flow

```mermaid
flowchart TD
A[Install Docker and Git] --> B[Clone repository]
B --> C[Create .env from template]
C --> D[Add watsonx credentials]
D --> E[Build containers]
E --> F[Start docker compose services]
F --> G[Check backend health]
G --> H[Open frontend UI]
H --> I[Validate app readiness]