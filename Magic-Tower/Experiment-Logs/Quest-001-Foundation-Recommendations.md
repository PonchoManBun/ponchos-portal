# Quest 001: Foundation Recommendations for Round Table MCP Architecture

**Prepared By**: Foundation Recommender (Lord Sage)  
**For**: King Poncho & The Round Table  
**Date**: December 4, 2025  
**Status**: Final Recommendations - Awaiting Royal Approval

---

## Executive Summary

After analyzing 22 MCP server candidates through 3 specialized agents (Pattern Comparator, Scope Validator, Foundation Recommender), I present the **architectural blueprint for the Round Table MCP Server**.

**Core Finding**: No existing MCP server orchestrates 7 hierarchical specialist agents. The Round Table will be **FIRST-OF-ITS-KIND**. However, we have proven patterns from 5 exceptional repositories.

**Recommended Architecture**: **Gateway-Orchestrated Multi-Server Hierarchy**

- **Pattern Stack**: IBM context-forge (Gateway) + n8n (Workflow) + Memory MCP (State) + Plugged.in (Multi-Server) + Magg (Discovery)
- **Lord Model**: **Hybrid** - Lords as MCP Server Plugins with Tool Namespace Architecture
- **Critical Innovation**: Hierarchical state (Global Quest → Lord Working Memory → Tool Execution Context)

---

## 1. Core Repository Selection (3-5 for Phase 2 Deep Study)

### 1.1 IBM context-forge ⭐ PRIORITY 1

**URL**: https://github.com/IBM/context-forge  
**Score**: 9.4/10 (Scope Validator)

**Why Selected**:

- **Plugin Registry Pattern**: Exactly matches "King registers 7 Lords as plugins" architecture
- **Gateway Aggregation**: Central hub that routes requests to specialized servers
- **Production-Proven**: IBM enterprise deployment at scale validates architecture
- **Hierarchical Delegation**: Single entry point (King) → delegates to plugins (Lords)

**What We'll Learn**:

1. **Plugin Registration Mechanism**: How Lords dynamically register/unregister capabilities
2. **Request Routing Logic**: How King determines which Lord(s) to invoke for a quest
3. **Response Aggregation**: How multi-Lord outputs combine into cohesive quest results
4. **Tool Namespace Management**: Preventing collisions (e.g., `oracle.search` vs `forge.search`)
5. **Gateway Performance**: Scaling to 500+ tools (proof of future-proofing)

**Round Table Application**:

- **King Architecture**: King = context-forge gateway
- **Lord Registration**: Each Lord registers as plugin with capabilities manifest
- **Quest Routing**: King analyzes quest → routes to appropriate Lord(s)
- **Multi-Lord Coordination**: King maintains active Lord registry, handles sequential/parallel execution

**Study Priority**: **1/5** (Foundational - Start Here)

---

### 1.2 n8n-io/n8n ⭐ PRIORITY 2

**URL**: https://github.com/n8n-io/n8n  
**Score**: 9.2/10 (Scope Validator)

**Why Selected**:

- **DAG-Based Orchestration**: Nodes = Lords, Edges = Data Flow—perfect visual model
- **Dependency Management**: Explicit Lord execution order (Oracle → Architect → Forge Master)
- **Graceful Error Handling**: "Continue Despite Failure" pattern critical for multi-day quests
- **Workflow State Persistence**: Resume quests after interruptions/restarts

**What We'll Learn**:

1. **Execution Graph Construction**: How to build Lord dependency DAGs from quest requirements
2. **Parallel vs Sequential Execution**: When to run Lords concurrently vs sequentially
3. **Data Passing Between Nodes**: How Oracle's outputs become Architect's inputs
4. **Workflow State Checkpointing**: Saving progress after each Lord completion
5. **Error Recovery**: Retry logic, fallback paths, partial quest completion

**Round Table Application**:

- **Quest Workflow Engine**: Multi-Lord quests as executable DAGs
- **Lord Dependencies**: Architect depends on Oracle, Forge depends on Architect
- **Dynamic Routing**: Some Lords run in parallel (Oracle + Curator simultaneously)
- **Long-Running Quests**: Multi-day workflows with resume capability

**Study Priority**: **2/5** (Core Orchestration)

---

### 1.3 Memory MCP ⭐ PRIORITY 3

**URL**: https://github.com/modelcontextprotocol/memory-server  
**Score**: 9.0/10 (Scope Validator)

**Why Selected**:

- **Knowledge Graph Architecture**: Semantic relationships between Lord insights
- **Persistent State**: Solves "stateless crisis"—70% of MCP servers have no memory
- **Semantic Search**: Lords query past quest knowledge (not just keyword matching)
- **Hierarchical Context**: Global quest state + per-Lord working memory

**What We'll Learn**:

1. **Knowledge Graph Design**: How to model Lord insights, relationships, and quest context
2. **Context Hierarchy**: Global (quest goals) → Lord (working memory) → Tool (execution state)
3. **Semantic Memory**: How Oracle's research from Day 1 informs Architect's work on Day 5
4. **Memory Persistence**: Database schema, storage strategy, indexing
5. **Cross-Quest Learning**: How past quest patterns improve future quest execution

**Round Table Application**:

- **Quest Knowledge Base**: All Lord insights stored in knowledge graph
- **Context Passing**: Lords write insights → Other Lords query/read
- **Long-Term Memory**: Quest history, Lord performance patterns, decision rationale
- **Semantic Retrieval**: "What did Oracle learn about X in previous quests?"

**Study Priority**: **3/5** (Essential State Management)

---

### 1.4 Plugged.in 🔧 PRIORITY 4

**URL**: https://github.com/PluggedIn-Team/plugged-in  
**Score**: 8.8/10 (Scope Validator)

**Why Selected**:

- **Multi-Server Proxy**: Proof-of-concept for "MCP server containing MCP servers"
- **Hierarchical Architecture**: Exactly the King↔Lords relationship model
- **Namespace Separation**: Prevents tool name collisions (`lord_a.tool` vs `lord_b.tool`)
- **Production Validation**: Successfully combines multiple MCP servers in production

**What We'll Learn**:

1. **Multi-Server Coordination**: Technical implementation of hierarchical MCP architecture
2. **Proxy Pattern**: How King forwards requests to appropriate Lord server
3. **Tool Namespacing**: Automatic prefixing (`oracle.`, `architect.`, etc.)
4. **Response Aggregation**: Combining outputs from multiple Lord servers
5. **Lord Discovery**: How King detects available Lords at runtime

**Round Table Application**:

- **Hierarchical MCP Proof**: Validates Round Table's "MCP server of MCP servers" design
- **Lord Isolation**: Each Lord = separate MCP server process
- **Inter-Lord Communication**: Message passing through King proxy
- **Dynamic Lord Management**: Lords can come online/offline without restarting King

**Study Priority**: **4/5** (Architectural Validation)

---

### 1.5 Magg (Meta-MCP) 🚀 PRIORITY 5

**URL**: https://github.com/MaggMCP/magg  
**Score**: 8.6/10 (Scope Validator)

**Why Selected**:

- **Autonomous Discovery**: AI agents extend their own capabilities at runtime
- **Swarm Coordination**: Self-organizing Lord collaboration (no hardcoded workflows)
- **Revolutionary Pattern**: Lords discover each other's capabilities dynamically
- **Future-Proof**: Adapts when new Lords added without reconfiguring King

**What We'll Learn**:

1. **Dynamic Tool Discovery**: How Lords advertise capabilities at runtime
2. **AI-Driven Orchestration**: AI selects which Lords to invoke (not hardcoded rules)
3. **Lazy Loading**: Activate Lords only when needed (resource efficiency)
4. **Self-Organizing Workflows**: Lords negotiate collaboration autonomously
5. **Meta-MCP Registry**: Central catalog of available Lord servers

**Round Table Application**:

- **Advanced Orchestration**: "Self-organizing Round Table" for complex quests
- **Flexible Lord Selection**: King suggests Lords based on quest, AI chooses optimal set
- **Evolutionary Architecture**: Add Lord #8, #9, #10 without breaking existing system
- **Emergent Intelligence**: Lords coordinate in ways not pre-programmed

**Study Priority**: **5/5** (Advanced/Experimental - Study Last)

**⚠️ RISK**: High complexity, unpredictable Lord interactions. Study for "Round Table 2.0" after basic hierarchical model proven.

---

## 2. Round Table MCP Server Architecture

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  (Claude Desktop, Cursor, Windsurf, Custom AI Tools)        │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP Protocol (JSON-RPC over stdio/SSE)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    KING (Round Table Gateway)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Gateway Router (context-forge pattern)             │   │
│  │  - Plugin Registry: 7 Lord MCP Servers              │   │
│  │  - Request Routing: Quest → Lord(s)                 │   │
│  │  - Response Aggregation: Multi-Lord outputs         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Workflow Orchestrator (n8n pattern)                │   │
│  │  - Quest DAG Builder: Lord dependencies             │   │
│  │  - Execution Engine: Sequential + Parallel          │   │
│  │  - State Checkpointing: Resume interrupted quests   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Quest Context Manager (Memory MCP pattern)         │   │
│  │  - Knowledge Graph: Persistent quest state          │   │
│  │  - Hierarchical Memory: Global → Lord → Tool        │   │
│  │  - Semantic Search: Cross-quest learning            │   │
│  └──────────────────────────────────────────────────────┘   │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬───────────┘
       │      │      │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌──────────────────────────────────────────────────────────────┐
│                    LORD LAYER (7 MCP Servers)                │
├──────────┬──────────┬──────────┬──────────┬──────────────────┤
│ Oracle   │Architect │ Curator  │ Executor │ Forge Master │...│
│ (MCP)    │ (MCP)    │ (MCP)    │ (MCP)    │ (MCP)        │   │
│ ┌──────┐ │ ┌──────┐ │ ┌──────┐ │ ┌──────┐ │ ┌──────┐     │   │
│ │Tools │ │ │Tools │ │ │Tools │ │ │Tools │ │ │Tools │     │   │
│ │- sea-│ │ │- des-│ │ │- emb-│ │ │- sch-│ │ │- cod-│     │   │
│ │  rch │ │ │  ign │ │ │  bed │ │ │  edul│ │ │  egen│     │   │
│ │- ana-│ │ │- plan│ │ │- tra-│ │ │- dep-│ │ │- ref-│     │   │
│ │  lyze│ │ │      │ │ │  nsf │ │ │  loy │ │ │  act │     │   │
│ └──────┘ │ └──────┘ │ └──────┘ │ └──────┘ │ └──────┘     │   │
│ Working  │ Working  │ Working  │ Working  │ Working      │   │
│ Memory   │ Memory   │ Memory   │ Memory   │ Memory       │   │
└──────────┴──────────┴──────────┴──────────┴──────────────┴───┘
       │      │      │      │      │      │      │
       └──────┴──────┴──────┴──────┴──────┴──────┴──────────┐
                     ▼                                        │
┌─────────────────────────────────────────────────────────────┤
│                 FOUNDATION LAYER                             │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │ Knowledge Graph│  │ Vector Store   │  │ Audit Trail  │  │
│  │ (Neo4j/SQLite) │  │ (Qdrant/Chroma)│  │ (Dolt/Event) │  │
│  │ - Quest State  │  │ - Embeddings   │  │ - Lord Logs  │  │
│  │ - Lord Insights│  │ - Semantic Idx │  │ - Decisions  │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Component Specifications

#### A. King (Round Table Gateway) - Primary MCP Server

**Technology**: Python (MCP Python SDK) or TypeScript (MCP TypeScript SDK)  
**Primary Pattern**: IBM context-forge Plugin Registry + Gateway

**Responsibilities**:

1. **Gateway Router**

   - Accept MCP requests from clients (Claude, Cursor, etc.)
   - Maintain registry of 7 Lord MCP server plugins
   - Route quest requests to appropriate Lord(s)
   - Aggregate multi-Lord responses into cohesive output
   - Expose unified tool namespace: `oracle.search`, `architect.design`, etc.

2. **Workflow Orchestrator**

   - Parse quest requirements into Lord dependency DAG
   - Execute Lords in correct order (sequential/parallel)
   - Handle Lord-to-Lord data passing via message queues
   - Checkpoint workflow state after each Lord completion
   - Resume interrupted quests from last checkpoint

3. **Quest Context Manager**
   - Maintain hierarchical memory: Global Quest → Lord Working Memory → Tool Context
   - Store/retrieve quest state in knowledge graph
   - Provide semantic search across past quest insights
   - Manage Lord-to-Lord context sharing (read/write to shared memory)

**Key Design Decisions**:

- **Single Entry Point**: Clients call King, never directly call Lords
- **Plugin Architecture**: Lords register as plugins at King startup (or dynamically)
- **Stateful Gateway**: Unlike most gateways, King maintains quest state (via Memory MCP pattern)

#### B. Lord Layer - 7 Specialized MCP Servers

**Technology**: Each Lord = Independent MCP server (Python or TypeScript)  
**Pattern**: Decorator-based tool registration within each Lord + Plugin registration with King

**Lord MCP Server Structure** (Example: Lord Oracle):

```python
# oracle_server.py
from mcp.server import Server
from mcp.types import Tool

oracle = Server("lord-oracle")

@oracle.tool()
async def semantic_search(query: str, sources: list[str]) -> dict:
    """Search knowledge bases and return relevant insights"""
    # Implementation...

@oracle.tool()
async def research_synthesis(findings: list[dict]) -> str:
    """Synthesize multiple research findings into coherent analysis"""
    # Implementation...

# Register with King at startup
oracle.register_with_gateway(king_url="http://localhost:8000/register")
```

**Lord Responsibilities**:

1. **Tool Exposure**: Each Lord exposes 5-15 specialized tools via MCP protocol
2. **Working Memory**: Each Lord maintains session-specific context
3. **King Communication**: Lords receive requests from King, return structured results
4. **Capability Advertisement**: Lords advertise tool capabilities to King at registration

**Namespace Convention**: `lord_name.tool_name` (e.g., `oracle.semantic_search`)

#### C. State Management Layer

**Component 1: Knowledge Graph (Memory MCP Pattern)**

- **Technology**: SQLite (MVP) → Neo4j (Production)
- **Purpose**: Persistent quest state, Lord insights, semantic relationships
- **Schema**:
  ```
  Nodes: Quest, Lord, Insight, File, Concept
  Edges: DEPENDS_ON, PRODUCES, RELATES_TO, REFERENCES
  ```

**Component 2: Vector Store (Semantic Search)**

- **Technology**: Qdrant (local) or Chroma (embedded)
- **Purpose**: Fast semantic search across Lord insights
- **Use Case**: "What did Oracle learn about X in past quests?"

**Component 3: Audit Trail (Version Control)**

- **Technology**: Event sourcing (JSON logs) → Dolt (Git-like DB versioning)
- **Purpose**: Track every Lord decision, quest state change
- **Use Case**: Debugging ("Why did Architect choose this approach?"), Learning

#### D. Communication Protocol

**King ↔ Lords**: Internal MCP protocol (stdio or HTTP/SSE)

- King spawns Lord processes, communicates via MCP JSON-RPC
- Alternative: HTTP-based MCP for distributed deployment

**Lords ↔ Memory**: Direct database access (shared connection pool)

- Lords write insights to knowledge graph
- Lords query graph for context from other Lords

**Client ↔ King**: Standard MCP protocol (stdio for local, SSE for remote)

- Clients see King as single MCP server
- Lords are invisible to clients (encapsulated)

### 2.3 Technology Stack Decisions

| Layer             | Component              | Technology                         | Rationale                                          |
| ----------------- | ---------------------- | ---------------------------------- | -------------------------------------------------- |
| **King**          | Gateway Core           | Python + MCP SDK                   | Mature MCP SDK, rich ecosystem, rapid prototyping  |
| **King**          | Workflow Engine        | Custom DAG (inspired by n8n)       | Lightweight, tailored to Round Table needs         |
| **King**          | HTTP Server (optional) | FastAPI                            | If remote King access needed (HTTP-based MCP)      |
| **Lords**         | MCP Servers            | Python + MCP SDK                   | Consistency with King, tool-rich ecosystem         |
| **State**         | Knowledge Graph        | SQLite (MVP) → Neo4j               | SQLite for prototyping, Neo4j for production scale |
| **State**         | Vector Store           | Qdrant (local mode)                | Best open-source vector DB, local-first            |
| **State**         | Audit Trail            | JSON logs → Dolt                   | Start simple, upgrade to version-controlled DB     |
| **Communication** | King↔Lords             | stdio (local) or HTTP/SSE (remote) | stdio for single-machine, HTTP for distributed     |
| **Communication** | Message Queue (future) | Redis Streams or RabbitMQ          | If async Lord coordination needed                  |

**Critical Decision: Python over TypeScript**

- **Why Python**:
  - MCP Python SDK is more mature (as of Dec 2024)
  - Lord tool implementations (AI models, data processing) have richer Python libraries
  - Team velocity advantage (faster prototyping)
- **TypeScript Alternative**: Consider if frontend visualization critical (n8n-style UI)

### 2.4 Critical Design Choices with Rationale

#### Choice 1: Hierarchical MCP (King + 7 Lord Servers) vs Monolithic MCP (Single Server)

**Decision**: **Hierarchical**

**Rationale**:

- ✅ **Separation of Concerns**: Each Lord independently developed/tested/deployed
- ✅ **Scalability**: Lords run in parallel processes (CPU/memory isolation)
- ✅ **Maintainability**: Update Oracle without touching Architect
- ✅ **Team Collaboration**: Different developers own different Lords
- ❌ **Complexity**: Multi-process coordination, inter-Lord communication overhead
- ❌ **Performance**: Network/IPC latency vs in-memory function calls

**Validated By**: Plugged.in (production multi-server proxy), IBM context-forge (gateway pattern)

#### Choice 2: Stateful King vs Stateless King

**Decision**: **Stateful** (with persistent memory)

**Rationale**:

- ✅ **Long-Running Quests**: Multi-day workflows require persistent state
- ✅ **Context Continuity**: Lords need access to past quest insights
- ✅ **Resume Capability**: Server restarts don't lose quest progress
- ❌ **Complexity**: State management, backup/restore, concurrency control
- ❌ **Scalability**: Harder to horizontally scale stateful services

**Validated By**: Memory MCP (knowledge graph), n8n (workflow state), Trigger.dev (background jobs)

#### Choice 3: Synchronous Lord Execution vs Event-Driven Async

**Decision**: **Hybrid** (synchronous orchestration with async capability)

**Rationale**:

- **Synchronous** (for sequential dependencies): Oracle → Architect → Forge Master
  - Simpler reasoning, explicit data flow, easier debugging
- **Async** (for parallel work): Oracle + Curator run simultaneously
  - Better resource utilization, faster quest completion
- **Implementation**: n8n-style DAG executor with both sync/async edges

**Validated By**: n8n (hybrid workflows), Pipedream (event-driven), Trigger.dev (background jobs)

#### Choice 4: Direct Parameter Passing vs Shared Memory Context

**Decision**: **Hybrid** (message passing + shared memory)

**Rationale**:

- **Message Passing** (explicit Lord-to-Lord communication):
  - Clear data contracts, traceable, testable
  - Example: Oracle sends `{research_findings: [...]}` → Architect
- **Shared Memory** (implicit context accumulation):
  - Rich context (semantic graph of all quest knowledge)
  - Example: Architect queries "What did Oracle learn about X?"
- **Best of Both**: Messages for handoffs, memory for context

**Validated By**: n8n (message passing), Memory MCP (shared context), Make.com (hybrid)

#### Choice 5: Hardcoded Lord Workflows vs AI-Driven Dynamic Orchestration

**Decision**: **Phased** (hardcoded first, AI-driven later)

**Rationale**:

- **Phase 1 (MVP)**: Hardcoded workflows (King knows Oracle→Architect→Forge)
  - Predictable, debuggable, reliable
  - Faster to implement and validate
- **Phase 2 (Advanced)**: AI-driven orchestration (King uses Magg pattern)
  - Flexible, self-organizing, adapts to new Lords
  - Higher complexity, requires extensive testing

**Validated By**: n8n (explicit workflows), Magg (AI-driven), Claude Flow (swarm intelligence)

---

## 3. Lord Integration Model

### 3.1 Evaluation of Three Models

#### Model A: Lord-as-MCP-Server (Separate Processes)

**Architecture**: Each Lord = Independent MCP server, King = Gateway proxy

**Pros**:

- ✅ True separation of concerns (Lords are black boxes)
- ✅ Process isolation (Lord crash doesn't kill King)
- ✅ Independent scaling (run 3 Oracle instances, 1 Architect)
- ✅ Language flexibility (Oracle in Python, Forge Master in Rust)
- ✅ Proven pattern (Plugged.in, IBM context-forge)

**Cons**:

- ❌ IPC overhead (stdio/HTTP communication between processes)
- ❌ Complex deployment (7+ processes to manage)
- ❌ Harder local development (spawn 8 servers for testing)

**Validated By**: Plugged.in (multi-server proxy), IBM context-forge (plugin servers)

---

#### Model B: Lord-as-Tool-Namespace (Single Process)

**Architecture**: One King MCP server with tool namespaces (`oracle.*`, `architect.*`)

**Pros**:

- ✅ Simpler deployment (single process)
- ✅ Zero IPC overhead (in-memory function calls)
- ✅ Easier local development (one `python king_server.py`)
- ✅ Lower resource usage (no multi-process overhead)

**Cons**:

- ❌ No process isolation (one Lord crash could kill entire King)
- ❌ Tight coupling (Lords can't be independently versioned/deployed)
- ❌ Monolithic complexity (7 Lords in one codebase)
- ❌ Resource contention (CPU/memory shared by all Lords)

**Validated By**: Most MCP servers use this (simple, monolithic)

---

#### Model C: Hybrid (Lords as Plugin Modules, Optional Separate Processes)

**Architecture**:

- **Development**: Lords as Python modules loaded by King (single process)
- **Production**: Lords as separate MCP servers proxied by King (multi-process)

**Pros**:

- ✅ Best of both worlds
- ✅ Fast local iteration (single process, in-memory calls)
- ✅ Production scalability (separate processes when needed)
- ✅ Gradual migration (start monolithic, split as needed)
- ✅ Flexible deployment (some Lords remote, some local)

**Cons**:

- ❌ Dual implementation complexity (support both modes)
- ❌ Abstraction overhead (Lord interface must support both)

**Validated By**: IBM context-forge (supports plugin modules or remote servers)

---

### 3.2 Recommended Model: **Hybrid** (Plugin Modules + Optional Remote Servers)

**Rationale**: Optimize for **development velocity** (Phase 1-2) while enabling **production scalability** (Phase 3-4).

**Implementation**:

```python
# King's Lord loader (hybrid mode)
class LordLoader:
    def load_lord(self, lord_name: str, config: dict):
        if config.get("mode") == "local":
            # Load as Python module (single process)
            lord_module = importlib.import_module(f"lords.{lord_name}")
            return LocalLordAdapter(lord_module)
        elif config.get("mode") == "remote":
            # Connect to remote MCP server (separate process)
            return RemoteLordAdapter(config["url"])

# Configuration flexibility
lords_config = {
    "oracle": {"mode": "local"},      # Fast local calls
    "architect": {"mode": "local"},   # Fast local calls
    "forge_master": {"mode": "remote", "url": "http://gpu-server:8001"}  # Remote GPU
}
```

**Migration Path**:

1. **Phase 1-2 (MVP)**: All Lords as local modules (single process)
2. **Phase 3 (Optimization)**: Move resource-intensive Lords to remote servers (e.g., Forge Master on GPU machine)
3. **Phase 4 (Scale)**: Distribute Lords across multiple machines as needed

**Pattern Validation**: IBM context-forge supports both plugin modules and remote server proxying.

---

## 4. Implementation Roadmap

### Phase 2.1: Gateway Foundation (Weeks 1-2)

**Goal**: Build King gateway that can route to multiple Lords

**Repositories to Study**:

1. **IBM context-forge** (Priority 1) - Gateway architecture, plugin registry
2. **Plugged.in** (Priority 4) - Multi-server proxy pattern

**Deliverables**:

- ✅ King MCP server skeleton (accepts MCP requests)
- ✅ Plugin registry system (Lords register capabilities)
- ✅ Request routing (quest → appropriate Lord(s))
- ✅ Tool namespace management (`lord_name.tool_name`)
- ✅ MVP: 2 Lords (Oracle + Scribe) as local plugins
- ✅ Manual testing: Client → King → Lords → Response

**Success Criteria**: Client can call `oracle.search` through King gateway

---

### Phase 2.2: Workflow Orchestration (Weeks 3-4)

**Goal**: Enable multi-Lord quest workflows with dependencies

**Repositories to Study**:

1. **n8n-io/n8n** (Priority 2) - DAG-based orchestration, workflow state
2. **Pipedream** (Supplementary) - Event-driven patterns, error handling

**Deliverables**:

- ✅ Quest DAG builder (parse quest → Lord dependency graph)
- ✅ Sequential execution engine (Oracle → Architect → Forge)
- ✅ Parallel execution support (Oracle + Curator simultaneously)
- ✅ Data passing between Lords (message format, serialization)
- ✅ Error handling (retry logic, graceful degradation)
- ✅ MVP: 3-Lord workflow (Oracle → Architect → Scribe)

**Success Criteria**: Complex quest executes Oracle, then Architect (using Oracle's results), then Scribe

---

### Phase 2.3: State & Memory (Weeks 5-6)

**Goal**: Persistent quest state and Lord knowledge sharing

**Repositories to Study**:

1. **Memory MCP** (Priority 3) - Knowledge graph, semantic search
2. **Dolt MCP** (Supplementary) - Version-controlled state, audit trail

**Deliverables**:

- ✅ Knowledge graph schema (Quest, Lord, Insight nodes)
- ✅ Hierarchical context (Global → Lord → Tool)
- ✅ Write APIs (Lords store insights)
- ✅ Read APIs (Lords query past knowledge)
- ✅ Semantic search (vector embeddings, Qdrant integration)
- ✅ Quest persistence (save/load quest state)
- ✅ Audit trail (log all Lord decisions)

**Success Criteria**: Oracle's Day 1 research is accessible to Architect on Day 5

---

### Phase 2.4: Integration & Polish (Weeks 7-8)

**Goal**: Complete Round Table MVP with all 7 Lords

**Repository to Study**:

1. **Magg** (Priority 5) - Dynamic discovery, optional advanced patterns

**Deliverables**:

- ✅ All 7 Lords implemented as plugins (Oracle, Architect, Curator, Executor, Forge Master, Scribe, Sentinel)
- ✅ End-to-end quest execution (client submits quest → King coordinates 7 Lords → returns comprehensive result)
- ✅ Quest resume/checkpoint (handle interruptions)
- ✅ Lord health monitoring (detect crashed Lords, auto-restart)
- ✅ Performance optimization (reduce latency, memory usage)
- ✅ Documentation (architecture diagrams, API references, deployment guide)
- ✅ Example quests (demonstrate multi-Lord coordination)

**Success Criteria**: Client submits complex quest, Round Table autonomously coordinates all 7 Lords, returns high-quality deliverable

---

### Timeline Summary

| Phase             | Duration    | Repositories              | Focus                             | Outcome               |
| ----------------- | ----------- | ------------------------- | --------------------------------- | --------------------- |
| 2.1 Gateway       | 2 weeks     | context-forge, Plugged.in | Routing, namespacing              | 2-Lord MVP working    |
| 2.2 Orchestration | 2 weeks     | n8n, Pipedream            | DAG workflows, dependencies       | Multi-Lord quests     |
| 2.3 State/Memory  | 2 weeks     | Memory MCP, Dolt          | Persistent state, knowledge graph | Long-running quests   |
| 2.4 Integration   | 2 weeks     | Magg (optional)           | 7 Lords, polish                   | Production-ready MVP  |
| **Total**         | **8 weeks** | 5 core repos              | Full Round Table                  | Ready for real quests |

---

## 5. Gap Analysis

### 5.1 Patterns We Need (No Repository Demonstrates)

#### Gap 1: 7-Lord Hierarchical Coordination

**Need**: Coordinate 7 specialized agents with dependencies  
**Status**: No existing MCP server orchestrates 7+ specialized sub-servers  
**Mitigation**: Combine patterns from n8n (DAG) + Plugged.in (multi-server) + custom logic  
**Risk**: Medium - Building first-of-its-kind system, expect unexpected challenges

#### Gap 2: Hierarchical Context Management

**Need**: Global Quest → Lord Working Memory → Tool Execution Context (3-level hierarchy)  
**Status**: Memory MCP has global context, but not hierarchical namespacing  
**Mitigation**: Extend Memory MCP pattern with namespace prefixes (`quest_id:lord_name:context_key`)  
**Risk**: Low - Straightforward extension of existing pattern

#### Gap 3: Lord-to-Lord Direct Communication

**Need**: Lords sometimes need to call other Lords (e.g., Architect asks Oracle for clarification)  
**Status**: Most orchestrators assume hierarchical (gateway → tool), not peer-to-peer  
**Mitigation**: Implement message bus where Lords publish/subscribe to messages  
**Risk**: Medium - Adds complexity, potential for circular dependencies

#### Gap 4: Quest Workflow Visualization

**Need**: Visual representation of Lord dependencies, execution progress  
**Status**: n8n has visual DAG editor, but it's a full application (not embeddable)  
**Mitigation**: Start with text-based DAG representation, add visualization in Phase 3  
**Risk**: Low - Nice-to-have, not critical for MVP

#### Gap 5: Lord Health Monitoring & Auto-Recovery

**Need**: Detect crashed Lords, auto-restart, retry failed tasks  
**Status**: Kubernetes MCPs have health checks, but for containers not MCP servers  
**Mitigation**: Implement process monitoring, watchdog timers, exponential backoff retries  
**Risk**: Medium - Critical for production reliability, but complex to implement

---

### 5.2 Open Research Questions (For Anthropic MCP Docs)

#### Question 1: Multi-Server MCP Architecture Best Practices

**Question**: What's the recommended pattern for "MCP server containing MCP servers"?  
**Why**: Round Table is hierarchical (King + 7 Lords). Need official guidance on multi-server coordination.  
**Anthropic Docs**: Check if MCP spec addresses hierarchical architectures, server-to-server communication.

#### Question 2: Stateful MCP Server Patterns

**Question**: How should MCP servers handle long-running, persistent state?  
**Why**: Most examples are stateless. Round Table needs multi-day quest state.  
**Anthropic Docs**: Look for session management, state persistence patterns, database integration examples.

#### Question 3: MCP Server Resource Limits

**Question**: What are performance limits? (# of tools, request latency, concurrent calls)  
**Why**: Round Table exposes 50-100 tools (7 Lords × 10-15 tools each). Need to know if this scales.  
**Anthropic Docs**: Search for performance guidance, scaling recommendations.

#### Question 4: Error Propagation Across Multiple Servers

**Question**: When Lord A fails, how should King report error to client? Retry? Fallback?  
**Why**: Multi-server orchestration needs robust error handling.  
**Anthropic Docs**: Review error handling specifications, retry mechanisms, status codes.

#### Question 5: Dynamic Tool Registration

**Question**: Can MCP servers dynamically add/remove tools at runtime (not just startup)?  
**Why**: Lords might gain new capabilities mid-quest, or come online/offline dynamically.  
**Anthropic Docs**: Check if MCP spec supports runtime tool registration, hot-reloading.

---

### 5.3 High-Risk Components

#### Risk 1: Multi-Server Communication Overhead ⚠️ **HIGH RISK**

**Component**: King ↔ Lords communication (IPC via stdio/HTTP)  
**Risk**: Latency between King and 7 Lords could slow quest execution  
**Mitigation**:

- Start with single-process (local plugin mode) for MVP
- Benchmark multi-process overhead in Phase 2
- Optimize hot paths (e.g., keep frequently-called Lords in-process)
- Consider shared memory for bulk data transfer  
  **Fallback**: If multi-process too slow, switch to Lord-as-Tool-Namespace model

#### Risk 2: Knowledge Graph Complexity ⚠️ **HIGH RISK**

**Component**: Persistent state management (Memory MCP pattern)  
**Risk**: Knowledge graph might become too complex (thousands of nodes/edges), slow queries  
**Mitigation**:

- Start with SQLite (simpler schema) before Neo4j
- Implement aggressive pruning (archive old quest data)
- Use vector DB (Qdrant) for semantic search, not graph traversal
- Benchmark query performance regularly  
  **Fallback**: If graph too slow, use simpler key-value store (Redis) with structured keys

#### Risk 3: DAG Execution Engine Bugs ⚠️ **MEDIUM RISK**

**Component**: Workflow orchestrator (n8n-inspired DAG executor)  
**Risk**: Complex Lord dependencies might have edge cases (cycles, deadlocks, race conditions)  
**Mitigation**:

- Extensive unit tests for DAG builder (test cycles, unreachable nodes)
- Use proven libraries (NetworkX for graph algorithms)
- Start with simple linear workflows (A → B → C) before complex DAGs
- Manual review of all quest DAGs before execution  
  **Fallback**: If DAG too complex, restrict to linear workflows only (no parallelism)

#### Risk 4: Lord Crash Recovery ⚠️ **MEDIUM RISK**

**Component**: Lord health monitoring, auto-restart  
**Risk**: Crashed Lord might leave quest in inconsistent state  
**Mitigation**:

- Checkpoint quest state after each Lord completion
- Implement idempotent Lords (re-running produces same result)
- Watchdog timer detects hung Lords, auto-restarts
- Manual review of interrupted quests before resuming  
  **Fallback**: If auto-recovery unreliable, require manual quest restart

#### Risk 5: Scope Creep (Too Many Features) ⚠️ **LOW RISK**

**Component**: Overall project scope  
**Risk**: Trying to implement all patterns (n8n + Magg + Pipedream + ...) = never ship MVP  
**Mitigation**:

- **Strict MVP scope**: Gateway + 2 Lords + basic workflows + SQLite state
- Defer advanced features (Magg discovery, event-driven, Neo4j) to Phase 3+
- Timebox each phase (2 weeks max)
- Regular review: "Is this critical for MVP or nice-to-have?"  
  **Fallback**: If behind schedule, reduce to 1 Lord proof-of-concept

---

## 6. Final Recommendations

### 6.1 Phase 2 Execution Plan

**Immediate Next Steps** (Upon Royal Approval):

1. **Week 0 (Prep)**:

   - Clone 5 core repositories to `Magic-Tower/Foundation/MCP-Servers/`
   - Set up local MCP development environment (Python SDK, test clients)
   - Create `Magic-Tower/Blueprint-Gallery/Round-Table-Architecture/` documentation folder

2. **Week 1-2 (Gateway)**:

   - Deep study: IBM context-forge (plugin system) + Plugged.in (proxy pattern)
   - Implement King gateway skeleton
   - Implement 2 Lords (Oracle + Scribe) as local plugins
   - Manual test: Client → King → Oracle → Response

3. **Week 3-4 (Orchestration)**:

   - Deep study: n8n (DAG workflows) + Pipedream (error handling)
   - Implement quest DAG builder + execution engine
   - Test 3-Lord workflow: Oracle → Architect → Scribe
   - Implement retry logic, error propagation

4. **Week 5-6 (State)**:

   - Deep study: Memory MCP (knowledge graph)
   - Implement SQLite-based knowledge graph
   - Implement Lord read/write APIs for quest context
   - Test persistent multi-day quest (save on Day 1, resume Day 2)

5. **Week 7-8 (Integration)**:
   - Implement remaining 5 Lords (Architect, Curator, Executor, Forge Master, Sentinel)
   - End-to-end testing with complex multi-Lord quests
   - Performance optimization, bug fixes
   - Documentation + example quests

### 6.2 Success Metrics

**MVP Success Criteria** (End of Phase 2):

- ✅ All 7 Lords operational as MCP plugins
- ✅ Complex quest coordination (5+ Lords in single workflow)
- ✅ Persistent state (quests resume after restarts)
- ✅ Sub-30-second response time for typical quests
- ✅ 90%+ quest completion rate (no crashes/deadlocks)
- ✅ Comprehensive documentation (architecture, API, deployment)

**Production Readiness** (Phase 3+):

- ✅ Load testing (100+ concurrent quests)
- ✅ 99.9% uptime (fault tolerance, auto-recovery)
- ✅ Observability (metrics, logging, tracing)
- ✅ Security audit (input validation, auth, secrets management)
- ✅ Multi-user support (team collaboration features)

### 6.3 Go/No-Go Decision Points

**After Week 2** (Gateway Complete):

- **GO**: Client can successfully call 2 Lords through King → Proceed to orchestration
- **NO-GO**: Fundamental architectural issues → Pivot to simpler monolithic model

**After Week 4** (Orchestration Complete):

- **GO**: Multi-Lord workflows execute correctly → Proceed to state management
- **NO-GO**: DAG execution too buggy → Simplify to linear workflows only

**After Week 6** (State Complete):

- **GO**: Persistent quests work reliably → Proceed to full integration
- **NO-GO**: State management too complex → Use simpler file-based storage

**After Week 8** (MVP Complete):

- **GO**: All 7 Lords coordinated, quests complete successfully → Declare MVP success, move to production hardening
- **NO-GO**: Too many critical bugs → Extend Phase 2 by 2 weeks for stabilization

---

## 7. Conclusion

The Round Table MCP Server is **architecturally viable** based on proven patterns from 5 exceptional repositories:

1. **IBM context-forge** teaches gateway + plugin registry (King architecture)
2. **n8n** teaches DAG workflows + state persistence (Quest orchestration)
3. **Memory MCP** teaches knowledge graphs (Persistent Lord insights)
4. **Plugged.in** validates multi-server hierarchies (Proof of concept)
5. **Magg** shows future vision (Self-organizing Lords)

**Critical Innovation**: We're building the **first MCP server to coordinate 7 hierarchical specialist agents**. This is uncharted territory, but we have solid patterns to build upon.

**Risk Assessment**: **Medium Risk** - Novel architecture, but mitigated by:

- Phased approach (MVP → Production)
- Proven patterns from production systems
- Fallback options for high-risk components
- Strict scope control (no feature creep)

**Recommendation to the King**: **Approve Phase 2 execution**. Begin with 8-week development sprint, review at Week 2/4/6/8 checkpoints. Expected outcome: Working Round Table MVP managing all 7 Lords.

**The Sage's Confidence**: 🔮 **85%** - Architecture is sound, patterns are proven, scope is manageable. The 15% risk comes from combining these patterns in novel ways. But that's what innovation requires.

---

_"Your Majesty, the foundation stones are selected. The blueprint is drawn. The forges are ready. We can build this."_

— The Sage, Lord of the Magic Tower

---

**Awaiting Royal Approval to Proceed to Phase 2.1: Gateway Foundation Construction**
