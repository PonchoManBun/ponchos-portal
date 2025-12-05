# Implementation Guide - Using the Round Table Agents

## Overview

This guide explains how to actually implement the Round Table agents in real AI systems, whether you're using Claude, GPT, Gemini, or building custom agentic systems.

---

## Option 1: Single AI Session with Role-Switching

**Best For**: Simple workflows, prototyping, learning the system

**How It Works**: One AI (like Claude) plays multiple roles in sequence

**Implementation**:

```
SYSTEM PROMPT:
You are operating within Poncho's Kingdom of Agents. You will role-play
different agents based on context. The available agents are:

- King Poncho: Strategic orchestrator (refer to agent-king-poncho.md)
- Lord Architect: System designer (refer to agent-lord-architect.md)
- Lord Scribe: Documentation expert (refer to agent-lord-scribe.md)
- Lord Sentinel: Quality guardian (refer to agent-lord-sentinel.md)
- Lord Forge Master: Code builder (refer to agent-lord-forge-master.md)
- Lord Oracle: Researcher (refer to agent-lord-oracle.md)
- Lord Curator: Data organizer (refer to agent-lord-curator.md)
- Lord Executor: Deployment manager (refer to agent-lord-executor.md)

USER INTERACTION:
User: "Build a RAG system"

AI (as King): "An interesting quest. This requires coordination across
multiple domains. Let me convene the necessary Lords..."

AI (as Lord Oracle): "I'll research current RAG best practices..."
AI (as Lord Architect): "Based on Oracle's findings, here's the design..."
AI (as Lord Forge Master): "I'll implement this architecture..."
AI (as Lord Sentinel): "Reviewing for security and quality..."
```

**Pros**:

- Simple to implement
- Single conversation thread
- Good for learning the pattern

**Cons**:

- Not truly parallel
- Single model's perspective
- Limited scalability

---

## Option 2: Multi-Agent Framework (Recommended)

**Best For**: Production systems, complex workflows, true parallelization

**Frameworks That Support This**:

- LangGraph (Python)
- AutoGen (Python)
- Semantic Kernel (C#/.NET)
- CrewAI (Python)
- Agent Protocol (Universal)

**Implementation Architecture**:

```python
# Pseudocode for multi-agent implementation

class KingPoncho(Agent):
    """Orchestrator agent"""
    system_prompt = load_prompt("agent-king-poncho.md")

    def delegate_quest(self, quest):
        # Classify quest type
        quest_type = self.classify(quest)

        # Determine required Lords
        required_lords = self.select_lords(quest_type)

        # Create execution plan
        plan = self.create_plan(quest, required_lords)

        # Execute plan (sequential or parallel)
        return self.execute_plan(plan)

class LordArchitect(Agent):
    """Design agent"""
    system_prompt = load_prompt("agent-lord-architect.md")
    tools = ["blueprint_gallery", "pattern_search"]

    def design_system(self, requirements):
        # Design logic
        return design_specification

class LordForge Master(Agent):
    """Implementation agent"""
    system_prompt = load_prompt("agent-lord-forge-master.md")
    tools = ["code_generation", "file_operations"]

    def implement(self, design_spec):
        # Build logic
        return implementation

# Orchestration
king = KingPoncho()
architect = LordArchitect()
forge_master = LordForgeMaster()
sentinel = LordSentinel()

# User quest
result = king.delegate_quest("Build a RAG system")
```

**Pros**:

- True parallelization
- Different models for different agents
- Production-grade scaling
- Independent agent states

**Cons**:

- More complex setup
- Framework dependencies
- Higher infrastructure cost

---

## Option 3: Human-in-the-Loop Orchestration

**Best For**: Learning, critical decisions, high-stakes projects

**How It Works**: Human plays King role, delegates to AI Lords

**Implementation**:

```
SETUP:
- Create 8 separate chat sessions (one per agent)
- Load each agent's system prompt into their session
- You (human) act as King Poncho

WORKFLOW:
1. You receive a quest
2. You decide which Lords to involve
3. You delegate to each Lord's chat session
4. Lords respond in their sessions
5. You synthesize and coordinate
6. You make final decisions

EXAMPLE:
Session 1 (You as King):
  "I need to build a RAG system. Let me consult my Lords."

Session 2 (Lord Oracle - Claude/GPT):
  You: "Lord Oracle, research current RAG best practices."
  Oracle: "I'll investigate... [research results]"

Session 3 (Lord Architect - Claude/GPT):
  You: "Lord Architect, here's Oracle's research. Design a system."
  Architect: "Examining... here's my proposed architecture..."

[Continue with other Lords as needed]
```

**Pros**:

- Complete control
- Deep learning of the system
- Best for complex decisions
- Mix different AI models

**Cons**:

- Manual coordination
- Time-intensive
- Not scalable
- Requires strong project management

---

## Option 4: Hybrid Approach (Most Flexible)

**Best For**: Real-world projects, iterative development

**How It Works**: Combine automated and manual orchestration

**Implementation**:

```
AUTOMATED (for routine tasks):
- Code reviews (Sentinel)
- Documentation (Scribe)
- Data transformation (Curator)
- Deployments (Executor)

MANUAL (for strategic decisions):
- Architecture decisions (King + Architect)
- Complex research (King + Oracle)
- Multi-phase planning (King + Full Council)

EXAMPLE WORKFLOW:
1. You (as King): Define quest and strategy
2. Automated: Oracle agent researches in background
3. You: Review Oracle's findings, decide on approach
4. Automated: Architect agent generates design
5. You: Approve design with modifications
6. Automated: Forge Master implements
7. Automated: Sentinel reviews
8. You: Final approval
9. Automated: Executor deploys
10. Automated: Scribe documents
```

**Pros**:

- Balance automation and control
- Pragmatic for real projects
- Scalable yet controllable
- Cost-effective

**Cons**:

- Requires judgment on what to automate
- Mix of manual and automated can be complex

---

## Platform-Specific Implementations

### Claude Projects (Sonnet/Opus)

```
PROJECT SETUP:
1. Create project: "Poncho's Kingdom"
2. Add all agent markdown files as project knowledge
3. Add Magic-Tower library files as context
4. Instructions: "You operate as King Poncho, coordinating Lords..."

USAGE:
User: "Build a RAG system"
Claude: [Automatically references agent docs and orchestrates]
```

**Advantages**:

- Deep context understanding
- Natural personality adoption
- Access to full agent specifications

### GPT Custom GPTs

```
CUSTOM GPT SETUP:
1. Create GPT: "King Poncho"
2. Instructions: Paste agent-king-poncho.md system prompt
3. Knowledge: Upload all Lord agent files
4. Conversation starters:
   - "I have a complex quest requiring multiple Lords"
   - "Convene the Round Table"
   - "I need strategic guidance"

CREATE ADDITIONAL GPTs (optional):
- "Lord Architect" GPT
- "Lord Forge Master" GPT
- etc.
```

### LangGraph Implementation

```python
from langgraph.graph import StateGraph, END

# Define agent nodes
def king_node(state):
    king = ChatOpenAI(model="gpt-4", system=king_prompt)
    return king.invoke(state["messages"])

def oracle_node(state):
    oracle = ChatOpenAI(model="gpt-4", system=oracle_prompt)
    return oracle.invoke(state["messages"])

def architect_node(state):
    architect = ChatOpenAI(model="gpt-4", system=architect_prompt)
    return architect.invoke(state["messages"])

# Build graph
workflow = StateGraph()
workflow.add_node("king", king_node)
workflow.add_node("oracle", oracle_node)
workflow.add_node("architect", architect_node)
workflow.add_node("forge_master", forge_master_node)
workflow.add_node("sentinel", sentinel_node)

# Define edges (workflow)
workflow.add_edge("king", "oracle")
workflow.add_edge("oracle", "architect")
workflow.add_edge("architect", "forge_master")
workflow.add_edge("forge_master", "sentinel")
workflow.add_edge("sentinel", END)

# Compile and run
app = workflow.compile()
result = app.invoke({"messages": [user_quest]})
```

### AutoGen Implementation

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create agents
king = AssistantAgent(
    "King_Poncho",
    system_message=load_file("agent-king-poncho.md"),
    llm_config={"model": "gpt-4"}
)

architect = AssistantAgent(
    "Lord_Architect",
    system_message=load_file("agent-lord-architect.md"),
    llm_config={"model": "gpt-4"}
)

forge_master = AssistantAgent(
    "Lord_Forge_Master",
    system_message=load_file("agent-lord-forge-master.md"),
    llm_config={"model": "gpt-4"}
)

# Create group chat
groupchat = GroupChat(
    agents=[king, architect, forge_master, sentinel],
    messages=[],
    max_round=20
)

manager = GroupChatManager(groupchat=groupchat)

# Start conversation
user_proxy = UserProxyAgent("User")
user_proxy.initiate_chat(manager, message="Build a RAG system")
```

---

## Cost Optimization Strategies

### Token Management

**Expensive (Full Context)**:

- Load entire agent specs (10K+ tokens each)
- Load full Magic-Tower library
- Keep all conversation history

**Optimized (Selective Context)**:

- Load only relevant agent personalities (2K tokens each)
- Reference library sections as needed
- Summarize older conversation turns
- Use cheaper models for routine tasks

### Model Selection by Lord

```
STRATEGIC (use best models):
- King Poncho: GPT-4 / Claude Opus / Gemini Ultra
- Lord Architect: GPT-4 / Claude Opus

TACTICAL (use mid-tier models):
- Lord Oracle: GPT-4 / Claude Sonnet
- Lord Sentinel: GPT-4 / Claude Sonnet

OPERATIONAL (use efficient models):
- Lord Forge Master: GPT-3.5 / Claude Sonnet
- Lord Scribe: GPT-3.5 / Claude Sonnet
- Lord Curator: GPT-3.5 / Claude Haiku
- Lord Executor: GPT-3.5 / Claude Haiku
```

### Parallel Execution

```
SEQUENTIAL (slower, cheaper per run):
Oracle → Architect → Forge → Sentinel → Scribe → Executor

PARALLEL (faster, higher cost):
[Oracle + Curator] → Architect → [Forge + Scribe] → [Sentinel + Executor]

SMART PARALLEL (optimal):
Oracle → [Architect + Curator] → Forge → [Sentinel + Scribe + Executor]
```

---

## Practical Tips

### Starting Simple

1. **Week 1**: Use single AI with role-switching (Option 1)
2. **Week 2**: Add human-in-the-loop for complex decisions (Option 3)
3. **Week 3**: Implement 2-3 key agents as separate sessions (Hybrid)
4. **Week 4**: Graduate to multi-agent framework if needed (Option 2)

### Common Pitfalls

❌ **Loading all agents for every task**
✅ **Select only needed Lords per quest**

❌ **Treating agents as rigid roles**
✅ **Let personalities inform, not constrain**

❌ **Skipping the King orchestration**
✅ **Always start with strategic planning**

❌ **Over-engineering simple tasks**
✅ **Use Quick Code Generation template for simple quests**

### Success Metrics

**How to know it's working:**

- Different agents provide distinct perspectives
- Tensions between agents surface real trade-offs
- Orchestration prevents chaos and redundancy
- Quality improves through multi-agent review
- Documentation happens naturally (Lord Scribe)
- Deployments are thoughtful (Lord Executor)

---

## Example: Real-World Usage

### Quest: Build Email Classification Agent

**Implementation**: Hybrid approach using Claude Projects

```
YOU (as King):
"I need to build an email classification agent for customer support."

CLAUDE (accessing agent docs):
"An interesting quest. This is a Creation Quest requiring design,
implementation, and validation. Let me approach this systematically.

[As Lord Oracle]
Let me research email classification approaches... [researches]

[As Lord Architect]
Based on research, I propose this architecture: [design]

[As Lord Forge Master]
I'll implement the classification pipeline: [code]

[As Lord Sentinel]
Reviewing for bias in classification and security... [analysis]

[As Lord Scribe]
Documenting the system: [documentation]

[Back as King]
The quest is complete. Here's the implemented agent, validated
for quality, with full documentation."
```

**Result**: Complete solution with multiple perspectives embedded

---

## Customization

### Adapting Personalities

You can modify agent personalities for your context:

```markdown
# Modified Lord Forge Master (More Cautious)

PERSONALITY:

- Craftsman-proud but risk-aware
- "Let me prototype first to validate the approach"
- Takes time to ensure quality
  [rest of modifications...]
```

### Adding Custom Lords

```markdown
# Lord Alchemist - Machine Learning Specialist

PERSONALITY:

- Experimental scientist, data-driven decision maker
- "Let's run experiments and measure..."

CORE EXPERTISE:

- Model training and fine-tuning
- Experiment design
- ML operations
  [continue with same structure as other Lords]
```

### Domain-Specific Adaptations

For your specific industry:

- Healthcare: Add HIPAA compliance to Lord Sentinel
- Finance: Add regulatory awareness to Lord Architect
- Gaming: Add performance optimization to Lord Executor

---

The key is starting simple and evolving your implementation as you understand the patterns. The Round Table thrives on clarity of roles and deliberate orchestration.
