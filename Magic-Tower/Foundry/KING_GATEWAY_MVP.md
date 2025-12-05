# Round Table King Gateway - MVP

Minimal proof-of-concept for King gateway coordinating 2 Lords (Architect + Scribe).

Based on IBM ContextForge gateway patterns extracted in Quest 001 Phase 2.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATION                        │
│                  (HTTP/JSON-RPC 2.0 requests)               │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   KING GATEWAY (port 8000)                  │
│  - Routes quests to appropriate Lords                       │
│  - In-memory Lord registry (LORDS dict)                     │
│  - HTTP transport for Lord communication                    │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              ▼                              ▼
┌──────────────────────────┐   ┌────────────────────────────┐
│  LORD ARCHITECT (8001)   │   │   LORD SCRIBE (8002)       │
│  - design_system         │   │   - write_docs             │
│  - analyze_architecture  │   │   - create_summary         │
│  JSON-RPC 2.0 MCP Server │   │   JSON-RPC 2.0 MCP Server  │
└──────────────────────────┘   └────────────────────────────┘
```

## Components

### 1. King Gateway (`king_gateway.py`)

- **Port**: 8000
- **Endpoints**:
  - `GET /`: Health check
  - `GET /lords`: List registered Lords
  - `POST /quest`: Route quest to appropriate Lord
- **Routing Logic**: Maps quest_type to Lord name via routing table
- **Transport**: HTTP client (httpx) sending JSON-RPC 2.0 requests

### 2. Lord Architect (`lord_architect.py`)

- **Port**: 8001
- **MCP Endpoint**: `POST /mcp`
- **Tools**:
  - `design_system`: Create system architecture designs
  - `analyze_architecture`: Analyze existing architectures
- **Protocol**: JSON-RPC 2.0 (methods: `tools/list`, `tools/call`)

### 3. Lord Scribe (`lord_scribe.py`)

- **Port**: 8002
- **MCP Endpoint**: `POST /mcp`
- **Tools**:
  - `write_docs`: Generate documentation
  - `create_summary`: Summarize content
- **Protocol**: JSON-RPC 2.0 (methods: `tools/list`, `tools/call`)

## Setup

### Prerequisites

```bash
pip install fastapi uvicorn httpx pydantic
```

### Running Services

**Terminal 1 - King Gateway:**

```powershell
cd c:\dev\Poncho's-Portal\Magic-Tower\Foundry
python king_gateway.py
```

**Terminal 2 - Lord Architect:**

```powershell
cd c:\dev\Poncho's-Portal\Magic-Tower\Foundry
python lord_architect.py
```

**Terminal 3 - Lord Scribe:**

```powershell
cd c:\dev\Poncho's-Portal\Magic-Tower\Foundry
python lord_scribe.py
```

## Testing

### Automated Test Suite

```powershell
python test_king_gateway.py
```

### Manual Testing

**1. Health Checks:**

```powershell
curl http://localhost:8000/
curl http://localhost:8001/
curl http://localhost:8002/
```

**2. List Lords:**

```powershell
curl http://localhost:8000/lords
```

**3. Design System Quest (Lord Architect):**

```powershell
curl -X POST http://localhost:8000/quest `
  -H "Content-Type: application/json" `
  -d '{
    "quest_type": "design_system",
    "quest_data": {
      "app_name": "CRM System",
      "requirements": ["Handle 5k users", "Mobile support"],
      "scale": "medium"
    }
  }'
```

**4. Write Docs Quest (Lord Scribe):**

```powershell
curl -X POST http://localhost:8000/quest `
  -H "Content-Type: application/json" `
  -d '{
    "quest_type": "write_docs",
    "quest_data": {
      "topic": "Python Best Practices",
      "format": "markdown",
      "detail_level": "standard"
    }
  }'
```

## Key Patterns Extracted from ContextForge

### 1. **Database-Backed Registry Pattern**

- **ContextForge**: PostgreSQL `mcp_servers` table with dynamic server registration
- **MVP**: In-memory `LORDS` dict (will migrate to PostgreSQL in Phase 2)
- **Benefit**: Dynamic Lord registration without code changes

### 2. **Transport Abstraction Pattern**

- **ContextForge**: `Transport` ABC with stdio/SSE/HTTP/WebSocket implementations
- **MVP**: HTTP-only transport via httpx
- **Benefit**: Can add SSE/WebSocket transports later without changing King logic

### 3. **JSON-RPC 2.0 Protocol**

- **ContextForge**: All MCP communication uses JSON-RPC 2.0 format
- **MVP**: Full JSON-RPC 2.0 compliance (request/response/error handling)
- **Benefit**: Standard protocol for LLM-tool integration

## MVP Success Criteria

- [x] King Gateway routes quests based on quest_type
- [x] Lord Architect responds to `design_system` quests
- [x] Lord Scribe responds to `write_docs` quests
- [x] JSON-RPC 2.0 protocol correctly implemented
- [x] Error handling for unknown quest types
- [x] Explicit Lord targeting via `lord_name` parameter

## Files

- `king_gateway.py`: Main gateway coordinator (~170 LOC)
- `lord_architect.py`: System design Lord (~240 LOC)
- `lord_scribe.py`: Documentation Lord (~260 LOC)
- `test_king_gateway.py`: Automated test suite (~200 LOC)
- `KING_GATEWAY_MVP.md`: This file

**Total MVP Code**: ~870 LOC (vs. ContextForge's 1,775 files) - pattern extraction successful!

---

_"The King now coordinates his first Lords. The Round Table begins."_

— Quest 001, Week 1-2 Checkpoint
