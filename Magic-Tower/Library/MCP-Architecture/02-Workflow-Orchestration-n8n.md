# Quest 001 Week 3-4: n8n Workflow Orchestration Patterns

**Study Focus**: Sequential & Parallel Agent Coordination  
**Repository**: https://github.com/n8n-io/n8n (295MB, 13,363 files)  
**Date**: December 5, 2025

---

## 🎯 Study Goals

Extract patterns from n8n to design **Round Table workflow orchestration**:

1. **Sequential Lord Chains**: Architect → Forge Master → Sentinel
2. **Parallel Lord Execution**: Multiple Lords working simultaneously
3. **State Management**: Preserving context between Lord invocations
4. **Error Handling**: Retry logic, failure recovery, partial execution

---

## 📂 Key Architecture Components

### Core Packages

```
packages/
├── workflow/           # Core workflow logic & DAG processing
├── core/              # Execution engine & node execution
├── cli/               # CLI & server orchestration
└── nodes-base/        # Built-in node implementations
```

### Execution Engine Location

**Main Files**:
- `packages/core/src/execution-engine/workflow-execute.ts` (2,615 LOC)
- `packages/workflow/src/workflow.ts` (929 LOC)
- `packages/core/src/execution-engine/partial-execution-utils/` (DAG utilities)

---

## 🔄 Execution Model

### 1. Workflow Representation

**Workflow Class** (`packages/workflow/src/workflow.ts`):

```typescript
export class Workflow {
  id: string;
  name: string | undefined;
  nodes: INodes = {};
  connectionsBySourceNode: IConnections = {};
  connectionsByDestinationNode: IConnections = {};
  nodeTypes: INodeTypes;
  expression: Expression;
  active: boolean;
  settings: IWorkflowSettings = {};
  staticData: IDataObject;
  pinData?: IPinData;
  
  constructor(parameters: WorkflowParameters) {
    // Initialize nodes, connections, settings
    this.setNodes(parameters.nodes);
    this.setConnections(parameters.connections);
    this.setPinData(parameters.pinData);
  }
}
```

**Key Insight**: n8n represents workflows as a **graph of connected nodes**, stored in two directions:
- `connectionsBySourceNode`: Forward edges (A → B)
- `connectionsByDestinationNode`: Backward edges (B ← A)

### 2. Node Execution Stack

**Stack-Based Execution** (`workflow-execute.ts` lines 1400-1700):

```typescript
executionLoop: while (
  this.runExecutionData.executionData!.nodeExecutionStack.length !== 0
) {
  // Pop next node to execute
  executionData = this.runExecutionData.executionData!.nodeExecutionStack.shift();
  executionNode = executionData.node;
  
  // Execute node
  let runNodeData = await this.runNode(
    workflow,
    executionData,
    this.runExecutionData,
    runIndex,
    this.additionalData,
    this.mode,
    this.abortController.signal,
    subNodeExecutionResults,
  );
  
  // Process results and add downstream nodes to stack
  this.addNodeToBeExecuted(workflow, connectionData, ...);
}
```

**Key Insight**: n8n uses a **node execution stack** (FIFO queue) to manage execution order:
1. Pop node from stack
2. Execute node
3. Push downstream nodes to stack (if their inputs are ready)
4. Repeat until stack is empty

### 3. Multi-Input Node Handling (Critical Pattern!)

**Waiting Execution Pattern** (`workflow-execute.ts` lines 400-600):

```typescript
const numberOfInputs = workflow.connectionsByDestinationNode[node]?.main?.length ?? 0;

if (numberOfInputs > 1) {
  // Node has multiple inputs - use waiting queue
  if (!this.runExecutionData.executionData!.waitingExecution[node]) {
    this.runExecutionData.executionData!.waitingExecution[node] = {};
  }
  
  // Add incoming data to waiting queue
  this.runExecutionData.executionData!.waitingExecution[node][waitingIndex]
    .main[connectionIndex] = nodeSuccessData[outputIndex];
  
  // Check if all inputs are ready
  let allDataFound = true;
  for (let i = 0; i < inputs.length; i++) {
    if (waitingExecution[node][waitingIndex].main[i] === null) {
      allDataFound = false;
      break;
    }
  }
  
  if (allDataFound) {
    // All inputs ready - add to execution stack
    this.runExecutionData.executionData!.nodeExecutionStack.push({
      node: workflow.nodes[node],
      data: waitingExecution[node][waitingIndex],
      source: waitingExecutionSource[node][waitingIndex],
    });
    
    // Remove from waiting queue
    delete waitingExecution[node][waitingIndex];
  }
}
```

**Key Insight**: For nodes with **multiple inputs** (e.g., merge operations):
- Don't execute until **ALL** inputs have data
- Store partial data in `waitingExecution` queue
- Only push to execution stack when all inputs ready
- This enables **parallel execution** with synchronization

---

## 🗂️ State Management

### Run Execution Data Structure

```typescript
interface IRunExecutionData {
  startData?: {
    destinationNode?: IDestinationNode;
    runNodeFilter?: string[];
  };
  
  resultData: {
    runData: IRunData;           // Historical data for each node
    lastNodeExecuted: string;
    error?: ExecutionBaseError;
    pinData?: IPinData;          // Pre-set output data
  };
  
  executionData?: {
    nodeExecutionStack: IExecuteData[];     // Nodes to execute
    waitingExecution: IWaitingForExecution; // Multi-input sync
    waitingExecutionSource: IWaitingForExecutionSource;
  };
}
```

### Data Flow Between Nodes

**Task Data Structure**:

```typescript
interface ITaskData {
  startTime: number;
  executionTime: number;
  executionStatus: ExecutionStatus;
  executionIndex: number;
  source: ITaskDataConnections | null;
  data?: ITaskDataConnections;  // Output data
  error?: ExecutionBaseError;
  metadata?: ITaskMetadata;
  hints?: NodeExecutionHint[];
}

interface ITaskDataConnections {
  main?: INodeExecutionData[][] | null;
  // Other connection types...
}
```

**Key Insight**: Each node execution stores:
- **Input** (`source`): Where data came from
- **Output** (`data`): Results to pass downstream
- **Metadata**: Execution time, status, errors
- All stored in `runData[nodeName][runIndex]`

### Partial Execution & Run Data

**Reusing Previous Results** (`workflow-execute.ts` lines 175-280):

```typescript
runPartialWorkflow2(
  workflow: Workflow,
  runData: IRunData,              // Previous execution results
  pinData: IPinData = {},
  dirtyNodeNames: string[] = [],  // Nodes to re-execute
  destinationNode: IDestinationNode,
) {
  // 1. Find the Trigger
  let trigger = findTriggerForPartialExecution(workflow, destinationNode, runData);
  
  // 2. Find the Subgraph (trigger → destination)
  graph = findSubgraph({ graph, destination, trigger });
  
  // 3. Find Start Nodes (nodes without cached data)
  let startNodes = findStartNodes({ graph, trigger, destination, runData, pinData });
  
  // 4-5. Detect & Handle Cycles
  startNodes = handleCycles(graph, startNodes, trigger);
  
  // 6. Clean Run Data (remove invalid cached data)
  runData = cleanRunData(runData, graph, startNodes);
  
  // 7. Recreate Execution Stack (from cached + start nodes)
  const { nodeExecutionStack, waitingExecution, waitingExecutionSource } =
    recreateNodeExecutionStack(graph, startNodes, runData, pinData);
    
  // 8. Execute
  return this.processRunExecutionData(workflow);
}
```

**Key Insight**: n8n supports **partial re-execution**:
- Reuse cached results from `runData`
- Only re-execute "dirty" nodes (and downstream dependents)
- Critical for **iterative development** & **debugging**

---

## ⚠️ Error Handling & Retries

### Retry Mechanism

**Node-Level Retries** (`workflow-execute.ts` lines 1630-1680):

```typescript
let maxTries = 1;
if (executionData.node.retryOnFail === true) {
  maxTries = Math.min(5, Math.max(2, executionData.node.maxTries || 3));
}

let waitBetweenTries = 0;
if (executionData.node.retryOnFail === true) {
  waitBetweenTries = Math.min(5000, Math.max(0, executionData.node.waitBetweenTries || 1000));
}

for (let tryIndex = 0; tryIndex < maxTries; tryIndex++) {
  try {
    if (tryIndex !== 0 && waitBetweenTries !== 0) {
      await new Promise((resolve) => {
        setTimeout(resolve, waitBetweenTries);
      });
    }
    
    runNodeData = await this.runNode(...);
    
    // Check if node failed
    let nodeFailed = runNodeData.data?.[0]?.[0]?.json?.error !== undefined;
    
    if (!nodeFailed || tryIndex === maxTries - 1) {
      break; // Success or final attempt
    }
  } catch (error) {
    if (tryIndex === maxTries - 1) {
      throw error; // Final attempt failed
    }
  }
}
```

**Key Insight**: Each node can have **retry configuration**:
- `maxTries`: 1-5 attempts (default: 3)
- `waitBetweenTries`: 0-5000ms delay (default: 1000ms)
- Exponential backoff possible

### Error Propagation Modes

**Continue on Fail** (`workflow-execute.ts` lines 1850-1870):

```typescript
if (executionError !== undefined) {
  taskData.error = executionError;
  taskData.executionStatus = 'error';
  
  if (executionData.node.continueOnFail === true ||
      ['continueRegularOutput', 'continueErrorOutput'].includes(executionData.node.onError)) {
    // Workflow continues - pass input data through
    if (executionData.data.main.length > 0 && executionData.data.main[0] !== null) {
      nodeSuccessData = [executionData.data.main[0]];
    }
  } else {
    // Stop execution - re-add node to stack for restart
    this.runExecutionData.executionData!.nodeExecutionStack.unshift(executionData);
    break; // Exit execution loop
  }
}
```

**Error Modes**:
1. **Stop on Error** (default): Halt execution, save error state
2. **Continue on Fail**: Pass input data through, continue workflow
3. **Continue Regular Output**: Execute downstream with original output
4. **Continue Error Output**: Pass error as data to special error branch

**Key Insight**: n8n allows **error branching** - workflows can handle errors gracefully and continue with fallback logic.

---

## 🔀 Parallel Execution Patterns

### Detection of Parallel Branches

**Multiple Output Connections** (`workflow-execute.ts` lines 2000-2100):

```typescript
// After node execution, find downstream nodes
if (workflow.connectionsBySourceNode[executionNode.name]?.main) {
  for (outputIndex in workflow.connectionsBySourceNode[executionNode.name].main) {
    for (connectionData of workflow.connectionsBySourceNode[executionNode.name].main[outputIndex]) {
      
      if (nodeSuccessData[outputIndex] && nodeSuccessData[outputIndex].length !== 0) {
        // Add downstream node to execution stack
        this.addNodeToBeExecuted(
          workflow,
          connectionData,
          runIndex,
          outputIndex,
          executionNode.name,
          nodeSuccessData,
        );
      }
    }
  }
}
```

**Key Insight**: Parallel branches happen when:
- A node has **multiple output connections** on the same output port
- All downstream nodes get added to stack **simultaneously**
- Execution is **breadth-first** by default (unless execution order changed)

### Synchronization at Merge Points

Using the **Waiting Execution** pattern described earlier:
- Merge nodes (multiple inputs) wait for ALL parent branches
- Prevents race conditions
- Ensures deterministic execution

---

## 🎭 Round Table Application

### Pattern Mapping

| n8n Concept | Round Table Equivalent |
|-------------|------------------------|
| **Workflow** | Quest with multi-Lord coordination |
| **Node** | Individual Lord invocation |
| **Node Execution Stack** | Quest execution queue |
| **Waiting Execution** | Lord synchronization for multi-input Quests |
| **Run Data** | Historical Lord responses for caching |
| **Partial Execution** | Re-running failed/modified Lord steps |
| **Error Modes** | Quest failure strategies |

### Proposed Architecture

#### 1. Sequential Lord Chain

**Quest Flow**: `design_microservice`

```
Client
  ↓
King Gateway
  ↓
Lord Architect (design_system)
  ↓
Lord Forge Master (generate_code)
  ↓
Lord Sentinel (review_code)
  ↓
Response to Client
```

**Implementation**:
```python
# King maintains execution state
quest_execution = {
    "quest_id": "q-001",
    "quest_type": "design_microservice",
    "execution_stack": [
        {"lord": "architect", "tool": "design_system", "status": "pending"},
        {"lord": "forge_master", "tool": "generate_code", "status": "pending"},
        {"lord": "sentinel", "tool": "review_code", "status": "pending"},
    ],
    "run_data": {},  # Cache results
    "current_step": 0,
}

async def execute_quest_chain(quest_execution):
    while quest_execution["current_step"] < len(quest_execution["execution_stack"]):
        step = quest_execution["execution_stack"][quest_execution["current_step"]]
        
        # Execute Lord
        result = await invoke_lord(step["lord"], step["tool"], previous_output)
        
        # Store result
        quest_execution["run_data"][step["lord"]] = result
        step["status"] = "completed"
        
        # Move to next step
        quest_execution["current_step"] += 1
        previous_output = result
    
    return quest_execution["run_data"]
```

#### 2. Parallel Lord Execution

**Quest Flow**: `comprehensive_analysis`

```
                King Gateway
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Lord Oracle  Lord Sentinel  Lord Scribe
   (research)   (analyze)      (summarize)
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
              Merge Results
                     ↓
              Response to Client
```

**Implementation**:
```python
async def execute_parallel_quest(quest_execution):
    parallel_lords = quest_execution["parallel_steps"]
    
    # Invoke all Lords concurrently
    tasks = [
        invoke_lord(lord["name"], lord["tool"], quest_data)
        for lord in parallel_lords
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Wait for ALL results before merging
    merged_result = merge_lord_outputs(results)
    
    return merged_result
```

#### 3. Error Handling Strategy

**Retry Configuration** (per Lord):
```python
LORD_RETRY_CONFIG = {
    "architect": {"max_tries": 3, "wait_between_tries": 1000},
    "forge_master": {"max_tries": 2, "wait_between_tries": 2000},
    "sentinel": {"max_tries": 1, "wait_between_tries": 0},
}

async def invoke_lord_with_retry(lord_name, tool_name, data):
    config = LORD_RETRY_CONFIG[lord_name]
    
    for attempt in range(config["max_tries"]):
        try:
            result = await call_lord_jsonrpc(lord_name, tool_name, data)
            return result
        except Exception as e:
            if attempt == config["max_tries"] - 1:
                raise
            await asyncio.sleep(config["wait_between_tries"] / 1000)
```

**Continue on Fail**:
```python
# Quest definition with error handling
quest_chain = [
    {"lord": "architect", "on_error": "stop"},         # Critical - must succeed
    {"lord": "forge_master", "on_error": "continue"},  # Optional - can skip
    {"lord": "sentinel", "on_error": "stop"},          # Critical - must succeed
]
```

#### 4. State Management & Caching

**Run Data Structure**:
```python
quest_run_data = {
    "quest_id": "q-001",
    "quest_type": "design_microservice",
    "run_data": {
        "architect": {
            "start_time": 1701780000,
            "execution_time": 2500,
            "status": "success",
            "data": {"design": "..."},
            "run_index": 0,
        },
        "forge_master": {
            "start_time": 1701780003,
            "execution_time": 5000,
            "status": "success",
            "data": {"code": "..."},
            "run_index": 0,
        },
    },
    "dirty_lords": [],  # Lords to re-execute
}

# Partial re-execution (user modifies Architect output)
quest_run_data["dirty_lords"] = ["architect"]
# → Re-executes Architect, Forge Master, Sentinel (downstream deps)
```

---

## 🎓 Key Learnings

### 1. Stack-Based Execution is Powerful

**Why n8n Uses a Stack**:
- Simple to implement
- Easy to pause/resume (serialize stack state)
- Natural support for branches (push multiple nodes)
- FIFO = breadth-first, LIFO = depth-first

**Round Table Should**:
- Use similar `quest_execution_stack` in King
- Store stack in database for long-running Quests
- Support Quest "pause" and "resume"

### 2. Multi-Input Nodes Need Special Handling

**The Synchronization Problem**:
- If 2+ Lords feed into 1 Lord, when do we execute the consumer?
- Answer: **Wait until ALL producers complete**

**Round Table Should**:
- Implement `waiting_lords` queue
- Track which Lord inputs are ready
- Only invoke when all dependencies satisfied

### 3. Partial Execution Enables Iterative Development

**User Workflow**:
1. Run Quest → Architect designs system
2. User modifies design manually
3. Re-run Quest → Skip Architect (cached), re-run downstream Lords

**Round Table Should**:
- Store all Lord outputs in `run_data`
- Allow users to mark Lords as "dirty"
- Re-execute only dirty Lords + dependents
- Massive time savings for complex Quests

### 4. Error Handling is Not One-Size-Fits-All

**Different Failure Strategies**:
- **Critical Lords** (Architect): Stop Quest on failure
- **Optional Lords** (Scribe): Continue Quest, use fallback
- **Retry-able Lords** (Oracle): Auto-retry on transient errors

**Round Table Should**:
- Define error handling per Lord + tool
- Support "error branches" (try Lord A, if fails use Lord B)
- Log all errors for debugging

### 5. Observable Execution is Essential

**n8n Hooks** (lines 1430-1440):
```typescript
await hooks.runHook('workflowExecuteBefore', [workflow]);
await hooks.runHook('nodeExecuteBefore', [nodeName, taskData]);
// ... execute node ...
await hooks.runHook('nodeExecuteAfter', [nodeName, taskData]);
await hooks.runHook('workflowExecuteAfter', [runData]);
```

**Round Table Should**:
- Emit events: `quest_started`, `lord_invoked`, `lord_completed`, `quest_finished`
- WebSocket real-time updates to client
- Store execution timeline for debugging

---

## 📋 Next Steps (Week 3-4)

### Immediate Tasks

- [x] Study workflow execution loop (2,615 LOC)
- [ ] Analyze DirectedGraph utilities (`partial-execution-utils/`)
- [ ] Study `waitingExecution` synchronization logic in detail
- [ ] Examine error handling patterns across different node types
- [ ] Review pinData (pre-set outputs) for testing workflows

### Design Phase

- [ ] Design King's `QuestExecutor` class (n8n's `WorkflowExecute`)
- [ ] Design `QuestGraph` for dependency tracking
- [ ] Design `LordRegistry` with retry/error configs
- [ ] Design Quest serialization format (JSON)
- [ ] Design Quest execution API endpoints

### Implementation Phase (Week 5-6)

- [ ] Build `QuestExecutor` with stack-based execution
- [ ] Implement multi-input Lord synchronization
- [ ] Add retry logic with exponential backoff
- [ ] Build Quest state persistence (SQLite)
- [ ] Create Quest debugging UI

---

## 📚 References

**n8n Source Code**:
- Main execution engine: `packages/core/src/execution-engine/workflow-execute.ts`
- Workflow model: `packages/workflow/src/workflow.ts`
- DAG utilities: `packages/core/src/execution-engine/partial-execution-utils/`

**n8n Documentation**:
- Execution order: https://docs.n8n.io/workflows/executions/execution-order/
- Error handling: https://docs.n8n.io/workflows/error-handling/
- Workflow settings: https://docs.n8n.io/workflows/settings/

**Round Table Context**:
- King Gateway MVP: `Magic-Tower/Foundry/KING_GATEWAY_MVP.md`
- Week 1-2 Checkpoint: `Magic-Tower/Experiment-Logs/Quest-001-Week-1-2-Checkpoint.md`
- IBM ContextForge Study: `Magic-Tower/Library/MCP-Architecture/01-Gateway-Patterns-IBM-ContextForge.md`

---

**Study Status**: ⏳ In Progress (Day 1 of 14)  
**Next Session**: Analyze DAG utilities and graph traversal algorithms
