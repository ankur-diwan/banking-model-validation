"""
Model Context Protocol (MCP) Client
Enables agents to use external tools and resources via MCP
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import httpx
from loguru import logger


class MCPClient:
    """
    Client for interacting with MCP servers
    Enables agents to use external tools and resources
    """
    
    def __init__(self, mcp_server_url: Optional[str] = None):
        """
        Initialize MCP client
        
        Args:
            mcp_server_url: URL of MCP server
        """
        self.mcp_server_url = mcp_server_url or "http://localhost:3001"
        self.available_tools = {}
        self.available_resources = {}
        
    async def initialize(self):
        """Initialize connection and discover available tools"""
        try:
            await self._discover_tools()
            await self._discover_resources()
            logger.info(f"MCP client initialized with {len(self.available_tools)} tools")
        except Exception as e:
            logger.warning(f"MCP server not available: {e}")
    
    async def _discover_tools(self):
        """Discover available tools from MCP server"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/tools")
                if response.status_code == 200:
                    tools = response.json()
                    self.available_tools = {tool["name"]: tool for tool in tools}
        except Exception as e:
            logger.debug(f"Could not discover MCP tools: {e}")
    
    async def _discover_resources(self):
        """Discover available resources from MCP server"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/resources")
                if response.status_code == 200:
                    resources = response.json()
                    self.available_resources = {r["uri"]: r for r in resources}
        except Exception as e:
            logger.debug(f"Could not discover MCP resources: {e}")
    
    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP tool
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool {tool_name} not available")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/{tool_name}",
                    json={"arguments": arguments}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Tool call failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            raise
    
    async def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        Read an MCP resource
        
        Args:
            resource_uri: URI of the resource
            
        Returns:
            Resource content
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.mcp_server_url}/resources",
                    params={"uri": resource_uri}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Resource read failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"Error reading resource {resource_uri}: {e}")
            raise
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        return list(self.available_tools.values())
    
    def get_available_resources(self) -> List[Dict[str, Any]]:
        """Get list of available resources"""
        return list(self.available_resources.values())


class MCPToolRegistry:
    """
    Registry of MCP tools for validation agents
    """
    
    # Define validation-specific tools
    VALIDATION_TOOLS = {
        "calculate_gini": {
            "name": "calculate_gini",
            "description": "Calculate Gini coefficient for model discrimination",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "actual": {"type": "array", "items": {"type": "number"}},
                    "predicted": {"type": "array", "items": {"type": "number"}}
                },
                "required": ["actual", "predicted"]
            }
        },
        "calculate_ks": {
            "name": "calculate_ks",
            "description": "Calculate Kolmogorov-Smirnov statistic",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "actual": {"type": "array", "items": {"type": "number"}},
                    "predicted": {"type": "array", "items": {"type": "number"}}
                },
                "required": ["actual", "predicted"]
            }
        },
        "calculate_psi": {
            "name": "calculate_psi",
            "description": "Calculate Population Stability Index",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "expected": {"type": "array", "items": {"type": "number"}},
                    "actual": {"type": "array", "items": {"type": "number"}},
                    "bins": {"type": "integer", "default": 10}
                },
                "required": ["expected", "actual"]
            }
        },
        "test_assumptions": {
            "name": "test_assumptions",
            "description": "Test statistical assumptions for model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {"type": "array"},
                    "model_type": {"type": "string"},
                    "assumptions": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["data", "model_type"]
            }
        },
        "query_regulatory_database": {
            "name": "query_regulatory_database",
            "description": "Query regulatory requirements database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "framework": {"type": "string"},
                    "component": {"type": "string"}
                },
                "required": ["framework"]
            }
        },
        "fetch_benchmark_data": {
            "name": "fetch_benchmark_data",
            "description": "Fetch industry benchmark data",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model_type": {"type": "string"},
                    "scorecard_type": {"type": "string"},
                    "metric": {"type": "string"}
                },
                "required": ["model_type", "scorecard_type"]
            }
        },
        "validate_data_quality": {
            "name": "validate_data_quality",
            "description": "Perform comprehensive data quality checks",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {"type": "array"},
                    "checks": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["data"]
            }
        },
        "generate_validation_report": {
            "name": "generate_validation_report",
            "description": "Generate validation report section",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "section": {"type": "string"},
                    "data": {"type": "object"},
                    "format": {"type": "string", "enum": ["markdown", "html", "docx"]}
                },
                "required": ["section", "data"]
            }
        }
    }
    
    @classmethod
    def get_tool_definition(cls, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool definition by name"""
        return cls.VALIDATION_TOOLS.get(tool_name)
    
    @classmethod
    def get_all_tools(cls) -> List[Dict[str, Any]]:
        """Get all tool definitions"""
        return list(cls.VALIDATION_TOOLS.values())


class MCPEnabledAgent:
    """
    Base class for MCP-enabled validation agents
    """
    
    def __init__(self, mcp_client: MCPClient):
        """
        Initialize MCP-enabled agent
        
        Args:
            mcp_client: MCP client instance
        """
        self.mcp = mcp_client
        self.tool_usage_log = []
    
    async def use_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use an MCP tool
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            context: Context for tool usage
            
        Returns:
            Tool result
        """
        logger.info(f"Agent using tool: {tool_name}")
        
        # Log tool usage
        self.tool_usage_log.append({
            "tool": tool_name,
            "arguments": arguments,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Call tool via MCP
        result = await self.mcp.call_tool(tool_name, arguments)
        
        return result
    
    async def access_resource(
        self,
        resource_uri: str
    ) -> Dict[str, Any]:
        """
        Access an MCP resource
        
        Args:
            resource_uri: Resource URI
            
        Returns:
            Resource content
        """
        logger.info(f"Agent accessing resource: {resource_uri}")
        
        result = await self.mcp.read_resource(resource_uri)
        
        return result
    
    def get_tool_usage_history(self) -> List[Dict[str, Any]]:
        """Get history of tool usage"""
        return self.tool_usage_log


class ValidationAgentWithMCP(MCPEnabledAgent):
    """
    Validation agent with MCP capabilities
    """
    
    async def calculate_performance_metrics(
        self,
        actual: List[float],
        predicted: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate performance metrics using MCP tools
        
        Args:
            actual: Actual values
            predicted: Predicted values
            
        Returns:
            Performance metrics
        """
        metrics = {}
        
        # Calculate Gini using MCP tool
        try:
            gini_result = await self.use_tool(
                "calculate_gini",
                {"actual": actual, "predicted": predicted},
                context="Performance validation"
            )
            metrics["gini"] = gini_result.get("value")
        except Exception as e:
            logger.warning(f"Could not calculate Gini via MCP: {e}")
            metrics["gini"] = None
        
        # Calculate KS using MCP tool
        try:
            ks_result = await self.use_tool(
                "calculate_ks",
                {"actual": actual, "predicted": predicted},
                context="Performance validation"
            )
            metrics["ks"] = ks_result.get("value")
        except Exception as e:
            logger.warning(f"Could not calculate KS via MCP: {e}")
            metrics["ks"] = None
        
        return metrics
    
    async def check_stability(
        self,
        expected: List[float],
        actual: List[float]
    ) -> Dict[str, Any]:
        """
        Check population stability using MCP tools
        
        Args:
            expected: Expected distribution
            actual: Actual distribution
            
        Returns:
            Stability metrics
        """
        try:
            psi_result = await self.use_tool(
                "calculate_psi",
                {
                    "expected": expected,
                    "actual": actual,
                    "bins": 10
                },
                context="Stability analysis"
            )
            
            return {
                "psi": psi_result.get("value"),
                "interpretation": psi_result.get("interpretation"),
                "stable": psi_result.get("value", 1.0) < 0.25
            }
        except Exception as e:
            logger.warning(f"Could not calculate PSI via MCP: {e}")
            return {"psi": None, "stable": None}
    
    async def fetch_benchmarks(
        self,
        model_type: str,
        scorecard_type: str
    ) -> Dict[str, Any]:
        """
        Fetch industry benchmarks using MCP
        
        Args:
            model_type: Type of model
            scorecard_type: Type of scorecard
            
        Returns:
            Benchmark data
        """
        try:
            benchmarks = await self.use_tool(
                "fetch_benchmark_data",
                {
                    "model_type": model_type,
                    "scorecard_type": scorecard_type,
                    "metric": "all"
                },
                context="Benchmarking"
            )
            
            return benchmarks
        except Exception as e:
            logger.warning(f"Could not fetch benchmarks via MCP: {e}")
            return {}
    
    async def query_regulations(
        self,
        framework: str = "SR 11-7"
    ) -> Dict[str, Any]:
        """
        Query regulatory requirements using MCP
        
        Args:
            framework: Regulatory framework
            
        Returns:
            Regulatory requirements
        """
        try:
            regulations = await self.use_tool(
                "query_regulatory_database",
                {"framework": framework},
                context="Compliance checking"
            )
            
            return regulations
        except Exception as e:
            logger.warning(f"Could not query regulations via MCP: {e}")
            return {}


# Example MCP server implementation (for reference)
MCP_SERVER_EXAMPLE = """
# Example MCP Server for Banking Validation

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics import roc_auc_score

app = FastAPI()

class ToolRequest(BaseModel):
    arguments: Dict[str, Any]

@app.get("/tools")
async def list_tools():
    return MCPToolRegistry.get_all_tools()

@app.post("/tools/calculate_gini")
async def calculate_gini(request: ToolRequest):
    actual = np.array(request.arguments["actual"])
    predicted = np.array(request.arguments["predicted"])
    
    auc = roc_auc_score(actual, predicted)
    gini = 2 * auc - 1
    
    return {
        "value": float(gini),
        "interpretation": "Excellent" if gini > 0.6 else "Good" if gini > 0.4 else "Fair"
    }

@app.post("/tools/calculate_psi")
async def calculate_psi(request: ToolRequest):
    expected = np.array(request.arguments["expected"])
    actual = np.array(request.arguments["actual"])
    bins = request.arguments.get("bins", 10)
    
    # Calculate PSI
    exp_hist, _ = np.histogram(expected, bins=bins)
    act_hist, _ = np.histogram(actual, bins=bins)
    
    exp_pct = exp_hist / len(expected)
    act_pct = act_hist / len(actual)
    
    psi = np.sum((act_pct - exp_pct) * np.log(act_pct / (exp_pct + 1e-10)))
    
    return {
        "value": float(psi),
        "interpretation": "Stable" if psi < 0.1 else "Moderate shift" if psi < 0.25 else "Significant shift"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
"""

# Made with Bob
