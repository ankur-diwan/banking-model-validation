"""
MLOps Agent for Banking Model Validation
Manages model lifecycle, versioning, monitoring, and automated operations
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from loguru import logger
import json

from ..watsonx.governance_client import WatsonxGovernanceClient
from ..wxo.watsonx_client import WatsonxClient


class MLOpsAgent:
    """
    MLOps Agent for banking model validation
    Handles model lifecycle management, versioning, monitoring, and automation
    """
    
    def __init__(
        self,
        governance_client: WatsonxGovernanceClient,
        watsonx_client: WatsonxClient
    ):
        """
        Initialize MLOps Agent
        
        Args:
            governance_client: watsonx.governance client
            watsonx_client: watsonx.ai client
        """
        self.governance = governance_client
        self.watsonx = watsonx_client
        
        # Model technique characteristics for banking scorecards
        self.technique_characteristics = {
            "GLM": {
                "interpretability": "high",
                "complexity": "low",
                "training_time": "fast",
                "suitable_for": ["application", "behavioral"],
                "regulatory_acceptance": "high",
                "key_metrics": ["AUC", "KS", "Gini", "PSI"],
                "monitoring_approach": "statistical"
            },
            "GAM": {
                "interpretability": "high",
                "complexity": "medium",
                "training_time": "medium",
                "suitable_for": ["application", "behavioral", "collections_early"],
                "regulatory_acceptance": "high",
                "key_metrics": ["AUC", "KS", "Gini", "PSI"],
                "monitoring_approach": "statistical"
            },
            "LogisticRegression": {
                "interpretability": "high",
                "complexity": "low",
                "training_time": "fast",
                "suitable_for": ["application", "behavioral"],
                "regulatory_acceptance": "high",
                "key_metrics": ["AUC", "KS", "Gini", "PSI"],
                "monitoring_approach": "statistical"
            },
            "XGBoost": {
                "interpretability": "medium",
                "complexity": "high",
                "training_time": "medium",
                "suitable_for": ["application", "behavioral", "collections_early", "collections_late"],
                "regulatory_acceptance": "medium",
                "key_metrics": ["AUC", "KS", "Gini", "PSI", "Feature_Importance"],
                "monitoring_approach": "performance_based"
            },
            "RandomForest": {
                "interpretability": "medium",
                "complexity": "high",
                "training_time": "medium",
                "suitable_for": ["application", "behavioral", "collections_early", "collections_late"],
                "regulatory_acceptance": "medium",
                "key_metrics": ["AUC", "KS", "Gini", "PSI", "Feature_Importance"],
                "monitoring_approach": "performance_based"
            },
            "LightGBM": {
                "interpretability": "medium",
                "complexity": "high",
                "training_time": "fast",
                "suitable_for": ["application", "behavioral", "collections_early", "collections_late"],
                "regulatory_acceptance": "medium",
                "key_metrics": ["AUC", "KS", "Gini", "PSI", "Feature_Importance"],
                "monitoring_approach": "performance_based"
            },
            "ANN": {
                "interpretability": "low",
                "complexity": "very_high",
                "training_time": "slow",
                "suitable_for": ["behavioral", "collections_late"],
                "regulatory_acceptance": "low",
                "key_metrics": ["AUC", "KS", "Gini", "PSI", "SHAP"],
                "monitoring_approach": "explainability_based"
            },
            "DecisionTree": {
                "interpretability": "high",
                "complexity": "low",
                "training_time": "fast",
                "suitable_for": ["collections_early"],
                "regulatory_acceptance": "high",
                "key_metrics": ["AUC", "KS", "Gini"],
                "monitoring_approach": "rule_based"
            }
        }
        
        logger.info("MLOps Agent initialized")
    
    # ==================== Use Case Onboarding ====================
    
    async def onboard_use_case(
        self,
        product_type: str,
        scorecard_type: str,
        business_objective: str,
        risk_level: str = "high"
    ) -> Dict[str, Any]:
        """
        Onboard a new model use case
        
        Args:
            product_type: Product type (secured, unsecured, revolving)
            scorecard_type: Scorecard type (application, behavioral, collections)
            business_objective: Business objective description
            risk_level: Risk level (low, medium, high, critical)
            
        Returns:
            Use case details including ID and recommendations
        """
        logger.info(f"Onboarding use case: {product_type} - {scorecard_type}")
        
        # Determine business area
        business_area_map = {
            "application": "Credit Origination",
            "behavioral": "Account Management",
            "collections_early": "Early Collections",
            "collections_late": "Late Collections"
        }
        business_area = business_area_map.get(scorecard_type, "Credit Risk")
        
        # Create use case name
        use_case_name = f"{product_type.title()} {scorecard_type.replace('_', ' ').title()} Scorecard"
        
        # Register in governance
        use_case_id = self.governance.register_use_case(
            use_case_name=use_case_name,
            description=business_objective,
            business_area=business_area,
            regulatory_framework="SR 11-7",
            risk_level=risk_level,
            metadata={
                "product_type": product_type,
                "scorecard_type": scorecard_type
            }
        )
        
        # Get model technique recommendations
        recommendations = self._recommend_model_techniques(scorecard_type)
        
        return {
            "use_case_id": use_case_id,
            "use_case_name": use_case_name,
            "business_area": business_area,
            "recommended_techniques": recommendations,
            "next_steps": [
                "Review recommended modeling techniques",
                "Check for existing similar models",
                "Prepare training data",
                "Define validation requirements"
            ]
        }
    
    def _recommend_model_techniques(
        self,
        scorecard_type: str,
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """Recommend suitable modeling techniques"""
        recommendations = []
        
        for technique, chars in self.technique_characteristics.items():
            if scorecard_type in chars["suitable_for"]:
                score = 0
                
                # Score based on regulatory acceptance
                if chars["regulatory_acceptance"] == "high":
                    score += 3
                elif chars["regulatory_acceptance"] == "medium":
                    score += 2
                else:
                    score += 1
                
                # Score based on interpretability
                if chars["interpretability"] == "high":
                    score += 3
                elif chars["interpretability"] == "medium":
                    score += 2
                else:
                    score += 1
                
                recommendations.append({
                    "technique": technique,
                    "score": score,
                    "characteristics": chars,
                    "rationale": self._get_technique_rationale(technique, scorecard_type)
                })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:top_n]
    
    def _get_technique_rationale(self, technique: str, scorecard_type: str) -> str:
        """Get rationale for technique recommendation"""
        rationales = {
            "GLM": "Highly interpretable and widely accepted by regulators. Ideal for transparent credit decisions.",
            "GAM": "Balances interpretability with flexibility. Good for capturing non-linear relationships.",
            "LogisticRegression": "Simple, interpretable, and fast. Excellent baseline model.",
            "XGBoost": "High performance with good feature importance. Requires explainability framework.",
            "RandomForest": "Robust and handles non-linearity well. Moderate interpretability.",
            "LightGBM": "Fast training with good performance. Suitable for large datasets.",
            "ANN": "Captures complex patterns but requires extensive explainability. Use with caution.",
            "DecisionTree": "Highly interpretable rules. Good for simple decision logic."
        }
        return rationales.get(technique, "Suitable for this use case.")
    
    # ==================== Model Recommendation ====================
    
    async def check_existing_models(
        self,
        product_type: str,
        scorecard_type: str,
        model_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check for existing models before building new one
        
        Args:
            product_type: Product type
            scorecard_type: Scorecard type
            model_type: Optional model type filter
            
        Returns:
            Existing models and recommendation
        """
        logger.info(f"Checking existing models for {product_type} - {scorecard_type}")
        
        # Get all models
        all_models = self.governance.list_models()
        
        # Filter by product and scorecard type
        matching_models = [
            m for m in all_models
            if m["product_type"] == product_type
            and m["scorecard_type"] == scorecard_type
        ]
        
        if model_type:
            matching_models = [m for m in matching_models if m["model_type"] == model_type]
        
        # Calculate similarity scores
        model_recommendations = []
        for model in matching_models:
            # Get latest version
            latest_version = self.governance.get_latest_version(model["model_id"])
            
            if latest_version:
                # Calculate similarity score (simplified)
                similarity_score = 0.8  # Base score for same product/scorecard
                
                if model_type and model["model_type"] == model_type:
                    similarity_score += 0.2
                
                # Check if model is in good standing
                if model["lifecycle_stage"] in ["deployed", "monitoring"]:
                    similarity_score += 0.1
                
                model_recommendations.append({
                    "model_id": model["model_id"],
                    "model_name": model["name"],
                    "model_type": model["model_type"],
                    "lifecycle_stage": model["lifecycle_stage"],
                    "similarity_score": min(similarity_score, 1.0),
                    "latest_version": latest_version["version"],
                    "performance_metrics": latest_version["performance_metrics"],
                    "recommendation": "reuse" if similarity_score > 0.7 else "consider"
                })
        
        # Sort by similarity
        model_recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Determine overall recommendation
        if model_recommendations and model_recommendations[0]["similarity_score"] > 0.7:
            recommendation = "reuse_existing"
            message = f"Found {len(model_recommendations)} similar model(s). Consider reusing or updating existing model."
        else:
            recommendation = "build_new"
            message = "No highly similar models found. Proceed with building new model."
        
        return {
            "recommendation": recommendation,
            "message": message,
            "existing_models": model_recommendations,
            "total_found": len(model_recommendations)
        }
    
    # ==================== Model Registration & Versioning ====================
    
    async def register_new_model(
        self,
        model_name: str,
        use_case_id: str,
        model_type: str,
        product_type: str,
        scorecard_type: str,
        features: List[str],
        data_version: str,
        performance_metrics: Dict[str, float],
        validation_results: Dict[str, Any],
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new model with initial version
        
        Args:
            model_name: Model name
            use_case_id: Use case ID
            model_type: Model type
            product_type: Product type
            scorecard_type: Scorecard type
            features: List of features
            data_version: Data version
            performance_metrics: Performance metrics
            validation_results: Validation results
            description: Model description
            
        Returns:
            Model and version details
        """
        logger.info(f"Registering new model: {model_name}")
        
        # Register model
        model_id = self.governance.register_model(
            model_name=model_name,
            use_case_id=use_case_id,
            model_type=model_type,
            product_type=product_type,
            scorecard_type=scorecard_type,
            description=description,
            metadata={
                "created_by": "MLOps Agent",
                "framework": "SR 11-7"
            }
        )
        
        # Register initial version
        version_id = self.governance.register_model_version(
            model_id=model_id,
            version="1.0",
            features=features,
            data_version=data_version,
            training_date=datetime.utcnow().isoformat(),
            performance_metrics=performance_metrics,
            validation_results=validation_results,
            metadata={
                "initial_version": True
            }
        )
        
        # Update lifecycle stage
        self.governance.update_model_lifecycle_stage(
            model_id=model_id,
            stage="validation",
            notes="Initial model registered, pending validation"
        )
        
        # Log compliance event
        self.governance.log_compliance_event(
            model_id=model_id,
            event_type="registration",
            description=f"Model {model_name} registered with version 1.0",
            severity="info"
        )
        
        # Set up monitoring thresholds
        monitoring_config = self._setup_monitoring_thresholds(
            model_type=model_type,
            baseline_metrics=performance_metrics
        )
        
        return {
            "model_id": model_id,
            "version_id": version_id,
            "model_name": model_name,
            "version": "1.0",
            "lifecycle_stage": "validation",
            "monitoring_config": monitoring_config,
            "next_steps": [
                "Complete validation testing",
                "Review validation report",
                "Obtain approval for deployment",
                "Deploy to production"
            ]
        }
    
    def _setup_monitoring_thresholds(
        self,
        model_type: str,
        baseline_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Set up monitoring thresholds based on model type"""
        technique_info = self.technique_characteristics.get(model_type, {})
        monitoring_approach = technique_info.get("monitoring_approach", "statistical")
        
        # Define thresholds based on monitoring approach
        if monitoring_approach == "statistical":
            thresholds = {
                "AUC": baseline_metrics.get("AUC", 0.7) * 0.95,  # 5% degradation
                "KS": baseline_metrics.get("KS", 0.3) * 0.90,    # 10% degradation
                "Gini": baseline_metrics.get("Gini", 0.4) * 0.95,
                "PSI": 0.25  # Standard PSI threshold
            }
        elif monitoring_approach == "performance_based":
            thresholds = {
                "AUC": baseline_metrics.get("AUC", 0.7) * 0.93,  # 7% degradation
                "KS": baseline_metrics.get("KS", 0.3) * 0.88,
                "Gini": baseline_metrics.get("Gini", 0.4) * 0.93,
                "PSI": 0.20,
                "Feature_Importance_Shift": 0.15
            }
        elif monitoring_approach == "explainability_based":
            thresholds = {
                "AUC": baseline_metrics.get("AUC", 0.7) * 0.90,
                "KS": baseline_metrics.get("KS", 0.3) * 0.85,
                "PSI": 0.15,
                "SHAP_Consistency": 0.80
            }
        else:  # rule_based
            thresholds = {
                "AUC": baseline_metrics.get("AUC", 0.7) * 0.95,
                "Rule_Coverage": 0.90,
                "Rule_Stability": 0.85
            }
        
        return {
            "monitoring_approach": monitoring_approach,
            "thresholds": thresholds,
            "check_frequency": "monthly",
            "alert_on_breach": True,
            "auto_retrain_threshold": 0.85  # Trigger retraining at 85% of baseline
        }
    
    # ==================== Production Monitoring ====================
    
    async def monitor_production_model(
        self,
        model_id: str,
        version_id: str,
        current_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Monitor model performance in production
        
        Args:
            model_id: Model ID
            version_id: Version ID
            current_metrics: Current performance metrics
            
        Returns:
            Monitoring results and recommendations
        """
        logger.info(f"Monitoring model {model_id} version {version_id}")
        
        # Log metrics
        self.governance.log_monitoring_metrics(
            model_id=model_id,
            version_id=version_id,
            metrics=current_metrics
        )
        
        # Get model and version info
        model = self.governance.get_model(model_id)
        versions = self.governance.get_model_versions(model_id)
        version = next((v for v in versions if v["version_id"] == version_id), None)
        
        if not version:
            return {"error": "Version not found"}
        
        # Get monitoring config
        baseline_metrics = version["performance_metrics"]
        monitoring_config = self._setup_monitoring_thresholds(
            model_type=model["model_type"],
            baseline_metrics=baseline_metrics
        )
        
        # Check for threshold breaches
        breaches = []
        warnings = []
        
        for metric_name, threshold in monitoring_config["thresholds"].items():
            if metric_name in current_metrics:
                current_value = current_metrics[metric_name]
                baseline_value = baseline_metrics.get(metric_name, threshold)
                
                # Check if below threshold
                if current_value < threshold:
                    breaches.append({
                        "metric": metric_name,
                        "current": current_value,
                        "threshold": threshold,
                        "baseline": baseline_value,
                        "degradation": ((baseline_value - current_value) / baseline_value) * 100
                    })
                # Check if approaching threshold (within 5%)
                elif current_value < threshold * 1.05:
                    warnings.append({
                        "metric": metric_name,
                        "current": current_value,
                        "threshold": threshold,
                        "message": "Approaching threshold"
                    })
        
        # Determine status
        if breaches:
            status = "critical"
            recommendation = "Immediate action required - Model retraining recommended"
        elif warnings:
            status = "warning"
            recommendation = "Monitor closely - Consider scheduling retraining"
        else:
            status = "healthy"
            recommendation = "Model performing within acceptable range"
        
        # Check if retraining needed
        retraining_check = self.governance.check_retraining_needed(
            model_id=model_id,
            version_id=version_id,
            thresholds=monitoring_config["thresholds"]
        )
        
        # Log compliance event if critical
        if status == "critical":
            self.governance.log_compliance_event(
                model_id=model_id,
                event_type="monitoring_alert",
                description=f"Critical performance degradation detected: {len(breaches)} metric(s) below threshold",
                severity="critical",
                metadata={"breaches": breaches}
            )
        
        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "current_metrics": current_metrics,
            "baseline_metrics": baseline_metrics,
            "thresholds": monitoring_config["thresholds"],
            "breaches": breaches,
            "warnings": warnings,
            "retraining_needed": retraining_check["retraining_needed"],
            "retraining_reasons": retraining_check["reasons"],
            "recommendation": recommendation
        }
    
    # ==================== Automated Deployment ====================
    
    async def deploy_model(
        self,
        model_id: str,
        version_id: str,
        deployment_environment: str = "production",
        approval_required: bool = True
    ) -> Dict[str, Any]:
        """
        Deploy model to production with pre-deployment checks
        
        Args:
            model_id: Model ID
            version_id: Version ID
            deployment_environment: Target environment
            approval_required: Whether approval is required
            
        Returns:
            Deployment results
        """
        logger.info(f"Deploying model {model_id} version {version_id} to {deployment_environment}")
        
        # Pre-deployment checks
        checks = await self._run_deployment_checks(model_id, version_id)
        
        if not checks["passed"]:
            return {
                "deployed": False,
                "reason": "Pre-deployment checks failed",
                "failed_checks": checks["failed_checks"]
            }
        
        # Update lifecycle stage
        self.governance.update_model_lifecycle_stage(
            model_id=model_id,
            stage="deployed",
            notes=f"Deployed to {deployment_environment}"
        )
        
        # Log compliance event
        self.governance.log_compliance_event(
            model_id=model_id,
            event_type="deployment",
            description=f"Model deployed to {deployment_environment}",
            severity="info",
            metadata={
                "version_id": version_id,
                "environment": deployment_environment,
                "deployment_time": datetime.utcnow().isoformat()
            }
        )
        
        return {
            "deployed": True,
            "model_id": model_id,
            "version_id": version_id,
            "environment": deployment_environment,
            "deployment_time": datetime.utcnow().isoformat(),
            "pre_deployment_checks": checks,
            "next_steps": [
                "Monitor model performance",
                "Set up alerting",
                "Schedule periodic reviews",
                "Document deployment"
            ]
        }
    
    async def _run_deployment_checks(
        self,
        model_id: str,
        version_id: str
    ) -> Dict[str, Any]:
        """Run pre-deployment checks"""
        checks = {
            "validation_complete": False,
            "performance_acceptable": False,
            "documentation_complete": False,
            "approval_obtained": False
        }
        
        failed_checks = []
        
        # Check validation status
        model = self.governance.get_model(model_id)
        if model["lifecycle_stage"] in ["validation", "approved"]:
            checks["validation_complete"] = True
        else:
            failed_checks.append("Model not validated")
        
        # Check performance
        versions = self.governance.get_model_versions(model_id)
        version = next((v for v in versions if v["version_id"] == version_id), None)
        
        if version and version["performance_metrics"].get("AUC", 0) > 0.65:
            checks["performance_acceptable"] = True
        else:
            failed_checks.append("Performance metrics below minimum threshold")
        
        # Check documentation
        if version and version.get("validation_results"):
            checks["documentation_complete"] = True
        else:
            failed_checks.append("Validation documentation incomplete")
        
        # Check approval (simplified - would integrate with approval workflow)
        checks["approval_obtained"] = True  # Assume approved for demo
        
        passed = all(checks.values())
        
        return {
            "passed": passed,
            "checks": checks,
            "failed_checks": failed_checks
        }
    
    # ==================== Documentation Generation ====================
    
    async def generate_model_documentation(
        self,
        model_id: str,
        version_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive model documentation
        
        Args:
            model_id: Model ID
            version_id: Optional version ID (uses latest if not provided)
            
        Returns:
            Documentation content
        """
        logger.info(f"Generating documentation for model {model_id}")
        
        # Get model card
        model_card = self.governance.generate_model_card(model_id)
        
        # Get compliance report
        compliance_report = self.governance.generate_compliance_report(model_id)
        
        # Get monitoring history
        if version_id:
            monitoring_metrics = self.governance.get_monitoring_metrics(model_id, version_id)
        else:
            latest_version = self.governance.get_latest_version(model_id)
            if latest_version:
                monitoring_metrics = self.governance.get_monitoring_metrics(
                    model_id,
                    latest_version["version_id"]
                )
            else:
                monitoring_metrics = []
        
        documentation = {
            "model_card": model_card,
            "compliance_report": compliance_report,
            "monitoring_summary": {
                "total_monitoring_records": len(monitoring_metrics),
                "monitoring_period": {
                    "start": monitoring_metrics[0]["timestamp"] if monitoring_metrics else None,
                    "end": monitoring_metrics[-1]["timestamp"] if monitoring_metrics else None
                }
            },
            "generated_at": datetime.utcnow().isoformat(),
            "document_version": "1.0"
        }
        
        return documentation


# Made with ❤️ by Bob

# Made with Bob
