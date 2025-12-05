"""
King Gateway - Round Table MCP Server Coordinator
Minimal proof-of-concept based on IBM ContextForge patterns

This gateway routes quests to appropriate Lords (MCP servers) based on quest type.
Phase 1: In-memory Lord registry with HTTP transport.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import logging
from typing import Dict, Any, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Round Table King Gateway",
    version="0.1.0",
    description="Gateway coordinator for 7 specialized Lord MCP servers"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory Lord registry (Phase 1 - will migrate to PostgreSQL in Phase 2)
LORDS = {
    "architect": {
        "url": "http://localhost:8001/mcp",
        "transport": "http",
        "description": "System architecture and design patterns",
        "capabilities": ["design_system", "analyze_architecture"]
    },
    "scribe": {
        "url": "http://localhost:8002/mcp",
        "transport": "http",
        "description": "Documentation and knowledge management",
        "capabilities": ["write_docs", "create_summary"]
    },
}

# Request/Response models
class QuestRequest(BaseModel):
    """Quest request from client"""
    quest_type: str  # e.g., "design_system", "write_docs"
    quest_data: Dict[str, Any]  # Quest-specific parameters
    lord_name: Optional[str] = None  # Optional: explicitly target a Lord

class QuestResponse(BaseModel):
    """Quest response to client"""
    lord: str
    quest_type: str
    result: Any
    status: str = "success"


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Round Table King Gateway",
        "version": "0.1.0",
        "status": "operational",
        "lords_registered": len(LORDS)
    }


@app.get("/lords")
async def list_lords():
    """List all registered Lords and their capabilities"""
    return {
        "lords": {
            name: {
                "url": config["url"],
                "description": config["description"],
                "capabilities": config["capabilities"]
            }
            for name, config in LORDS.items()
        }
    }


@app.post("/quest", response_model=QuestResponse)
async def route_quest(quest: QuestRequest):
    """
    Route quest to appropriate Lord based on quest_type or explicit lord_name.
    
    This is the core coordination function - maps quests to Lords.
    """
    logger.info(f"Received quest: type={quest.quest_type}, data={quest.quest_data}")
    
    # Routing logic: determine which Lord handles this quest
    lord_name = quest.lord_name
    
    if not lord_name:
        # Auto-route based on quest_type
        lord_name = _route_quest_to_lord(quest.quest_type)
    
    if not lord_name:
        raise HTTPException(
            status_code=404,
            detail=f"No Lord handles quest type: {quest.quest_type}"
        )
    
    # Get Lord configuration from registry
    lord = LORDS.get(lord_name)
    if not lord:
        raise HTTPException(
            status_code=500,
            detail=f"Lord {lord_name} not registered in gateway"
        )
    
    logger.info(f"Routing quest to Lord: {lord_name} at {lord['url']}")
    
    # Forward quest to Lord via HTTP (JSON-RPC 2.0 format)
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Build JSON-RPC 2.0 request
            jsonrpc_request = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": quest.quest_type,
                    "arguments": quest.quest_data
                },
                "id": 1
            }
            
            response = await client.post(lord["url"], json=jsonrpc_request)
            response.raise_for_status()
            
            jsonrpc_response = response.json()
            
            logger.info(f"Raw JSON-RPC response from {lord_name}: {jsonrpc_response}")
            
            # Extract result from JSON-RPC response
            # JSON-RPC 2.0 spec: only check if error key exists AND is not null
            if "error" in jsonrpc_response:
                error = jsonrpc_response["error"]
                logger.info(f"Error field present: {error}, type: {type(error)}")
                if error is not None and error != "None":
                    raise HTTPException(
                        status_code=500,
                        detail=f"Lord {lord_name} returned error: {error}"
                    )
            
            result = jsonrpc_response.get("result")
            
            return QuestResponse(
                lord=lord_name,
                quest_type=quest.quest_type,
                result=result,
                status="success"
            )
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Lord {lord_name}: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Lord {lord_name} returned HTTP error: {e.response.status_code}"
        )
    except httpx.RequestError as e:
        logger.error(f"Connection error to Lord {lord_name}: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to Lord {lord_name}: {str(e)}"
        )


def _route_quest_to_lord(quest_type: str) -> Optional[str]:
    """
    Route quest type to appropriate Lord.
    
    This is a simple routing table - will become more sophisticated
    with capability matching in Phase 2.
    """
    routing_table = {
        # Lord Architect
        "design_system": "architect",
        "analyze_architecture": "architect",
        "review_design": "architect",
        
        # Lord Scribe
        "write_docs": "scribe",
        "create_summary": "scribe",
        "index_knowledge": "scribe",
    }
    
    return routing_table.get(quest_type)


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Round Table King Gateway...")
    logger.info(f"Registered Lords: {list(LORDS.keys())}")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
