# Cloned MCP Server Repositories

This directory contains cloned repositories from Quest 001 Phase 2 deep study.

**Note**: These repositories are excluded from version control (see `.gitignore`) due to size.

## Repositories Studied

### 1. IBM ContextForge (Week 1-2)

**Repository**: https://github.com/IBM/mcp-context-forge  
**Size**: 105MB, 1,775 files  
**Purpose**: Gateway architecture patterns for King coordination  
**Key Patterns Extracted**:

- Database-backed server registry
- Multi-transport abstraction (stdio/SSE/HTTP/WebSocket)
- JSON-RPC 2.0 protocol implementation
- Middleware stack (auth, logging, security)
- Health monitoring and metrics

**Clone Command**:

```bash
git clone https://github.com/IBM/mcp-context-forge.git
```

### 2. n8n (Week 3-4 - Planned)

**Repository**: https://github.com/n8n-io/n8n  
**Size**: 295MB, 13,363 files  
**Purpose**: Workflow orchestration patterns for sequential/parallel Lord coordination  
**Patterns to Study**:

- DAG execution engine
- Node dependency resolution
- Workflow state management
- Error handling and retries

**Clone Command**:

```bash
git clone https://github.com/n8n-io/n8n.git
```

### 3. MCP Official Servers (Week 5-6 - Planned)

**Repository**: https://github.com/modelcontextprotocol/servers  
**Size**: 27MB  
**Purpose**: Reference implementations including Memory MCP for persistent state  
**Patterns to Study**:

- PostgreSQL + pgvector integration
- Vector similarity search
- Resource management
- Persistent memory patterns

**Clone Command**:

```bash
git clone https://github.com/modelcontextprotocol/servers.git mcp-official-servers
```

### 4. LastMile AI MCP Agent (Week 5-6 - Planned)

**Repository**: https://github.com/lastmile-ai/mcp-agent  
**Size**: 27MB, 1,159 files  
**Purpose**: Durable workflows and hybrid memory patterns  
**Patterns to Study**:

- Temporal integration for durable execution
- Hybrid memory (in-memory + persistent)
- Agent state management
- Workflow recovery

**Clone Command**:

```bash
git clone https://github.com/lastmile-ai/mcp-agent.git
```

## Study Workflow

For each repository:

1. **Week 1**: Clone repository, explore structure, identify key patterns
2. **Week 2**: Deep dive into code, extract minimal patterns (~200 LOC)
3. **Document**: Create analysis document in `Magic-Tower/Library/MCP-Architecture/`
4. **Implement**: Build proof-of-concept in `Magic-Tower/Foundry/`
5. **Test**: Validate patterns with automated tests

## Documentation

Study findings are documented in:

- `Magic-Tower/Library/MCP-Architecture/01-Gateway-Patterns-IBM-ContextForge.md`
- `Magic-Tower/Library/MCP-Architecture/02-Workflow-Patterns-n8n.md` (Week 3-4)
- `Magic-Tower/Library/MCP-Architecture/03-State-Patterns-Memory-MCP.md` (Week 5-6)

## Why Not Commit?

These repositories total ~454MB and contain 15k+ files. We document patterns and extract minimal implementations instead of version controlling full clones.

---

**Status**: IBM ContextForge cloned and studied ✅  
**Next**: n8n clone for workflow orchestration study (Week 3-4)
