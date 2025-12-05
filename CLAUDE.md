# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Poncho's-Portal is a DND-style knowledge kingdom for mastering AI and agentic systems. It's a structured documentation and orchestration framework where autonomous agents, workflows, and AI fundamentals are organized using a fantasy-themed architecture.

**This is not a code repository**—it's a living knowledge system and agent orchestration framework. There is no code to build, test, or run. The fantasy theming is intentional structure, not decoration.

## Core Architecture

### The Three Pillars

1. **Magic-Tower** - Knowledge repository organized by AI domain
2. **Kingdom-of-Agents** - Agent orchestration framework with seven specialized "Lords"
3. **Ponchos-Avatar** - Meta-orchestration layer (the "Agent King")

### Agent Orchestration Model

The system uses a hierarchical agent architecture:

- **Poncho's-Avatar (The Agent King)**: Meta-orchestrator that coordinates multiple Agent Lords
- **Seven Agent Lords**: Each commands specialized sub-agents in their domain
  - Lord Architect: System design & planning
  - Lord Scribe: Knowledge & documentation
  - Lord Sentinel: Analysis & validation
  - Lord Forge Master: Code generation
  - Lord Oracle: Research & intelligence
  - Lord Curator: Data & context management
  - Lord Executor: Deployment & automation
- **Lord Sage** (Guardian of the Magic-Tower): Not part of the Seven—serves the Library itself
  - Expert in GitHub repos, Claude, GPT, Gemini, agentic architectures, and MCP servers
  - Maintains Library structure, conducts experiments, researches infrastructure patterns
  - Currently researching MCP server architectures for Lord management (Quest 001)
  - Philosophy: "Generated content is sand. Documentation, repositories, and refined notes are stone."
  - Reports directly to the King on Library status and experimental results

### Key Organizational Principles

**Delegation over Execution**: The King delegates to Lords, Lords coordinate specialized agents. Never bypass this hierarchy.

**Workflow Templates**: Standard multi-lord orchestrations are defined in [Ponchos-Avatar/workflow-templates.md](Ponchos-Avatar/workflow-templates.md). Use these patterns for complex quests.

**Quest Classification**: Before taking action, categorize the request as Research, Design, Creation, Knowledge, Deployment, Optimization, or Complex Quest. This determines which Lords are needed.

## Directory Structure

### Magic-Tower/Library/AI-section/

Knowledge domains organized by AI concept:

- Agentic-Loops, Prompt-Craft, RAG-Archives, Embedding-Forge
- Fine-Tuning-Sanctum, Context-Windows, Transformer-Cathedral
- Evaluation-Chamber, Orchestration-Tower, Function-Calling-Nexus
- Model-Zoo, Token-Economics, Vector-Database-Vaults, Safety-Scrolls

### Kingdom-of-Agents/

Agent definitions organized by Lord, with each Lord containing specialized agent definitions:

- Round-Table: Coordination protocols
- Lord-[Name]/: Each lord's directory contains agent specs (e.g., system-designer.md, code-reviewer.md)

### Ponchos-Avatar/

Meta-orchestration guidance:

- [kings-playbook.md](Ponchos-Avatar/kings-playbook.md): Quest classification and delegation patterns
- [round-table-protocol.md](Ponchos-Avatar/round-table-protocol.md): Communication and coordination rules
- [workflow-templates.md](Ponchos-Avatar/workflow-templates.md): Standard multi-lord orchestrations

### Setting/

Meta-organization:

- Quest-Log: Active tasks and goals
- Reference-Grimoire: Reference materials
- Glossary-Stone: Terminology definitions
- Portal-Rules: Naming conventions and structure rules
- vibe.md: Philosophy and mission

### Magic-Tower/ (Infrastructure)

- **Lord-Sage/**: Guardian of the Library, expert in AI platforms and repository curation
  - Commands specialized intelligence loops (e.g., Quest 001: 6-agent MCP server analysis workflow)
  - See [quest-001-workflow.md](Magic-Tower/Lord-Sage/quest-001-workflow.md) for sequential-parallel hybrid architecture example
- Foundry: Training infrastructure concepts
- Ritual-Scripts: Code templates and patterns
- Experiment-Logs: Quest outcomes and learnings
- Blueprint-Gallery: Architecture patterns

## Working with This Codebase

### When Creating New Content

1. **Choose the correct pillar**: Knowledge goes in Magic-Tower, agent specs go in Kingdom-of-Agents
2. **Follow the fantasy naming convention**: Use thematic names (Chamber, Sanctum, Vaults, etc.)
3. **Create minimal READMEs**: Each directory should have a brief README.md explaining its purpose
4. **Log experiments**: Document outcomes in [Magic-Tower/Experiment-Logs/](Magic-Tower/Experiment-Logs/) and [Setting/Quest-Log/](Setting/Quest-Log/)

### When Orchestrating Multi-Agent Workflows

1. **Consult the King's Playbook**: Check [Ponchos-Avatar/kings-playbook.md](Ponchos-Avatar/kings-playbook.md) for delegation patterns
2. **Use workflow templates**: Reference [Ponchos-Avatar/workflow-templates.md](Ponchos-Avatar/workflow-templates.md) for standard orchestrations
3. **Identify required Lords**: Determine which domains are needed before delegating
4. **Follow Round Table Protocol**: Structure coordination per [Ponchos-Avatar/round-table-protocol.md](Ponchos-Avatar/round-table-protocol.md)

### When Adding New Agent Definitions

Place agent specs under the appropriate Lord in [Kingdom-of-Agents/Lord-[Name]/](Kingdom-of-Agents/). Each agent should have:

- Clear role definition
- Specific capabilities
- Tools they can wield
- Knowledge domains they reference from Magic-Tower

### File Organization Rules

- All directories must have a README.md
- Use descriptive, thematic names aligned with the DND framing
- Group related concepts within appropriate AI domain sections
- Cross-reference between pillars when agents need Magic-Tower knowledge

### When Designing Agentic Workflows

Lord Sage demonstrates the canonical architectural pattern for multi-agent intelligence loops in [Magic-Tower/Lord-Sage/quest-001-workflow.md](Magic-Tower/Lord-Sage/quest-001-workflow.md):

**Sequential-Parallel Hybrid Architecture**:

- **Parallel**: Independent agents run simultaneously (e.g., README analysis + pattern comparison)
- **Sequential**: Dependent agents wait for prerequisites (e.g., validation needs comparison results)

**Core Principles**:

1. **Understand Before Action**: Analyze documentation/metadata before downloading/executing (e.g., analyze READMEs before cloning repos)
2. **Explicit Handoffs**: Each agent has clear inputs, outputs, and success criteria
3. **Quality Gates**: Each phase must meet standards before proceeding to next phase
4. **Synthesis Agents**: Final agent compiles all outputs into cohesive report
5. **Parallel When Independent, Sequential When Dependent**: Optimize for efficiency while respecting dependencies

**Example from Quest 001** (MCP Server Architecture Research):

```
Repository Scout (sequential) - Discover MCP servers
    ↓
[README Analyst + Pattern Comparator] (parallel) → Scope Validator (Lord management fit)
    ↓
Foundation Recommender (strategic) - Proposes Round Table architecture
    ↓
Evaluation Report Compiler (synthesis) - MCP Architecture Report
```

### Orchestration Decision Tree

When given a request, identify the quest type and determine which Lords to involve:

**Research Quests**: Lord Oracle leads, Lord Scribe documents findings
**Design Quests**: Lord Architect plans, Lord Sentinel validates feasibility
**Creation Quests**: Lord Forge Master generates, Lord Sentinel reviews quality
**Knowledge Quests**: Lord Scribe organizes, Lord Curator structures data
**Deployment Quests**: Lord Executor manages, Lord Sentinel monitors quality
**Optimization Quests**: Lord Curator refines data, Lord Executor improves performance
**Complex Quests**: Multiple Lords in coordinated workflows (use [workflow-templates.md](Ponchos-Avatar/workflow-templates.md))

**When to involve each Lord**:

- **Lord Architect**: Complex systems, unclear requirements, need for planning
- **Lord Scribe**: Documentation gaps, knowledge organization, reference needs
- **Lord Sentinel**: Quality concerns, security risks, validation required
- **Lord Forge Master**: Code needed, APIs to build, prompts to craft
- **Lord Oracle**: Unknown information, research needed, comparison required
- **Lord Curator**: Data transformation, embeddings needed, context optimization
- **Lord Executor**: Deployment, automation, performance monitoring, workflows

See [Ponchos-Avatar/kings-playbook.md](Ponchos-Avatar/kings-playbook.md) for complete delegation patterns.

## Philosophy

From [Setting/vibe.md](Setting/vibe.md):

> Master the matrix through structured exploration. Every agent type you'll need. Every AI concept mapped. Real tools, real patterns, mythical framing.

**Lord Sage's Philosophy**:

> _"Generated content is sand. Documentation, repositories, and refined notes are stone. Build the Library on stone."_

When in doubt, ask: **"Which Lord handles this?"** and **"Where in the Magic-Tower does this knowledge belong?"**
