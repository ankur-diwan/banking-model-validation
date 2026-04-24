"""
watsonx.governance Client for Banking Model Validation
Comprehensive model lifecycle management and regulatory compliance tracking
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from loguru import logger
import json


class WatsonxGovernanceClient:
    """
    Client for IBM watsonx.governance
    Manages model lifecycle, monitoring, and compliance for banking models
    """
    
    def __init__(self):
        """Initialize watsonx.governance client"""
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.space_id = os.getenv("WATSONX_SPACE_ID")
        self.governance_url = os.getenv("WATSONX_GOVERNANCE_URL", "https://api.dataplatform.cloud.ibm.com")
        
        # In-memory storage for demo (replace with actual API calls in production)
        self.use_cases = {}
        self.models = {}
        self.model_versions = {}
        self.monitoring_data = {}
        self.compliance_records = {}
        
        logger.info("watsonx.governance client initialized")
    
    # ==================== Use Case Management ====================
    
    def register_use_case(
        self,
        use_case_name: str,
        description: str,
        business_area: str,
        regulatory_framework: str = "SR 11-7",
        risk_level: str = "high",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a new model use case in watsonx.governance
        
        Args:
            use_case_name: Name of the use case
            description: Detailed description
            business_area: Business area (e.g., "Credit Risk", "Collections")
            regulatory_framework: Regulatory framework (default: SR 11-7)
            risk_level: Risk level (low, medium, high, critical)
            metadata: Additional metadata
            
        Returns:
            Use case ID
        """
        use_case_id = f"UC_{datetime.utcnow().timestamp()}"
        
        use_case = {
            "use_case_id": use_case_id,
            "name": use_case_name,
            "description": description,
            "business_area": business_area,
            "regulatory_framework": regulatory_framework,
            "risk_level": risk_level,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.use_cases[use_case_id] = use_case
        
        logger.info(f"Registered use case: {use_case_name} ({use_case_id})")
        return use_case_id
    
    def get_use_case(self, use_case_id: str) -> Dict[str, Any]:
        """Get use case details"""
        if use_case_id not in self.use_cases:
            raise ValueError(f"Use case not found: {use_case_id}")
        return self.use_cases[use_case_id]
    
    def list_use_cases(self) -> List[Dict[str, Any]]:
        """List all use cases"""
        return list(self.use_cases.values())
    
    # ==================== Model Registry ====================
    
    def register_model(
        self,
        model_name: str,
        use_case_id: str,
        model_type: str,
        product_type: str,
        scorecard_type: str,
        description: Optional[str] = None,
        owner: str = "Model Risk Management",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a model in watsonx.governance
        
        Args:
            model_name: Name of the model
            use_case_id: Associated use case ID
            model_type: Type of model (GLM, XGBoost, etc.)
            product_type: Product type (secured, unsecured, revolving)
            scorecard_type: Scorecard type (application, behavioral, collections)
            description: Model description
            owner: Model owner
            metadata: Additional metadata
            
        Returns:
            Model ID
        """
        model_id = f"MDL_{datetime.utcnow().timestamp()}"
        
        model = {
            "model_id": model_id,
            "name": model_name,
            "use_case_id": use_case_id,
            "model_type": model_type,
            "product_type": product_type,
            "scorecard_type": scorecard_type,
            "description": description or f"{scorecard_type} scorecard for {product_type} products",
            "owner": owner,
            "status": "registered",
            "lifecycle_stage": "development",
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.models[model_id] = model
        
        logger.info(f"Registered model: {model_name} ({model_id})")
        return model_id
    
    def get_model(self, model_id: str) -> Dict[str, Any]:
        """Get model details"""
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        return self.models[model_id]
    
    def list_models(self, use_case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List models, optionally filtered by use case"""
        models = list(self.models.values())
        if use_case_id:
            models = [m for m in models if m["use_case_id"] == use_case_id]
        return models
    
    def update_model_lifecycle_stage(
        self,
        model_id: str,
        stage: str,
        notes: Optional[str] = None
    ):
        """
        Update model lifecycle stage
        
        Stages: development, validation, approved, deployed, monitoring, retired
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        self.models[model_id]["lifecycle_stage"] = stage
        self.models[model_id]["stage_updated_at"] = datetime.utcnow().isoformat()
        
        if notes:
            if "lifecycle_history" not in self.models[model_id]:
                self.models[model_id]["lifecycle_history"] = []
            
            self.models[model_id]["lifecycle_history"].append({
                "stage": stage,
                "timestamp": datetime.utcnow().isoformat(),
                "notes": notes
            })
        
        logger.info(f"Updated model {model_id} lifecycle stage to: {stage}")
    
    # ==================== Model Versioning ====================
    
    def register_model_version(
        self,
        model_id: str,
        version: str,
        features: List[str],
        data_version: str,
        training_date: str,
        performance_metrics: Dict[str, float],
        validation_results: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a new model version
        
        Args:
            model_id: Parent model ID
            version: Version number (e.g., "1.0", "1.1")
            features: List of feature names
            data_version: Version of training data
            training_date: Date model was trained
            performance_metrics: Performance metrics (AUC, KS, Gini, etc.)
            validation_results: Validation test results
            metadata: Additional metadata
            
        Returns:
            Version ID
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        version_id = f"VER_{datetime.utcnow().timestamp()}"
        
        model_version = {
            "version_id": version_id,
            "model_id": model_id,
            "version": version,
            "features": features,
            "feature_count": len(features),
            "data_version": data_version,
            "training_date": training_date,
            "performance_metrics": performance_metrics,
            "validation_results": validation_results or {},
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        if model_id not in self.model_versions:
            self.model_versions[model_id] = []
        
        self.model_versions[model_id].append(model_version)
        
        logger.info(f"Registered model version: {version} for model {model_id}")
        return version_id
    
    def get_model_versions(self, model_id: str) -> List[Dict[str, Any]]:
        """Get all versions of a model"""
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        return self.model_versions.get(model_id, [])
    
    def get_latest_version(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest version of a model"""
        versions = self.get_model_versions(model_id)
        if not versions:
            return None
        
        return max(versions, key=lambda v: v["created_at"])
    
    # ==================== Model Monitoring ====================
    
    def log_monitoring_metrics(
        self,
        model_id: str,
        version_id: str,
        metrics: Dict[str, float],
        timestamp: Optional[str] = None
    ):
        """
        Log monitoring metrics for a model version
        
        Args:
            model_id: Model ID
            version_id: Version ID
            metrics: Performance metrics
            timestamp: Timestamp (defaults to now)
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        key = f"{model_id}_{version_id}"
        
        if key not in self.monitoring_data:
            self.monitoring_data[key] = []
        
        monitoring_record = {
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "metrics": metrics
        }
        
        self.monitoring_data[key].append(monitoring_record)
        
        logger.debug(f"Logged monitoring metrics for {model_id} version {version_id}")
    
    def get_monitoring_metrics(
        self,
        model_id: str,
        version_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get monitoring metrics for a model version"""
        key = f"{model_id}_{version_id}"
        
        if key not in self.monitoring_data:
            return []
        
        metrics = self.monitoring_data[key]
        
        # Filter by date range if provided
        if start_date:
            metrics = [m for m in metrics if m["timestamp"] >= start_date]
        if end_date:
            metrics = [m for m in metrics if m["timestamp"] <= end_date]
        
        return metrics
    
    def detect_model_drift(
        self,
        model_id: str,
        version_id: str,
        baseline_metrics: Dict[str, float],
        threshold: float = 0.05
    ) -> Dict[str, Any]:
        """
        Detect model drift by comparing recent metrics to baseline
        
        Args:
            model_id: Model ID
            version_id: Version ID
            baseline_metrics: Baseline performance metrics
            threshold: Drift threshold (default: 5%)
            
        Returns:
            Drift detection results
        """
        recent_metrics = self.get_monitoring_metrics(model_id, version_id)
        
        if not recent_metrics:
            return {
                "drift_detected": False,
                "message": "No monitoring data available"
            }
        
        # Get most recent metrics
        latest = recent_metrics[-1]["metrics"]
        
        # Calculate drift for each metric
        drift_results = {}
        drift_detected = False
        
        for metric_name, baseline_value in baseline_metrics.items():
            if metric_name in latest:
                current_value = latest[metric_name]
                drift = abs(current_value - baseline_value) / baseline_value
                
                drift_results[metric_name] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "drift_percentage": drift * 100,
                    "threshold_exceeded": drift > threshold
                }
                
                if drift > threshold:
                    drift_detected = True
        
        return {
            "drift_detected": drift_detected,
            "timestamp": recent_metrics[-1]["timestamp"],
            "metrics": drift_results,
            "recommendation": "Model retraining recommended" if drift_detected else "Model performance stable"
        }
    
    # ==================== Compliance & Audit ====================
    
    def log_compliance_event(
        self,
        model_id: str,
        event_type: str,
        description: str,
        severity: str = "info",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a compliance event
        
        Args:
            model_id: Model ID
            event_type: Type of event (validation, audit, review, etc.)
            description: Event description
            severity: Severity level (info, warning, critical)
            metadata: Additional metadata
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        if model_id not in self.compliance_records:
            self.compliance_records[model_id] = []
        
        event = {
            "event_id": f"EVT_{datetime.utcnow().timestamp()}",
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "description": description,
            "severity": severity,
            "metadata": metadata or {}
        }
        
        self.compliance_records[model_id].append(event)
        
        logger.info(f"Logged compliance event for {model_id}: {event_type}")
    
    def get_compliance_history(
        self,
        model_id: str,
        event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get compliance history for a model"""
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        events = self.compliance_records.get(model_id, [])
        
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        
        return events
    
    def generate_compliance_report(
        self,
        model_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate compliance report for a model
        
        Args:
            model_id: Model ID
            start_date: Start date for report
            end_date: End date for report
            
        Returns:
            Compliance report
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        model = self.models[model_id]
        events = self.get_compliance_history(model_id)
        
        # Filter by date range
        if start_date:
            events = [e for e in events if e["timestamp"] >= start_date]
        if end_date:
            events = [e for e in events if e["timestamp"] <= end_date]
        
        # Categorize events
        event_summary = {}
        for event in events:
            event_type = event["event_type"]
            if event_type not in event_summary:
                event_summary[event_type] = 0
            event_summary[event_type] += 1
        
        # Check for critical events
        critical_events = [e for e in events if e["severity"] == "critical"]
        
        return {
            "model_id": model_id,
            "model_name": model["name"],
            "report_period": {
                "start": start_date or "inception",
                "end": end_date or datetime.utcnow().isoformat()
            },
            "total_events": len(events),
            "event_summary": event_summary,
            "critical_events": len(critical_events),
            "compliance_status": "compliant" if len(critical_events) == 0 else "requires_attention",
            "events": events
        }
    
    # ==================== Model Cards ====================
    
    def generate_model_card(self, model_id: str) -> Dict[str, Any]:
        """
        Generate a model card with comprehensive information
        
        Args:
            model_id: Model ID
            
        Returns:
            Model card
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        model = self.models[model_id]
        versions = self.get_model_versions(model_id)
        latest_version = self.get_latest_version(model_id)
        compliance_events = self.get_compliance_history(model_id)
        
        # Get use case info
        use_case = self.use_cases.get(model["use_case_id"], {})
        
        model_card = {
            "model_details": {
                "model_id": model_id,
                "name": model["name"],
                "type": model["model_type"],
                "product_type": model["product_type"],
                "scorecard_type": model["scorecard_type"],
                "description": model["description"],
                "owner": model["owner"],
                "lifecycle_stage": model["lifecycle_stage"],
                "created_at": model["created_at"]
            },
            "use_case": {
                "name": use_case.get("name", "Unknown"),
                "business_area": use_case.get("business_area", "Unknown"),
                "regulatory_framework": use_case.get("regulatory_framework", "SR 11-7"),
                "risk_level": use_case.get("risk_level", "high")
            },
            "versions": {
                "total": len(versions),
                "latest": latest_version["version"] if latest_version else None
            },
            "latest_version_details": latest_version,
            "compliance": {
                "total_events": len(compliance_events),
                "last_validation": None,
                "last_audit": None
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Find last validation and audit
        for event in reversed(compliance_events):
            if event["event_type"] == "validation" and not model_card["compliance"]["last_validation"]:
                model_card["compliance"]["last_validation"] = event["timestamp"]
            if event["event_type"] == "audit" and not model_card["compliance"]["last_audit"]:
                model_card["compliance"]["last_audit"] = event["timestamp"]
            
            if model_card["compliance"]["last_validation"] and model_card["compliance"]["last_audit"]:
                break
        
        return model_card
    
    # ==================== Recommendations ====================
    
    def check_retraining_needed(
        self,
        model_id: str,
        version_id: str,
        thresholds: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Check if model retraining is needed based on monitoring metrics
        
        Args:
            model_id: Model ID
            version_id: Version ID
            thresholds: Performance thresholds
            
        Returns:
            Retraining recommendation
        """
        # Get latest version info
        versions = self.get_model_versions(model_id)
        version = next((v for v in versions if v["version_id"] == version_id), None)
        
        if not version:
            return {
                "retraining_needed": False,
                "reason": "Version not found"
            }
        
        # Check for drift
        baseline_metrics = version["performance_metrics"]
        drift_result = self.detect_model_drift(model_id, version_id, baseline_metrics)
        
        # Check monitoring metrics
        recent_metrics = self.get_monitoring_metrics(model_id, version_id)
        
        reasons = []
        retraining_needed = False
        
        if drift_result["drift_detected"]:
            reasons.append("Performance drift detected")
            retraining_needed = True
        
        # Check if any metric falls below threshold
        if recent_metrics:
            latest = recent_metrics[-1]["metrics"]
            for metric_name, threshold in thresholds.items():
                if metric_name in latest and latest[metric_name] < threshold:
                    reasons.append(f"{metric_name} below threshold: {latest[metric_name]:.4f} < {threshold}")
                    retraining_needed = True
        
        # Check age of model
        training_date = datetime.fromisoformat(version["training_date"])
        age_days = (datetime.utcnow() - training_date).days
        
        if age_days > 365:  # More than 1 year old
            reasons.append(f"Model is {age_days} days old (>365 days)")
            retraining_needed = True
        
        return {
            "retraining_needed": retraining_needed,
            "reasons": reasons,
            "drift_analysis": drift_result,
            "model_age_days": age_days,
            "recommendation": "Schedule model retraining" if retraining_needed else "Continue monitoring"
        }


# Made with ❤️ by Bob

# Made with Bob
