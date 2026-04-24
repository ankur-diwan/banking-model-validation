"""
Banking Model Validation System - Main API
FastAPI application for model validation orchestration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
import asyncio

from .wxo.watsonx_client import WatsonxClient, WatsonxGovernanceTracker
from .agents.validation_orchestrator import ValidationOrchestratorAgent
from .validation.document_generator import SR117DocumentGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Banking Model Validation System",
    description="Automated model validation for banking scorecards using IBM watsonx",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
watsonx_client = None
orchestrator = None
governance_tracker = None

# Pydantic models
class ModelConfig(BaseModel):
    """Model configuration for validation"""
    model_name: str = Field(..., description="Name of the model")
    product_type: str = Field(..., description="Product type: secured, unsecured, revolving")
    scorecard_type: str = Field(..., description="Scorecard type: application, behavioral, collections_early, collections_late")
    model_type: str = Field(..., description="Model type: GLM, GAM, ANN, XGBoost, RandomForest, etc.")
    description: Optional[str] = Field(None, description="Model description")
    version: Optional[str] = Field("1.0", description="Model version")
    owner: Optional[str] = Field("Model Risk Management", description="Model owner")
    
    class Config:
        schema_extra = {
            "example": {
                "model_name": "US_Unsecured_Application_Scorecard_v1",
                "product_type": "unsecured",
                "scorecard_type": "application",
                "model_type": "XGBoost",
                "description": "Application scorecard for unsecured personal loans",
                "version": "1.0",
                "owner": "Credit Risk Team"
            }
        }


class ValidationRequest(BaseModel):
    """Validation request"""
    model_config: ModelConfig
    generate_document: bool = Field(True, description="Generate Word document")
    register_governance: bool = Field(True, description="Register in watsonx.governance")


class ValidationStatus(BaseModel):
    """Validation status response"""
    validation_id: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    model_name: str
    progress: Optional[Dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Validation result response"""
    validation_id: str
    status: str
    model_config: ModelConfig
    results: Dict[str, Any]
    document_path: Optional[str] = None


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global watsonx_client, orchestrator, governance_tracker
    
    try:
        # Initialize watsonx client
        watsonx_client = WatsonxClient()
        
        # Initialize orchestrator
        orchestrator = ValidationOrchestratorAgent(watsonx_client)
        
        # Initialize governance tracker
        governance_tracker = WatsonxGovernanceTracker(watsonx_client)
        
        print("✓ Banking Model Validation System initialized successfully")
        
    except Exception as e:
        print(f"✗ Failed to initialize system: {e}")
        print("  Note: Set WATSONX_API_KEY environment variable to enable watsonx features")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Banking Model Validation System shutting down...")


# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Banking Model Validation System",
        "version": "1.0.0",
        "status": "operational",
        "framework": "SR 11-7",
        "powered_by": "IBM watsonx"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "watsonx_connected": watsonx_client is not None
    }


@app.get("/api/v1/options")
async def get_options():
    """Get available options for model configuration"""
    return {
        "product_types": [
            {"value": "secured", "label": "Secured Loans"},
            {"value": "unsecured", "label": "Unsecured Loans"},
            {"value": "revolving", "label": "Revolving Credit"}
        ],
        "scorecard_types": [
            {"value": "application", "label": "Application Scorecard"},
            {"value": "behavioral", "label": "Behavioral Scorecard"},
            {"value": "collections_early", "label": "Early Stage Collections"},
            {"value": "collections_late", "label": "Late Stage Collections"}
        ],
        "model_types": [
            {"value": "GLM", "label": "Generalized Linear Model"},
            {"value": "GAM", "label": "Generalized Additive Model"},
            {"value": "ANN", "label": "Artificial Neural Network"},
            {"value": "XGBoost", "label": "XGBoost"},
            {"value": "RandomForest", "label": "Random Forest"},
            {"value": "LightGBM", "label": "LightGBM"},
            {"value": "LogisticRegression", "label": "Logistic Regression"},
            {"value": "DecisionTree", "label": "Decision Tree"}
        ]
    }


@app.post("/api/v1/validate", response_model=ValidationStatus)
async def start_validation(
    request: ValidationRequest,
    background_tasks: BackgroundTasks
):
    """
    Start model validation process
    
    This endpoint initiates a comprehensive validation workflow including:
    - Data quality assessment
    - Model performance validation
    - SR 11-7 compliance checking
    - Documentation generation
    """
    if not orchestrator:
        raise HTTPException(
            status_code=503,
            detail="Validation service not initialized. Check watsonx configuration."
        )
    
    try:
        # Register model in governance if requested
        if request.register_governance and governance_tracker:
            model_id = governance_tracker.register_model(
                model_name=request.model_config.model_name,
                model_config=request.model_config.dict()
            )
            print(f"Model registered in governance: {model_id}")
        
        # Start validation in background
        validation_id = f"VAL_{datetime.utcnow().timestamp()}"
        
        background_tasks.add_task(
            run_validation,
            validation_id,
            request.model_config.dict(),
            request.generate_document
        )
        
        return ValidationStatus(
            validation_id=validation_id,
            status="started",
            started_at=datetime.utcnow().isoformat(),
            model_name=request.model_config.model_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_validation(
    validation_id: str,
    model_config: Dict[str, Any],
    generate_document: bool
):
    """Run validation workflow in background"""
    try:
        # Run orchestrated validation
        results = await orchestrator.orchestrate_validation(model_config)
        
        # Generate Word document if requested
        if generate_document:
            doc_generator = SR117DocumentGenerator()
            output_dir = "output/documents"
            os.makedirs(output_dir, exist_ok=True)
            
            doc_path = os.path.join(
                output_dir,
                f"{model_config['model_name']}_validation_report_{datetime.utcnow().strftime('%Y%m%d')}.docx"
            )
            
            doc_generator.generate_validation_report(
                model_config=model_config,
                validation_results=results["results"],
                output_path=doc_path
            )
            
            results["document_path"] = doc_path
        
        print(f"Validation completed: {validation_id}")
        
    except Exception as e:
        print(f"Validation failed: {validation_id} - {e}")


@app.get("/api/v1/validate/{validation_id}", response_model=ValidationStatus)
async def get_validation_status(validation_id: str):
    """Get validation status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")
    
    try:
        status = orchestrator.get_validation_status(validation_id)
        
        return ValidationStatus(
            validation_id=validation_id,
            status=status["status"],
            started_at=status["started_at"],
            completed_at=status.get("completed_at"),
            model_name=status["model_config"].get("model_name", "Unknown"),
            progress=status.get("results", {})
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validate/{validation_id}/results")
async def get_validation_results(validation_id: str):
    """Get complete validation results"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")
    
    try:
        status = orchestrator.get_validation_status(validation_id)
        
        if status["status"] != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Validation not completed. Current status: {status['status']}"
            )
        
        return {
            "validation_id": validation_id,
            "model_config": status["model_config"],
            "results": status["results"],
            "completed_at": status["completed_at"]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validate/{validation_id}/document")
async def download_validation_document(validation_id: str):
    """Download validation document"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")
    
    try:
        status = orchestrator.get_validation_status(validation_id)
        
        if status["status"] != "completed":
            raise HTTPException(
                status_code=400,
                detail="Validation not completed"
            )
        
        doc_path = status["results"].get("documentation", {}).get("document_path")
        
        if not doc_path or not os.path.exists(doc_path):
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return FileResponse(
            doc_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=os.path.basename(doc_path)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validations")
async def list_validations():
    """List all validations"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")
    
    try:
        validations = orchestrator.list_validations()
        return {"validations": validations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/models")
async def list_models():
    """List registered models"""
    if not governance_tracker:
        raise HTTPException(status_code=503, detail="Governance service not initialized")
    
    try:
        models = governance_tracker.tracked_models
        return {"models": list(models.values())}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/models/{model_name}/compliance")
async def get_model_compliance(model_name: str):
    """Get model compliance status"""
    if not governance_tracker:
        raise HTTPException(status_code=503, detail="Governance service not initialized")
    
    try:
        compliance = governance_tracker.get_compliance_status(model_name)
        return compliance
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
