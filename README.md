# Poncho's Portal - Round Table MCP Server Architecture

A fantasy-themed Model Context Protocol (MCP) server architecture for coordinating specialized AI agents ("Lords") through a central gateway ("King").

## 🏰 Project Overview

Poncho's Portal implements a hierarchical agent coordination system inspired by Arthurian legend:
- **King Poncho**: Central gateway coordinating all Lords
- **7 Specialized Lords**: Domain experts handling specific quest types
  - Lord Architect: System design & architecture
  - Lord Scribe: Documentation & knowledge management
  - Lord Sentinel: Code review & quality assurance
  - Lord Forge Master: Code generation & refactoring
  - Lord Oracle: Research & semantic search
  - Lord Curator: Data transformation & dataset building
  - Lord Executor: Deployment & workflow orchestration

## 🎯 Current Status: Week 1-2 Complete ✅

**King Gateway MVP Built!**
- King coordinates 2 Lords (Architect + Scribe)
- Full JSON-RPC 2.0 protocol implementation
- Automated test suite: 6/6 tests passing
- ~890 lines of code total

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              CLIENT APPLICATION                  │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│           KING GATEWAY (port 8000)              │
│  Routes quests to appropriate Lords             │
└──────────┬──────────────────────┬───────────────┘
           │                      │
           ▼                      ▼
┌──────────────────┐   ┌──────────────────────────┐
│  LORD ARCHITECT  │   │     LORD SCRIBE          │
│  (port 8001)     │   │     (port 8002)          │
│  - design_system │   │  - write_docs            │
│  - analyze_arch  │   │  - create_summary        │
└──────────────────┘   └──────────────────────────┘
```

## 📂 Project Structure

```
Poncho's-Portal/
├── Kingdom-of-Agents/        # Agent definitions & Round Table specs
│   ├── Lord-Architect/
│   ├── Lord-Scribe/
│   ├── Lord-Sentinel/
│   ├── Lord-Forge-Master/
│   ├── Lord-Oracle/
│   ├── Lord-Curator/
│   ├── Lord-Executor/
│   └── Round-Table/          # Coordination mechanics
├── Magic-Tower/              # Implementation & experiments
│   ├── Foundry/              # King Gateway MVP
│   │   ├── king_gateway.py
│   │   ├── lord_architect.py
│   │   ├── lord_scribe.py
│   │   └── test_king_gateway.py
│   ├── Library/              # Research & documentation
│   │   └── MCP-Architecture/ # Quest 001 findings
│   ├── Experiment-Logs/      # Quest logs & checkpoints
│   └── Lord-Sage/            # Research agent definitions
├── Ponchos-Avatar/           # King Poncho agent definition
└── Setting/                  # World building & glossary
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install fastapi uvicorn httpx pydantic
```

### Running the MVP

**Terminal 1 - Lord Architect:**
```powershell
cd Magic-Tower/Foundry
python lord_architect.py
```

**Terminal 2 - Lord Scribe:**
```powershell
python lord_scribe.py
```

**Terminal 3 - King Gateway:**
```powershell
python king_gateway.py
```

**Terminal 4 - Run Tests:**
```powershell
python test_king_gateway.py
```

### Example Quest

```powershell
curl -X POST http://localhost:8000/quest `
  -H "Content-Type: application/json" `
  -d '{
    "quest_type": "design_system",
    "quest_data": {
      "app_name": "E-Commerce Platform",
      "requirements": ["Handle 10k users", "Mobile support"],
      "scale": "large"
    }
  }'
```

## 📚 Quest 001: MCP Server Architecture Research

**Objective**: Research MCP server architectures to design Round Table MCP Server for managing 7 specialized Lords.

**Phase 1 Results** (Intelligence Gathering):
- ✅ 22 MCP candidates identified and analyzed
- ✅ Pattern comparison across 6 dimensions
- ✅ 5 core repositories recommended for deep study
- ✅ Round Table architecture designed

**Phase 2 Progress** (Deep Study - Weeks 1-2):
- ✅ IBM ContextForge gateway patterns extracted
- ✅ Complete request flow traced and documented
- ✅ King Gateway MVP built (170 LOC)
- ✅ 2 Lord MCP servers deployed (Architect + Scribe)
- ✅ Automated test suite passing (6/6 tests)

**Key Findings**:
- Gateway + Workflow Engine + Persistent Memory = Winning Pattern
- Database-backed registry enables dynamic Lord registration
- JSON-RPC 2.0 provides standard protocol for LLM-tool integration
- Transport abstraction supports multiple communication methods

## 🔬 Technical Details

### MCP Protocol
All Lords communicate via [Model Context Protocol](https://modelcontextprotocol.io) using JSON-RPC 2.0:
- `tools/list`: Discover available tools
- `tools/call`: Execute a tool
- `resources/read`: Access resources
- `prompts/get`: Retrieve prompts

### Pattern Extraction
Based on analysis of production MCP servers:
- **IBM ContextForge** (9.4/10): Gateway architecture model
- **n8n** (9.2/10): Workflow orchestration patterns (Week 3-4)
- **Memory MCP** (9.0/10): Persistent state patterns (Week 5-6)

### Technology Stack
- **Framework**: FastAPI (async Python web framework)
- **Protocol**: JSON-RPC 2.0 over HTTP
- **Transport**: HTTP (SSE/WebSocket support planned)
- **Future DB**: PostgreSQL + pgvector for Lord registry

## 📖 Documentation

- **MVP Guide**: `Magic-Tower/Foundry/KING_GATEWAY_MVP.md`
- **Week 1-2 Checkpoint**: `Magic-Tower/Experiment-Logs/Quest-001-Week-1-2-Checkpoint.md`
- **Architecture Analysis**: `Magic-Tower/Library/MCP-Architecture/01-Gateway-Patterns-IBM-ContextForge.md`
- **Quest Specification**: `Magic-Tower/Setting/Quest-Log/Quest-001-Library-Foundation.md`

## 🎯 Roadmap

### Phase 2 Continuation

**Week 3-4: Workflow Orchestration**
- Study n8n DAG execution engine
- Implement sequential Lord coordination
- Add workflow state persistence

**Week 5-6: Persistent State**
- Study Memory MCP PostgreSQL + pgvector patterns
- Migrate Lord registry to database
- Add quest history and multi-day quest support

**Week 7-8: Full Integration**
- Deploy all 7 Lords
- Test complex multi-Lord quests
- Validate production readiness

## 🧪 Testing

Run the automated test suite:
```powershell
cd Magic-Tower/Foundry
python test_king_gateway.py
```

**Current Results**: 6/6 tests passing ✅
- Health checks
- Lord listing
- Quest routing to Lord Architect
- Quest routing to Lord Scribe
- Explicit Lord targeting
- Error handling

## 🤝 Contributing

This is a research project exploring MCP server architectures for multi-agent coordination. The focus is on pattern extraction from production systems and incremental implementation.

## 📜 License

MIT License - See LICENSE file for details

## 🎭 The Fantasy Theme

Poncho's Portal uses Arthurian legend as a mental model for distributed agent systems:
- **King**: Central coordinator (gateway)
- **Lords**: Specialized experts (MCP servers)
- **Round Table**: Democratic coordination (no hierarchy among Lords)
- **Quests**: User requests requiring multi-agent collaboration
- **Magic Tower**: Research & development workspace

The fantasy theme makes complex distributed systems more intuitive and memorable.

---

**Current Status**: Week 1-2 Complete ✅  
**Next Phase**: Workflow Orchestration (n8n study)  
**The Round Table has begun.** 👑

_"From ContextForge's gateway patterns, the King learned to coordinate. Next, from n8n's workflows, the King learns to orchestrate."_
