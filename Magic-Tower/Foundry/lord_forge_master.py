"""
Lord Forge Master - Code Generation Specialist

MCP Server providing code generation tools.
Transforms system designs into working code.

Tools:
- generate_code: Generate code from architecture design
- refactor_code: Improve existing code structure
- create_api: Build REST API endpoints
"""

import json
import asyncio
from typing import Any, Dict
from fastapi import FastAPI, Request
from pydantic import BaseModel


app = FastAPI(title="Lord Forge Master MCP Server")


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: Dict[str, Any]
    id: int


class JsonRpcResponse(BaseModel):
    jsonrpc: str
    result: Any = None
    error: Any = None
    id: int


@app.post("/mcp")
async def handle_jsonrpc(request: Request):
    """Handle JSON-RPC 2.0 requests (MCP protocol)"""
    try:
        body = await request.json()
        rpc_request = JsonRpcRequest(**body)
        
        # MCP protocol: tools/call with nested name and arguments
        if rpc_request.method == "tools/call":
            tool_name = rpc_request.params.get("name")
            arguments = rpc_request.params.get("arguments", {})
            
            # Route to tool handler
            if tool_name == "generate_code":
                result = await generate_code(arguments)
            elif tool_name == "refactor_code":
                result = await refactor_code(arguments)
            elif tool_name == "create_api":
                result = await create_api(arguments)
            else:
                return JsonRpcResponse(
                    jsonrpc="2.0",
                    error={"code": -32601, "message": f"Tool not found: {tool_name}"},
                    id=rpc_request.id
                ).dict()
        else:
            return JsonRpcResponse(
                jsonrpc="2.0",
                error={"code": -32601, "message": f"Method not found: {rpc_request.method}"},
                id=rpc_request.id
            ).dict()
        
        return JsonRpcResponse(
            jsonrpc="2.0",
            result=result,
            id=rpc_request.id
        ).dict()
    
    except Exception as e:
        return JsonRpcResponse(
            jsonrpc="2.0",
            error={"code": -32603, "message": str(e)},
            id=body.get("id", 0)
        ).dict()


async def generate_code(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate code from system design
    
    Args:
        params: {
            "design": str - System design from Lord Architect
            "language": str - Programming language (default: Python)
        }
    
    Returns:
        {
            "code": str - Generated code
            "files": List[Dict] - List of files with code
            "tests": str - Unit tests
        }
    """
    design = params.get("design", "")
    language = params.get("language", "Python")
    
    # Simulate code generation (2-3 seconds)
    await asyncio.sleep(2.5)
    
    # Extract components from design
    if "API Gateway" in design:
        code_files = [
            {
                "path": "app/main.py",
                "code": """from fastapi import FastAPI

app = FastAPI(title="Authentication API")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/login")
async def login(username: str, password: str):
    # TODO: Implement JWT token generation
    return {"token": "jwt_token_here"}
"""
            },
            {
                "path": "app/auth.py",
                "code": """import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
"""
            },
        ]
    else:
        code_files = [
            {
                "path": "app/main.py",
                "code": f"# Generated {language} code\n# Based on design: {design[:100]}..."
            }
        ]
    
    return {
        "code": code_files[0]["code"],
        "files": code_files,
        "tests": """import pytest
from app.auth import create_token, verify_token

def test_token_creation():
    token = create_token("user123")
    assert token is not None

def test_token_verification():
    token = create_token("user123")
    payload = verify_token(token)
    assert payload["user_id"] == "user123"
""",
        "language": language,
        "summary": f"Generated {len(code_files)} {language} files with FastAPI implementation"
    }


async def refactor_code(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refactor existing code for better structure
    
    Args:
        params: {
            "code": str - Code to refactor
            "strategy": str - Refactoring strategy (default: "clean")
        }
    
    Returns:
        {
            "refactored_code": str
            "changes": List[str] - List of changes made
        }
    """
    code = params.get("code", "")
    strategy = params.get("strategy", "clean")
    
    await asyncio.sleep(1.5)
    
    return {
        "refactored_code": code,  # Would apply actual refactoring
        "changes": [
            "Extracted authentication logic to separate module",
            "Added type hints to all functions",
            "Improved error handling with custom exceptions",
        ],
        "strategy": strategy,
    }


async def create_api(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create REST API endpoints
    
    Args:
        params: {
            "resources": List[str] - Resources to create APIs for
            "framework": str - Web framework (default: FastAPI)
        }
    
    Returns:
        {
            "endpoints": List[Dict] - Generated API endpoints
            "openapi_spec": Dict - OpenAPI specification
        }
    """
    resources = params.get("resources", ["users"])
    framework = params.get("framework", "FastAPI")
    
    await asyncio.sleep(2.0)
    
    endpoints = []
    for resource in resources:
        endpoints.extend([
            {"method": "GET", "path": f"/{resource}", "description": f"List all {resource}"},
            {"method": "POST", "path": f"/{resource}", "description": f"Create {resource}"},
            {"method": "GET", "path": f"/{resource}/{{id}}", "description": f"Get {resource} by ID"},
            {"method": "PUT", "path": f"/{resource}/{{id}}", "description": f"Update {resource}"},
            {"method": "DELETE", "path": f"/{resource}/{{id}}", "description": f"Delete {resource}"},
        ])
    
    return {
        "endpoints": endpoints,
        "framework": framework,
        "openapi_spec": {
            "openapi": "3.0.0",
            "info": {"title": "Generated API", "version": "1.0.0"},
            "paths": {ep["path"]: {} for ep in endpoints},
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "lord": "forge_master"}


if __name__ == "__main__":
    import uvicorn
    print("🔥 Lord Forge Master MCP Server starting on port 8003...")
    uvicorn.run(app, host="127.0.0.1", port=8003)
