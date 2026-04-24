#!/bin/bash

# Banking Model Validation System - Startup Script

echo "================================================"
echo "Banking Model Validation System"
echo "Powered by IBM watsonx"
echo "================================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

echo "✓ Docker is running"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your watsonx credentials"
    echo "   WATSONX_API_KEY=your_api_key_here"
    echo "   WATSONX_PROJECT_ID=your_project_id_here"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

echo ""
echo "Starting services..."
echo ""

# Stop any existing containers
docker-compose down 2>/dev/null

# Build and start services
docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo "Checking service health..."
echo ""

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✓ Backend API is running (http://localhost:8000)"
else
    echo "⚠️  Backend API is starting... (may take a few more seconds)"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✓ Frontend UI is running (http://localhost:3000)"
else
    echo "⚠️  Frontend UI is starting... (may take a few more seconds)"
fi

# Check database
if docker-compose exec -T postgres pg_isready -U validation_user > /dev/null 2>&1; then
    echo "✓ Database is running"
else
    echo "⚠️  Database is starting..."
fi

echo ""
echo "================================================"
echo "Services Status:"
echo "================================================"
docker-compose ps
echo ""

echo "================================================"
echo "Access Points:"
echo "================================================"
echo "Frontend UI:  http://localhost:3000"
echo "Backend API:  http://localhost:8000"
echo "API Docs:     http://localhost:8000/docs"
echo ""

echo "================================================"
echo "Quick Commands:"
echo "================================================"
echo "View logs:        docker-compose logs -f"
echo "Stop services:    docker-compose down"
echo "Restart:          docker-compose restart"
echo ""

echo "✓ Banking Model Validation System is ready!"
echo ""
echo "Open http://localhost:3000 to start validating models"
echo ""

# Made with Bob
