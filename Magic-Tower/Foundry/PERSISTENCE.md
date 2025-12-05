# Quest State Persistence System

## Overview

SQLite-based persistence layer for the Quest Executor, enabling:
- **Automatic state saving** during quest execution
- **Pause/Resume** functionality for long-running quests
- **Quest replay** from beginning or specific checkpoints
- **Historical analytics** and Lord performance tracking
- **Failure recovery** with complete audit trail

## Architecture

### Database Schema

#### `quest_executions` Table
Primary table for quest state:

```sql
CREATE TABLE quest_executions (
    quest_id TEXT PRIMARY KEY,
    quest_type TEXT NOT NULL,
    status TEXT NOT NULL,            -- new, running, completed, failed, paused
    
    -- Timing
    start_time REAL,
    end_time REAL,
    duration_seconds REAL,
    
    -- Data
    input_data TEXT NOT NULL,        -- JSON
    output_data TEXT,                -- JSON
    execution_stack TEXT NOT NULL,   -- JSON array of LordStep
    
    -- Metadata
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    schema_version INTEGER NOT NULL
);
```

#### `lord_runs` Table
Individual Lord execution tracking:

```sql
CREATE TABLE lord_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id TEXT NOT NULL,
    
    -- Lord details
    lord_name TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    run_index INTEGER NOT NULL,      -- Multiple runs of same Lord
    
    -- Execution
    status TEXT NOT NULL,            -- success, error, skipped
    start_time REAL NOT NULL,
    end_time REAL,
    duration_seconds REAL,
    
    -- Data
    input_data TEXT NOT NULL,        -- JSON
    output_data TEXT,                -- JSON
    error_message TEXT,
    
    -- Retry tracking
    attempt_number INTEGER NOT NULL DEFAULT 1,
    max_attempts INTEGER NOT NULL,
    
    created_at TEXT NOT NULL,
    
    FOREIGN KEY (quest_id) REFERENCES quest_executions(quest_id)
);
```

#### `quest_snapshots` Table
Quest state snapshots for pause/resume:

```sql
CREATE TABLE quest_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id TEXT NOT NULL,
    
    -- Complete state dump
    run_data TEXT NOT NULL,          -- JSON: full run_data dict
    execution_stack TEXT NOT NULL,   -- JSON: current stack
    
    -- Snapshot metadata
    snapshot_reason TEXT NOT NULL,   -- 'pause', 'checkpoint', 'error'
    created_at TEXT NOT NULL,
    
    FOREIGN KEY (quest_id) REFERENCES quest_executions(quest_id)
);
```

### Indexes
Performance optimized with indexes on:
- `quest_executions(status)`
- `quest_executions(created_at DESC)`
- `lord_runs(quest_id, run_index)`
- `lord_runs(lord_name, created_at DESC)`

## Usage

### 1. Basic Quest Execution with Persistence

```python
from quest_executor import QuestExecutor, QuestExecutionData, LordStep
from quest_persistence import QuestRepository

# Create repository
repo = QuestRepository("quests.db")

# Create executor with persistence
executor = QuestExecutor(repository=repo)

# Build quest
quest_data = QuestExecutionData(
    quest_id="q-001",
    quest_type="design_microservice",
    input_data={"service": "AuthService"},
    execution_stack=[
        LordStep("architect", "design_system"),
        LordStep("forge_master", "generate_code"),
        LordStep("sentinel", "review_code"),
    ]
)

# Execute - state automatically saved after each Lord
result = await executor.execute_quest(quest_data)
```

**Auto-save behavior**:
- Quest state saved after each Lord execution
- Lord run details saved with timing and results
- Complete audit trail maintained in database

### 2. Pause and Resume Quest

```python
# Pause a running quest
paused = await executor.pause_quest("q-001")

# Quest is now in PAUSED state
# Snapshot saved with current execution stack

# Resume later (can be in different session)
executor = QuestExecutor(repository=repo)
result = await executor.resume_quest("q-001")

# Quest continues from where it left off
```

**Use cases**:
- Long-running quests requiring user feedback
- System maintenance without losing progress
- Rate-limiting between Lord invocations
- Human-in-the-loop validation

### 3. Replay Quest

```python
# Replay entire quest from beginning
result = await executor.replay_quest("q-001")

# Replay from specific Lord (e.g., after fixing bug)
result = await executor.replay_quest("q-001", from_lord="forge_master")
```

**Use cases**:
- Re-run quest with updated Lord implementations
- Debug specific Lords with same inputs
- A/B testing different Lord configurations
- Recover from partial failures

### 4. Query Quest History

```python
# List all quests
quests = repo.list_quests(limit=100)

# Filter by status
completed = repo.list_quests(status=ExecutionStatus.COMPLETED, limit=50)
failed = repo.list_quests(status=ExecutionStatus.FAILED, limit=50)

# Pagination
page_1 = repo.list_quests(limit=20, offset=0)
page_2 = repo.list_quests(limit=20, offset=20)

# Load specific quest
quest_data = repo.load_quest("q-001")
```

### 5. Analytics and Performance Tracking

```python
# Overall quest statistics
stats = repo.get_quest_stats()
# Returns: {
#     "total_quests": 150,
#     "completed": 120,
#     "failed": 15,
#     "running": 10,
#     "paused": 5,
#     "avg_duration_seconds": 12.5,
#     "max_duration_seconds": 45.2,
#     "min_duration_seconds": 2.1
# }

# Lord performance metrics
lord_stats = repo.get_lord_stats()
# Returns list of: {
#     "lord_name": "architect",
#     "tool_name": "design_system",
#     "total_runs": 50,
#     "successful": 48,
#     "errors": 2,
#     "success_rate": 96.0,
#     "avg_duration_seconds": 2.5,
#     "max_duration_seconds": 5.0,
#     "min_duration_seconds": 1.2
# }

# Filter by specific Lord
architect_stats = repo.get_lord_stats(lord_name="architect")
```

## Implementation Details

### QuestRepository Class

**Core Methods**:
- `save_quest(quest_data)` - Save or update quest state
- `load_quest(quest_id)` - Load quest with full run_data
- `delete_quest(quest_id)` - Delete quest and all related data
- `save_lord_run(...)` - Save individual Lord execution
- `save_snapshot(...)` - Save quest state snapshot
- `load_latest_snapshot(quest_id)` - Load most recent snapshot
- `list_quests(status, limit, offset)` - Query quests
- `get_quest_stats()` - Overall statistics
- `get_lord_stats(lord_name)` - Lord performance metrics

**Serialization**:
- All state is JSON-serializable (no pickle)
- `LordStep` serialized to dict with retry config
- Complex nested structures handled cleanly
- Compatible with SQLite TEXT fields

**Connection Management**:
- Context manager for safe connections
- Row factory enabled for dict-like access
- Automatic commit on success
- Foreign key relationships maintained

### QuestExecutor Integration

**New Parameters**:
```python
QuestExecutor(
    hooks=ExecutionHooks(),
    repository=QuestRepository("quests.db")  # Optional
)
```

**Auto-save Points**:
1. Quest start: Save initial state
2. After each Lord: Save run_data and update stack
3. Quest completion: Save final state with output
4. On error: Save error state

**New Methods**:
- `pause_quest(quest_id)` - Pause quest with snapshot
- `resume_quest(quest_id)` - Resume from snapshot
- `replay_quest(quest_id, from_lord)` - Replay execution
- `load_quest(quest_id)` - Load quest from repository

### ExecutionStatus Extended

New status values:
- `PAUSED` - Quest paused, can be resumed
- `COMPLETED` - Quest finished successfully
- `FAILED` - Quest failed with error

## Testing

**Test Suite**: `test_quest_persistence.py`

**11 Comprehensive Tests** (all passing ✅):
1. Basic save and load
2. Save Lord runs
3. Quest snapshots
4. Executor with persistence
5. Pause/resume integration
6. Replay quest
7. Query quest list
8. Quest statistics
9. Lord performance stats
10. Update quest status
11. Delete quest

Run tests:
```powershell
python test_quest_persistence.py
```

## Demo Script

**Interactive Demo**: `demo_persistence.py`

Demonstrates:
1. Quest execution with auto-save
2. Quest snapshots (pause points)
3. Pause and resume functionality
4. Quest analytics and history
5. Lord performance metrics
6. Advanced query filtering and pagination

Run demo:
```powershell
python demo_persistence.py
```

Creates `demo_quests.db` with sample data for exploration.

## Performance Considerations

### Optimizations
- Indexed frequently queried columns
- Connection pooling via context manager
- Batch operations where possible
- Efficient JSON serialization

### Scaling
- SQLite suitable for single-node deployment
- For distributed: migrate to PostgreSQL
- Schema designed for easy migration
- Foreign keys maintained across databases

### Monitoring
- `get_quest_stats()` for health checks
- `get_lord_stats()` for performance tracking
- Duration tracking per quest and Lord
- Success rate monitoring

## Migration Path

### Future PostgreSQL Migration
1. Schema already compatible with PostgreSQL
2. JSON fields → JSONB for better indexing
3. Add distributed locking for concurrent access
4. Connection pooling with pgbouncer
5. Replication for high availability

### Schema Versioning
- `schema_version` field in quest_executions
- Enables backward-compatible migrations
- Current version: 1

## Integration with King Gateway

**Planned Integration** (Week 3-4 Days 8-10):

```python
# King Gateway routes complex quests to QuestExecutor
@app.post("/quest/submit")
async def submit_quest(quest_request: dict):
    repo = QuestRepository("quests.db")
    executor = QuestExecutor(repository=repo)
    
    # Build quest from request
    quest_data = build_quest_from_request(quest_request)
    
    # Execute with persistence
    result = await executor.execute_quest(quest_data)
    
    return {
        "quest_id": result.quest_id,
        "status": result.status,
        "output": result.output_data
    }

# Query quest status
@app.get("/quest/{quest_id}")
async def get_quest_status(quest_id: str):
    repo = QuestRepository("quests.db")
    quest = repo.load_quest(quest_id)
    
    return {
        "quest_id": quest.quest_id,
        "status": quest.status,
        "progress": {
            "completed": len(quest.run_data),
            "remaining": len(quest.execution_stack)
        }
    }
```

## Best Practices

### When to Use Persistence
✅ **Use persistence when**:
- Quest takes > 10 seconds
- Multiple Lords in sequence
- User feedback required mid-quest
- Production deployments
- Need audit trail

❌ **Skip persistence for**:
- Single Lord invocations
- Simple queries < 5 seconds
- Development testing
- Temporary experiments

### Error Handling
```python
# Repository handles database errors
try:
    repo.save_quest(quest_data)
except Exception as e:
    logger.error(f"Failed to save quest: {e}")
    # Quest still in memory, can retry
```

### Cleanup
```python
# Delete old completed quests
old_quests = repo.list_quests(
    status=ExecutionStatus.COMPLETED,
    limit=100,
    offset=0
)

for quest in old_quests:
    if quest_is_old(quest):
        repo.delete_quest(quest['quest_id'])
```

## Files

- `quest_persistence.py` (700 LOC) - Repository implementation
- `quest_executor.py` (updated) - Executor integration
- `test_quest_persistence.py` (650 LOC) - Test suite
- `demo_persistence.py` (400 LOC) - Interactive demo

## Metrics

- **Lines of Code**: 1,750 LOC total
- **Tests**: 11/11 passing ✅
- **Database Tables**: 3 (quest_executions, lord_runs, quest_snapshots)
- **Indexes**: 4 for performance
- **Features**: 6 (save, load, pause, resume, replay, analytics)

---

**Quest 001 - Week 3-4 - Day 2 Complete**

*"The King's quests are now eternal. State persists, execution resumes, history never forgotten."*
