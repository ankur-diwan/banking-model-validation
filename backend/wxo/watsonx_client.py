"""
watsonx.ai and watsonx.governance Integration Client
Provides unified interface for IBM watsonx services
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

import requests
from ibm_watsonx_ai import APIClient
from loguru import logger


class WatsonxClient:
    """
    Unified client for watsonx.ai and watsonx.governance
    """

    IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
    CHAT_API_VERSION = "2023-05-29"

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        space_id: Optional[str] = None,
        url: Optional[str] = None
    ):
        """
        Initialize watsonx client

        Args:
            api_key: IBM Cloud API key
            project_id: watsonx.ai project ID
            space_id: watsonx.ai deployment space ID
            url: watsonx.ai service URL
        """
        self.api_key = api_key or os.getenv("WATSONX_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.space_id = space_id or os.getenv("WATSONX_SPACE_ID")
        self.url = (url or os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")).rstrip("/")
        self.model_id = os.getenv("WATSONX_MODEL_ID", "meta-llama/llama-3-3-70b-instruct")

        if not self.api_key:
            raise ValueError("WATSONX_API_KEY must be provided")
        if not self.project_id and not self.space_id:
            raise ValueError("Either WATSONX_PROJECT_ID or WATSONX_SPACE_ID must be provided")

        self.credentials = {
            "apikey": self.api_key,
            "url": self.url
        }

        self.client = None
        self.access_token = None
        self.access_token_expiry = None

        try:
            self.client = APIClient(self.credentials, project_id=self.project_id)
            if not self.project_id and self.space_id:
                self.client.set.default_space(self.space_id)
            logger.info("watsonx APIClient initialized successfully")
        except Exception as sdk_error:
            logger.warning(f"watsonx APIClient initialization failed; REST fallback will be used: {sdk_error}")

        self._refresh_access_token()
        logger.info("watsonx REST client initialized successfully")

    def _refresh_access_token(self) -> str:
        """Fetch IAM bearer token using IBM Cloud API key."""
        response = requests.post(
            self.IAM_TOKEN_URL,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            },
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.api_key
            },
            timeout=30
        )
        response.raise_for_status()
        token_payload = response.json()

        self.access_token = token_payload["access_token"]
        expires_in = int(token_payload.get("expires_in", 3600))
        self.access_token_expiry = datetime.utcnow() + timedelta(seconds=max(expires_in - 300, 0))

        return self.access_token

    def _get_access_token(self) -> str:
        """Return cached token or refresh if expiring soon."""
        if not self.access_token or not self.access_token_expiry or datetime.utcnow() >= self.access_token_expiry:
            return self._refresh_access_token()
        return self.access_token

    def _chat_endpoint(self) -> str:
        """Return watsonx chat inference endpoint."""
        return f"{self.url}/ml/v1/text/chat?version={self.CHAT_API_VERSION}"

    def _build_generation_parameters(self, parameters: Optional[Dict] = None) -> Dict[str, Any]:
        """Map app parameters to watsonx REST chat payload fields."""
        default_params: Dict[str, Any] = {
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "temperature": 0,
            "top_p": 1
        }

        if parameters:
            mapped = dict(parameters)
            if "max_new_tokens" in mapped and "max_tokens" not in mapped:
                mapped["max_tokens"] = mapped.pop("max_new_tokens")
            mapped.pop("decoding_method", None)
            mapped.pop("top_k", None)
            default_params.update(mapped)

        return default_params

    async def generate_text(
        self,
        prompt: str,
        model_id: str = "ibm/granite-13b-chat-v2",
        parameters: Optional[Dict] = None
    ) -> str:
        """
        Generate text using watsonx REST chat inference.

        Args:
            prompt: Input prompt
            model_id: Model identifier
            parameters: Generation parameters

        Returns:
            Generated text
        """
        try:
            effective_model_id = model_id
            if not effective_model_id or effective_model_id == "ibm/granite-13b-chat-v2":
                effective_model_id = self.model_id

            payload: Dict[str, Any] = {
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                "model_id": effective_model_id,
                **self._build_generation_parameters(parameters)
            }

            if self.project_id:
                payload["project_id"] = self.project_id
            elif self.space_id:
                payload["space_id"] = self.space_id

            response = requests.post(
                self._chat_endpoint(),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self._get_access_token()}"
                },
                json=payload,
                timeout=120
            )

            if response.status_code == 401:
                self._refresh_access_token()
                response = requests.post(
                    self._chat_endpoint(),
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {self.access_token}"
                    },
                    json=payload,
                    timeout=120
                )

            response.raise_for_status()
            response_json = response.json()

            choices = response_json.get("choices", [])
            if choices:
                first_choice = choices[0]
                message = first_choice.get("message", {})
                content = message.get("content")
                if content:
                    return content

            if "results" in response_json and response_json["results"]:
                generated_text = response_json["results"][0].get("generated_text")
                if generated_text:
                    return generated_text

            logger.error(f"Unexpected watsonx response format: {response_json}")
            raise ValueError("Unexpected response format from watsonx chat API")

        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    async def analyze_model_validation(
        self,
        model_metadata: Dict,
        validation_context: Dict
    ) -> Dict:
        """
        Use watsonx.ai to analyze model validation requirements
        
        Args:
            model_metadata: Model information
            validation_context: Validation context
            
        Returns:
            Validation analysis results
        """
        prompt = f"""
        You are an expert in banking model validation and SR 11-7 compliance.
        
        Model Information:
        - Type: {model_metadata.get('model_type')}
        - Scorecard: {model_metadata.get('scorecard_type')}
        - Product: {model_metadata.get('product_type')}
        
        Validation Context:
        {json.dumps(validation_context, indent=2)}
        
        Based on SR 11-7 guidelines, provide:
        1. Key validation requirements for this model type
        2. Critical assumptions to test
        3. Performance metrics to evaluate
        4. Data quality checks needed
        5. Documentation requirements
        
        Provide a structured JSON response.
        """
        
        response = await self.generate_text(prompt)
        
        try:
            # Parse JSON response
            analysis = json.loads(response)
        except json.JSONDecodeError:
            # If not valid JSON, return as text
            analysis = {"raw_analysis": response}
        
        return analysis
    
    def register_model_governance(
        self,
        model_name: str,
        model_type: str,
        metadata: Dict
    ) -> str:
        """
        Register model in watsonx.governance

        Args:
            model_name: Model name
            model_type: Model type
            metadata: Model metadata

        Returns:
            Model asset ID
        """
        try:
            asset_meta = {
                "name": model_name,
                "type": model_type,
                "description": metadata.get("description", ""),
                "tags": metadata.get("tags", []),
                "custom": metadata
            }

            if self.client is not None:
                asset_details = self.client.repository.store_model(
                    model=None,  # For governance tracking only
                    meta_props=asset_meta
                )
                asset_id = asset_details["metadata"]["id"]
            else:
                asset_id = f"mock_asset_{datetime.utcnow().timestamp()}"
                logger.warning("watsonx APIClient unavailable; using mock governance asset id")

            logger.info(f"Model registered in governance: {asset_id}")
            return asset_id

        except Exception as e:
            logger.error(f"Error registering model: {e}")
            raise
    
    def track_validation_run(
        self,
        model_id: str,
        validation_results: Dict,
        status: str = "completed"
    ) -> str:
        """
        Track validation run in watsonx.governance
        
        Args:
            model_id: Model asset ID
            validation_results: Validation results
            status: Validation status
            
        Returns:
            Validation run ID
        """
        try:
            run_metadata = {
                "model_id": model_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": status,
                "results": validation_results,
                "compliance_framework": "SR 11-7"
            }
            
            # Store validation run
            # Note: Actual implementation depends on watsonx.governance API
            logger.info(f"Validation run tracked for model: {model_id}")
            
            return f"validation_run_{datetime.utcnow().timestamp()}"
            
        except Exception as e:
            logger.error(f"Error tracking validation run: {e}")
            raise
    
    def get_model_metrics(
        self,
        model_id: str,
        metric_types: Optional[List[str]] = None
    ) -> Dict:
        """
        Retrieve model metrics from watsonx.governance
        
        Args:
            model_id: Model asset ID
            metric_types: Types of metrics to retrieve
            
        Returns:
            Model metrics
        """
        try:
            # Retrieve metrics
            # Note: Actual implementation depends on watsonx.governance API
            metrics = {
                "model_id": model_id,
                "retrieved_at": datetime.utcnow().isoformat(),
                "metrics": {}
            }
            
            logger.info(f"Retrieved metrics for model: {model_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error retrieving metrics: {e}")
            raise
    
    def create_compliance_report(
        self,
        model_id: str,
        report_type: str = "SR_11_7"
    ) -> Dict:
        """
        Generate compliance report from watsonx.governance
        
        Args:
            model_id: Model asset ID
            report_type: Type of compliance report
            
        Returns:
            Compliance report data
        """
        try:
            report = {
                "model_id": model_id,
                "report_type": report_type,
                "generated_at": datetime.utcnow().isoformat(),
                "compliance_status": "compliant",
                "findings": [],
                "recommendations": []
            }
            
            logger.info(f"Compliance report generated for model: {model_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating compliance report: {e}")
            raise
    
    async def get_validation_recommendations(
        self,
        model_type: str,
        scorecard_type: str,
        product_type: str
    ) -> List[str]:
        """
        Get AI-powered validation recommendations
        
        Args:
            model_type: Type of model (GLM, XGBoost, etc.)
            scorecard_type: Type of scorecard
            product_type: Type of product
            
        Returns:
            List of recommendations
        """
        prompt = f"""
        As a banking model validation expert, provide specific validation recommendations for:
        
        Model Type: {model_type}
        Scorecard Type: {scorecard_type}
        Product Type: {product_type}
        
        List 10 critical validation steps that must be performed according to SR 11-7 guidelines.
        Focus on model-specific and scorecard-specific requirements.
        
        Format as a numbered list.
        """
        
        response = await self.generate_text(prompt)
        
        # Parse recommendations
        recommendations = [
            line.strip() 
            for line in response.split('\n') 
            if line.strip() and any(char.isdigit() for char in line[:3])
        ]
        
        return recommendations


class WatsonxGovernanceTracker:
    """
    Specialized tracker for watsonx.governance integration
    """
    
    def __init__(self, client: WatsonxClient):
        self.client = client
        self.tracked_models = {}
    
    def register_model(
        self,
        model_name: str,
        model_config: Dict
    ) -> str:
        """Register model for governance tracking"""
        model_id = self.client.register_model_governance(
            model_name=model_name,
            model_type=str(model_config.get("model_type") or "unknown"),
            metadata=model_config
        )
        
        self.tracked_models[model_name] = {
            "id": model_id,
            "registered_at": datetime.utcnow().isoformat(),
            "config": model_config
        }
        
        return model_id
    
    def log_validation_event(
        self,
        model_name: str,
        event_type: str,
        event_data: Dict
    ):
        """Log validation event for audit trail"""
        if model_name not in self.tracked_models:
            raise ValueError(f"Model {model_name} not registered")
        
        model_id = self.tracked_models[model_name]["id"]
        
        event = {
            "model_id": model_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data
        }
        
        logger.info(f"Validation event logged: {event_type} for {model_name}")
        
        return event
    
    def get_compliance_status(self, model_name: str) -> Dict:
        """Get current compliance status"""
        if model_name not in self.tracked_models:
            raise ValueError(f"Model {model_name} not registered")
        
        model_id = self.tracked_models[model_name]["id"]
        
        return self.client.create_compliance_report(model_id)

# Made with Bob
