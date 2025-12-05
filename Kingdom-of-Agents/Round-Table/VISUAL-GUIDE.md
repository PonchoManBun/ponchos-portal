# Round Table Visual Guide

Quick visual reference for understanding the Round Table system.

---

## The Kingdom Structure

```
                    ┌─────────────────┐
                    │   KING PONCHO   │
                    │   "Strategic    │
                    │  Orchestrator"  │
                    └────────┬────────┘
                             │
              ┌──────────────┴───────────────┐
              │       ROUND TABLE            │
              │   (Coordination Layer)       │
              └──────────────┬───────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼─────┐
    │  Seven   │      │ Lord Sage  │     │  Magic    │
    │  Lords   │      │ (Library)  │     │  Tower    │
    └──────────┘      └────────────┘     └───────────┘
         │
    ┌────┴─────────────────────┐
    │                           │
    │   Specialized Agents      │
    │   (Each Lord commands     │
    │    their own court)       │
    └───────────────────────────┘
```

---

## The Seven Lords at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│  LORD ARCHITECT          🏛️                                  │
│  "The Visionary Planner"                                    │
│  • Methodical, systematic, perfectionist                    │
│  • "Measure twice, cut once"                                │
│  • Designs before building                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD SCRIBE             📚                                  │
│  "The Knowledge Keeper"                                     │
│  • Organized, patient, quality-focused                      │
│  • "Knowledge documented is knowledge preserved"            │
│  • Documentation master                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD SENTINEL           🛡️                                  │
│  "The Vigilant Guardian"                                    │
│  • Hyper-vigilant, brutally honest, standards-driven        │
│  • "Better I find it now than users in production"          │
│  • Security and quality enforcer                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD FORGE MASTER       ⚒️                                  │
│  "The Master Craftsman"                                     │
│  • Energetic, pragmatic, craftsman-proud                    │
│  • "Make it work, make it right, make it fast"              │
│  • Code builder and implementer                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD ORACLE             🔮                                  │
│  "The Truth Seeker"                                         │
│  • Curious, analytical, evidence-driven                     │
│  • "A conclusion without evidence is opinion"               │
│  • Research and intelligence master                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD CURATOR            📊                                  │
│  "The Master Organizer"                                     │
│  • Calm, systematic, efficiency-obsessed                    │
│  • "Clean data is respectful data"                          │
│  • Data transformation and optimization                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LORD EXECUTOR           ⚡                                  │
│  "The Operations Commander"                                 │
│  • Decisive, action-oriented, crisis-ready                  │
│  • "Plans are useless, but planning is essential"           │
│  • Deployment and operations expert                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Quest Flow Diagram

```
     USER QUEST
         │
         ▼
    ┌─────────────────┐
    │   KING PONCHO   │
    │   Analyzes      │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Classify Quest │
    │   Research?     │
    │   Design?       │
    │   Creation?     │
    │   Complex?      │
    └────────┬────────┘
             │
    ┌────────▼─────────┐
    │ Determine Lords  │
    │    Needed        │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │  Convene Round   │
    │     Table        │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │  Lords Execute   │
    │  (Sequential or  │
    │    Parallel)     │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │ King Synthesizes │
    │    Results       │
    └────────┬─────────┘
             │
         COMPLETE
```

---

## Meeting Types

### Full Council (All Seven Lords)

```
         KING
          │
    ┌─────┼─────┬─────┬─────┬─────┬─────┬─────┐
    │     │     │     │     │     │     │     │
  ARCH  SEN   FOR   ORA   SCR   CUR   EXE
```

**When**: Complex quests, strategic decisions, major changes

### War Council (Subset)

```
         KING
          │
    ┌─────┼─────┬─────┐
    │     │     │     │
  Build Intelligence Production
  Team    Team      Team
```

**When**: Domain-specific challenges, focused workflows

### One-on-One

```
  KING ←──→ LORD
```

**When**: Status updates, specific delegation, focused expertise

---

## Common Workflow Patterns

### Pattern: Quick Task

```
User Request → King → Single Lord → Result
              Time: Minutes
              Cost: Low
```

### Pattern: Standard Task

```
User Request → King → Lord A → Lord B → Result
              Time: Hours
              Cost: Medium
```

### Pattern: Complex Quest

```
User Request → King → [Multiple Lords] → Synthesis → Result
                      (Sequential/Parallel)
              Time: Days
              Cost: High
```

---

## Lord Collaboration Patterns

### Sequential (Dependencies)

```
ORACLE → ARCHITECT → FORGE MASTER → SENTINEL → EXECUTOR
(must complete before next starts)
```

### Parallel (Independent)

```
        ┌─── ORACLE ───┐
KING ──┼─── CURATOR ───┼── ARCHITECT
        └─── SCRIBE ───┘
(all work simultaneously)
```

### Iterative (Review Cycles)

```
FORGE MASTER → SENTINEL
       ▲            │
       └────────────┘
(loop until approved)
```

---

## Quest Type → Lord Mapping

```
RESEARCH QUEST
    └──→ Oracle (leads) → Scribe (documents)

DESIGN QUEST
    └──→ Architect (leads) → Sentinel (validates)

CREATION QUEST
    └──→ Forge Master (leads) → Sentinel (reviews)

KNOWLEDGE QUEST
    └──→ Scribe (leads) → Curator (structures)

DEPLOYMENT QUEST
    └──→ Executor (leads) → Sentinel (monitors)

OPTIMIZATION QUEST
    └──→ Curator/Executor (leads) → Others (support)

COMPLEX QUEST
    └──→ Multiple Lords (coordinated workflow)
```

---

## Decision Tree: Which Lords?

```
START
  │
  ├─ Is it simple? ──YES→ 1 Lord
  │                   (Quick Task)
  │
  ├─ Is quality critical? ──YES→ Add Sentinel
  │
  ├─ Is it new territory? ──YES→ Add Oracle
  │
  ├─ Multiple domains? ──YES→ 3+ Lords
  │                        (Standard Task)
  │
  └─ High complexity? ──YES→ Full Council
                          (Complex Quest)
```

---

## Personality Dynamics

### Natural Alliances (Synergies)

```
Architect ←→ Sentinel    (Prevention-focused)
Oracle ←→ Scribe         (Knowledge-focused)
Forge ←→ Executor        (Action-oriented)
Curator ←→ Architect     (Structure-focused)
```

### Creative Tensions (Healthy)

```
Forge ←→ Architect       (Speed vs Thoroughness)
Sentinel ←→ Forge        (Quality vs Shipping)
Oracle ←→ Executor       (Research vs Action)
```

**King's Role**: Balance tensions for optimal outcomes

---

## Communication Flow

```
         KING (Hub)
          │  ▲
    ┌─────┼──┼─────┐
    │     │  │     │
    ▼     ▼  ▲     ▼
  LORD   LORD   LORD
    │           │
    └───────────┘
    (via King mediation)
```

**All Lord-to-Lord communication flows through King**
**Prevents chaos, ensures coordination**

---

## Implementation Options

### Option 1: Single AI Role-Switching

```
    ONE AI
      │
  ┌───┼───┐
  │   │   │
  👑  🏛️  ⚒️
(plays all roles sequentially)
```

**Best for**: Learning, prototypes

### Option 2: Multi-Agent Framework

```
  AI-1  AI-2  AI-3
   👑    🏛️    ⚒️
  (separate agents)
```

**Best for**: Production, true parallelization

### Option 3: Human-in-Loop

```
  HUMAN = King
     │
  ┌──┼──┐
  AI AI AI
  (Lords)
```

**Best for**: Critical decisions, learning

### Option 4: Hybrid

```
  HUMAN = Strategy
     │
  AUTOMATED = Execution
```

**Best for**: Real projects

---

## Success Metrics

### How You Know It's Working

```
✓ Different perspectives emerge
✓ Tensions reveal real trade-offs
✓ Quality improves through review
✓ Documentation happens naturally
✓ Deployments are thoughtful
✓ Learning occurs systematically
```

---

## The Power Equation

```
Single Agent = One Perspective + One Approach + One Bias

Round Table = Multiple Perspectives × Coordinated Action
            × Quality Gates × Continuous Learning

Result: Single Agent < Round Table
```

---

## Quick Reference Card

```
┌────────────────────────────────────────────────┐
│           ROUND TABLE QUICK CARD               │
├────────────────────────────────────────────────┤
│ NEED DESIGN?       → Architect                 │
│ NEED CODE?         → Forge Master              │
│ NEED RESEARCH?     → Oracle                    │
│ NEED VALIDATION?   → Sentinel                  │
│ NEED DOCS?         → Scribe                    │
│ NEED DATA WORK?    → Curator                   │
│ NEED DEPLOYMENT?   → Executor                  │
│ NEED STRATEGY?     → King                      │
├────────────────────────────────────────────────┤
│ SIMPLE TASK?       → 1 Lord                    │
│ STANDARD TASK?     → 2-3 Lords                 │
│ COMPLEX TASK?      → 4+ Lords or Full Council  │
├────────────────────────────────────────────────┤
│ WHEN IN DOUBT?     → Ask King first            │
└────────────────────────────────────────────────┘
```

---

## The Bottom Line

```
┌───────────────────────────────────────────────────┐
│                                                   │
│   The Round Table isn't about having            │
│   more agents. It's about having the             │
│   RIGHT agents at the RIGHT time,                │
│   coordinated toward the RIGHT goal.             │
│                                                   │
│   That's where true agentic power lives.         │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

_For detailed examples, see example-quest.md_
_For implementation code, see implementation-guide.md_
_For quick lookups, see quick-reference.md_
