# Model Context Protocol (MCP) Integration Guide

## Overview

The Banking Model Validation System includes full support for the Model Context Protocol (MCP), enabling validation agents to use external tools and resources for enhanced capabilities.

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how AI applications connect to external data sources and tools. It enables:

- **Tool Usage**: Agents can call external tools for specialized computations
- **Resource Access**: Agents can read from external data sources
- **Extensibility**: Easy addition of new capabilities without modifying core code
- **Interoperability**: Standard protocol for tool integration

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Validation Orchestrator Agent                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP Client                              │
│  ┌────────────────────────────────────────────────┐    │
│  │  Tool Registry                                  │    │
│  │  - calculate_gini                              │    │
│  │  - calculate_ks                                │    │
│  │  - calculate_psi                               │    │
│  │  - test_assumptions                            │    │
│  │  - query_regulatory_database                   │    │
│  │  - fetch_benchmark_data                        │    │
│  │  - validate_data_quality                       │    │
│  └────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP Server                              │
│  (External service providing tools and resources)        │
└─────────────────────────────────────────────────────────┘
```

## Available MCP Tools

### 1. Performance Metrics Tools

#### calculate_gini
Calculate Gini coefficient for model discrimination power.

```python
result = await agent.use_tool(
    "calculate_gini",
    {
        "actual": [0, 1, 0, 1, 1],
        "predicted": [0.2, 0.8, 0.3, 0.9, 0.7]
    }
)
# Returns: {"value": 0.65, "interpretation": "Excellent"}
```

#### calculate_ks
Calculate Kolmogorov-Smirnov statistic.

```python
result = await agent.use_tool(
    "calculate_ks",
    {
        "actual": [0, 1, 0, 1, 1],
        "predicted": [0.2, 0.8, 0.3, 0.9, 0.7]
    }
)
# Returns: {"value": 0.42, "interpretation": "Strong"}
```

### 2. Stability Analysis Tools

#### calculate_psi
Calculate Population Stability Index.

```python
result = await agent.use_tool(
    "calculate_psi",
    {
        "expected": [100, 200, 150, 180, 120],
        "actual": [105, 195, 155, 175, 125],
        "bins": 10
    }
)
# Returns: {"value": 0.08, "interpretation": "Stable"}
```

### 3. Validation Tools

#### test_assumptions
Test statistical assumptions for models.

```python
result = await agent.use_tool(
    "test_assumptions",
    {
        "data": dataset,
        "model_type": "GLM",
        "assumptions": ["linearity", "independence", "normality"]
    }
)
# Returns: {"tests": {...}, "all_passed": true}
```

#### validate_data_quality
Perform comprehensive data quality checks.

```python
result = await agent.use_tool(
    "validate_data_quality",
    {
        "data": dataset,
        "checks": ["completeness", "accuracy", "consistency"]
    }
)
# Returns: {"quality_score": 0.95, "issues": [...]}
```

### 4. External Data Tools

#### query_regulatory_database
Query regulatory requirements.

```python
result = await agent.use_tool(
    "query_regulatory_database",
    {
        "framework": "SR 11-7",
        "component": "model_performance"
    }
)
# Returns: {"requirements": [...], "guidelines": [...]}
```

#### fetch_benchmark_data
Fetch industry benchmark data.

```python
result = await agent.use_tool(
    "fetch_benchmark_data",
    {
        "model_type": "XGBoost",
        "scorecard_type": "application",
        "metric": "gini"
    }
)
# Returns: {"benchmark": 0.60, "percentiles": {...}}
```

### 5. Report Generation Tools

#### generate_validation_report
Generate validation report sections.

```python
result = await agent.use_tool(
    "generate_validation_report",
    {
        "section": "executive_summary",
        "data": validation_results,
        "format": "docx"
    }
)
# Returns: {"content": "...", "format": "docx"}
```

## Using MCP in Validation Agents

### Basic Usage

```python
from backend.mcp.mcp_client import MCPClient, ValidationAgentWithMCP

# Initialize MCP client
mcp_client = MCPClient(mcp_server_url="http://localhost:3001")
await mcp_client.initialize()

# Create MCP-enabled agent
agent = ValidationAgentWithMCP(mcp_client)

# Use tools
metrics = await agent.calculate_performance_metrics(
    actual=[0, 1, 0, 1, 1],
    predicted=[0.2, 0.8, 0.3, 0.9, 0.7]
)

# Check stability
stability = await agent.check_stability(
    expected=train_distribution,
    actual=test_distribution
)

# Fetch benchmarks
benchmarks = await agent.fetch_benchmarks(
    model_type="XGBoost",
    scorecard_type="application"
)
```

### Advanced Usage

```python
# Custom tool usage
result = await agent.use_tool(
    tool_name="custom_validation_tool",
    arguments={
        "data": dataset,
        "parameters": {"threshold": 0.5}
    },
    context="Custom validation step"
)

# Access external resources
resource = await agent.access_resource(
    resource_uri="file:///data/regulatory_guidelines.pdf"
)

# Get tool usage history
history = agent.get_tool_usage_history()
```

## Setting Up MCP Server

### Option 1: Use Provided Example Server

```bash
# Navigate to MCP server directory
cd banking-model-validation/mcp-server

# Install dependencies
pip install fastapi uvicorn numpy scikit-learn

# Start server
python mcp_server.py
```

### Option 2: Create Custom MCP Server

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

class ToolRequest(BaseModel):
    arguments: Dict[str, Any]

@app.get("/tools")
async def list_tools():
    return [
        {
            "name": "my_custom_tool",
            "description": "Custom validation tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {"type": "array"}
                }
            }
        }
    ]

@app.post("/tools/my_custom_tool")
async def my_custom_tool(request: ToolRequest):
    # Implement tool logic
    data = request.arguments["data"]
    result = process_data(data)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
```

## Configuration

### Environment Variables

Add to `.env`:

```env
# MCP Configuration
MCP_SERVER_URL=http://localhost:3001
MCP_ENABLED=true
MCP_TIMEOUT=30
```

### Docker Compose

Add MCP server to `docker-compose.yml`:

```yaml
services:
  mcp-server:
    build:
      context: ./mcp-server
      dockerfile: Dockerfile
    container_name: banking-validation-mcp
    ports:
      - "3001:3001"
    environment:
      - LOG_LEVEL=INFO
    networks:
      - banking-validation-network
```

## Integration with Validation Orchestrator

Update the orchestrator to use MCP:

```python
from backend.mcp.mcp_client import MCPClient, ValidationAgentWithMCP

class ValidationOrchestratorAgent:
    def __init__(self, watsonx_client: WatsonxClient):
        self.watsonx = watsonx_client
        
        # Initialize MCP
        self.mcp_client = MCPClient()
        asyncio.create_task(self.mcp_client.initialize())
    
    async def _validate_model_performance(
        self,
        model_config: Dict[str, Any],
        datasets: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Create MCP-enabled agent
        agent = ValidationAgentWithMCP(self.mcp_client)
        
        # Use MCP tools for validation
        metrics = await agent.calculate_performance_metrics(
            actual=datasets["test"]["target"],
            predicted=datasets["test"]["predictions"]
        )
        
        # Fetch benchmarks via MCP
        benchmarks = await agent.fetch_benchmarks(
            model_type=model_config["model_type"],
            scorecard_type=model_config["scorecard_type"]
        )
        
        return {
            "metrics": metrics,
            "benchmarks": benchmarks,
            "tool_usage": agent.get_tool_usage_history()
        }
```

## Benefits of MCP Integration

### 1. Extensibility
- Add new validation tools without modifying core code
- Integrate with external systems easily
- Support custom validation requirements

### 2. Modularity
- Tools are independent services
- Easy to update and maintain
- Can be developed in any language

### 3. Reusability
- Tools can be shared across projects
- Standard protocol for integration
- Community-contributed tools

### 4. Performance
- Offload heavy computations to specialized services
- Parallel tool execution
- Caching and optimization

### 5. Compliance
- Audit trail of tool usage
- Version control for tools
- Reproducible validations

## Tool Development Guidelines

### Creating New MCP Tools

1. **Define Tool Schema**
```python
{
    "name": "tool_name",
    "description": "What the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "number"}
        },
        "required": ["param1"]
    }
}
```

2. **Implement Tool Logic**
```python
@app.post("/tools/tool_name")
async def tool_name(request: ToolRequest):
    # Validate inputs
    # Process data
    # Return results
    return {"result": result}
```

3. **Add Error Handling**
```python
try:
    result = process_data(request.arguments)
    return {"result": result, "status": "success"}
except Exception as e:
    return {"error": str(e), "status": "error"}
```

4. **Document Tool**
- Purpose and use cases
- Input parameters
- Output format
- Examples

## Testing MCP Integration

### Unit Tests

```python
import pytest
from backend.mcp.mcp_client import MCPClient

@pytest.mark.asyncio
async def test_mcp_tool_call():
    client = MCPClient("http://localhost:3001")
    await client.initialize()
    
    result = await client.call_tool(
        "calculate_gini",
        {"actual": [0, 1], "predicted": [0.2, 0.8]}
    )
    
    assert "value" in result
    assert 0 <= result["value"] <= 1
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_validation_with_mcp():
    orchestrator = ValidationOrchestratorAgent(watsonx_client)
    
    results = await orchestrator.orchestrate_validation(model_config)
    
    assert "tool_usage" in results
    assert len(results["tool_usage"]) > 0
```

## Troubleshooting

### MCP Server Not Available
```
Warning: MCP server not available
```
**Solution:** Start MCP server or disable MCP in configuration

### Tool Not Found
```
Error: Tool calculate_gini not available
```
**Solution:** Verify tool is registered in MCP server

### Timeout Errors
```
Error: Tool call timeout
```
**Solution:** Increase MCP_TIMEOUT or optimize tool implementation

## Best Practices

1. **Graceful Degradation**: System should work without MCP
2. **Error Handling**: Catch and log MCP errors
3. **Caching**: Cache tool results when appropriate
4. **Monitoring**: Track tool usage and performance
5. **Documentation**: Document all custom tools
6. **Testing**: Test tools independently and in integration

## Conclusion

MCP integration provides powerful extensibility to the Banking Model Validation System, enabling:
- Custom validation tools
- External data integration
- Specialized computations
- Community contributions
- Future enhancements

The system works seamlessly with or without MCP, ensuring reliability while providing advanced capabilities when needed.