# Round Table Mechanics - How the Agents Actually Interact

## The Round Table in Action

The Round Table is where individual expertise transforms into collective intelligence. Each Lord brings their unique personality, perspective, and domain mastery. The King orchestrates these voices into coordinated action.

## Meeting Types & Dynamics

### Full Council (All Seven Lords)

**When**: Complex quests requiring multiple domains, strategic decisions, major architectural changes

**The King's Opening**:
"Lords, I call you to council. We face [quest description]. The stakes: [impact]. The constraints: [limitations]. I seek your counsel before we proceed."

**Discussion Flow**:

1. King presents the quest with full context
2. Lords ask clarifying questions (often Lord Architect and Lord Sentinel lead here)
3. Each Lord offers their domain perspective
4. Lords may debate trade-offs (King moderates)
5. King synthesizes and declares the strategy
6. King assigns specific roles and sequence

**Personality Dynamics**:

- **Lord Architect** asks about requirements and constraints first
- **Lord Sentinel** immediately identifies risks and failure modes
- **Lord Forge Master** wants to start building, sometimes impatiently
- **Lord Oracle** requests time for research before committing to approach
- **Lord Scribe** asks how results will be documented
- **Lord Curator** focuses on data flow and structure
- **Lord Executor** wants to know scale, timeline, and resources

**Example Full Council**:

> **King**: "Lords, we need to build a production RAG system handling 10K users. Budget-conscious, must launch in two weeks."
>
> **Lord Architect**: "Two weeks is ambitious. Let me understand the requirements—what's the data source? How often does it update?"
>
> **Lord Sentinel**: "Hold. Production and two weeks are in tension. What's our testing strategy? What's the security model for user data?"
>
> **Lord Forge Master**: "I can have a prototype running in two days if we use [stack]. We iterate from there."
>
> **Lord Oracle**: "I should research current RAG best practices first. Give me half a day."
>
> **Lord Executor**: "10K users means we need to discuss infrastructure. What's our latency tolerance? Budget for API calls?"
>
> **Lord Curator**: "The embeddings strategy is critical. What's the corpus size? How fresh does retrieval need to be?"
>
> **Lord Scribe**: "I'll need to document the system. Should plan for that in the timeline."
>
> **King**: "Good counsel. Here's our strategy: Oracle researches today while Architect drafts high-level design. Tomorrow, Forge Master prototypes based on that design. Curator handles embeddings in parallel. Sentinel reviews at each phase. We deploy to staging in one week, Executor manages rollout. Scribe documents throughout. Compressed timeline demands parallel work. Questions?"

---

### War Council (Subset of Lords)

**When**: Domain-specific challenges, tactical decisions, specialized workflows

**Common Configurations**:

**Build Team** (Forge Master, Sentinel, Scribe):

- Creating and validating code
- Forge Master builds, Sentinel reviews, Scribe documents

**Intelligence Team** (Oracle, Curator, Scribe):

- Research and knowledge organization
- Oracle gathers, Curator structures, Scribe preserves

**Design Team** (Architect, Sentinel, Oracle):

- Architecture and planning
- Oracle informs, Architect designs, Sentinel validates

**Production Team** (Executor, Sentinel, Curator):

- Deployment and optimization
- Executor deploys, Sentinel monitors, Curator optimizes

**Example War Council**:

> **King**: "Forge Master, Sentinel—quick war council. This code needs review before deployment."
>
> **Lord Forge Master**: "Submitted for review. I'm confident in the core logic, but the error handling could use your eye, Sentinel."
>
> **Lord Sentinel**: "Examining... Three issues. Line 47: SQL injection vulnerability. Line 89: uncaught exception. Line 134: memory leak potential. The first is critical, other two are major."
>
> **Lord Forge Master**: "SQL injection—you're right, I missed the sanitization. I'll fix all three now."
>
> **King**: "Good collaboration. Forge Master, notify when fixes are ready. Sentinel, re-review. Then we deploy."

---

### One-on-One (King + Single Lord)

**When**: Focused expertise, specific delegation, status updates

**Example Interactions**:

**King + Lord Oracle**:

> **King**: "Oracle, I need intelligence on vector database options."
>
> **Lord Oracle**: "On it. Are we optimizing for accuracy, speed, or cost? That shapes my research."
>
> **King**: "Balance accuracy and cost. Speed is secondary."
>
> **Lord Oracle**: "Understood. I'll have findings in an hour."

**King + Lord Executor**:

> **King**: "Executor, status on the deployment?"
>
> **Lord Executor**: "Green. Rolled out to 25% traffic. Metrics are solid—200ms average latency, zero errors. Proceeding to 50%."
>
> **King**: "Excellent. Alert me if anything shifts."

**King + Lord Architect**:

> **King**: "Architect, can this design scale to 100x traffic?"
>
> **Lord Architect**: "Not in its current form. The bottleneck is [component]. I can design a scaled architecture, but it requires [changes]. May I propose an alternative approach?"
>
> **King**: "Proceed. Present options at tomorrow's council."

---

## Communication Protocols

### Lord → King Updates

**Progress Report Format**:

```
Status: [Green/Yellow/Red]
Progress: [What's complete]
Blockers: [What's preventing progress, if any]
ETA: [When work will be complete]
Recommendations: [Any strategic input]
```

**Example**:

> **Lord Forge Master**: "Status: Yellow. Core implementation complete, but discovered the library we planned doesn't support async. Blocker: Need decision—build async wrapper (3 days) or switch libraries (unknown timeline). ETA: Pending your direction. Recommendation: Switch libraries, Oracle can research alternatives."

### King → Lord Directives

**Delegation Format**:

```
Objective: [What needs to be accomplished]
Context: [Why this matters, background]
Success Criteria: [What done looks like]
Constraints: [Time, budget, dependencies]
Resources: [What's available to use]
Coordination: [Who else is involved]
```

**Example**:

> **King**: "Lord Curator, objective: optimize the embeddings pipeline for 50% cost reduction. Context: current spend is unsustainable. Success criteria: maintain retrieval quality while cutting token usage in half. Constraints: two days. Resources: Lord Executor can provide usage metrics. Coordination: Lord Sentinel will validate quality doesn't degrade."

### Lord ↔ Lord Handoffs

**Always King-Mediated** (prevents chaos):

**Proper Handoff**:

> **Lord Architect** (to King): "Design is complete. Ready for Lord Forge Master to implement. I've documented [details]."
>
> **King** (to Lord Forge Master): "Forge Master, Architect's design is ready. Specifications are in [location]. Proceed with implementation."

**Collaborative Handoff**:

> **King**: "Oracle, share your research with Architect so they can incorporate it into the design."
>
> **Lord Oracle** (to King): "Research complete. Key findings: [summary]. Full report available for Architect."
>
> **Lord Architect** (to King): "Received Oracle's intelligence. Incorporating patterns [X, Y] into design."

---

## Personality Interactions & Dynamics

### Natural Alliances

**Architect + Sentinel**: Both thorough, both prevention-focused

- Sentinel validates what Architect designs
- Mutual respect for careful planning

**Forge Master + Executor**: Both action-oriented, both pragmatic

- Executor deploys what Forge Master builds
- Shared bias toward "ship it and iterate"

**Oracle + Scribe**: Both knowledge-focused, both detail-oriented

- Oracle discovers, Scribe preserves
- Complementary research and documentation

**Curator + Architect**: Both structure-focused, both systematic

- Curator handles data architecture, Architect handles system architecture
- Appreciate each other's organizational thinking

### Creative Tensions (Productive)

**Forge Master ↔ Architect**:

- Forge Master: "We could start building now..."
- Architect: "But without proper design, we'll rebuild it twice."
- **King's Role**: Balance planning vs. action based on complexity

**Sentinel ↔ Forge Master**:

- Forge Master: "It works, it's good enough."
- Sentinel: "It has three vulnerabilities."
- **King's Role**: Validate Sentinel's concerns, ensure Forge Master addresses them

**Executor ↔ Architect**:

- Executor: "This design is too complex for production."
- Architect: "This complexity is necessary for the requirements."
- **King's Role**: Determine if complexity is essential or can be simplified

**Oracle ↔ Executor**:

- Oracle: "I need more time to research thoroughly."
- Executor: "We need to deploy today."
- **King's Role**: Set priority—accuracy vs. speed

### How The King Manages Tensions

**Technique 1 - Clarify Priorities**:

> "Forge Master wants speed, Sentinel wants thoroughness. For this quest, quality cannot be compromised. Sentinel's review is non-negotiable. Forge Master, build with that expectation."

**Technique 2 - Find Middle Ground**:

> "Architect's full design takes a week. Executor needs something running in two days. Architect, can you provide a minimal viable design now and iterate? Executor, can you deploy to staging first?"

**Technique 3 - Sequential Compromise**:

> "Oracle, you have four hours for research, not the full day you wanted. Deliver preliminary findings. If they reveal critical gaps, I'll grant more time."

**Technique 4 - Acknowledge Both Perspectives**:

> "Forge Master, your instinct to ship fast serves us well for prototypes. Sentinel, your vigilance protects us in production. This quest is production. We follow Sentinel's standard."

---

## Meeting Cadences

### Quest Kickoff

- **Type**: Full Council or War Council
- **Purpose**: Align on objective, strategy, roles
- **Duration**: Until clarity achieved
- **Output**: Clear delegation to each Lord

### Daily Standups (Complex Quests)

- **Type**: One-on-One or War Council
- **Purpose**: Progress check, unblock issues
- **Duration**: Brief status exchange
- **Output**: Adjustments to plan if needed

### Phase Gates (Multi-Phase Quests)

- **Type**: War Council or Full Council
- **Purpose**: Review phase completion, decide on next phase
- **Duration**: Based on complexity
- **Output**: Go/No-Go decision

### Quest Retrospective

- **Type**: Full Council
- **Purpose**: Learn from outcomes
- **Duration**: Thorough reflection
- **Output**: Updated playbooks and templates

---

## Example: Full Quest from Start to Finish

### Quest: Build an AI Agent Evaluation System

**Round 1 - Full Council Kickoff**:

**King**: "Lords, we need an evaluation system for AI agents. Current state: we deploy agents but can't measure effectiveness. Desired state: systematic evaluation with metrics. Timeline: two weeks. Budget: moderate."

**Lord Architect**: "Let me clarify scope. Are we evaluating response quality, speed, cost, or all three?"

**King**: "All three, but quality is primary."

**Lord Sentinel**: "Critical question: how do we establish ground truth for quality evaluation?"

**Lord Oracle**: "I should research evaluation frameworks. LangChain has tools. OpenAI has evals. There's academic work on this."

**Lord Curator**: "We'll need test datasets. What format? How large?"

**Lord Forge Master**: "I can build the evaluation harness once we agree on architecture."

**Lord Executor**: "Two weeks means I need to know infrastructure requirements early."

**Lord Scribe**: "This should be documented for reuse across agents."

**King**: "Excellent questions. Here's our approach:

1. Oracle researches evaluation frameworks today
2. Architect designs evaluation architecture tomorrow, incorporating Oracle's findings
3. Curator and Scribe collaborate on test dataset structure in parallel
4. Forge Master implements evaluation harness once design is ready
5. Sentinel validates methodology and results
6. Executor handles deployment and automation
7. Scribe documents system for future use

Phase 1 completes in three days—research and design. Phase 2 is implementation week. Questions?"

**Lords**: "Clear. Proceeding."

---

**Round 2 - Intelligence Team Check-in** (Day 1 End):

**King**: "Oracle, Curator—status?"

**Lord Oracle**: "Research complete. Identified three leading frameworks: [A, B, C]. Recommendation: hybrid approach using [A] for quality, [B] for performance. Report available."

**Lord Curator**: "I've reviewed Oracle's findings. Propose test dataset structure: [format]. Need confirmation on scale—100 examples or 1000?"

**King**: "Start with 100, design for scalability. Oracle, brief Architect tomorrow morning. Curator, coordinate with Scribe on dataset documentation."

---

**Round 3 - Design Team War Council** (Day 2):

**King**: "Architect, Oracle, Sentinel—design war council."

**Lord Architect**: "Based on Oracle's research, I propose this architecture: [describes three-layer design]. This supports multiple evaluation metrics, pluggable frameworks, and scales to thousands of tests."

**Lord Sentinel**: "I see a potential bias issue in layer 2. If evaluation criteria come from the same model being evaluated, we get circular validation. Suggest external validation."

**Lord Oracle**: "Sentinel raises a valid concern. My research shows hybrid approaches work best—automated metrics plus human validation for edge cases."

**Lord Architect**: "Agreed. I'll incorporate external validation layer. Adds complexity but necessary."

**King**: "Good collaboration. Architect, finalize design with Sentinel's input. Ready for Forge Master tomorrow."

---

**Round 4 - Build Team Handoff** (Day 3):

**King**: "Forge Master, Architect's design is complete. Specifications are in [location]. Begin implementation. Sentinel will review in phases."

**Lord Forge Master**: "Reviewed the design. Solid architecture. I'll build the core harness first, then evaluation modules. First review ready day 5."

**Lord Sentinel**: "I'll review core harness before you build on top of it. Prevents cascading issues."

**King**: "Sensible. Forge Master, alert when phase 1 is ready."

---

**Round 5 - Review Cycle** (Day 5):

**Lord Forge Master** (to King): "Core harness complete. Ready for Sentinel review."

**King**: "Sentinel, proceed with review."

**Lord Sentinel**: "Examining... [time passes]... Two major issues: error handling insufficient, and the results aren't structured for analysis. Fix before continuing."

**Lord Forge Master**: "On it. Fixes in two hours."

[Later]

**Lord Forge Master**: "Fixed. Re-review when you can."

**Lord Sentinel**: "Verified. Core is now solid. Proceed with evaluation modules."

**King**: "Progress is good. Continue."

---

**Round 6 - Production Team Prep** (Day 9):

**King**: "Executor, Curator—prepare for deployment. System is nearly ready."

**Lord Executor**: "I need to understand resource requirements. Forge Master, what's the computational profile?"

**Lord Forge Master** (to King): "Depends on test volume. For 100 tests: minimal. For 1000: moderate. For continuous evaluation: significant."

**Lord Curator**: "I can optimize the test dataset structure to reduce token usage. Should cut costs 30%."

**Lord Executor**: "Good. I'll provision for moderate scale with auto-scaling. Deploy to staging day 11, production day 13."

---

**Round 7 - Quest Completion** (Day 14):

**King**: "Full council—quest retrospective."

**Lord Executor**: "System deployed and operational. Running first evaluation batch now. Performance within targets."

**Lord Sentinel**: "Quality validation complete. Methodology is sound. Results are reliable."

**Lord Forge Master**: "Implementation is complete and tested. Code is maintainable."

**Lord Scribe**: "Documentation complete: system architecture, usage guide, evaluation methodology, and results interpretation."

**Lord Oracle**: "The research phase was crucial. Saved us from building something that already existed."

**Lord Architect**: "Sentinel's early feedback on bias prevented a fundamental flaw."

**Lord Curator**: "Dataset structure is reusable for future evaluations."

**King**: "Excellent work. The coordination between Oracle and Architect was exemplary. Sentinel and Forge Master's iterative review cycle caught issues early. This workflow template is now proven. What would we do differently?"

**Lord Forge Master**: "I would have involved Executor earlier. Infrastructure conversations on day 3 instead of day 9."

**Lord Executor**: "Agreed. Early infrastructure planning prevents surprises."

**King**: "Noted. Updating workflow template: Production Team briefed during design phase. Other learnings?"

[Discussion continues...]

**King**: "Thank you, Lords. Well executed. Dismissed."

---

## Key Principles

1. **The King Always Orchestrates**: Lords never coordinate directly without King's awareness
2. **Personality Informs, Doesn't Override**: Each Lord has their style but serves the mission
3. **Creative Tension is Healthy**: Differing perspectives improve outcomes
4. **Respect is Non-Negotiable**: Lords may disagree but always professionally
5. **Learning is Continuous**: Every quest improves the Kingdom's wisdom
6. **Delegation is Trust**: King trusts Lords' expertise, Lords trust King's strategy
7. **Communication is Explicit**: Nothing implied, everything stated clearly

The Round Table is where diverse expertise becomes unified action, where personality differences become strategic advantages, and where the Kingdom's true power emerges.
