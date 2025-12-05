# Round Table Quick Reference

Fast lookup for common quest types and which Lords to involve.

## Quest Type → Lord Configuration

### 🔍 Research & Analysis

**Simple Research**: Oracle
**Deep Research**: Oracle → Scribe
**Competitive Analysis**: Oracle + Curator → Scribe
**Research Report**: Oracle → Curator → Sentinel → Scribe

**Why**: Oracle gathers, Curator structures, Sentinel validates, Scribe documents

---

### 🏗️ System Design

**Architecture Planning**: Architect
**Architecture + Validation**: Architect → Sentinel
**Full Design Cycle**: Oracle → Architect → Sentinel → Scribe

**Why**: Oracle provides patterns, Architect designs, Sentinel validates, Scribe documents

---

### ⚙️ Code Implementation

**Quick Script**: Forge Master
**Reviewed Code**: Forge Master → Sentinel
**Production Code**: Architect → Forge Master → Sentinel → Scribe
**Complex Feature**: Oracle → Architect → Forge Master → Sentinel → Scribe → Executor

**Why**: More Lords = more quality gates for higher-stakes code

---

### 🛡️ Security & Quality

**Code Review**: Sentinel
**Security Audit**: Sentinel + Architect
**Full Quality Assessment**: Sentinel → Forge Master (fixes) → Sentinel (re-review)

**Why**: Sentinel identifies issues, Forge Master fixes, iterative cycle

---

### 📚 Documentation

**Quick Docs**: Scribe
**Technical Docs**: Forge Master (explains) → Scribe (documents)
**Comprehensive Docs**: Oracle (research) → Architect (structure) → Scribe (write)

**Why**: Scribe always writes, but others provide domain expertise

---

### 🗄️ Data Management

**Data Transformation**: Curator
**Data + Quality**: Curator → Sentinel
**Full Pipeline**: Oracle (gather) → Curator (structure) → Sentinel (validate) → Scribe (document)

**Why**: Curator specializes in data structure and optimization

---

### 🚀 Deployment

**Simple Deploy**: Executor
**Validated Deploy**: Sentinel → Executor
**Production Deploy**: Forge Master → Sentinel → Executor → Scribe (ops docs)

**Why**: Executor handles deployment, but validation before is critical

---

### 🔄 Optimization

**Performance Optimization**: Executor → Curator
**Code Refactoring**: Sentinel (identify) → Forge Master (refactor) → Sentinel (verify)
**Cost Optimization**: Executor (metrics) → Curator (data efficiency) → Architect (redesign if needed)

**Why**: Optimization requires measurement, implementation, and validation

---

### 🧪 Experiments

**Quick Test**: Forge Master
**Validated Experiment**: Architect → Forge Master → Sentinel
**Research Experiment**: Oracle → Architect → Forge Master → Sentinel → Scribe

**Why**: Experiments need design before implementation to be meaningful

---

## Personality-Based Selection Guide

### When You Need...

**Deep Thinking**: Architect, Oracle
**Fast Action**: Forge Master, Executor
**Risk Mitigation**: Sentinel, Architect
**Organization**: Curator, Scribe
**Balance**: King (orchestrates all)

### When You're Dealing With...

**Ambiguity**: King + Architect (clarify before proceeding)
**Urgency**: Forge Master + Executor (action-oriented)
**Complexity**: Full Council (all perspectives)
**Risk**: Sentinel + Architect (thorough validation)
**Scale**: Executor + Curator (operations expertise)

---

## Common Workflows

### The "Build Something" Workflow

```
Standard Path:
Architect (design) → Forge Master (build) → Sentinel (review) → Executor (deploy)

With Research:
Oracle → Architect → Forge Master → Sentinel → Executor

With Full Documentation:
Oracle → Architect → Forge Master → Sentinel → Scribe → Executor
```

### The "Fix Something" Workflow

```
Identify:
Sentinel (find issues) or Executor (surface metrics)

Fix:
Forge Master (implement) → Sentinel (verify)

Document:
Scribe (update docs)
```

### The "Learn Something" Workflow

```
Research:
Oracle (gather intelligence)

Organize:
Curator (structure) or Scribe (document)

Validate:
Sentinel (fact-check)

Preserve:
Scribe (add to Library)
```

### The "Optimize Something" Workflow

```
Measure:
Executor (current state)

Analyze:
Sentinel (identify bottlenecks) + Curator (data efficiency)

Redesign (if needed):
Architect (propose changes)

Implement:
Forge Master (execute) → Sentinel (validate)

Deploy:
Executor (rollout) → Monitor
```

---

## Cost-Conscious Configurations

### Minimal (Fast & Cheap)

**One Lord**: For simple, clear tasks

- Quick code: Forge Master
- Simple research: Oracle
- Basic docs: Scribe

### Standard (Balanced)

**Two-Three Lords**: For typical work

- Code with review: Forge Master → Sentinel
- Research + docs: Oracle → Scribe
- Design + build: Architect → Forge Master

### Premium (Thorough)

**Four+ Lords**: For critical work

- Production feature: Oracle → Architect → Forge Master → Sentinel → Executor
- Major architecture: Full Council

### When to Go Full Council

✅ **Use Full Council When**:

- Stakes are high (production, security, major investment)
- Requirements are unclear
- Multiple domains affected
- Strategic decision needed

❌ **Skip Full Council When**:

- Task is routine
- Requirements are crystal clear
- Single domain expertise sufficient
- Time/cost constraints tight

---

## Lord Pairing Guide

### Natural Synergies

**Architect + Sentinel**: Thorough planning + validation
**Oracle + Scribe**: Research + preservation
**Forge Master + Executor**: Build + deploy
**Curator + Architect**: Data structure + system structure

### Creative Tensions (Good!)

**Forge Master ↔ Architect**: Speed vs. thoroughness
**Sentinel ↔ Forge Master**: Quality vs. shipping
**Oracle ↔ Executor**: Research time vs. action urgency

_King manages these tensions to find optimal balance_

### Complementary Pairs

**Oracle + Architect**: Research informs design
**Architect + Forge Master**: Design → implementation handoff
**Forge Master + Sentinel**: Build → review cycle
**Sentinel + Executor**: Quality → deployment gate
**Curator + Scribe**: Structure → documentation
**Executor + Curator**: Operations → optimization

---

## Decision Trees

### "Should I involve multiple Lords?"

```
Is task complex? → YES → Multiple Lords
  ↓ NO
Is quality critical? → YES → Multiple Lords
  ↓ NO
Is this new territory? → YES → Multiple Lords (start with Oracle)
  ↓ NO
Single Lord sufficient
```

### "Which Lord should lead?"

```
What's the primary need?

Understanding → Oracle
Planning → Architect
Building → Forge Master
Validation → Sentinel
Organization → Scribe or Curator
Execution → Executor
Strategy → King
```

### "Sequential or Parallel?"

```
Do tasks depend on each other? → YES → Sequential
  ↓ NO
Do tasks share resources? → YES → Sequential or careful parallel
  ↓ NO
Can tasks run independently? → YES → Parallel
```

---

## Emergency Situations

### Production Down

**Immediate**: Executor (assess + mitigate)
**Investigation**: Sentinel (find root cause)
**Fix**: Forge Master (implement)
**Validation**: Sentinel (verify fix)
**Postmortem**: Full Council

### Security Breach

**Immediate**: Sentinel (assess damage) + Executor (contain)
**Fix**: Forge Master (patch)
**Audit**: Sentinel (full review)
**Documentation**: Scribe (incident report)
**Prevention**: Architect (redesign if needed)

### Major Bug Found

**Severity High**: Sentinel → Forge Master → Sentinel → Executor
**Severity Low**: Create backlog item for Forge Master

### Unclear Requirements

**Stop**: Convene King + Architect
**Clarify**: Before proceeding
**Then**: Continue with appropriate Lords

---

## Templates by Industry

### Web Development

**New Feature**: Architect → Forge Master → Sentinel → Executor
**Bug Fix**: Sentinel → Forge Master → Sentinel
**Performance Issue**: Executor → Curator → Forge Master

### Data Science

**New Model**: Oracle (research) → Architect (design) → Forge Master (implement) → Sentinel (validate)
**Data Pipeline**: Curator → Sentinel → Executor
**Analysis**: Oracle → Curator → Scribe

### AI/ML Systems

**Agent Development**: Oracle → Architect → Forge Master → Sentinel → Executor
**Evaluation**: Sentinel → Scribe
**Optimization**: Executor → Curator → Forge Master

---

## Quick Cheat Sheet

| Quest Type        | Minimum Lords     | Recommended Lords                  | Optional Add    |
| ----------------- | ----------------- | ---------------------------------- | --------------- |
| Quick Code        | Forge Master      | Forge + Sentinel                   | Scribe          |
| Research          | Oracle            | Oracle + Scribe                    | Sentinel        |
| Design            | Architect         | Arch + Sentinel                    | Oracle          |
| Production Deploy | Executor          | Forge + Sentinel + Executor        | Scribe          |
| Data Pipeline     | Curator           | Curator + Sentinel                 | Scribe          |
| Full Feature      | Forge + Sentinel  | Arch + Forge + Sentinel + Executor | Oracle + Scribe |
| Emergency         | Context-dependent | Executor + Sentinel                | Full Council    |

---

## Red Flags

### Don't Do This:

❌ Skip Sentinel for production code
❌ Deploy without Executor's readiness check
❌ Start building before Architect designs (for complex systems)
❌ Document without Scribe's structure
❌ Optimize without Executor's metrics

### Do This Instead:

✅ Always involve Sentinel for production
✅ Executor validates deployment readiness
✅ Complex systems get Architect review first
✅ Scribe handles documentation structure
✅ Executor provides data for optimization decisions

---

## When In Doubt

1. **Start with King**: Strategic clarity before tactical execution
2. **Err on thoroughness**: Adding Lords costs tokens, but fixing mistakes costs more
3. **Use templates**: Proven patterns in workflow-templates.md
4. **Ask**: "What could go wrong?" → Probably need Sentinel
5. **Ask**: "Will this scale?" → Probably need Architect + Executor
6. **Ask**: "Is this clear?" → Probably need Architect or King

The Round Table's power is in **intentional coordination**, not random involvement. Choose Lords deliberately based on the quest's true needs.
