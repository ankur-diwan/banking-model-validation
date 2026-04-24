#!/bin/bash

# Banking Model Validation System - Deployment Verification Script
# This script verifies that all components are properly deployed and functional

set -e

echo "🔍 Banking Model Validation System - Deployment Verification"
echo "=============================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

# Function to print failure
print_failure() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

echo "1. Checking Prerequisites..."
echo "----------------------------"

# Check Docker
if command_exists docker; then
    print_success "Docker is installed"
    docker --version
else
    print_failure "Docker is not installed"
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_success "Docker Compose is installed"
    docker-compose --version
else
    print_failure "Docker Compose is not installed"
fi

# Check Node.js
if command_exists node; then
    print_success "Node.js is installed"
    node --version
else
    print_warning "Node.js is not installed (required for local development)"
fi

# Check Python
if command_exists python3; then
    print_success "Python 3 is installed"
    python3 --version
else
    print_failure "Python 3 is not installed"
fi

echo ""
echo "2. Checking Project Structure..."
echo "--------------------------------"

# Check backend files
if [ -f "backend/main.py" ]; then
    print_success "Backend main.py exists"
else
    print_failure "Backend main.py not found"
fi

if [ -f "backend/requirements.txt" ]; then
    print_success "Backend requirements.txt exists"
else
    print_failure "Backend requirements.txt not found"
fi

# Check frontend files
if [ -f "frontend/package.json" ]; then
    print_success "Frontend package.json exists"
else
    print_failure "Frontend package.json not found"
fi

if [ -f "frontend/src/App.jsx" ]; then
    print_success "Frontend App.jsx exists"
else
    print_failure "Frontend App.jsx not found"
fi

# Check Docker files
if [ -f "docker-compose.yml" ]; then
    print_success "docker-compose.yml exists"
else
    print_failure "docker-compose.yml not found"
fi

if [ -f "backend/Dockerfile" ]; then
    print_success "Backend Dockerfile exists"
else
    print_failure "Backend Dockerfile not found"
fi

if [ -f "frontend/Dockerfile" ]; then
    print_success "Frontend Dockerfile exists"
else
    print_failure "Frontend Dockerfile not found"
fi

echo ""
echo "3. Checking Component Files..."
echo "------------------------------"

# Count frontend components
COMPONENT_COUNT=$(find frontend/src/components -name "*.jsx" 2>/dev/null | wc -l)
if [ "$COMPONENT_COUNT" -ge 39 ]; then
    print_success "Found $COMPONENT_COUNT frontend components (expected 39+)"
else
    print_warning "Found only $COMPONENT_COUNT frontend components (expected 39+)"
fi

# Check critical components
CRITICAL_COMPONENTS=(
    "frontend/src/components/Shared/DataTable.jsx"
    "frontend/src/components/Workflows/TaskInbox.jsx"
    "frontend/src/components/Workflows/ApprovalInterface.jsx"
    "frontend/src/components/RAG/RAGAssistant.jsx"
    "frontend/src/components/Monitoring/MonitoringDashboard.jsx"
    "frontend/src/components/Models/ModelInventory.jsx"
)

for component in "${CRITICAL_COMPONENTS[@]}"; do
    if [ -f "$component" ]; then
        print_success "$(basename $component) exists"
    else
        print_failure "$(basename $component) not found"
    fi
done

echo ""
echo "4. Checking Backend Components..."
echo "----------------------------------"

BACKEND_COMPONENTS=(
    "backend/watsonx/governance_client.py"
    "backend/agents/mlops_agent.py"
    "backend/wxo/orchestrate_client.py"
    "backend/rag/document_rag.py"
    "backend/auth/rbac.py"
)

for component in "${BACKEND_COMPONENTS[@]}"; do
    if [ -f "$component" ]; then
        print_success "$(basename $component) exists"
    else
        print_failure "$(basename $component) not found"
    fi
done

echo ""
echo "5. Checking Documentation..."
echo "----------------------------"

DOCS=(
    "README.md"
    "FRONTEND_COMPLETE_SUMMARY.md"
    "ENHANCEMENT_SUMMARY.md"
    "DEPLOYMENT_TESTING_GUIDE.md"
    "PRODUCTION_DEPLOYMENT_PACKAGE.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        print_success "$doc exists"
    else
        print_warning "$doc not found"
    fi
done

echo ""
echo "6. Checking Environment Configuration..."
echo "----------------------------------------"

if [ -f ".env" ]; then
    print_success ".env file exists"
else
    print_warning ".env file not found (copy from .env.example)"
fi

if [ -f ".env.example" ]; then
    print_success ".env.example exists"
else
    print_warning ".env.example not found"
fi

echo ""
echo "7. Checking Docker Services..."
echo "------------------------------"

# Check if Docker is running
if docker info >/dev/null 2>&1; then
    print_success "Docker daemon is running"
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Docker containers are running"
        docker-compose ps
    else
        print_warning "Docker containers are not running (run 'docker-compose up -d')"
    fi
else
    print_warning "Docker daemon is not running"
fi

echo ""
echo "8. Testing API Endpoints (if running)..."
echo "----------------------------------------"

# Check if backend is accessible
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    print_success "Backend API is accessible at http://localhost:8000"
else
    print_warning "Backend API is not accessible (may not be running)"
fi

# Check if frontend is accessible
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    print_success "Frontend is accessible at http://localhost:3000"
else
    print_warning "Frontend is not accessible (may not be running)"
fi

echo ""
echo "9. Code Quality Checks..."
echo "-------------------------"

# Count total lines of code
if command_exists cloc; then
    echo "Lines of code:"
    cloc backend frontend --quiet
    print_success "Code statistics generated"
else
    print_warning "cloc not installed (install for code statistics)"
fi

echo ""
echo "=============================================================="
echo "Verification Summary"
echo "=============================================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Configure .env file with your watsonx credentials"
    echo "2. Start the application: docker-compose up -d"
    echo "3. Access frontend: http://localhost:3000"
    echo "4. Access API docs: http://localhost:8000/docs"
    echo "5. Review documentation in README.md"
    exit 0
else
    echo -e "${RED}✗ Some critical checks failed. Please fix the issues above.${NC}"
    exit 1
fi

# Made with Bob
