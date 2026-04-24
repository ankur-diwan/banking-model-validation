"""
Document Review Agent
Critically reviews model development documentation using watsonx.ai
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
import re

from ..wxo.watsonx_client import WatsonxClient


class DocumentReviewAgent:
    """
    Agent for critically reviewing model development documentation
    Uses watsonx.ai for intelligent document analysis
    """
    
    def __init__(self, watsonx_client: WatsonxClient):
        """
        Initialize document review agent
        
        Args:
            watsonx_client: watsonx client instance
        """
        self.watsonx = watsonx_client
        self.review_findings = []
        
    async def review_development_documentation(
        self,
        documentation: Dict[str, Any],
        model_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Critically review model development documentation
        
        Args:
            documentation: Model development documentation
            model_config: Model configuration
            
        Returns:
            Comprehensive review findings
        """
        logger.info("Starting critical review of development documentation")
        
        review_results = {
            "overall_assessment": None,
            "sections_reviewed": [],
            "findings": [],
            "gaps": [],
            "recommendations": [],
            "regulatory_compliance": {},
            "quality_score": 0.0
        }
        
        # Review each required section
        sections_to_review = [
            "model_purpose",
            "data_description",
            "model_specification",
            "model_development",
            "model_assumptions",
            "performance_results",
            "limitations",
            "implementation_plan"
        ]
        
        for section in sections_to_review:
            section_review = await self._review_section(
                section,
                documentation.get(section, {}),
                model_config
            )
            review_results["sections_reviewed"].append(section_review)
        
        # Identify gaps
        review_results["gaps"] = await self._identify_gaps(
            documentation,
            model_config
        )
        
        # Generate recommendations
        review_results["recommendations"] = await self._generate_recommendations(
            review_results["sections_reviewed"],
            review_results["gaps"]
        )
        
        # Check regulatory compliance
        review_results["regulatory_compliance"] = await self._check_regulatory_compliance(
            documentation,
            model_config
        )
        
        # Calculate quality score
        review_results["quality_score"] = self._calculate_quality_score(
            review_results
        )
        
        # Overall assessment
        review_results["overall_assessment"] = await self._generate_overall_assessment(
            review_results
        )
        
        return review_results
    
    async def _review_section(
        self,
        section_name: str,
        section_content: Dict[str, Any],
        model_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Review a specific documentation section"""
        
        prompt = f"""
        You are an expert model validator reviewing banking model documentation for SR 11-7 compliance.
        
        Section: {section_name}
        Model Type: {model_config.get('model_type')}
        Scorecard Type: {model_config.get('scorecard_type')}
        
        Content to review:
        {section_content}
        
        Critically evaluate this section for:
        1. Completeness - Are all required elements present?
        2. Clarity - Is the documentation clear and unambiguous?
        3. Technical Accuracy - Are technical details correct?
        4. Regulatory Compliance - Does it meet SR 11-7 requirements?
        5. Assumptions - Are assumptions clearly stated and justified?
        6. Limitations - Are limitations acknowledged?
        
        Provide:
        - Rating (Excellent/Good/Adequate/Inadequate)
        - Specific findings (both positive and negative)
        - Required improvements
        - Regulatory concerns
        
        Format as JSON.
        """
        
        try:
            response = await self.watsonx.generate_text(prompt)
            
            # Parse response
            import json
            try:
                review = json.loads(response)
            except:
                review = {
                    "section": section_name,
                    "rating": "Adequate",
                    "findings": [response],
                    "improvements_needed": [],
                    "regulatory_concerns": []
                }
            
            review["section"] = section_name
            return review
            
        except Exception as e:
            logger.error(f"Error reviewing section {section_name}: {e}")
            return {
                "section": section_name,
                "rating": "Not Reviewed",
                "error": str(e)
            }
    
    async def _identify_gaps(
        self,
        documentation: Dict[str, Any],
        model_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify gaps in documentation"""
        
        gaps = []
        
        # Required sections per SR 11-7
        required_sections = {
            "model_purpose": "Model purpose and intended use",
            "data_description": "Data sources and quality",
            "model_specification": "Mathematical formulation",
            "model_development": "Development methodology",
            "model_assumptions": "Key assumptions and limitations",
            "performance_results": "Performance metrics and validation",
            "limitations": "Model limitations and weaknesses",
            "implementation_plan": "Implementation and monitoring",
            "governance": "Model governance and oversight"
        }
        
        # Check for missing sections
        for section, description in required_sections.items():
            if section not in documentation or not documentation[section]:
                gaps.append({
                    "type": "missing_section",
                    "section": section,
                    "description": description,
                    "severity": "High",
                    "regulatory_impact": "SR 11-7 requirement not met"
                })
        
        # Use AI to identify content gaps
        prompt = f"""
        Review this model documentation for gaps and missing information:
        
        Model Type: {model_config.get('model_type')}
        Scorecard Type: {model_config.get('scorecard_type')}
        
        Documentation sections present: {list(documentation.keys())}
        
        Identify:
        1. Missing critical information
        2. Insufficient detail in key areas
        3. Regulatory requirements not addressed
        4. Technical details lacking
        5. Assumptions not documented
        
        List specific gaps with severity (High/Medium/Low).
        Format as JSON array.
        """
        
        try:
            response = await self.watsonx.generate_text(prompt)
            import json
            ai_gaps = json.loads(response)
            gaps.extend(ai_gaps)
        except Exception as e:
            logger.warning(f"Could not identify AI gaps: {e}")
        
        return gaps
    
    async def _generate_recommendations(
        self,
        section_reviews: List[Dict[str, Any]],
        gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for improvement"""
        
        recommendations = []
        
        # Recommendations based on section reviews
        for review in section_reviews:
            if review.get("rating") in ["Inadequate", "Adequate"]:
                recommendations.append({
                    "area": review["section"],
                    "priority": "High" if review["rating"] == "Inadequate" else "Medium",
                    "recommendation": f"Improve {review['section']} documentation",
                    "details": review.get("improvements_needed", [])
                })
        
        # Recommendations based on gaps
        for gap in gaps:
            if gap.get("severity") == "High":
                recommendations.append({
                    "area": gap.get("section", "General"),
                    "priority": "High",
                    "recommendation": f"Address missing: {gap.get('description')}",
                    "regulatory_impact": gap.get("regulatory_impact")
                })
        
        # Use AI for strategic recommendations
        prompt = f"""
        Based on the documentation review findings, provide strategic recommendations
        for improving the model documentation to meet SR 11-7 standards.
        
        Focus on:
        1. Critical gaps that must be addressed
        2. Areas needing more detail
        3. Regulatory compliance improvements
        4. Best practices to implement
        
        Prioritize recommendations (Critical/High/Medium/Low).
        Format as JSON array.
        """
        
        try:
            response = await self.watsonx.generate_text(prompt)
            import json
            ai_recommendations = json.loads(response)
            recommendations.extend(ai_recommendations)
        except Exception as e:
            logger.warning(f"Could not generate AI recommendations: {e}")
        
        return recommendations
    
    async def _check_regulatory_compliance(
        self,
        documentation: Dict[str, Any],
        model_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check regulatory compliance"""
        
        compliance_check = {
            "framework": "SR 11-7",
            "components": {},
            "overall_status": "Compliant",
            "issues": []
        }
        
        # SR 11-7 components
        sr_11_7_components = [
            "Model Development and Implementation",
            "Model Validation",
            "Governance and Controls"
        ]
        
        for component in sr_11_7_components:
            prompt = f"""
            Assess compliance with SR 11-7 component: {component}
            
            Model documentation provided: {list(documentation.keys())}
            Model type: {model_config.get('model_type')}
            
            Evaluate:
            1. Are all requirements met?
            2. Is documentation sufficient?
            3. Are there compliance gaps?
            
            Provide compliance status (Compliant/Partially Compliant/Non-Compliant)
            and specific issues if any.
            Format as JSON.
            """
            
            try:
                response = await self.watsonx.generate_text(prompt)
                import json
                component_check = json.loads(response)
                compliance_check["components"][component] = component_check
                
                if component_check.get("status") != "Compliant":
                    compliance_check["overall_status"] = "Partially Compliant"
                    compliance_check["issues"].extend(
                        component_check.get("issues", [])
                    )
            except Exception as e:
                logger.warning(f"Could not check compliance for {component}: {e}")
        
        return compliance_check
    
    def _calculate_quality_score(
        self,
        review_results: Dict[str, Any]
    ) -> float:
        """Calculate overall documentation quality score"""
        
        scores = []
        
        # Score based on section ratings
        rating_scores = {
            "Excellent": 1.0,
            "Good": 0.8,
            "Adequate": 0.6,
            "Inadequate": 0.3,
            "Not Reviewed": 0.0
        }
        
        for section in review_results.get("sections_reviewed", []):
            rating = section.get("rating", "Not Reviewed")
            scores.append(rating_scores.get(rating, 0.0))
        
        # Penalty for gaps
        high_severity_gaps = len([
            g for g in review_results.get("gaps", [])
            if g.get("severity") == "High"
        ])
        gap_penalty = min(high_severity_gaps * 0.1, 0.3)
        
        # Calculate average
        if scores:
            base_score = sum(scores) / len(scores)
            final_score = max(0.0, base_score - gap_penalty)
        else:
            final_score = 0.0
        
        return round(final_score, 2)
    
    async def _generate_overall_assessment(
        self,
        review_results: Dict[str, Any]
    ) -> str:
        """Generate overall assessment"""
        
        prompt = f"""
        Generate an executive summary assessment of model documentation quality.
        
        Quality Score: {review_results['quality_score']}
        Gaps Found: {len(review_results['gaps'])}
        High Priority Recommendations: {len([r for r in review_results['recommendations'] if r.get('priority') == 'High'])}
        Regulatory Status: {review_results['regulatory_compliance'].get('overall_status')}
        
        Provide:
        1. Overall assessment (2-3 sentences)
        2. Key strengths
        3. Critical weaknesses
        4. Readiness for regulatory submission
        
        Be direct and professional.
        """
        
        try:
            assessment = await self.watsonx.generate_text(prompt)
            return assessment
        except Exception as e:
            logger.error(f"Could not generate assessment: {e}")
            return "Assessment could not be generated due to technical error."

# Made with Bob
