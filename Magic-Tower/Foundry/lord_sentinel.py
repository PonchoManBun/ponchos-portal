"""
Lord Sentinel - Code Review & Quality Assurance Specialist

MCP Server providing code review and quality assessment tools.
Ensures code meets quality standards before deployment.

Tools:
- review_code: Comprehensive code review
- analyze_security: Security vulnerability analysis
- check_quality: Code quality metrics
"""

import json
import asyncio
from typing import Any, Dict, List
from fastapi import FastAPI, Request
from pydantic import BaseModel


app = FastAPI(title="Lord Sentinel MCP Server")


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
            if tool_name == "review_code":
                result = await review_code(arguments)
            elif tool_name == "analyze_security":
                result = await analyze_security(arguments)
            elif tool_name == "check_quality":
                result = await check_quality(arguments)
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


async def review_code(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive code review
    
    Args:
        params: {
            "code": str - Code to review (or files from Forge Master)
            "files": List[Dict] - Optional list of files to review
            "focus": str - Review focus (default: "all")
        }
    
    Returns:
        {
            "score": int - Overall quality score (0-100)
            "issues": List[Dict] - List of issues found
            "suggestions": List[str] - Improvement suggestions
            "approved": bool - Whether code is approved
        }
    """
    code = params.get("code", "")
    files = params.get("files", [])
    focus = params.get("focus", "all")
    
    # Simulate code review (2-3 seconds)
    await asyncio.sleep(2.0)
    
    issues = []
    score = 85  # Default good score
    
    # Analyze code patterns
    if "TODO" in code:
        issues.append({
            "severity": "medium",
            "type": "incomplete",
            "message": "Found TODO comments - implementation incomplete",
            "line": None,
        })
        score -= 10
    
    if "SECRET_KEY = " in code and '"your-secret-key"' in code:
        issues.append({
            "severity": "high",
            "type": "security",
            "message": "Hardcoded secret key detected - use environment variables",
            "line": None,
        })
        score -= 15
    
    if "except Exception" in code:
        issues.append({
            "severity": "low",
            "type": "best-practice",
            "message": "Broad exception catching - consider specific exception types",
            "line": None,
        })
        score -= 5
    
    # Check if there are type hints
    if "def " in code and "->" not in code:
        issues.append({
            "severity": "low",
            "type": "style",
            "message": "Missing type hints on function returns",
            "line": None,
        })
    
    suggestions = [
        "Add comprehensive docstrings to all functions",
        "Implement input validation for API endpoints",
        "Add logging for authentication events",
        "Consider rate limiting for login endpoint",
        "Add unit tests for edge cases",
    ]
    
    if len(files) > 0:
        suggestions.append(f"Create integration tests for {len(files)} modules")
    
    approved = score >= 70 and not any(issue["severity"] == "high" for issue in issues)
    
    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "approved": approved,
        "summary": f"Found {len(issues)} issues. " + 
                   ("Code approved for deployment." if approved else "Code requires fixes before deployment."),
        "focus": focus,
    }


async def analyze_security(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Security vulnerability analysis
    
    Args:
        params: {
            "code": str - Code to analyze
            "files": List[Dict] - Optional list of files
        }
    
    Returns:
        {
            "vulnerabilities": List[Dict] - Security issues
            "risk_level": str - Overall risk (low/medium/high/critical)
        }
    """
    code = params.get("code", "")
    
    await asyncio.sleep(1.5)
    
    vulnerabilities = []
    
    # Check for common security issues
    if "eval(" in code or "exec(" in code:
        vulnerabilities.append({
            "severity": "critical",
            "type": "code-injection",
            "message": "Use of eval() or exec() detected - major security risk",
        })
    
    if "password" in code.lower() and "hash" not in code.lower():
        vulnerabilities.append({
            "severity": "high",
            "type": "weak-crypto",
            "message": "Password handling without hashing detected",
        })
    
    if "SQL" in code or "SELECT" in code:
        if "?" not in code and "execute(" in code:
            vulnerabilities.append({
                "severity": "critical",
                "type": "sql-injection",
                "message": "Potential SQL injection vulnerability - use parameterized queries",
            })
    
    risk_level = "low"
    if any(v["severity"] == "critical" for v in vulnerabilities):
        risk_level = "critical"
    elif any(v["severity"] == "high" for v in vulnerabilities):
        risk_level = "high"
    elif len(vulnerabilities) > 0:
        risk_level = "medium"
    
    return {
        "vulnerabilities": vulnerabilities,
        "risk_level": risk_level,
        "safe_to_deploy": risk_level in ["low", "medium"],
        "recommendations": [
            "Use environment variables for secrets",
            "Implement proper authentication middleware",
            "Add rate limiting to prevent brute force attacks",
            "Use HTTPS only for token transmission",
        ],
    }


async def check_quality(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Code quality metrics analysis
    
    Args:
        params: {
            "code": str - Code to analyze
            "files": List[Dict] - Optional list of files
        }
    
    Returns:
        {
            "metrics": Dict - Quality metrics
            "grade": str - Quality grade (A-F)
        }
    """
    code = params.get("code", "")
    files = params.get("files", [])
    
    await asyncio.sleep(1.0)
    
    # Calculate basic metrics
    lines_of_code = len(code.split("\n"))
    num_functions = code.count("def ")
    num_classes = code.count("class ")
    num_comments = code.count("#")
    
    # Calculate complexity (simplified)
    complexity = code.count("if ") + code.count("for ") + code.count("while ")
    avg_complexity = complexity / max(num_functions, 1)
    
    # Calculate maintainability
    maintainability_score = 100
    if avg_complexity > 10:
        maintainability_score -= 20
    if num_comments < lines_of_code * 0.1:
        maintainability_score -= 10
    if lines_of_code > 500:
        maintainability_score -= 10
    
    # Determine grade
    if maintainability_score >= 90:
        grade = "A"
    elif maintainability_score >= 80:
        grade = "B"
    elif maintainability_score >= 70:
        grade = "C"
    elif maintainability_score >= 60:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "metrics": {
            "lines_of_code": lines_of_code,
            "num_functions": num_functions,
            "num_classes": num_classes,
            "num_comments": num_comments,
            "cyclomatic_complexity": complexity,
            "avg_complexity_per_function": round(avg_complexity, 2),
            "maintainability_index": maintainability_score,
        },
        "grade": grade,
        "test_coverage": 0,  # Would integrate with coverage tool
        "passed": grade in ["A", "B", "C"],
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "lord": "sentinel"}


if __name__ == "__main__":
    import uvicorn
    print("🛡️  Lord Sentinel MCP Server starting on port 8004...")
    uvicorn.run(app, host="127.0.0.1", port=8004)
