"""
Lord Scribe - Documentation and Knowledge Management MCP Server
Handles write_docs, create_summary, and index_knowledge quests

Minimal MCP server implementation following JSON-RPC 2.0 protocol.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

# Initialize FastAPI app
app = FastAPI(
    title="Lord Scribe MCP Server",
    version="0.1.0",
    description="Documentation and knowledge management specialist"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# JSON-RPC 2.0 models
class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request format"""
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: int


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response format"""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: int
    
    class Config:
        # Exclude null fields from JSON output
        exclude_none = True


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "lord": "Scribe",
        "status": "operational",
        "capabilities": ["write_docs", "create_summary", "index_knowledge"]
    }


@app.post("/mcp")
async def handle_mcp_request(request: JSONRPCRequest):
    """
    Handle MCP JSON-RPC 2.0 requests.
    
    Supports:
    - tools/list: List available tools
    - tools/call: Execute a tool
    """
    logger.info(f"Received MCP request: method={request.method}, params={request.params}")
    
    try:
        if request.method == "tools/list":
            # Return list of available tools
            result = {
                "tools": [
                    {
                        "name": "write_docs",
                        "description": "Write comprehensive documentation for a project or feature",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string"},
                                "format": {"type": "string", "enum": ["markdown", "rst", "html"]},
                                "detail_level": {"type": "string", "enum": ["brief", "standard", "comprehensive"]}
                            },
                            "required": ["topic"]
                        }
                    },
                    {
                        "name": "create_summary",
                        "description": "Create a concise summary of provided content",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "max_length": {"type": "integer"}
                            },
                            "required": ["content"]
                        }
                    }
                ]
            }
            
            return JSONRPCResponse(result=result, id=request.id)
        
        elif request.method == "tools/call":
            # Execute a tool
            params = request.params or {}
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "write_docs":
                result = _write_docs(arguments)
            elif tool_name == "create_summary":
                result = _create_summary(arguments)
            else:
                return JSONRPCResponse(
                    error={
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    },
                    id=request.id
                )
            
            return JSONRPCResponse(result=result, id=request.id)
        
        else:
            # Unsupported method
            return JSONRPCResponse(
                error={
                    "code": -32601,
                    "message": f"Method not found: {request.method}"
                },
                id=request.id
            )
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return JSONRPCResponse(
            error={
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            },
            id=request.id
        )


def _write_docs(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write documentation for a topic.
    
    Mock implementation for MVP - in Phase 2, this will use LLM for actual doc generation.
    """
    topic = arguments.get("topic", "Unknown Topic")
    doc_format = arguments.get("format", "markdown")
    detail_level = arguments.get("detail_level", "standard")
    
    # Mock documentation
    docs = f"""# {topic} Documentation

## Overview
This documentation provides a {detail_level} guide to {topic}.

## Getting Started

### Prerequisites
- Basic understanding of the domain
- Development environment set up
- Required dependencies installed

### Installation
```bash
# Clone the repository
git clone https://github.com/example/{topic.lower().replace(' ', '-')}.git

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Core Concepts

### Key Features
1. **Feature A**: Primary capability for handling core workflows
2. **Feature B**: Advanced functionality for power users
3. **Feature C**: Integration points with external systems

### Architecture
The system follows a modular design pattern with clear separation between:
- **Interface Layer**: User-facing API and UI components
- **Business Logic**: Core processing and validation
- **Data Layer**: Persistence and caching

## Usage Examples

### Basic Example
```python
from {topic.lower().replace(' ', '_')} import Client

client = Client(api_key="your_key")
result = client.process(data)
print(result)
```

### Advanced Example
```python
# Configure with custom options
client = Client(
    api_key="your_key",
    timeout=30,
    retry_policy="exponential"
)

# Process batch
results = client.batch_process(items)
```

## API Reference

### Client Class
- `__init__(api_key, **options)`: Initialize client
- `process(data)`: Process single item
- `batch_process(items)`: Process multiple items

## Best Practices
1. Always handle errors gracefully
2. Use batch operations for large datasets
3. Implement proper logging and monitoring
4. Follow security guidelines for API keys

## Troubleshooting

### Common Issues
**Problem**: Connection timeout
**Solution**: Increase timeout value or check network connectivity

**Problem**: Invalid API key
**Solution**: Verify API key is correctly configured in environment

## Contributing
See CONTRIBUTING.md for guidelines on contributing to this project.

## License
MIT License - see LICENSE file for details.

---
*Documentation generated by Lord Scribe*
*Format: {doc_format} | Detail Level: {detail_level}*
"""
    
    return {
        "content": [
            {
                "type": "text",
                "text": docs
            }
        ],
        "metadata": {
            "lord": "scribe",
            "tool": "write_docs",
            "topic": topic,
            "format": doc_format,
            "detail_level": detail_level
        }
    }


def _create_summary(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a summary of content.
    
    Mock implementation for MVP.
    """
    content = arguments.get("content", "")
    max_length = arguments.get("max_length", 200)
    
    # Simple mock summary (in Phase 2, use actual summarization logic)
    words = content.split()
    if len(words) <= max_length // 5:  # Rough estimate: 5 chars per word
        summary_text = content
    else:
        # Truncate and add ellipsis
        truncated = " ".join(words[:max_length // 5])
        summary_text = truncated + "..."
    
    summary = f"""## Content Summary

**Original Length**: {len(content)} characters ({len(words)} words)
**Summary Length**: {len(summary_text)} characters

### Summary
{summary_text}

### Key Points
- Main topic identified in content
- Supporting details extracted
- Context preserved in condensed form

---
*Summary generated by Lord Scribe*
"""
    
    return {
        "content": [
            {
                "type": "text",
                "text": summary
            }
        ],
        "metadata": {
            "lord": "scribe",
            "tool": "create_summary",
            "original_length": len(content),
            "summary_length": len(summary_text)
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Lord Scribe MCP Server on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
